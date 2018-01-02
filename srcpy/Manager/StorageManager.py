import logging
from werkzeug import secure_filename
import cloudstorage as gcs
import datetime
from openpyxl.writer.excel import save_virtual_workbook

from google.cloud import storage
from google.appengine.api import app_identity
import time

import config

# START [saveContentXLSToStorage]
def saveContentXLSToStorage(wb):
	"""
		Save the workbook-parameter as Productivas-adicionales-basicas-Year.xlsx into the Cloud Storage Bucket.

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


# START [generateSignedURL]
# Generate a signed URL to access the file
def generateSignedURL(ID, expires_after_seconds = 3600):
   	logging.debug("Storage Manager Entry generateSignedURL")
	client = storage.Client()
	default_bucket = config.BUCKET_VF_SIGNED_NAME
	bucket = client.get_bucket(default_bucket)
	if ID == "XLS":
		blob = storage.Blob(renameFileYear(config.EXCEL_SIGNED_FILE), bucket)
	else:
		blob = storage.Blob(renameFileYear(config.SCRIPT_INFO), bucket)
	expiration_time = int(time.time() + expires_after_seconds)

	url = blob.generate_signed_url(expiration_time)
	return url
# END [generateSignedURL]


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


# START [saveFilePBA]
# Save Productivas-basicas-adicionales-<current_year> File
def saveFilePBA(file):
	iName = config.EXCEL_VF_FILE
	fName = renameFileYear(iName, False)
	urlOnStorage = config.BUCKET_VF_NAME + fName
	saveFile(file, urlOnStorage)
	return urlOnStorage
# END [saveFile]


# START [saveFile]
# Save File at the specified URL
def saveFile(file, urlOnStorage):
	fileStorage = openFile(urlOnStorage, 'w', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
	fileStorage.write(file.read())
	file.seek(0)
	fileStorage.close()
# END [saveFile]


# START [deleteFile]
# Delete File at the specified URL
def deleteFile(urlOnStorage):
	gcs.delete(urlOnStorage)
# END [deleteFile]
	

# START [renameFileYear]
# Renames the file
def renameFileYear(filename, boolPlusOne = True):
	filename = secure_filename(filename)
	date = datetime.datetime.utcnow().strftime("%Y")
	if boolPlusOne:
		date = str(int(date)+1)
	basename, extension = filename.rsplit('.', 1)
	return "{0}-{1}.{2}".format(basename, date, extension)
# END [renameFileYear]


