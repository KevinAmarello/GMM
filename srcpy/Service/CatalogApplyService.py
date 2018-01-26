import logging
from flask import Response
from google.appengine.api import taskqueue


from srcpy.Manager.SQLManager import SQLManagerClass
import srcpy.Manager.ExcelManager as ExcelManager
from srcpy.Manager.ExcelManager import ExcelManagerClass
from srcpy.Manager import StorageManager
import srcpy.Notifier as Notifier

from srcpy.Dictionary import ExcelDictionary
from srcpy.Dictionary import CatalogDictionary
from srcpy.Dictionary import SQLDictionary
import config

from collections import defaultdict

# START [handleService]
def handleService(catalog):
	"""
		Saves the file into Storage
		Initiates a taskqueue to proceed next steps in background

		Input:
		file - Catalog File

		Output:
		Response -  200 if OK
					503 if Saving into Cloud Storage failed
	"""
	logging.debug("CatalogApplyService: handleService")
	try:
		# Save Catalog to Cloud Storage
		urlOnStorage = config.BUCKET_CATALOG_NAME + StorageManager.renameFileHourDayMonth(config.CATALOG_FILE_NAME)
		StorageManager.saveFile(catalog, urlOnStorage)

		# Iniciates background process
		task = taskqueue.add(url='/queueApplyCatalog', params = {'url': urlOnStorage})
		return Response("El proceso inicio. Estara notificado del resultado.", status = 200)
	except:
		return Response("Un error sucedio al guardar el archivo, favor de reintentar.", status = 503) 
# END [handleService]


# START [backgroundApply]
def backgroundApply(url):
	"""
		For each update to do, get values in the catalog,
		builds the query and executes it.
		Notifies the result of the process by mail.

		Input:
		url - Catalog's url

	"""
	logging.debug("CatalogApplyService: backgroundApply")
	try:
		# Initiates ExcelManager
		catalogFile = StorageManager.openFile(url, 'r')
		catalogManager = ExcelManagerClass(catalogFile, True)

		# Instanciates SQLManager
		sqlManager = SQLManagerClass()
		checkValidity(catalogManager)
		createDatabase(catalogManager, sqlManager)
		checkValues(sqlManager)
		updateValues(sqlManager)
				
		StorageManager.writeResultInHistoric(url, "Exito")
		Notifier.notifByMail("AC", True)
		return Response ("Process done", status = 200)
	except Exception as e:
		StorageManager.writeResultInHistoric(url, "Fracaso")
	finally:
		sqlManager._closeConnection()
		q = taskqueue.Queue('default')
		q.purge()
		return Response("Process done", status = 200)
# END [backgroundApply]


# START [checkValidity]
def checkValidity(catalogManager):
	"""
		Check that the file is valid <=> Sheets that contain new versions
		have all lines filled.
		If not, notify.
	"""
	logging.debug("CatalogApplyService: checkValidity")
	try:
		listError = []

		# Sheets with new value
		for sheet in ["VERSION", "DEDUCIBLE", "SUMA ASEGURADA"]:
			logging.debug("Loop in " + sheet)
			try:
				# Get column to check
				col = 0
				if sheet == "VERSION":
					col = 7
				else:
					col = 4
				s = catalogManager._getSheetByName(sheet)
				# Parse all lines
				for i in range(2, s.max_row + 1):
					# If it is not last line
					if not isLastLineLittle([s.cell(row = i, column = x) for x in range(1,4)]):
						# Check there is value
						if s.cell(row = i, column = col).value is None:
							listError.append((sheet, "Celdas de nueva version vacias"))
							break
					else:
						break
			except Exception as e:
				logging.debug(str(e))
				listError.append((sheet, str(e)))				
				continue

		d = defaultdict(list)
		for k,v in listError:
			d[k].append(v)

		if len(d) != 0:
			logging.debug("Errors found")
			Notifier.notifByMail("AC", False, d)
			raise Exception

		logging.debug("No errors found")
	except Exception as e:
		raise e
# END [checkValidity]


# START [createDatabase]
def createDatabase(catalogManager, sqlManager):
	"""
		Opens the catalog to create the table into the database.
		Some adjustments are made to bypass encoding issues (spaces, special characters).
		Important: Empty Cells are None in the DB
				   Some N/A values

		Input:
			catalogManager - Catalog Excel File
			sqlManager - To act on the database

		Output:
			Exception - SQL exception
	"""
	logging.debug("CatalogApplyService: createDatabase")
	try:
		listError = []

		listCatalogSheetNames = catalogManager._getListSheetNames()
		for sheetName in listCatalogSheetNames:
			logging.debug("Creating table: " + sheetName)
			sheet = catalogManager._getSheetByName(sheetName)
				
			#Drop table if exists
			dropQuery = sqlManager._getDropTableQuery(sheetName.replace(" ", "_")) # Replace to SUMA_ASEGURADA
			sqlManager._executeQuery(dropQuery)
			logging.debug("Previous table deleted")

			# Create table 	
			columnNames = []
			firstLine = list(sheet.rows)[0][:ExcelDictionary.getEndColumnCatalog(sheetName)]
			for cell in firstLine:
				columnNames.append(cell.value.encode('utf-8').replace(" ", ""))
		

			createTableQuery = SQLDictionary._getCatalogCreateTableQuery(sheetName).format(v = columnNames)
			sqlManager._executeQuery(createTableQuery)

			# Parse sheet to insert data
			logging.debug("Populating table: " + sheetName)
			# Get all lines and slice them to get values only
			tableDataList = list(sheet.rows)[1:]
			for lineC in tableDataList:
				line = lineC[:ExcelDictionary.getEndColumnCatalog(sheetName)]
				try:
					valuesList = []
					# Build valuesList
					if not isLastLine(line):
						for cell in line:
							if(cell is None):
								continue
							if(cell is not None):
								valuesList.append("\""+str(cell.value)+"\"")
						# Formatting the SQL Query if there are values
						if valuesList:
							SQLQuery = SQLDictionary._getCatalogInsertTableQuery(sheetName).format(v = valuesList)
							sqlManager._executeQuery(SQLQuery)
					else:
						continue
				except Exception as ex:
					logging.debug("Exception: " + str(ex))
					listError.append((sheetName, str(ex).replace("\"", "").replace("\'", "")))
					continue
		
		sqlManager._executeQuery("COMMIT")
		d = defaultdict(list)
		for k,v in listError:
			d[k].append(v)

		if len(d) != 0:
			logging.debug("Errors found")
			Notifier.notifByMail("AC", False, d)
			raise Exception

		logging.debug("No errors found")
	except Exception as e:
		raise e

# END [createDatabase]


# START [checkValues]
def checkValues(sqlManager):
	"""
		For each catalog in table Concentrado, and for each table associated to this catalog,
		assert that every line, applying filters to eliminate comodine values, existing in this 
		table is described in the catalog. Thus, the table must be incluided in the catalog.
		Each table doesnt have explicitly all the columns of the catalog, so we have to adapt the 
		queries to each table




		Input:
		sqlManager - To acces the database

		Output:
		AssertException - If table is not incluided in the catalog

	"""
	logging.debug("CatalogApplyService: checkValues")
	listNames = sqlManager._getColumnsName("Concentrado")
	listError = []
	try:
		# For each type of catalog ...
		for catalogName in listNames:
			logging.debug("Loop in " + catalogName)
			tableList = sqlManager._executeQuery("SELECT DISTINCT {col} FROM Concentrado WHERE {col} <> \"None\"".format(col = catalogName))
			logging.debug("Tables associated: " + str(tableList))
			# ... and for each related table
			for table in tableList:
				logging.debug("Checking " + table[0])
				# VERSION and PRODUCTOS are almost the same
				if catalogName in ["VERSION", "PRODUCTOS"]:
					#############################
					# Vertical control
					# For each column of Catalog_Table, we exclude possible comodin values of the table's adapted column
					# and check that the values in it are stored in the catalog
					listColumn = sqlManager._getColumnsName(catalogName)
					logging.debug(str(listColumn))
					# For each column of the catalog
					for column in listColumn:
						logging.debug("Vertical control " + column)
						# Get the associated column in the table
						colTable = adaptColumn(column)
						# Some columns are not mapped
						if colTable is not None:
							if CatalogDictionary.columnToIgnoreByTable(table[0]) is not None and colTable in CatalogDictionary.columnToIgnoreByTable(table[0]):
								continue
							query = "" 
							# If the table may present comodin values for this column, we have to filter them
							if CatalogDictionary.getTableByToIgnoreComodin(colTable) is not None and table[0] in CatalogDictionary.getTableByToIgnoreComodin(colTable):
								logging.debug("This column may present comodin values")
								valuesToIgnore = CatalogDictionary.getValueToIgnoreByTableAndComodin(table[0], colTable)
								query = """
								SELECT DISTINCT {colT} FROM {table} WHERE {colT} NOT IN {values} AND {colT} NOT IN (SELECT DISTINCT {colC} FROM {cat})
								""".format(colT = colTable, table = table[0], cat = catalogName, values = valuesToIgnore, colC = column)
							# The column hasnt comodin value
							else:
								# 6WT only has TCNUMVER and CDPLAN, the CDPLAN check passes in the first branch
								if table[0] == "KTPT6WT" and colTable != "TCNUMVER":
									continue
								logging.debug("This column hasnt comodin columns")
								query = """
								SELECT DISTINCT {colT} FROM {table} WHERE {colT} NOT IN (SELECT DISTINCT {colC} FROM {cat})
								""".format(colT = colTable, table = table[0], cat = catalogName, colC = column)

							logging.debug(query)
							dataTable = sqlManager._executeQuery(query)

							try:
								assert len(dataTable) == 0, "Valor de {0}: {1} no es permitida por el catalogo {2} ".format(colTable, dataTable, catalogName)
							except Exception as e:
								logging.debug(str(e))
								listError.append((table[0], str(e).replace("\"", "").replace("\'", "")))

						else:
							continue

					###########################
					# Horizontal control
					# Select lines from the table and check that they are included in the catalog
					logging.debug("Horizontal control 1: " + catalogName + "/" + table[0])
					query = CatalogDictionary.getSelectDifferenceQueryByCatalogAndTable(catalogName, table[0])
					dataTable = sqlManager._executeQuery(query)
					try:
						assert len(dataTable) == 0, "Linea: {0} no es permitida por el catalogo {1} ".format(dataTable, catalogName)
					except Exception as e:
						logging.debug("AssertionError " + str(e))
						listError.append((table[0], str(e).replace("\"", "").replace("\'", "")))
				# SUMA SEGURADA must have a double check too
				elif catalogName == "SUMA_ASEGURADA":
					###########
					# Vertical Control
					# Control CDSUASEG, VASUASEG, CDSAPERM, CPASEGUR
					# Get Catalog column name
					listColumn = sqlManager._getColumnsName(catalogName)
					if table[0] == "KTPTCKT":
						query = """ 
						SELECT DISTINCT CPASLINN FROM {table} WHERE CPASLINN NOT IN (SELECT DISTINCT DSELEMEN FROM SUMA_ASEGURADA)
						""".format(table = table[0])
						dataTable = sqlManager._executeQuery(query)

						try:
							assert len(dataTable) == 0, "Valor de CPASLINN: {0} no es permitida por el catalogo {1} ".format(dataTable,catalogName)
						except Exception as e:
							logging.debug(str(e))
							listError.append((table[0], str(e).replace("\"", "").replace("\'", "")))

						query = """ 
						SELECT DISTINCT CPASLINI FROM {table} WHERE CPASLINI NOT IN (SELECT DISTINCT DSELEMEN FROM SUMA_ASEGURADA)
						""".format(table = table[0])
						dataTable = sqlManager._executeQuery(query)

						try:
							assert len(dataTable) == 0, "Valor de CPASLINI: {0} no es permitida por el catalogo {1} ".format(dataTable, catalogName)
						except Exception as e:
							logging.debug(str(e))
							listError.append((table[0], str(e).replace("\"", "").replace("\'", "")))

					else:
						for column in listColumn:
							logging.debug("Vertical control " + column)
							colTable = adaptASEGColumn(column, table[0])
							# Some column are not mapped
							if colTable is not None:
								query = "" 
								# If the table may present comodin values for this column, we have to filter them
								if CatalogDictionary.getTableByToIgnoreComodin(colTable) is not None and table[0] in CatalogDictionary.getTableByToIgnoreComodin(colTable):
									logging.debug("This column may present comodin values")
									valuesToIgnore = CatalogDictionary.getValueToIgnoreByTableAndComodin(table[0], colTable)
									query = """ 
									SELECT DISTINCT {colT} FROM {table} WHERE {colT} NOT IN {values} AND {colT} NOT IN (SELECT DISTINCT {colC} FROM SUMA_ASEGURADA)
									""".format(colT = colTable, table = table[0], values = valuesToIgnore, colC = column)
								# The column hasnt comodin value
								else:
									logging.debug("This column hasnt comodin columns")
									query = """ 
									SELECT DISTINCT {colT} FROM {table} WHERE {colT} NOT IN (SELECT DISTINCT {colC} FROM SUMA_ASEGURADA)
									""".format(colT = colTable, table = table[0], colC = column)

								logging.debug(query)
								dataTable = sqlManager._executeQuery(query)

								try:
									assert len(dataTable) == 0, "Valor de {0}: {1} no es permitida por el catalogo {2} ".format(colTable, dataTable, catalogName)
								except Exception as e:
									logging.debug(str(e))
									listError.append((table[0], str(e).replace("\"", "").replace("\'", "")))
					###########################
					# Horizontal control
					# Select lines from the table and check that they are included in the catalog
					logging.debug("Horizontal control 2: " + catalogName + "/" + table[0])
					query = CatalogDictionary.getSelectDifferenceQueryByCatalogAndTable(catalogName, table[0])
					dataTable = sqlManager._executeQuery(query)
					try:
						assert len(dataTable) == 0, "Linea: {0} no es permitida por el catalogo {1} ".format(dataTable, catalogName)
					except Exception as e:
						logging.debug("AssertionError " + str(e))
						listError.append((table[0], str(e).replace("\"", "").replace("\'", "")))
				# Other Catalogs are basically the control of a single column
				else:
					###########################
					# Horizontal control
					# Select lines from the table and check that they are included in the catalog
					logging.debug("Horizontal control 3: " + catalogName + "/" + table[0])
					query = CatalogDictionary.getSelectDifferenceQueryByCatalogAndTable(catalogName, table[0])
					dataTable = sqlManager._executeQuery(query)
					try:
						assert len(dataTable) == 0, "Linea: {0} no es permitida por el catalogo {1} ".format(dataTable, catalogName)
					except Exception as e:
						logging.debug("AssertionError " + str(e))
						listError.append((table[0], str(e).replace("\"", "").replace("\'", "")))

		d = defaultdict(list)
		for k,v in listError:
			d[k].append(v)

		if len(d) != 0:
			logging.debug("Errors found.")
			Notifier.notifByMail("AC", False, d)
			raise EndException

	except EndException as ee:
		logging.debug("Except to end process")
		raise ee
	except Exception as ex:
		logging.debug(str(ex))
		Notifier.notifByMail("AC", False, str(ex).replace("\"", "").replace("\'", ""))
		raise ex
				
# END [checkValues]


# START [updateValues]
def updateValues(sqlManager):
	"""
		Update the values of the table with what is in the catalog.
		Three catalogs are related: Version, Deducibles, Suma Asegurada.
		Get dataSet of tables and catalogs, and execute query to update.

		Input:
		sqlManager - To access the database

		Ouput:
		Exception if something goes wrong
	"""
	try:

		listError = []

		logging.debug("CatalogApplyService updateValues")
		# We start TRANSACTION so we can cancel changes if something goes wrong
		sqlManager._executeQuery("SET autocommit = 0")
		sqlManager._executeQuery("START TRANSACTION")
		for sheetName in ["VERSION", "DEDUCIBLE", "SUMA_ASEGURADA"]:
			logging.debug("Loop in catalog " + sheetName)
			# Select Table
			if sheetName in ["DEDUCIBLE", "SUMA_ASEGURADA"]:
				if sheetName == "SUMA_ASEGURADA":
					tableData = sqlManager._executeQuery("SELECT CDELEMEN, NCODIGO FROM {0}".format(sheetName))			
					tableList = sqlManager._executeQuery("SELECT {0} FROM Concentrado WHERE {0} <> \"None\"".format(sheetName))
					logging.debug("Tables to act on " + str(tableList))
					for table in tableList:
						logging.debug("Loop in table " + table[0])
						if table[0] in ["KTPTCPT", "KTPTBCT", "KTPTBQT", "KTPTDNT"]:
							for line in tableData:
								try:
									# Build and execute query
									query = "UPDATE {table} SET {col} = \"{newV}\" WHERE {col} = \"{oldV}\"".format(
										table = table[0],
										col = CatalogDictionary.getColumnBySheet(sheetName, table[0]),
										oldV = line[0],
										newV = line[1])
									logging.debug(query)
									sqlManager._executeQuery(query)	
								except Exception as e:
									logging.debug("Exception " + str(e))
									listError.append((table[0], str(e).replace("\"", "").replace("\'", "")))
									continue
						else: 
							continue
				elif sheetName == "DEDUCIBLE":
					tableData = sqlManager._executeQuery("SELECT CDELEMEN, NCODIGO FROM {0}".format(sheetName))			
					tableList = sqlManager._executeQuery("SELECT DEDUCIBLES FROM Concentrado WHERE DEDUCIBLES <> \"None\"")
					logging.debug("Tables to act on " + str(tableList))
					for table in tableList:
						logging.debug("Loop in table " + table[0])
						for line in tableData:
							try:
								# Build and execute query
								query = "UPDATE {table} SET {col} = \"{newV}\" WHERE {col} = \"{oldV}\"".format(
									table = table[0],
									col = CatalogDictionary.getColumnBySheet(sheetName, table[0]),
									oldV = line[0],
									newV = line[1])
								logging.debug(query)
								sqlManager._executeQuery(query)	
							except Exception as e:
								logging.debug("Exception " + str(e))
								listError.append((table[0], str(e).replace("\"", "").replace("\'", "")))
								continue			
			else:
				versionData = sqlManager._executeQuery("SELECT * FROM VERSION")
				# Table Column is incluided in the table
				for line in versionData:
					try:
						query = CatalogDictionary.getUpdateVersionQueryByTable(line[1], line)					
						logging.debug(query)
						sqlManager._executeQuery(query)	
					except Exception as e:
						logging.debug("Exception " + str(e))
						listError.append((table[0], str(e).replace("\"", "").replace("\'", "")))
						continue

		d = defaultdict(list)
		for k,v in listError:
			d[k].append(v)

		if len(d) != 0:
			logging.debug("Errors found.")
			# Cancel changes
			sqlManager._executeQuery("ROLLBACK")
			Notifier.notifByMail("AC", False, d)
			raise EndException

		logging.debug("No errors found.")
		# Commit changes
		sqlManager._executeQuery("COMMIT")

	except EndException as ee:
		logging.debug("Except to end process")
		raise ee

	except Exception as e:
		logging.debug(str(ex))
		sqlManager._executeQuery("ROLLBACK")
		Notifier.notifByMail("AC", False, str(ex).replace("\"", "").replace("\'", ""))
		raise e				
# END [updateValues]


# START [isLastLine]
def isLastLine(iterable):
	"""
		Used to know if parameter is the last line of 
		an excel sheet.
	"""
	for element in iterable[:10]:
		if element.value:
			return False
	return True
# END [isLastLine]


# START [isLastLine]
def isLastLineLittle(iterable):
	"""
		Used to know if parameter is the last line of 
		an excel sheet.
	"""
	for element in iterable:
		if element.value:
			return False
	return True
# END [isLastLine]


def adaptColumn(col):
	if col == "FECHA":
		return "FEVALOR"
	elif col == "PRODUCTOTECNICO":
		return "CDPRODTE"
	elif col == "PRODUCTOCOMERCIAL":
		return "CDPRODCO"
	elif col == "CODIGODELPLAN":
		return "CDPLAN"
	elif col == "VERSIONACTUAL":
		return "TCNUMVER"
	else:
		return None


def adaptASEGColumn(col, table):
	if col == "CDELEMEN":
		if table in ["KTPTBCT", "KTPTCPT"]:
			return "CDSUASEG"
		elif table in ["KTPTDNT"]:
			return "CDSAPERM"
		else:
			return None
	# VASUASEG
	if col == "CDELEMEN":
		if table in ["KTPTBCT", "KTPTCPT", "KTPT8LT"]:
			return "VASUASEG"
		else:
			return "CPASEGUR"


# This exception allows the process to end
# when listError is populated and thus consider 
# other types of exception.
class EndException(Exception):
	pass