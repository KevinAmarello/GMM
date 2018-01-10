import logging
from flask import Response
from google.appengine.api import taskqueue

from srcpy.Manager.SQLManager import SQLManagerClass
import srcpy.Manager.ExcelManager as ExcelManager
from srcpy.Manager.ExcelManager import ExcelManagerClass
from srcpy.Manager import StorageManager
import srcpy.Notifier as Notifier

from srcpy.Dictionary import ExcelDictionary
from srcpy.Dictionary import ComodinDictionary

import config
from collections import defaultdict

# START [handleService]
def handleService(file):
	"""
		Checks if the registry control table exists in Cloud SQL  
		Saves the PBA file
		Initiates a taskqueue to proceed next steps in background

		Input:
		file - PBA File

		Output:
		Response -  200 if OK
					500 if Registry Control file not present
					503 if Saving into Cloud Storage failed
	"""
	logging.debug("DataValidationService: handleService")
	try:
		# Check if the control cifras table exists
		#try:
		#	SQLManagerClass()._getTable("CONTROL_CIFRAS")
		#except:
		#	return Response("Favor de ingresar el control de cifras primero.", status = 420)
		# Save file to Storage
		url = StorageManager.saveFilePBA(file)
	except:
		return Response("Un error sucedio al guardar el archivo, favor de reintentar.", status = 503) 
	# Iniciates background process
	task = taskqueue.add(url='/queueValidate', params = {'url': url})
	return Response("El proceso inicio. Estara notificado del resultado.", status = 200)
# END [handleService]


# START [backgroundValidation]
def backgroundValidation(url):
	"""
		Creates the DB according to the file: this checks the data format and raise an Exception if fail
		Does registry control by doing SELECT COUNT for each table in the database
		Checks comodines values by interrogating the database: raises an AssertionException if fail
	"""	
	logging.debug("DataValidationService: backgroundValidation")
	try:	
		# Load PBA		
		logging.debug("DataValidationService: backgroundValidation: Loading PBA File: " + url)
		pbaFile = StorageManager.openFile(url, 'r')
		pbaManager = ExcelManagerClass(pbaFile, True)
		
		createDatabase(pbaManager)
		#registryControl()
		#checkComodin()
		StorageManager.writeResultInHistoric(url, "Exito")
		Notifier.notifByMail("DV", True)
		return Response ("Process done", status = 200)
	except Exception as e:
		StorageManager.writeResultInHistoric(url, "Fracaso")
	finally:
		q = taskqueue.Queue('default')
		q.purge()
		return Response("Process done", status = 200)
# END [backgroundValidation]


# START [registryControl]
def registryControl():
	"""
		Checks that the tables previously created contain the same amount of data
		that what is indicated in the CONTROL_CIFRAS table.

		Output:
			List - If OK
			Exception - If AssertException
	"""
	logging.debug("DataValidationService: registryControl")
	try:
		# Instanciates SQLManager
		sqlManager = SQLManagerClass()
		registryNumberList = sqlManager._getTable("CONTROL_CIFRAS")
		for table in registryNumberList:
			tableCount = sqlManager._executeQuery(sqlManager._getSelectCountQuery(table[0]))[0][0]
			assert tableCount == table[1], "Control de cifras incorrecto. Hoja: {0} - Esperado: {1}, obtenido: {2}".format(table, table[1], tableCount)
	except Exception as e:
		logging.debug(str(e))
		raise e
	finally:
		sqlManager._closeConnection()
# END [registryControl]


# START [createDatabase]
def createDatabase(excelManager):
	"""
		Create the database from the PBA file

		Input:
			excelManager
			sqlManager
	"""
	logging.debug("DataValidationService: createDatabase")
	try:
		# Instanciates SQLManager
		sqlManager = SQLManagerClass()

		# Initializes list error
		listError = []
		listExcelSheetNames = excelManager._getListSheetNames()

		for sheetName in listExcelSheetNames:
			logging.debug("Loop on sheet: " + sheetName)
			# Control name 
			if(len(sheetName)==7):
				#Drop table if exists
				dropQuery = sqlManager._getDropTableQuery(sheetName)
				sqlManager._executeQuery(dropQuery)

				# Create table 
				createTableQuery = sqlManager._getCreateTableQuery(sheetName)
				sqlManager._executeQuery(createTableQuery)

				# Parse sheet to insert data
				sheet = excelManager._getSheetByName(sheetName)
				flod = ExcelManager.getFirstLineOfData(sheetName)
				# Get all lines and slice them to get values only
				tableDataList = list(sheet.rows)[flod-1:]
				# Ignoring empty sheets
				if len(tableDataList) != 0:
					for line in tableDataList:
						try:
							valuesList = []
							# Build valuesList
							for cell in line[1:]:
								if(cell is None or cell.value is None):
									continue
								if(cell is not None and cell.value is not None):
									valuesList.append("\""+str(cell.value)+"\"")
							# Formatting the SQL Query if there are values
							if valuesList:
								SQLQuery = sqlManager._getInsertIntoQuery(sheetName, valuesList)
								sqlManager._executeQuery(SQLQuery)
						except Exception as ex:
							logging.debug("Exception: " + str(ex))
							listError.append((sheetName, str(ex).replace("\"", "").replace("\'", "")))
							continue
		# Concentrate listError by sheetName
		# We will have something like d["KTPT"] = ["Error1", "Error2"]
		# d can be empty
		d = defaultdict(list)
		for k,v in listError:
			d[k].append(v)

		if len(d) != 0:
			logging.debug("Errors found.")
			Notifier.notifByMail("DV", False, d)
			raise Exception

	except Exception as e:
		raise e
	finally:
		sqlManager._closeConnection()
# END [createDatabase]


# START [checkComodin]
def checkComodin():
	"""
		For each table in tha database which contains comodin,
		interrogates the database, selects the comodin column
		and compares the value to what is expected.

		Output:
			List - Boolean, Details
			Exception - Details 
	"""
	logging.debug("DataValidationService: checkComodin")
	try:
		# Initiates list error
		listError = []

		# Instanciates SQLManager
		sqlManager = SQLManagerClass()
		sheetsToCheck = ComodinDictionary.getSheetWithComodin()

		for sheet in sheetsToCheck:
			logging.debug("Loop in: " + sheet)

			# Get columns to check
			columnsToCheck = ComodinDictionary.getComodinColumnBySheet(sheet)

			for column in columnsToCheck:
				logging.debug(sheet + " : Loop in : " + column)
				try:
					# If integer column...
					if(ComodinDictionary.getIntegerColumnBySheet(sheet) is not None and column in ComodinDictionary.getIntegerColumnBySheet(sheet)):
						logging.debug("Integers are expected in this one")
						# ... and if this column has conditions ...
						if(ComodinDictionary.getConditionedComodinColumnBySheet(sheet) is not None and column in ComodinDictionary.getConditionedComodinColumnBySheet(sheet)):
							logging.debug("Conditions are expected in this one")
							checkLines_Condition(sheet , column, sqlManager)
												
						# ... and doesn't take conditions to check value
						else:
							logging.debug("No conditions are expected in this one")
							# Get column
							resultSet = sqlManager._executeQuery(sqlManager._getColumnByTableQuery(sheet, column))
							if(len(resultSet) != 0):
								# Check value of these lines
								for result in resultSet:
									assert is_integer(result[0]) or result[0] == ComodinDictionary.getComodinValueBySheet(sheet, column), "Valor de comodin incorecta. Hoja: {0} - Comodin: {1} - Valor: {2}".format(sheet, column, result[0])

					# If decimal column...
					elif(ComodinDictionary.getDecimalColumnBySheet(sheet) is not None and column in ComodinDictionary.getDecimalColumnBySheet(sheet)):
						logging.debug("Decimals are expected in this one")
						# ... and if this column has conditions ...
						if(ComodinDictionary.getConditionedComodinColumnBySheet(sheet) is not None and column in ComodinDictionary.getConditionedComodinColumnBySheet(sheet)):
							logging.debug("Conditions are expected in this one")
							checkLines_Condition(sheet , column, sqlManager)

						# ... and doesn't take conditions to check value
						else:
							logging.debug("No conditions are expected in this one")
							# Get column
							if(len(resultSet) != 0):
								resultSet = sqlManager._executeQuery(sqlManager._getColumnByTableQuery(sheet, column))
								for result in resultSet:
									assert is_decimal(result[0]) or result[0] == ComodinDictionary.getComodinValueBySheet(sheet, column), "Valor de comodin incorecta. Hoja: {0} - Comodin: {1} - Valor: {2}".format(sheet, column, str(result[0]))
				except Exception as ex:
					logging.debug("Exception " + str(ex))
					# If catch an assertException, populates the listError
					listError.append((sheetName, str(ex).replace("\"", "").replace("\'", "")))
					continue

		# Concentrate listError by sheetName
		# We will have something like d["KTPT"] = ["Error1", "Error2"]
		# d can be empty
		d = defaultdict(list)
		for k,v in listError:
			d[k].append(v)

		if len(d) != 0:
			logging.debug("Errors found.")
			Notifier.notifByMail("DV", False, d)
			raise Exception
	except Exception as ex:
		logging.debug(str(ex))
		raise ex
	finally:
		sqlManager._closeConnection()
# END [checkComodin]


# START [checkLines_Condition_OK]
def checkLines_Condition(sheet , column, sqlManager):
	"""
		Select all the lines in the table that fits with the condition
		Assert that the value equals the conditioned comodin

		Then select the other lines and check they are integers or have 
		a default value corresponding to the column type.

		Input:
			Sheet - Table name
			Column - Column Name

		Output:
			AssertException - If control fails
	"""
	logging.debug("Checking Conditions OK")
	# ... get lines fitting with the conditions
	queryCond = getComodinCondition_OK_Query(sheet , column, sqlManager)
	resultSet = sqlManager._executeQuery(queryCond)

	if(len(resultSet) != 0):
		# Check value of these lines
		for result in resultSet:
			assert str(result[0]) == ComodinDictionary.getConditionedComodinValueBySheet(sheet, column), "Valor de comodin incorecta. Hoja: {0} - Comodin: {1} - Valor: {2}".format(sheet, column, str(result[0]))
					
	# Get the other lines
	logging.debug("Checking Conditions NOK")
	queryBis = getComodinCondition_NOK_Query(sheet, column, queryCond)
	resultSet = sqlManager._executeQuery(queryCond)

	if(len(resultSet) != 0):
		# Check value of these lines
		for result in resultSet:
			assert is_integer(result[0]) or str(result[0]) == ComodinDictionary.getComodinValueBySheet(sheet, column), "Valor de comodin incorecta. Hoja: {0} - Comodin: {1} - Valor: {2}".format(sheet, column, str(result[0]))
# END [checkLines_Condition_OK]


# START [getComodinCondition_OK_Query]
def getComodinCondition_OK_Query(sheet , column, sqlManager):
	"""
		Returns the Query to select lines that fit with conditions

		Input:
			Sheet - Table Name
			Column - Column Name

		Output:
			Query
	"""
	conditions = ComodinDictionary.getConditionColumnBySheet(sheet)
	logging.debug("Conditions: "+ str(conditions))
	cN = []
	cV = []
	for c in conditions:
		cN.append(c)
		logging.debug(str(ComodinDictionary.getConditionValueBySheet(sheet, c)))
		cV.append(ComodinDictionary.getConditionValueBySheet(sheet, c))
	logging.debug(sqlManager.getSelectComodinQuery(sheet, column, cN, cV))
	return sqlManager.getSelectComodinQuery(sheet, column, cN, cV)
# END [getComodinCondition_OK_Query]


# START [getComodinCondition_NOK_Query]
def getComodinCondition_NOK_Query(table, column, queryConditionOK):
	"""
		Return the column without lines contained in parameters

		Input:
			Table - Table name
			Column - Column Name
			QueryConditionOK - Query to substract

		Output:
			Query 
	"""
	logging.debug("SELECT {0} FROM {1} WHERE {0} NOT IN ({2})".format(column, table, queryConditionOK))
	return "SELECT {0} FROM {1} WHERE {0} NOT IN ({2})".format(column, table, queryConditionOK)
# END [getComodinCondition_NOK_Query]


def is_integer(s):
	try:
		int(s)
		return True
	except ValueError:
		return False


def is_decimal(s):
	try:
		float(s)
		return True
	except ValueError:
		return False