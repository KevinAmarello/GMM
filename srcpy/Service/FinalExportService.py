import logging
from flask import Response
from google.appengine.api import taskqueue

from srcpy.Manager.SQLManager import SQLManagerClass
import srcpy.Manager.ExcelManager as ExcelManager
from srcpy.Manager.ExcelManager import ExcelManagerClass
import srcpy.Manager.StorageManager as StorageManager
import srcpy.Notifier as Notifier


SERVICE_ID = "FES"
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

		# For each name
		for name in listNames:
			# Select sheet in Template
			try:
				sheet = workbook.get_sheet_by_name(name[0])
			except Exception as e:
				logging.debug(str(e))
				continue
			if sheet is not None:
				# SELECT * FROM <tableName>
				tableValues = sqlManager._getTable(name[0])
				# Set Excel cursor to FLoD
				cursor = ExcelManager.getFirstLineOfData(name[0])
				# For each line
				for line in tableValues:
					excelColCount = 1
					# For each cell
					for cell in line:
						excelColCount += 1
						# Write data into Excel sheet
						ExcelManager.setCell(sheet, cursor, excelColCount, str(cell))
					cursor += 1

		# Save Excel to Storage
		StorageManager.saveContentXLSToStorage(workbook)

		# Generate signed URL to access file
		excelSignedURL = StorageManager.generateSignedURL(EXCEL_FILE_ID)
		# Notificate SUCCES
		Notifier.notifByMail(SERVICE_ID, True, excelSignedURL)
	except Exception as e:
		logging.debug(str(e))
		Notifier.notifByMail(SERVICE_ID, False, str(e))
	finally:
		q = taskqueue.Queue('default')
		q.purge()
		return Response("Process done", status = 200)
# END [backgroundExport]
