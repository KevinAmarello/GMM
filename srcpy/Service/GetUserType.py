import logging

from flask import Response, json

from srcpy.Manager.SQLManager import SQLManagerClass

# START [getType]
def getType(mail):
	logging.debug("GetUserType Entry: " + mail)
	result = "" 
	sqlM = SQLManagerClass()
	logging.debug("SELECT TYPE FROM UserType WHERE MAIL = \'{mail}\'".format(mail = mail))
	userType = sqlM._executeQuery("SELECT TYPE FROM UserType WHERE MAIL = \'{mail}\'".format(mail = mail))
	logging.debug(str(userType))
	if len(userType) == 0:
		logging.debug("Type not found")
		result = "None"
	else:
		logging.debug("Type found")
		result = userType[0][0]

	# Format JSON
	payload = {}
	payload['type'] = result

	return Response(response = json.dumps(payload), status = 200, mimetype='application/json')
# END [getType]


