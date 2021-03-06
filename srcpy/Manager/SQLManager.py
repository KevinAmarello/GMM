import os

import MySQLdb
import logging

from srcpy.Dictionary import SQLDictionary
import config

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
           	  db = config.DATABASE_NAME,
           	  charset = "utf8")

	    # If the unix socket is unavailable, then try to connect using TCP. This
	    # will work if you're running a local MySQL server or using the Cloud SQL
	    # proxy, for example:
	    #
	    #   $ cloud_sql_proxy -instances=your-connection-name=tcp:3306
	    #
		else:
			self.db = MySQLdb.connect('35.192.228.4', CLOUDSQL_USER, CLOUDSQL_PASSWORD, config.DATABASE_NAME)
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
		cursor = self._executeQuery("SHOW columns FROM {0}".format(tableName))
		listC = []
		for x in cursor:
			listC.append(x[0])
		return listC
	# END [_getColumnsName]


	# START [_getTable]
	# Returns the content of the table <tableName>
	def _getTable(self, tableName):		
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
		return "SELECT * FROM {0}".format(tableName)
	# END [_getSelectQuery]


	# START [_getColumnByTableQuery]
	def _getColumnByTableQuery(self, table, column):
		return "SELECT {0} FROM {1}".format(column, table)
	# END [_getColumnByTableQuery]


	# START [_getSelectCountQuery]
	# Returns the query to select the whole table
	def _getSelectCountQuery(self, tableName):
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


	# START [getSelectConditionedComodinQuery]
	# Returns the query to insert data into the table
	def getSelectConditionedComodinQuery(self, tableName, comodinName, value, conditionNames):
		if len(conditionNames) == 2:
			return "SELECT DISTINCT {cond[0]}, {cond[1]} FROM {table} WHERE {comodinColumn} = \'{conditionedValue}\'".format(cond = conditionNames, comodinColumn = comodinName, table = tableName, conditionedValue = value)
		else:
			return "SELECT DISTINCT {cond[0]} FROM {table} WHERE {comodinColumn} = \'{conditionedValue}\'".format(cond = conditionNames, comodinColumn = comodinName, table = tableName, conditionedValue = value)
	# END [getSelectConditionedComodinQuery]


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
			if isinstance(data, float):
				row_data.append(float(data))
			elif isinstance(data, int):
				row_data.append(int(data))
			else:
				row_data.append(str(data))
		output.append(row_data)
	return output


