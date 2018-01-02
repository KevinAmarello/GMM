import json
import logging

from flask import Flask, request, Response

from srcpy.Service import FinalExportService, DataValidationService, RegControlService

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
		return Response("Un error ocurrio. Favor de reintentar.", status = 420)	

@app.route('/queueValidate', methods=['POST'])
def queueValidate():
	logging.debug("***** Received request queueValidate *****")
	return DataValidationService.backgroundValidation()

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