import os

import MySQLdb
from decimal import *
import logging

from srcpy.Dictionary import SQLDictionary

# These environment variables are configured in app.yaml.
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')

class SQLManagerClass:

	def __init__(self):		
		logging.debug("SQLManager Init")
		# When deployed to App Engine, the `SERVER_SOFTWARE` environment variable
		# will be set to 'Google App Engine/version'.
		if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        	# Connect using the unix socket located at
        	# /cloudsql/cloudsql-connection-name.
			cloudsql_socket = os.path.join('/cloudsql', CLOUDSQL_CONNECTION_NAME)
			self.db = MySQLdb.connect(
          	  unix_socket = cloudsql_socket,
          	  user = CLOUDSQL_USER,
           	  passwd = CLOUDSQL_PASSWORD,
           	  db = "PBA",
           	  charset = "utf8")

	    # If the unix socket is unavailable, then try to connect using TCP. This
	    # will work if you're running a local MySQL server or using the Cloud SQL
	    # proxy, for example:
	    #
	    #   $ cloud_sql_proxy -instances=your-connection-name=tcp:3306
	    #
		else:
			self.db = MySQLdb.connect('35.192.228.4', CLOUDSQL_USER, CLOUDSQL_PASSWORD, "PBA")
		self.cursor = self.db.cursor()


	# START [_getAllTablesName]
	# Returns a list of all table names
	def _getAllTablesName(self):		
		logging.debug("SQLManager _getAllTablesName")
		return self._executeQuery("SHOW TABLES")
	# END [_getAllTablesName]


	# START [_getColumnsName]
	# Retuns the columns' name of the specified table
	def _getColumnsName(self, tableName):
		logging.debug("SQLManager _getColumnsName")
		return self._executeQuery("SHOW columns FROM {0}".format(tableName))
	# END [_getColumnsName]


	# START [_getTable]
	# Returns the content of the table <tableName>
	def _getTable(self, tableName):		
		logging.debug("SQLManager _getTable")
		return self._executeQuery(self._getSelectQuery(tableName))	
	# END [_getTable]


	# START [_executeQuery]
	# Executes the query and return result
	def _executeQuery(self, SQLQuery):		
		self.cursor.execute(SQLQuery)
		return sortResult(self.cursor)
	# END [_executeQuery]


	# START [_getSelectQuery]
	# Returns the query to select the whole table
	def _getSelectQuery(self, tableName):		
		logging.debug("SQLManager _getSelectQuery")
		return "SELECT * FROM {0}".format(tableName)
	# END [_getSelectQuery]


	# START [_getColumnByTableQuery]
	def _getColumnByTableQuery(self, table, column):
		logging.debug("SQLManager _getColumnByTable")
		return "SELECT {0} FROM {1}".format(column, table)
	# END [_getColumnByTableQuery]


	# START [_getSelectCountQuery]
	# Returns the query to select the whole table
	def _getSelectCountQuery(self, tableName):
		logging.debug("SQLManager _getSelectCountQuery")
		return "SELECT COUNT(*) FROM {0}".format(tableName)
	# END [_getSelectCountQuery]


	# START [_getCreateTableQuery]
	# Returns the query to create the table
	def _getCreateTableQuery(self, tableName):
		return SQLDictionary._getCreateTableQuery(tableName)
	# END [_getCreateTableQuery]


	# START [_getDropTableQuery]
	# Returns the query to delete the table
	def _getDropTableQuery(self, tableName):
		return "DROP TABLE IF EXISTS {0}".format(tableName)
	# END [_getDropTableQuery]


	# START [_getInsertIntoQuery]
	# Returns the query to insert data into the table
	def _getInsertIntoQuery(self, tableName, listValues):
		SQLQuery = SQLDictionary._getInsertTableQuery(tableName)
		SQLQuery = SQLQuery.format(title = tableName, v = listValues)
		return SQLQuery
	# END [_getInsertIntoQuery]


	# START [_getInsertIntoCCQuery]
	# Returns the query to insert data into the table
	def _getInsertIntoCCQuery(self, tableName, value):
		SQLQuery = SQLDictionary._getInsertTableQuery("CONTROL_CIFRAS")
		SQLQuery = SQLQuery.format(table = tableName, value = value)
		return SQLQuery
	# END [_getInsertIntoCCQuery]


	# START [getSelectComodinQuery]
	# Returns the query to insert data into the table
	def getSelectComodinQuery(self, tableName, comodinName, conditionNames, conditionValues):
		logging.debug("cN: "+ str(conditionNames) + " - cV: " + str(conditionValues))
		if len(conditionNames) == 2:
			return "SELECT DISTINCT {com} FROM {t} WHERE {cN[0]} IN {cV[0]} AND {cN[1]} IN {cV[1]}".format(com = comodinName, t = tableName, cN = conditionNames, cV = conditionValues)
		else:
			#if(len(conditionValues) == 1):
			#	return "SELECT {com} FROM {t} WHERE {cN[0]} = {cV[0]}".format(com = comodinName, t = tableName, cN = conditionNames, cV = conditionValues)
			#else:
			return "SELECT DISTINCT {com} FROM {t} WHERE {cN[0]} IN {cV[0]}".format(com = comodinName, t = tableName, cN = conditionNames, cV = conditionValues)
	# END [getSelectComodinQuery]


	# START [_closeConnection]
	# Close connection with the database
	def _closeConnection(self):
		self.db.close()
	# END [_closeConnection]
	#################################################
	################# END CLASS #####################

def sortResult(cursor):
	output = []
	for row in cursor:
		row_data = []
		for data in row:
			if type(data) is Decimal:
				row_data.append(float(data))
			else:
				row_data.append(str(data))
		output.append(row_data)
	return output

