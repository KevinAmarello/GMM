import logging
from flask import Response
from google.appengine.api import taskqueue

from srcpy.Manager.SQLManager import SQLManagerClass
import srcpy.Manager.ExcelManager as ExcelManager
from srcpy.Manager.ExcelManager import ExcelManagerClass
import srcpy.Manager.StorageManager as StorageManager
import srcpy.Manager.ZipCreator as ZipCreator

import srcpy.Notifier as Notifier
from srcpy.Dictionary import FinalExportDictionary

import config
from collections import defaultdict

import gc
from google.appengine.api.runtime import runtime

EXCEL_FILE_ID = "XLS"
SCRIPT_ID = "INFO"


# START [handleService]
def handleService():
	"""
		Initiates a taskqueue to proceed to the exportation in background.

	"""
	logging.debug("FinalExportService: handleService")

	# Iniciates background process
	task = taskqueue.add(url='/queueExport')

	return Response("El proceso inicio. Estara notificado del resultado.", status = 200)
# END [handleService]


# START [backgroundExport]
def backgroundExport():
	"""
		Gets template of Productivas-basicas-adicionales.xlsx
		Populates it with data from Database
		Saves it into Google Cloud Storage
		Notifies the result of process to users saved in Contactos.txt
		URLs of download are shared inside mail, in the case of success.
	"""
	logging.debug("FinalExportService: backgroundExport")
	try:
		# Get Template from Storage
		excelTemplate = StorageManager.getTemplateVF()
		excelManager = ExcelManagerClass(excelTemplate, False)
		workbook = excelManager.getWB()

		# Get All table name
		logging.debug("Init SQL class")
		sqlManager = SQLManagerClass()
		listNames = sqlManager._getAllTablesName()

		gc.collect()

		# Initalizes INFO's files signedURL list
		listURL = []
		listNamesToSign = []
		# For each name
		for name in listNames:
			logging.debug("Loop table " + name[0])
			# Select sheet in Template
			try:
				sheet = workbook.get_sheet_by_name(name[0])
				logging.info(runtime.memory_usage())

				# Memory Clean
				excelTemplate = None
				excelManager = None
			except Exception as e:
				logging.debug(str(e))
				continue
			if sheet is not None:
				tableTreatment(sqlManager, name, sheet)
		
				logging.debug("Ending Table")
				logging.info(runtime.memory_usage())

				listNamesToSign.append(name[0] + ".txt")
				gc.collect()

		# Save Files to Storage
		filename = StorageManager.saveContentXLSToStorage(workbook)
		zipFile = ZipCreator.createZip(listNamesToSign)

		# Generate signed URL to access file
		excelSignedURL = StorageManager.generateSignedURL(filename)

		if zipFile is None:
			logging.debug("Error occured while creating Zip")
			# Generate file's signed url and add it to the list
			for name in listNamesToSign:
				logging.debug("Signing URL: " + name)
				scriptSignedURL = StorageManager.generateSignedURL(name, listScript = True)
				listURL.append((name, scriptSignedURL))

			d = defaultdict(list)
			for k,v in listURL:
				d[k].append(v)

			# Notificate SUCCES
			Notifier.notifByMail("FES", True, excelSignedURL, d)
			return Response("Process done", status = 200)

		scriptSignedURL = StorageManager.generateSignedURL(zipFile)

		# Notificate SUCCES
		Notifier.notifByMail("FES", True, excelSignedURL, scriptSignedURL)
	except Exception as e:
		logging.debug(str(e))
		Notifier.notifByMail("FES", False, str(e))
	finally:
		q = taskqueue.Queue('default')
		q.purge()
		return Response("Process done", status = 200)
# END [backgroundExport]


# START [tableTreatment]
def tableTreatment(sqlManager, name, sheet):
	# SELECT * FROM <tableName>
	logging.debug("Getting table")
	logging.info(runtime.memory_usage())
	tableValues = sqlManager._getTable(name[0])		
	########### SCRIPT INFO TREATMENT
	# Initializes Script INFO File 
	url = config.BUCKET_VF_INFO_NAME + name[0] + ".txt"
	fileStorage = StorageManager.openFile(url, "w", ct= "text/plain")
	#lineInfo = ""
	logging.debug("Txt File created")
	########### EXCEL TREATMENT
	# Set Excel cursor to FLoD
	cursor = ExcelManager.getFirstLineOfData(name[0])
	# For each line
	for line in tableValues:
		excelColCount = 1
		# Prepare SCRIPT INFO line
		# lineInfo += prepareINFOLine(line, name[0])	
		fileStorage.write(prepareINFOLine(line, name[0]))
		if line != tableValues[-1]:
			fileStorage.write("\r\n")
		# For each cell
		for cell in line:
			excelColCount += 1
			# Write data into Excel sheet
			ExcelManager.setCell(sheet, cursor, excelColCount, str(cell))
		cursor += 1
	
	# Write INFO
	# Delete last break line in file
	#lineInfo = lineInfo[:-2]
	#fileStorage.write(lineInfo)
	#del lineInfo
	del tableValues
	fileStorage.close()
# END [tableTreatment]


# START [prepareINFOLine]
def prepareINFOLine(dbLine, table):
	tmp = ""
	formatTable = FinalExportDictionary.getFormatByTable(table)
	count = 0
	for cell in dbLine:
		# Get cell's format
		f = formatTable[count]
		# Cast to String and get longitud
		valueString = str(cell)
		lenCellValue = len(valueString)
		if f[0] == "CHAR":
			length = f[1]
			valueString += " "*(length-lenCellValue)
		# Numerique
		else:
			# Integer
			if f[2] == 0:
				l = len(cell)
				valueString = "0"*(f[1] - l) + valueString
			else:
				digB = len(valueString.rsplit(".")[0])
				digA = len(valueString.rsplit(".")[1])			
				lengthAfterPoint = int((f[2]))
				lengthBeforePoint = int((f[1])) - lengthAfterPoint - 1
				## As there is a conflict between MySQL and INFO
				# VACTTAR (7.6): 1 digit before point - 5 after
				if int(f[1]) == 7 and int(f[2]) == 6:
					# Truncate last digit if there are 6
					if digA == 6:
						valueString = valueString[:-1]
					valueString = valueString + "0"*(5-digA)
				else:				
					valueString = "0"*(lengthBeforePoint - digB) + valueString + "0"*(lengthAfterPoint-digA)
		count += 1
		tmp += valueString
	tmp = tmp + FinalExportDictionary.commonDataEndLine()
	return tmp


