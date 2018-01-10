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
		
		createDatabase(catalogManager, sqlManager)
		checkValues(sqlManager)
		updateValues(sqlManager)
				
		# Notify
		StorageManager.writeResultInHistoric(url, "Exito")
		Notifier.notifByMail("AC", True)
	except Exception as e:
		logging.debug(str(e))
		StorageManager.writeResultInHistoric(url, "Fracaso")
		Notifier.notifByMail("AC", False, str(e))
	finally:
		q = taskqueue.Queue('default')
		q.purge()
		sqlManager._closeConnection()
		return Response("Process done", status = 200)
# END [backgroundApply]


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
	listCatalogSheetNames = catalogManager._getListSheetNames()
	for sheetName in listCatalogSheetNames:
		logging.debug("Creating table: " + sheetName)
		sheet = catalogManager._getSheetByName(sheetName)
			
		#Drop table if exists
		dropQuery = sqlManager._getDropTableQuery(sheetName.replace(" ", "_")) # Replace to SUMA_ASEGURADA
		sqlManager._executeQuery(dropQuery)

		# Create table 	
		columnNames = []
		for cell in list(sheet.rows)[0]:
			columnNames.append(cell.value.encode('utf-8').replace(" ", ""))
			#"\""+
		createTableQuery = SQLDictionary._getCatalogCreateTableQuery(sheetName).format(v = columnNames)
		logging.debug(columnNames)
		logging.debug(createTableQuery)
		sqlManager._executeQuery(createTableQuery)

		# Parse sheet to insert data
		logging.debug("Populating table: " + sheetName)
		# Get all lines and slice them to get values only
		tableDataList = list(sheet.rows)[1:]
		for line in tableDataList:
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
# END [createDatabase]


# START [checkValues]
def checkValues(sqlManager):
	"""
		For each catalog in table Concentrado, and for each table associated to this catalog,
		assert that every line existing in this table is described in the catalog. Thus, the table must be incluided
		in the catalog.

		Input:
		sqlManager - To acces the database

		Output:
		AssertException - If table is not incluided in the catalog

	"""
	logging.debug("CatalogApplyService: checkValues")
	listNames = sqlManager._getColumnsName("Concentrado")
	logging.debug("Catalogs: " + str(listNames))

	# For each type of catalog 
	for catalogName in listNames:
		logging.debug("Loop in " + catalogName)
		colTable = sqlManager._executeQuery("SELECT {col} FROM Concentrado WHERE {col} <> \"None\"".format(col = catalogName))
		logging.debug(colTable)

		# Version is special as it presents the associated table inside the table
		if catalogName == "VERSION":
			# For each table associated
			for table in colTable:
				logging.debug("Loop in " + table[0])
				# Get all lines related to this table
				data = sqlManager._executeQuery("SELECT * FROM VERSION WHERE TABLA = \"{0}\"".format(table[0]))
				# KTPT6WT is special as it doesnt need all columns
				if table[0] == "KTPT6WT":
					diff = sqlManager._executeQuery("""
						SELECT {table}.{planT}, {table}.{numverT} 
						FROM {cat} RIGHT JOIN {table}
						ON {cat}.{planC} = {table}.{planT}
						AND {cat}.{numverC} = {table}.{numverT}
						WHERE {cat}.{planC} IS NULL
						""".format(cat = catalogName, table = table[0],
							planC = "CODIGODELPLAN", planT = "CDPLAN",
							numverC = "VERSI\xc3\x93NACTUAL", numverT = "TCNUMVER"))
					logging.debug(diff)
					assert len(diff) == 0, "Una linea no corresponde al catalogo {0} en la tabla {1}: {2}".format(catalogName, table[0], diff)
				else:
					diff = sqlManager._executeQuery("""
						SELECT {table}.*
						FROM {cat} RIGHT JOIN {table}
						ON {cat}.{prodteC} = {table}.{prodteT}
						AND {cat}.{prodcoC} = {table}.{prodcoT}
						AND {cat}.{planC} = {table}.{planT}
						AND {cat}.{numverC} = {table}.{numverT}
						WHERE {cat}.{prodteC} IS NULL
						""".format(cat = catalogName, table = table[0], prodteC = "PRODUCTOTECNICO",
							prodteT = "CDPRODTE", prodcoC = "PRODUCTOCOMERCIAL", prodcoT = "CDPRODCO",
							planC = "CODIGODELPLAN", planT = "CDPLAN",
							numverC = "VERSI\xc3\x93NACTUAL", numverT = "TCNUMVER"))
					logging.debug(diff)
					assert len(diff) == 0, "Una linea no corresponde al catalogo {0} en la tabla {1}: {2}".format(catalogName, table[0], diff)
		# For every each catalog
		else:
			# For each table associated
			for table in colTable:
				logging.debug("Loop in " + table[0])
				# Get the query to apply depending on the catalog type and the table
				# Every table doesn't have the same columns
				query = CatalogDictionary.getQueryByCatalogAndTable(catalogName, table[0])
				diff = sqlManager._executeQuery(query)
				assert len(diff) == 0, "Una linea no corresponde al catalogo {0} en la tabla {1}: {2}".format(catalogName, table[0], diff)
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
		# We start TRANSACTION so we can cancel changes if something goes wrong
		sqlManager._executeQuery("START TRANSACTION")
		for sheetName in ["VERSION", "DEDUCIBLES", "SUMAASEGURADA"]:
			logging.debug("Loop in " + sheetName)
			# Select Table
			if sheetName in ["DEDUCIBLES", "SUMAASEGURADA"]:
				tableData = sqlManager._executeQuery("SELECT CDELEMEN, NCODIGO FROM {0}".format(sheetName))			
				tableList = sqlManager._executeQuery("SELECT {0} FROM Concentrado".format(sheetName))
				logging.debug("Tables to act on " + str(tableList))
				for table in tableList:
					logging.debug("Loop in " + table)
					for line in tableData:
						# Build and execute query
						query = "UPDATE {table} SET {col} = {newV} WHERE {col} = {oldV}".format(
							table = table,
							col = CatalogDictionary.getColumnBySheet(sheetName, table),
							oldV = line[0],
							newV = line[1])
						logging.debug(query)
						sqlManager._executeQuery(query)	
			else:
				tableData = sqlManager._executeQuery("SELECT * FROM VERSION")
				# Table Column is incluided in the table
				for line in tableData:
					query = Catalog.getUpdateVersionQueryByTable(table, line)					
					logging.debug(query)
					sqlManager._executeQuery(query)	
		# Commit changes
		sqlManager._executeQuery("COMMIT")
	except Exception as e:
		# Cancel changes
		sqlManager._executeQuery("ROLLBACK")
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