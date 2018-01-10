import logging
import requests
import json

import config
import srcpy.Manager.StorageManager as StorageManager


# START [notifByMail]
def notifByMail(operation, success, info = None):
	logging.debug("Entry notifByMail")
	"""
		Sends a mail to each person listed in the contact file on Storage.
		Invariables: To's
		Variables: Body / Subject

		Output - JSON
		Example JSON 
		{
    		"to": [<Mail>],
    		"cc": [<MailCC>],
    		"cco": [],
    		"attachments": [],
    		"body": "<BODY_HTML>",
    		"subject": "<SUBJECT>"
		}
	"""

	# Get contact list
	urlContact = config.BUCKET_CONTACT_NAME + config.CONTACT_FILE
	contactFile = StorageManager.openFile(urlContact, 'r')
	contactList = []
	logging.debug("Contact file opened")
	logging.debug("Info: " + str(info))

	for line in contactFile:
		mail = line.rsplit()[0]
		contactList.append(mail)
	contactFile.close()

	payload = {}
	payload['to'] = contactList

	if operation != "DV":
		# Clean body
		if info is not None:
			info = info.replace("\"", "")
			info = info.replace("\'", "")
	else:
		if info is not None:
			info = prepareBodyDV(info)
		
	logging.debug("Info: " + str(info))

	if operation == "FES":
		payload['subject'] = "Resultado de la exportacion final de archivos."
		if success:
			##################### INSERT HTML FORMAT TO REDUCE LINK LENGTH ####################################
			payload['body'] = "El proceso de exportacion sucedio exitosamente. <a href=\"{0}\">Descargar el archivo Excel</a>{0}. Esta disponible solo una hora".format(info)
		else:
			payload['body'] = "Un error ocurrio en el proceso de exportacion: {0}. Favor de reintentar.".format(info)

	if operation == "DV":
		payload['subject'] = "Resultado de la validacion de datos."
		if success:
			payload['body'] = "Proceso realizado con exito."
		else:
			payload['body'] = "Se han encontrado los siguientes errores al ejecutar el proceso:<br> {0}Favor de verificar el documento e intentar de nuevo.".format(info)

	if operation == "AC":
		payload['subject'] = "Resultado de la aplicacion de catalogo."
		if success:
			payload['body'] = "El proceso de aplicacion de catalogo sucedio exitosamente."
		else:
			payload['body'] = "Un error ocurrio en el proceso de aplicacion: {0}. Favor de verificar el documento e intentar de nuevo.".format(info)

	logging.debug(str(json.dumps(payload)))

	headers = {'content-type': 'application/json'}
	requests.post("http://api-dev.oscp.gnp.com.mx/notifier/notification/mail", data=json.dumps(payload), headers = headers)
# END [notifByMail]


# START [prepareBodyDV]
def prepareBodyDV(info):
	"""
		In the case of the validation Data, info is a dictionary
		sheetName : [Errors]
		This method formats the mail's body to clean it up.

		Input:
			info - dictionary

		Output:
			info - HTML format
	"""
	logging.debug("Entry prepareBody")
	infoTemp = "" 
	
	for k in info.keys():
		logging.debug("Table " + k)
		for v in info[k]:
			logging.debug("Error " + v)
			infoTemp += v + " en tabla " + k +"<br>"
	return infoTemp
# END [prepareBodyDV]
