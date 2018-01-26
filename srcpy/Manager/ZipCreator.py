import logging
from io import BytesIO

from zipfile import ZipFile, ZIP_DEFLATED

import config

import srcpy.Manager.StorageManager as StorageManager



def createZip(listFileNames):
	logging.debug("ZipCreator createZip")
	urlToScripts = config.BUCKET_VF_INFO_NAME
	try:
		
		# urlToStorage
		zipUrlInStorage = config.BUCKET_VF_NAME + config.ZIP_VF_FILE
		logging.debug("URL Zip: " + zipUrlInStorage)
		
		strFlow = BytesIO()

		# Open zipFile
		# Write data in StringIO
		with ZipFile(strFlow, "w", ZIP_DEFLATED) as zipF:
			for fileName in listFileNames:
				logging.debug("Adding {0} to Zip".format(fileName))
				urlToFile = urlToScripts + fileName

				addResource(zipF, urlToFile, fileName)


		file = StorageManager.openFile(zipUrlInStorage, "w", "application/zip")
		file.write(strFlow.getvalue())
		file.close()


		return config.ZIP_VF_FILE
	except Exception as e:
		logging.debug(str(e))
		return None





def addResource(zfile, urlFile, fileName):
	fileStream = StorageManager.openFile(urlFile, 'r')
	# write the contents to the zip file
	zfile.writestr(fileName, fileStream.read())
	fileStream.close()


