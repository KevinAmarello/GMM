import logging
from flask import Response

from srcpy.Manager.SQLManager import SQLManagerClass

# START [isThereControlCifrasTableinDatabase]
def isThereControlCifrasTableinDatabase():
	logging.debug("RegControlService isThereControlCifrasTableinDatabase")
	# Check if the control cifras table exists
	try:
		SQLManagerClass()._getTable("CONTROL_CIFRAS")
		return True
	except:
		return False
# END [isThereControlCifrasTableinDatabase]


# START [uploadControlCifras]
def uploadControlCifras(request):
	"""
		Drops the previous Control_cifras table if it exists
		and creates a new one with values present in the Input JSON.

		Input:
		JSON	-	Table : Value

		Output:
		Response
	"""
	logging.debug("RegControlService uploadControlCifras")
	try:
		sqlManager = SQLManagerClass()
		# Delete table if exists
		dropQuery = sqlManager._getDropTableQuery("CONTROL_CIFRAS")
		sqlManager._executeQuery(dropQuery)

		# Create table 
		logging.debug("RegControlService creating table")
		sqlManager._executeQuery(sqlManager._getCreateTableQuery("CONTROL_CIFRAS"))

		# Get JSON
		logging.debug("RegControlService parsing JSON")
		json = request.get_json()

		# Insert values
		for table in json.keys():
			query = sqlManager._getInsertIntoCCQuery("\"" + str(table) + "\"", json[table])
			logging.debug(str(query))
			sqlManager._executeQuery(query)

		return Response("El control de cifras ha sido tomado en cuenta.", status = 200)
	except Exception as e:
		logging.debug(str(e))
		return Response(str(e), status = 500)
	finally:
		sqlManager._closeConnection()	
# END [uploadControlCifras]