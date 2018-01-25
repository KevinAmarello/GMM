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
		try:
			SQLManagerClass()._getTable("CONTROL_CIFRAS")
		except:
			return Response("Favor de ingresar el control de cifras primero.", status = 420)
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
		registryControl()
		checkComodin()
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

		listError = []

		for table in registryNumberList:
			try:
				tableCount = sqlManager._executeQuery(sqlManager._getSelectCountQuery(table[0]))[0][0]
				assert tableCount == table[1], "Control de cifras incorrecto. Esperado: {0}, obtenido: {1}".format(table[1], tableCount)
			except Exception as ex:
				logging.debug("Exception: " + str(ex))
				listError.append((table[0], str(ex).replace("\"", "").replace("\'", "")))
				continue

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
				for line in tableDataList:
					try:
						if not isLastLine(line):
							valuesList = []
							# Build valuesList
							for cell in line[1:]:
								if(cell is None or cell.value is None):
									continue
								if(cell is not None and cell.value is not None):
									valuesList.append("\""+str(cell.value)+"\"")
							# Formatting the SQL Query if there are values
							if len(valuesList) != 0:
								SQLQuery = sqlManager._getInsertIntoQuery(sheetName, valuesList)
								sqlManager._executeQuery(SQLQuery)
						else:
							break
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

		sqlManager._executeQuery("COMMIT")
	except Exception as e:
		raise e
	finally:
		sqlManager._closeConnection()
# END [createDatabase]


# START [checkComodin]
def checkComodin():
	"""
		Algorithm:
		For each table with comodin:
			For each comodin in table:
				If it is conditioned_comodin_column:
					Get lines with conditioned_comodin_value
					Assert conditions respected

					Get line without conditioned_comodin_value 
					If Integer expected:
						If it is default_comodin_colummn:
							Assert Value is Integer or default_comodin_value
						If not:
							Assert Value is Integer
					If Decimal expected
						If it is default_comodin_column:
							Assert Value is Decimal or default_comodin_value
						If not:
							Assert Value is Decimal
					If String expected
						Assert Value is not condition_comodin_value

				If not:
					Get whole column
					If Integer expected:
						If it is default_comodin_value:
							Assert Value is Integer or default_comodin_value
						If not:
							Assert Value is Integer
					If Decimal expected
						If it is default_comodin_value:
							Assert Value is Decimal or default_comodin_value
						If not:
							Assert Value is Decimal

		IMPORTANT: As we cannot check a String is type(String) or default_comodin_value as it is the same check,
		we only check that in some cases, it is not the condition_comodin_value.

		Output:
			Exception - Details 
	"""
	logging.debug("DataValidationService: checkComodin")
	try:
		# Initiates list error
		listError = []

		# Instanciates SQLManager
		sqlManager = SQLManagerClass()
		tableToCheckList = ComodinDictionary.getTableWithComodin()

		for table in tableToCheckList:
			logging.debug("Loop in: " + table)

			# Get columns to check
			columnsToCheck = ComodinDictionary.getComodinColumnByTable(table)
			for column in columnsToCheck:
				logging.debug("Checking " + column + " in " + table)
				# If the column may present a conditioned comodine value ...
				if ComodinDictionary.getConditionedComodinColumnByTable(table) is not None and column in ComodinDictionary.getConditionedComodinColumnByTable(table):
					logging.debug("This column may present a conditioned comodine value")
					# ... check that if the comodin has its conditioned value, the conditions are respected
					listError = checkLines_Condition(table , column, sqlManager, listError)
				# If the column may not conditioned comodin value ...
				else:
					logging.debug("This column hasnt conditioned comodine value")
					# ... get whole column
					resultSet = sqlManager._executeQuery(sqlManager._getColumnByTableQuery(table, column))
					# Check data depend column's type
					listError = checkDataDependingOnColumntypes(table, column, resultSet, listError)

			
		# Concentrate listError by sheetName
		# We will have something like d["KTPT"] = ["Error1", "Error2"]
		# d can be empty
		d = defaultdict(list)
		for k,v in listError:
			d[k].append(v)

		if len(d) != 0:
			logging.debug("Errors found.")
			Notifier.notifByMail("DV", False, d)
			raise EndException
	except EndException as ee:
		logging.debug("Except to end process")
		raise ee
	except Exception as ex:
		logging.debug(str(ex))
		Notifier.notifByMail("DV", False, str(ex).replace("\"", "").replace("\'", ""))
		raise ex
	finally:
		sqlManager._closeConnection()
# END [checkComodin]


# START [checkLines_Condition_OK]
def checkLines_Condition(table , column, sqlManager, listError):
	"""
		Select all the lines in the table where comodin = conditioned_comodin_value
		Assert that the conditions are respected

		Then select the other lines and check they are integers or have 
		a default comdin value depending on the column type.

		Input:
			Sheet - Table name
			Column - Column Name

		Output:
			AssertException - If control fails
	"""
	logging.debug("Checking values with Conditions OK")
	# Get lines with Conditioned Comodin Value
	queryCond = getComodinCondition_OK_Query(table , column, sqlManager)
	logging.debug(queryCond)
	resultSet = sqlManager._executeQuery(queryCond)
	
	# So we get the conditions colums, assert expexted values are respected
	for result in resultSet:
		# If two conditions
		if len(result) == 2:
			logging.debug("Two conditions")
			# [CDPRODCO, CDPLAN]
			try:
				assert str(result[0]) in ComodinDictionary.getConditionValueByTableAndColumn(table, "CDPRODCO") and str(result[1]) in ComodinDictionary.getConditionValueByTableAndColumn(table, "CDPLAN"), "Valor de comodin incorecta. Las condiciones no estan satisfechas. Comodin: {0} - Valor: {1}".format(column, ComodinDictionary.getConditionedComodinValueByTableAndComodin(table, column))
			except Exception as ex:
				logging.debug("Exception: " + str(ex))
				listError.append((table, str(ex).replace("\"", "").replace("\'", "")))
				continue

		# If simple condition, [CDPRODCO]
		else:
			logging.debug("Only one condition")
			try:
				assert str(result[0]) in ComodinDictionary.getConditionValueByTableAndColumn(table, "CDPRODCO"), "Valor de comodin incorecta. Las condiciones no estan satisfechas. Comodin: {0} - Valor: {1}".format(column, ComodinDictionary.getConditionedComodinValueByTableAndComodin(table, column))
			except Exception as ex:
				logging.debug("Exception: " + str(ex))
				listError.append((table, str(ex).replace("\"", "").replace("\'", "")))
				continue


	# Get lines where no Conditioned Comodin Value
	logging.debug("Checking values with Conditions NOK")
	queryBis = getComodinCondition_NOK_Query(table, column)
	logging.debug(queryBis)
	resultSet = sqlManager._executeQuery(queryBis)
	
	# Check the numeric data
	listError = checkDataDependingOnColumntypes(table, column, resultSet, listError)
	# Check the alphanumeric data
	# If the column is type String, we cannot confirm that the value is part of a Dictionary, but we can check that it is not the Conditioned Comodin Value
	if ComodinDictionary.getAlphaNumericColumnByTable(table) is not None and column in ComodinDictionary.getAlphaNumericColumnByTable(table):
		for line in resultSet:
			try:
				assert line[0] != ComodinDictionary.getConditionedComodinValueByTableAndComodin(table, column), "Valor de comodin incorecta. Las condiciones no estan satisfechas. Comodin: {0} - Valor: {1}".format(column, str(line[0]))
			except Exception as ex:
				logging.debug("Exception: " + str(ex))
				listError.append((table, str(ex).replace("\"", "").replace("\'", "")))
				continue
	return listError
# END [checkLines_Condition_OK]


# START [checkDataDependingOnColumntypes]
def checkDataDependingOnColumntypes(table, column, resultSet, listError):
	"""
		Checks each resultSet's line is Integer or Decimal, or possible default comodin value.
	"""
	# If the column is type Integer
	if ComodinDictionary.getIntegerColumnByTable(table) is not None and column in ComodinDictionary.getIntegerColumnByTable(table):
		logging.debug("This column presents Integer number")
		# Check that is Integer or possibly default comodin value
		listError = checkDataDependingOnDefaultComodinValue(table, column, resultSet, listError, True)
	# If the column is type Decimal
	elif ComodinDictionary.getDecimalColumnByTable(table) is not None and column in ComodinDictionary.getDecimalColumnByTable(table):
		logging.debug("This column presents Decimal number")
		# Check that is Decimal or possibly default comodin value
		listError = checkDataDependingOnDefaultComodinValue(table, column, resultSet, listError, False)
	return listError
# END [checkDataDependingOnColumntypes]	


# START [checkDataDependingOnDefaultComodinValue]
def checkDataDependingOnDefaultComodinValue(table, column, resultSet, listError, isInteger):
	"""
		Checks numeric data, including default comodin value if the column may present one.
	"""
	# If the column may have a default comodin value ...
	if ComodinDictionary.getDefaultComodinColumnByTable(table) is not None and column in ComodinDictionary.getDefaultComodinColumnByTable(table):
		logging.debug("This column may have a default comodin value")
		# ... assert that each line is an integer/decimal or the default comodin value
		for line in resultSet:
			try:
				if isInteger:
					assert is_integer(line[0]) or str(line[0]) == ComodinDictionary.getDefaultComodinValueByTableAndComodin(table, column), "Valor de comodin incorecta. Esperado Integer o Comodin por defecto. Comodin: {0} - Valor: {1}".format(column, str(line[0]))
				else:
					assert is_decimal(line[0]) or str(line[0]) == ComodinDictionary.getDefaultComodinValueByTableAndComodin(table, column), "Valor de comodin incorecta. Esperado Decimal o Comodin por defecto. Comodin: {0} - Valor: {1}".format(column, str(line[0]))
			except Exception as ex:
				logging.debug("Exception: " + str(ex))
				listError.append((table, str(ex).replace("\"", "").replace("\'", "")))
				continue
	# If the column may not have a default comodin value ...
	else:
		logging.debug("This column hasnt a default comodin value")
		# ... assert that each line is an integer/decimal
		for line in resultSet:
			try:
				if isInteger:
					assert is_integer(line[0]), "Valor de comodin incorecta. Esperado Integer. Comodin: {0} - Valor: {1}".format(column, str(line[0]))
				else:
					assert is_decimal(line[0]), "Valor de comodin incorecta. Esperado Decimal. Comodin: {0} - Valor: {1}".format(column, str(line[0]))
			except Exception as ex:
				logging.debug("Exception: " + str(ex))
				listError.append((table, str(ex).replace("\"", "").replace("\'", "")))
				continue
	return listError
# END [checkDataDependingOnDefaultComodinValue]


# START [getComodinCondition_OK_Query]
def getComodinCondition_OK_Query(table , column, sqlManager):
	"""
		Returns the Query to select lines that fit with conditioned comodin value

		Input:
			Table - Table Name
			Column - Column Name

		Output:
			Query
	"""
	conditions = ComodinDictionary.getConditionColumnByTable(table)
	conditionedComodinValue = ComodinDictionary.getConditionedComodinValueByTableAndComodin(table, column)
	return sqlManager.getSelectConditionedComodinQuery(table, column, conditionedComodinValue, conditions)
# END [getComodinCondition_OK_Query]


# START [getComodinCondition_NOK_Query]
def getComodinCondition_NOK_Query(table, column):
	"""
		Return the query to select lines where conditioned comodin hasnt its conditioned value

		Input:
			Table - Table name
			Column - Column Name

		Output:
			Query 
	"""
	conditionedComodinValue = ComodinDictionary.getConditionedComodinValueByTableAndComodin(table, column)
	return "SELECT DISTINCT {comodin} FROM {table} WHERE {comodin} != \'{condValue}\'".format(comodin = column, table = table, condValue = conditionedComodinValue) 
# END [getComodinCondition_NOK_Query]

#########################  UTILS  ##############################
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


# START [isLastLine]
def isLastLine(iterable):
	"""
		Used to know if parameter is the last line of 
		an excel sheet.
	"""
	for element in iterable[1:5]:
		if element.value:
			return False
	return True
# END [isLastLine]


# This exception allows the process to end
# when listError is populated and thus consider 
# other types of exception.
class EndException(Exception):
	pass