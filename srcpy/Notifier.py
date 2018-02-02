import logging
import requests
import json

import config
import srcpy.Manager.StorageManager as StorageManager

from collections import defaultdict


# START [notifByMail]
def notifByMail(operation, success, info = None, listScriptURL = None):
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
	temp = "" 

	# Get contact list
	urlContact = config.BUCKET_CONTACT_NAME + config.CONTACT_FILE
	contactFile = StorageManager.openFile(urlContact, 'r')
	contactList = []
	logging.debug("Contact file opened")

	for line in contactFile:
		mail = line.rsplit()[0]
		contactList.append(mail)
	contactFile.close()

	payload = {}
	payload['to'] = contactList

	if operation in ["DV", "AC"]: 
		if info is not None:
			if type(info) is defaultdict:
				info = prepareBody(info)
			else:
				info = info.replace("\"", "").replace("\'", "")
				info += "<br>"	

	elif operation in ["FES"]:
		if info is not None:
			info = info.replace("\"", "").replace("\'", "")
		
		if type(listScriptURL) is defaultdict:
			logging.debug("Adding List Zip files")
			temp = "" 
			for k in listScriptURL.keys():
				temp += "<a href=\"{0}\">Descargar el script {1}</a><br>".format(listScriptURL[k][0] , k)
			listScriptURL = temp
		else:
			logging.debug("Adding Zip body")
			if listScriptURL is not None:
				listScriptURL = listScriptURL.replace("\"", "").replace("\'", "")
				listScriptURL = "<a href=\"{0}\">Descargar los scripts INFO</a>.".format(listScriptURL)
				logging.debug(listScriptURL)
	else:
		# Clean body
		if info is not None:
			info = info.replace("\"", "").replace("\'", "")


		
	logging.debug("Info: " + str(info))

	if operation == "RC":
		payload['subject'] = "Resultado de la subida de cifras de control."
		if success:
			payload['body'] = "Se han recibido exitosamente las cifras de control."
		else:
			payload['body'] = "Un error ocurrio en el proceso de ingreso de cifras de control:<br> {0}. Favor de reintentar.".format(info)

	if operation == "FES":
		payload['subject'] = "Resultado de la exportacion final de archivos."
		if success:
			payload['body'] = "El proceso de exportacion sucedio exitosamente.<br><a href=\"{0}\">Descargar el archivo Excel</a>.<br>{1}<br>Estan disponibles solo una hora".format(info, listScriptURL)
		else:
			payload['body'] = "Un error ocurrio en el proceso de exportacion:<br> {0}. Favor de reintentar.".format(info)

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
			payload['body'] = "Un error ocurrio en el proceso de aplicacion:<br> {0}Favor de verificar el documento e intentar de nuevo.".format(info)

	logging.debug(str(json.dumps(payload)))

	## INSERT HERE HEADERS FOR NOTIFIER REQUESTS
	headers = {'Accept': 'application/json', 'content-type': 'application/json;charset=utf-8', 'apiKey': config.API_KEY}
	## INSERT HERE URL 
	requests.post(config.URL, data=json.dumps(payload), headers = headers)
# END [notifByMail]


# START [prepareBody]
def prepareBody(info):
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
		for v in info[k]:
			infoTemp += v.replace("],", "],<br>").replace("[[", "<br>[[") + " en tabla " + k +"<br>"
	return infoTemp
# END [prepareBody]

