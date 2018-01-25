import logging
from flask import Response
from google.appengine.api import taskqueue

from srcpy.Manager.SQLManager import SQLManagerClass
import srcpy.Manager.ExcelManager as ExcelManager
from srcpy.Manager.ExcelManager import ExcelManagerClass
import srcpy.Manager.StorageManager as StorageManager

import srcpy.Notifier as Notifier
from srcpy.Dictionary import FinalExportDictionary

import config
from collections import defaultdict

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
		sqlManager = SQLManagerClass()
		listNames = sqlManager._getAllTablesName()

		# Initalizes INFO's files signedURL list
		listURL = []

		# For each name
		for name in listNames:
			logging.debug("Loop table " + name[0])
			# Select sheet in Template
			try:
				sheet = workbook.get_sheet_by_name(name[0])
			except Exception as e:
				logging.debug(str(e))
				continue
			if sheet is not None:
				logging.debug("Excel sheet opened")
				# SELECT * FROM <tableName>
				tableValues = sqlManager._getTable(name[0])
				########### SCRIPT INFO TREATMENT
				# Initializes Script INFO File 
				url = config.BUCKET_VF_INFO_NAME + name[0] + ".txt"
				fileStorage = StorageManager.openFile(url, "w", ct= "text/plain")
				lineInfo = ""
				logging.debug("Txt File created")
				########### EXCEL TREATMENT
				# Set Excel cursor to FLoD
				cursor = ExcelManager.getFirstLineOfData(name[0])
				# For each line
				for line in tableValues:
					excelColCount = 1

					# Prepare SCRIPT INFO line
					lineInfo = prepareINFOLine(line, name[0])
					
					# For each cell
					for cell in line:
						excelColCount += 1
						# Write data into Excel sheet
						ExcelManager.setCell(sheet, cursor, excelColCount, str(cell))
					cursor += 1
					# Write INFO
					fileStorage.write(lineInfo)
				fileStorage.close()
				# Generate file's signed url and add it to the list
				scriptSignedURL = StorageManager.generateSignedURL(SCRIPT_ID, nameScript = name[0] + ".txt")
				listURL.append((name[0], scriptSignedURL))

		d = defaultdict(list)
		for k,v in listURL:
			d[k].append(v)

		# Save Excel to Storage
		filename = StorageManager.saveContentXLSToStorage(workbook)

		# Generate signed URL to access file
		excelSignedURL = StorageManager.generateSignedURL(EXCEL_FILE_ID, nameScript = filename)
		# Notificate SUCCES
		Notifier.notifByMail("FES", True, excelSignedURL, d)
	except Exception as e:
		logging.debug(str(e))
		Notifier.notifByMail("FES", False, str(e))
	finally:
		q = taskqueue.Queue('default')
		q.purge()
		return Response("Process done", status = 200)
# END [backgroundExport]

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
				valueString = "0"*(lengthBeforePoint - digB) + valueString + "0"*(lengthAfterPoint-digA)
		count += 1
		tmp += valueString
	tmp = tmp + FinalExportDictionary.commonDataEndLine()
	return tmp


