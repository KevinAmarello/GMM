import logging
from werkzeug import secure_filename
import cloudstorage as gcs
import datetime
from openpyxl.writer.excel import save_virtual_workbook

from google.cloud import storage
from google.appengine.api import app_identity
import time

import config

##########################################
##########################################
##########################################

# START [saveFilePBA]
def saveFilePBA(file):
	"""
		Save Productivas-basicas-adicionales-<current_year> File
		Used by DataValidationService
	"""
	iName = config.EXCEL_VF_FILE
	fName = renameFileHourDayMonth(iName)
	urlOnStorage = config.BUCKET_VF_NAME + fName
	saveFile(file, urlOnStorage)
	return urlOnStorage
# END [saveFile]


# START [saveFile]
def saveFile(file, urlOnStorage):
	"""
		Save File at the specified URL
		and stores the operation into the historic
		Used by DataValidationService and CatalogApplyService
	"""
	fileStorage = openFile(urlOnStorage, 'w', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
	
	fileStorage.write(file.read())
	file.seek(0)
	fileStorage.close()

	fileName = urlOnStorage.split("/")[3]
	writeEntryInHistoric(fileName)
# END [saveFile]


# START [saveContentXLSToStorage]
def saveContentXLSToStorage(wb):
	"""
		Save the workbook-parameter as Productivas-adicionales-basicas-Year.xlsx into the Cloud Storage Bucket.
		Used by FinalExportService

		Input:
			Workbook

	"""
	logging.debug("StorageManager: Entry saveContentXLSToStorage" )
	iName = config.EXCEL_VF_FILE
	fName = renameFileYear(iName)
	urlOnStorage = config.BUCKET_VF_NAME + fName
	xls = openFile(urlOnStorage, 'w', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
	xls.write(save_virtual_workbook(wb))
	xls.close()
# END [saveContentXLSToStorage]


##########################################
##########################################
##########################################


# START [getTemplateVF]
def getTemplateVF():
	logging.debug("StorageManager: Entry getTemplateVF" )
	urlTemplateFileName = config.BUCKET_VF_NAME + config.TEMPLATE_VF_FILE
	return openFile(urlTemplateFileName, 'r')
# END [getTemplateVF]


# START [openFile]
# Opens a file and returns the stream
def openFile(urlOnStorage, rw = None, ct = None):
	return gcs.open(urlOnStorage, rw, content_type = ct)
# END [openFile]


# START [deleteFile]
# Delete File at the specified URL
def deleteFile(urlOnStorage):
	gcs.delete(urlOnStorage)
# END [deleteFile]


##########################################
##########################################
##########################################


# START [renameFileYear]
# Renames the file
def renameFileYear(filename, boolPlusOne = True):
	filename = secure_filename(filename)
	date = datetime.datetime.now().strftime("%Y")
	if boolPlusOne:
		date = str(int(date)+1)
	basename, extension = filename.rsplit('.', 1)
	return "{0}-{1}.{2}".format(basename, date, extension)
# END [renameFileYear]


# START [renameFileDayMonthYear]
# Renames the file including complete date
def renameFileHourDayMonth(filename):
	filename = secure_filename(filename)
	date = (datetime.datetime.now() - datetime.timedelta(hours = 6)).strftime("%H:%M:%S_%d-%m")
	basename, extension = filename.rsplit('.', 1)
	return "{0}-{1}.{2}".format(basename, date, extension)
# END [renameFileDayMonthYear]


# START [generateSignedURL]
# Generate a signed URL to access the file
def generateSignedURL(ID, expires_after_seconds = 3600, nameScript = None):
   	logging.debug("Storage Manager Entry generateSignedURL")
	client = storage.Client()
	default_bucket = config.BUCKET_VF_SIGNED_NAME
	bucket = client.get_bucket(default_bucket)
	if ID == "XLS":
		blob = storage.Blob(renameFileYear(config.EXCEL_SIGNED_FILE), bucket)
	else:
		blob = storage.Blob(config.SCRIPT_INFO + nameScript, bucket)
	expiration_time = int(time.time() + expires_after_seconds)

	url = blob.generate_signed_url(expiration_time)
	return url
# END [generateSignedURL]


# START [writeEntryInHistoric]
def writeEntryInHistoric(fileName):
	"""
		Open the historic file in Cloud Storage and appends
		a line with the file name and the date of the operation.

		Input:
			fileName 
	"""
	bucketName = config.BUCKET_HISTORIC_NAME
	file = config.HISTORIC_FILE
	content = ""
	try:
		# Open read
		fileStream = openFile(bucketName + file, 'r')
		logging.debug("File exists")
		# Read
		content = fileStream.read()
	# Exception if the files doesn t exist
	# In that case it will be created
	except:
		logging.debug("File doesnt exist")
	# Open write 
	fileStream = openFile(bucketName + file, 'w', "text/plain")
	logging.debug("File created")
	# Write
	try:
		content = content + "{0} {1} \n".format(fileName, datetime.datetime.now().strftime("%d-%m-%Y"))
		fileStream.write(content)
		logging.debug(content)
	except Exception as e:
		logging.debug(str(e))

	# Close
	fileStream.close()
	return "OK"
# END [writeEntryInHistoric]


# START [writeResultInHistoric]
def writeResultInHistoric(url, result):
	"""
		Open the historic file in Cloud Storage,
		parse the file to find the line starting with the file name,
		append the process result.

		Input:
			url - Will be split to get the file name out
			result - Result to write
	"""
	bucketName = config.BUCKET_HISTORIC_NAME
	file = config.HISTORIC_FILE
	fileName = url.split("/")[3]
	content = ""
	try:
		# Open read
		fileStream = openFile(bucketName + file, 'r')
		content = fileStream.read()
		fileStream.seek(0)

		newContent = ""
		for line in content.split("\n"):
			if line.startswith(fileName):
				line = line + result
			newContent = newContent + line + "\n"
				
		# Open write 
		fileStream = openFile(bucketName + file, 'w', "text/plain")
		# Write
		fileStream.write(newContent)
		# Close
		fileStream.close()
		return "OK"
	except Exception as e:
		logging.debug(str(e))
# END [writeResultInHistoric]

