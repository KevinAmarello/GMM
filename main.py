import json
import logging

from flask import Flask, request, Response

from srcpy.Service import FinalExportService, DataValidationService, RegControlService, CatalogApplyService, GetHistorialService, GetUserType

app = Flask(__name__)

############## Data Validation Service ##############
@app.route('/uploadPBA', methods=['POST'])
def validateData():
	try:
		logging.debug("***** Received request uploadPBA *****")
		response = []
		if request.files['file'] is not None:
			excelPBA = request.files['file']
			response = DataValidationService.handleService(excelPBA)
		else:
			response = Response("Favor de seleccionar un archivo Excel.", status = 420)	
		response.headers['Access-Control-Allow-Origin'] = '*'
		return response
	except Exception as e:
		logging.debug(str(e))

@app.route('/queueValidate', methods=['POST'])
def queueValidate():
	logging.debug("***** Received request queueValidate *****")
	url = request.form['url']
	return DataValidationService.backgroundValidation(url)

########### Final Export Service ############
@app.route('/exportFiles', methods=['GET'])
def exportService():
	logging.debug("***** Received request exportFiles *****")
	response = FinalExportService.handleService()
	response.headers['Access-Control-Allow-Origin'] = '*'
	return response

@app.route('/queueExport', methods=['POST'])
def queueExport():
	logging.debug("***** Received request queueExport *****")
	return FinalExportService.backgroundExport()

########### Control de cifras Service ####################
@app.route('/isThereCC', methods=['GET'])
def isThereControlCifrasTableinDatabase():
	logging.debug("***** Received request isThereCC *****")
	##########################
	# A VOIR COMMENT RETOURNER CA
	return str(RegControlService.isThereControlCifrasTableinDatabase())

@app.route('/uploadCC', methods=['POST'])
def uploadCC():
	logging.debug('***** Received request uploadCC *****')
	response = RegControlService.uploadControlCifras(request)
	response.headers['Access-Control-Allow-Origin'] = '*'
	return response

########## Catalog Apply Service ########################
@app.route('/uploadCatalog', methods=['POST'])
def uploadCatalog():
	logging.debug('***** Received request uploadCatalog *****')
	try:
		response = []
		if request.files['file'] is not None:
			excelCatalog = request.files['file']
			response = CatalogApplyService.handleService(excelCatalog)
		else:
			response = Response("Favor de seleccionar un archivo Excel.", status = 420)	
		response.headers['Access-Control-Allow-Origin'] = '*'
		return response
	except Exception as e:
		return str(e)

@app.route('/queueApplyCatalog', methods=['POST'])
def queueApply():
	logging.debug('***** Received request queueApply *****')
	url = request.form['url']
	return CatalogApplyService.backgroundApply(url)


########## GET Historial Service #######################

@app.route('/getHistory', methods = ['GET'])
def history():
	logging.debug("***** Received request getHistory *****")
	return GetHistorialService.handleService()
	#response = GetHistorialService.handleService()
	#response.headers['Access-Control-Allow-Origin'] = '*'
	#return response

@app.route('/getUserType', methods = ['POST'])
def utype():
	logging.debug("***** Received request getUserType *****")
	mail = request.form['mail']
	return GetUserType.getType(mail)
	