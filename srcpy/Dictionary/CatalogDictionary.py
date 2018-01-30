import logging



# START [getSelectQueryByCatalogAndTable]
def getSelectDifferenceQueryByCatalogAndTable(catalog, table):
	"""
		Returns the query to execute to get the intersection of catalog and table
	"""
	if catalog == "VERSION":
		return getSelectVersionDifferenceQueryByTable(table)
	elif catalog == "PRODUCTOS":
		return getSelectProductosDifferenceQueryByTable(table)
	elif catalog == "DEDUCIBLES":
		return getSelectDeducibleDifferenceQueryByTable(table)
	elif catalog == "SUMA_ASEGURADA":
		return getSelectSumaAseguradaDifferenceQueryByTable(table)
	elif catalog == "CM":
		return getSelectCMDifferenceQueryByTable(table)
	elif catalog == "REGION":
		return getSelectRegionDifferenceQueryByTable(table)
	elif catalog == "COASEGURO":
		return getSelectCoaseguroDifferenceQueryByTable(table)
# END [getSelectQueryByCatalogAndTable]


# START [getSelectVersionIntersectionQueryByTable]
# Returns the SQL Query to get the difference between
# the table and the catalog VERSION
def getSelectVersionDifferenceQueryByTable(table):
	# These table have all fields and no comodin
	if table in ["KTPTCOT", "KTPTDFT", "KTPT8AT"]:
		logging.debug("This table have all fields and no comodin")
		return """\
				SELECT {table}.*
				FROM VERSION RIGHT JOIN {table}
				ON VERSION.FECHA = {table}.FEVALOR
				AND VERSION.PRODUCTOTECNICO = {table}.CDPRODTE
				AND VERSION.PRODUCTOCOMERCIAL = {table}.CDPRODCO
				AND VERSION.CODIGODELPLAN = {table}.CDPLAN
				AND VERSION.VERSIONACTUAL = {table}.TCNUMVER
				WHERE VERSION.CODIGODELPLAN IS NULL
				""".format(table = table)
	# This table has all fields and all are comodines
	elif table == "KTPTCPT":
		logging.debug("This table has all fields and all are comodines")
		return """\
				SELECT {table}.*
				FROM VERSION RIGHT JOIN {table}
				ON VERSION.FECHA = {table}.FEVALOR
				AND VERSION.PRODUCTOTECNICO = {table}.CDPRODTE
				AND VERSION.PRODUCTOCOMERCIAL = {table}.CDPRODCO
				AND VERSION.CODIGODELPLAN = {table}.CDPLAN
				AND VERSION.VERSIONACTUAL = {table}.TCNUMVER
				WHERE {table}.CDPLAN NOT IN {valPlan}
				AND {table}.CDPRODCO NOT IN {valCo}
				AND {table}.CDPRODTE NOT IN {valTe}
				AND VERSION.CODIGODELPLAN IS NULL
				""".format(table = table, valPlan = tuple(getValueToIgnoreByTableAndComodin(table, "CDPLAN")), 
											valCo = tuple(getValueToIgnoreByTableAndComodin(table, "CDPRODCO")),
											valTe = tuple(getValueToIgnoreByTableAndComodin(table, "CDPRODTE")))
	# This table has all fields and PRODCO y CDPLAN as comodins
	elif table == "KTPTDOT":
		logging.debug("This table has all fields and PRODCO y CDPLAN as comodins")
		return """\
				SELECT {table}.*
				FROM VERSION RIGHT JOIN {table}
				ON VERSION.FECHA = {table}.FEVALOR
				AND VERSION.PRODUCTOTECNICO = {table}.CDPRODTE
				AND VERSION.PRODUCTOCOMERCIAL = {table}.CDPRODCO
				AND VERSION.CODIGODELPLAN = {table}.CDPLAN
				AND VERSION.VERSIONACTUAL = {table}.TCNUMVER
				WHERE {table}.CDPLAN NOT IN {valPlan}
				AND {table}.CDPRODCO NOT IN {valCo}
				AND VERSION.CODIGODELPLAN IS NULL
				""".format(table = table, valPlan = tuple(getValueToIgnoreByTableAndComodin(table, "CDPLAN")), 
											valCo = tuple(getValueToIgnoreByTableAndComodin(table, "CDPRODCO")))
	# This table has all fields and CDPLAN as comodin
	elif table == "KTPTCNT":
		logging.debug("This table has all fields and CDPLAN as comodin")
		return """\
				SELECT {table}.*
				FROM VERSION RIGHT JOIN {table}
				ON VERSION.FECHA = {table}.FEVALOR
				AND VERSION.PRODUCTOTECNICO = {table}.CDPRODTE
				AND VERSION.PRODUCTOCOMERCIAL = {table}.CDPRODCO
				AND VERSION.CODIGODELPLAN = {table}.CDPLAN
				AND VERSION.VERSIONACTUAL = {table}.TCNUMVER
				WHERE {table}.CDPLAN NOT IN {valPlan}
				AND VERSION.CODIGODELPLAN IS NULL
				""".format(table = table, valPlan = tuple(getValueToIgnoreByTableAndComodin(table, "CDPLAN")))
	# This table has TCNUMVER AND CDPLAN fields and CDPLAN as comodin
	elif table == "KTPT6WT":
		logging.debug("This table has TCNUMVER AND CDPLAN fields and CDPLAN as comodin")
		return """\
				SELECT {table}.*
				FROM VERSION RIGHT JOIN {table}
				ON VERSION.CODIGODELPLAN = {table}.CDPLAN
				AND VERSION.VERSIONACTUAL = {table}.TCNUMVER
				WHERE {table}.CDPLAN NOT IN {valPlan}
				AND VERSION.CODIGODELPLAN IS NULL
				""".format(table = table, valPlan = tuple(getValueToIgnoreByTableAndComodin(table, "CDPLAN")))
# END [getSelectVersionIntersectionQueryByTable]


# START [getSelectProductosDifferenceQueryByTable]
# Returns the SQL Query to get the difference between
# the table and the catalog PRODUCTOS
def getSelectProductosDifferenceQueryByTable(table):
	# These tables have all fields and no comodins
	if table in ["KTPTCOT", "KTPTDFT", "KTPT8AT", "KTPTDGT", "KTPT8BT"]:
		logging.debug("These tables have all fields and no comodins")
		return """\
				SELECT {table}.*
				FROM PRODUCTOS RIGHT JOIN {table}
				ON PRODUCTOS.PRODUCTOTECNICO = {table}.CDPRODTE
				AND PRODUCTOS.PRODUCTOCOMERCIAL = {table}.CDPRODCO
				AND PRODUCTOS.CODIGODELPLAN = {table}.CDPLAN
				WHERE PRODUCTOS.CODIGODELPLAN IS NULL
				""".format(table = table)
	# These tables have all fields and all are comodins
	elif table == "KTPTCPT":
		logging.debug("These tables have all fields and all are comodins")
		return """\
				SELECT {table}.*
				FROM PRODUCTOS RIGHT JOIN {table}
				ON PRODUCTOS.PRODUCTOTECNICO = {table}.CDPRODTE
				AND PRODUCTOS.PRODUCTOCOMERCIAL = {table}.CDPRODCO
				AND PRODUCTOS.CODIGODELPLAN = {table}.CDPLAN
				WHERE {table}.CDPLAN NOT IN {valPlan}
				AND {table}.CDPRODCO NOT IN {valCo}
				AND {table}.CDPRODTE NOT IN {valTe}
				AND PRODUCTOS.CODIGODELPLAN IS NULL
				""".format(table = table, valPlan = tuple(getValueToIgnoreByTableAndComodin(table, "CDPLAN")), 
											valCo = tuple(getValueToIgnoreByTableAndComodin(table, "CDPRODCO")),
											valTe = tuple(getValueToIgnoreByTableAndComodin(table, "CDPRODTE")))
	# This table has all fields and PRODCO and CDPLAN as comodins
	elif table == "KTPTDOT":
		logging.debug("This table has all fields and PRODCO and CDPLAN as comodins")
		return """\
				SELECT {table}.*
				FROM PRODUCTOS RIGHT JOIN {table}
				ON PRODUCTOS.PRODUCTOTECNICO = {table}.CDPRODTE
				AND PRODUCTOS.PRODUCTOCOMERCIAL = {table}.CDPRODCO
				AND PRODUCTOS.CODIGODELPLAN = {table}.CDPLAN
				WHERE {table}.CDPLAN NOT IN {valPlan}
				AND {table}.CDPRODCO NOT IN {valCo}
				AND PRODUCTOS.CODIGODELPLAN IS NULL
				""".format(table = table, valPlan = tuple(getValueToIgnoreByTableAndComodin(table, "CDPLAN")), 
											valCo = tuple(getValueToIgnoreByTableAndComodin(table, "CDPRODCO")))
	# This table has all fields and CDPLAN as comodin
	elif table in ["KTPTCNT", "KTPTCKT", "KTPTDLT"]:
		logging.debug("This table has all fields and CDPLAN as comodin")
		return """\
				SELECT {table}.*
				FROM PRODUCTOS RIGHT JOIN {table}
				ON PRODUCTOS.PRODUCTOTECNICO = {table}.CDPRODTE
				AND PRODUCTOS.PRODUCTOCOMERCIAL = {table}.CDPRODCO
				AND PRODUCTOS.CODIGODELPLAN = {table}.CDPLAN
				WHERE {table}.CDPLAN NOT IN {valPlan}
				AND PRODUCTOS.CODIGODELPLAN IS NULL
				""".format(table = table, valPlan = tuple(getValueToIgnoreByTableAndComodin(table, "CDPLAN")))
	# This table have all fields and PRODCO as comodin
	elif table in ["KTPTDIT", "KTPTDMT"]:
		logging.debug("This table have all fields and PRODCO as comodin")
		return """\
				SELECT {table}.*
				FROM PRODUCTOS RIGHT JOIN {table}
				ON PRODUCTOS.PRODUCTOTECNICO = {table}.CDPRODTE
				AND PRODUCTOS.PRODUCTOCOMERCIAL = {table}.CDPRODCO
				AND PRODUCTOS.CODIGODELPLAN = {table}.CDPLAN
				WHERE {table}.CDPRODCO NOT IN {valCo}
				AND PRODUCTOS.CODIGODELPLAN IS NULL
				""".format(table = table, valCo = tuple(getValueToIgnoreByTableAndComodin(table, "CDPRODCO")))
	# This table has PRODCO and PRODTE as fields and none are comodins
	elif table in ["KTPTCQT", "KTPTDNT", "KTPTBCT", "KTPTCLT", "KACTPAT"]:
		logging.debug("This table has PRODCO and PRODTE as fields and none are comodins")
		return """\
				SELECT {table}.*
				FROM PRODUCTOS RIGHT JOIN {table}
				ON PRODUCTOS.PRODUCTOTECNICO = {table}.CDPRODTE
				AND PRODUCTOS.PRODUCTOCOMERCIAL = {table}.CDPRODCO
				WHERE PRODUCTOS.CODIGODELPLAN IS NULL
				""".format(table = table)
	# This table has CDPLAN as field and no comodin
	elif table in ["KTPT8LT", "KTPTAST"]:
		logging.debug("This table has CDPLAN as field and no comodin")
		return """\
				SELECT {table}.*
				FROM PRODUCTOS RIGHT JOIN {table}
				ON PRODUCTOS.CODIGODELPLAN = {table}.CDPLAN
				WHERE PRODUCTOS.CODIGODELPLAN IS NULL
				""".format(table = table)
	# This table has CDPLAN as field and comodin
	elif table == "KTPT6WT":
		logging.debug("This table has CDPLAN as fiels and comodin")		
		return """\
				SELECT {table}.*
				FROM PRODUCTOS RIGHT JOIN {table}
				ON PRODUCTOS.CODIGODELPLAN = {table}.CDPLAN
				WHERE {table}.CDPLAN NOT IN {valPlan}
				AND PRODUCTOS.CODIGODELPLAN IS NULL
				""".format(table = table, valPlan = tuple(getValueToIgnoreByTableAndComodin(table, "CDPLAN")))
# END [getSelectProductosDifferenceQueryByTable]


# START [getSelectDeducibleDifferenceQueryByTable]
def getSelectDeducibleDifferenceQueryByTable(table):
	# These tables has CDDEDUCI has comodin
	if table in ["KTPTCOT", "KTPTCPT", "KTPTDOT"]:
		logging.debug("This table has CDDEDUCI as comodin")
		return """\
		SELECT {table}.*
		FROM DEDUCIBLE RIGHT JOIN {table}
		ON DEDUCIBLE.CDELEMEN = {table}.CDDEDUCI
		WHERE {table}.CDDEDUCI NOT IN {val} 
		AND DEDUCIBLE.CDELEMEN IS NULL
		""".format(table = table, val = tuple(getValueToIgnoreByTableAndComodin(table, "CDDEDUCI"))) 
	else:
		logging.debug("This table hasnt comodin")
		return """\
		SELECT {table}.*
		FROM DEDUCIBLE RIGHT JOIN {table}
		ON DEDUCIBLE.CDELEMEN = {table}.CDDEDUCI
		WHERE DEDUCIBLE.CDELEMEN IS NULL
		""".format(table = table)
# END [getSelectDeducibleDifferenceQueryByTable]


# START [getSelectSumaAseguradaDifferenceQueryByTable]
def getSelectSumaAseguradaDifferenceQueryByTable(table):
	# These tables have CDSUASEG, VASUASEG
	if table in ["KTPTCPT", "KTPTBCT"]:
		if table == "KTPTCPT":
			logging.debug("This table has VASUASEG as comodin")
			return """\
			SELECT {table}.*
			FROM SUMA_ASEGURADA RIGHT JOIN {table}
			ON SUMA_ASEGURADA.CDELEMEN = {table}.CDSUASEG
			AND SUMA_ASEGURADA.DSELEMEN = {table}.VASUASEG
			WHERE {table}.VASUASEG NOT IN {val}
			AND SUMA_ASEGURADA.CDELEMEN IS NULL
			""".format(table = table, val = tuple(getValueToIgnoreByTableAndComodin(table, "VASUASEG")))
		else:
			logging.debug("This table has CDSUASEG as comodin")
			return """\
			SELECT {table}.*
			FROM SUMA_ASEGURADA RIGHT JOIN {table}
			ON SUMA_ASEGURADA.CDELEMEN = {table}.CDSUASEG
			AND SUMA_ASEGURADA.DSELEMEN = {table}.VASUASEG
			WHERE {table}.CDSUASEG NOT IN {val}
			AND SUMA_ASEGURADA.CDELEMEN IS NULL
			""".format(table = table, val = tuple(getValueToIgnoreByTableAndComodin(table, "CDSUASEG")))
	# These table only have VASUASEG
	elif table in ["KTPT8LT"]:
		logging.debug("This table only has VASUASEG as field")
		query = """\
		SELECT {table}.*
		FROM SUMA_ASEGURADA RIGHT JOIN {table}
		ON SUMA_ASEGURADA.DSELEMEN = {table}.VASUASEG
		WHERE SUMA_ASEGURADA.DSELEMEN IS NULL
		"""
		return query.format(table = table)
	# These table have CDSAPERM, CPASEGUR
	elif table in ["KTPTDNT"]:
		logging.debug("This table has CDSAPERM, CPASEGUR")
		query = """\
		SELECT {table}.*
		FROM SUMA_ASEGURADA RIGHT JOIN {table}
		ON SUMA_ASEGURADA.CDELEMEN = {table}.CDSAPERM
		AND SUMA_ASEGURADA.DSELEMEN = {table}.CPASEGUR
		WHERE SUMA_ASEGURADA.CDELEMEN IS NULL
		"""
		return query.format(table = table)
	elif table in ["KTPTBQT"]:
		logging.debug("This table only has CDSUASEG")
		query = """\
		SELECT {table}.*
		FROM SUMA_ASEGURADA RIGHT JOIN {table}
		ON SUMA_ASEGURADA.CDELEMEN = {table}.CDSUASEG 
		WHERE SUMA_ASEGURADA.CDELEMEN IS NULL
		"""
		return query.format(table = table)
	elif table in ["KTPTCKT"]: 
		logging.debug("This table has CPASLINN and CPASLINI")
		query = """\
		SELECT {table}.*
		FROM SUMA_ASEGURADA RIGHT JOIN {table}
		ON SUMA_ASEGURADA.DSELEMEN = {table}.CPASLINN 
		AND SUMA_ASEGURADA.DSELEMEN = {table}.CPASLINI 
		WHERE SUMA_ASEGURADA.DSELEMEN IS NULL
		"""
		return query.format(table = table)
	elif table in ["KACTPAT"]:
		logging.debug("This table has IMSANAC and IMSAEXT")
		query = """\
		SELECT {table}.*
		FROM SUMA_ASEGURADA RIGHT JOIN {table}
		ON SUMA_ASEGURADA.DSELEMEN = {table}.IMSANAC 
		AND SUMA_ASEGURADA.DSELEMEN = {table}.IMSAEXT 
		WHERE SUMA_ASEGURADA.DSELEMEN IS NULL
		"""
		return query.format(table = table)
# END [getSelectSumaAseguradaDifferenceQueryByTable]


# START [getSelectCMDifferenceQueryByTable]
def getSelectCMDifferenceQueryByTable(table):
	if table == "KTPTCNT":
		logging.debug("This table has INTABULA as comodin")
		query = """\
		SELECT {table}.*
		FROM CM RIGHT JOIN {table}
		ON CM.CDELEMEN = {table}.INTABULA
		WHERE {table}.INTABULA NOT IN {val}
		AND CM.CDELEMEN IS NULL
		"""
		return query.format(table = table, val = tuple(getValueToIgnoreByTableAndComodin(table, "INTABULA")))	
	else:
		logging.debug("This table has no comodin")
		query = """\
		SELECT {table}.*
		FROM CM RIGHT JOIN {table}
		ON CM.CDELEMEN = {table}.INTABULA
		WHERE CM.CDELEMEN IS NULL
		"""
		return query.format(table = table)	
# END [getSelectCMDifferenceQueryByTable]


# START [getSelectRegionDifferenceQueryByTable]
def getSelectRegionDifferenceQueryByTable(table):
	# These tables have CDREGGMM and it is a comodin
	if table in ["KTPTCNT", "KTPTCOT", "KTPTCPT", "KTPTDMT", "KTPTBCT", "KTPTCLT", "KTPTAST"]:
		logging.debug("This table as CDREGGMM as comodin")
		query = """\
		SELECT {table}.*
		FROM REGION RIGHT JOIN {table}
		ON REGION.CDELEMEN = {table}.CDREGGMM
		WHERE {table}.CDREGGMM NOT IN {val}
		AND REGION.CDELEMEN IS NULL
		"""
		return query.format(table = table, val = tuple(getValueToIgnoreByTableAndComodin(table, "CDREGGMM")))
	# These tables have CDREGION
	elif table in ["KTPT6WT", "KTPTDOT", "KTPT8AT", "KTPTDIT", "KTPT8BT"]:
		logging.debug("This table as CDREGION as comodin")
		query = """\
		SELECT {table}.*
		FROM REGION RIGHT JOIN {table}
		ON REGION.CDELEMEN = {table}.CDREGION
		WHERE {table}.CDREGION NOT IN {val}
		AND REGION.CDELEMEN IS NULL
		"""
		return query.format(table = table, val = tuple(getValueToIgnoreByTableAndComodin(table, "CDREGION")))
	# These tables have CDPARAM2
	elif table in ["KTPTCKT"]:
		logging.debug("This table as CDPARAM2 as comodin")
		query = """\
		SELECT {table}.*
		FROM REGION RIGHT JOIN {table}
		ON REGION.CDELEMEN = {table}.CDPARAM2
		WHERE {table}.CDPARAM2 NOT IN {val} 
		AND REGION.CDELEMEN IS NULL
		"""
		return query.format(table = table, val = tuple(getValueToIgnoreByTableAndComodin(table, "CDPARAM2")))
# END [getSelectRegionDifferenceQueryByTable]
	

# START [getSelectCoaseguroDifferenceQueryByTable]
def getSelectCoaseguroDifferenceQueryByTable(table):	
	if table in ["KTPTCNT", "KTPTDOT", "KTPTDJT", "KTPTCLT"]:
		if table == "KTPTDOT":
			logging.debug("This table has no comodin")
			query = """\
			SELECT {table}.*
			FROM COASEGURO RIGHT JOIN {table}
			ON COASEGURO.CDELEMEN = {table}.CDCOAINT
			WHERE COASEGURO.CDELEMEN IS NULL
			"""
			return query.format(table = table)
		else:		
			logging.debug("This table has CDCOAINT as comodin")
			query = """\
			SELECT {table}.*
			FROM COASEGURO RIGHT JOIN {table}
			ON COASEGURO.CDELEMEN = {table}.CDCOAINT
			WHERE {table}.CDCOAINT NOT IN {val}
			AND COASEGURO.CDELEMEN IS NULL
			"""
			return query.format(table = table, val = tuple(getValueToIgnoreByTableAndComodin(table, "CDCOAINT")))
	else:
		logging.debug("This table has TCSEGMEN as comodin")
		query = """\
		SELECT {table}.*
		FROM COASEGURO RIGHT JOIN {table}
		ON COASEGURO.CDELEMEN = {table}.TCSEGMEN
		WHERE {table}.TCSEGMEN NOT IN {val}
		AND COASEGURO.CDELEMEN IS NULL
		"""
		return query.format(table = table, val = tuple(getValueToIgnoreByTableAndComodin(table, "TCSEGMEN")))
# END [getSelectCoaseguroDifferenceQueryByTable]


# START [getColumnBySheet]
def getColumnBySheet(catalog, sheet):
	if catalog == "DEDUCIBLE":
		return "CDDEDUCI"
	if catalog == "SUMA_ASEGURADA":
		if sheet in ["KTPTCPT", "KTPTBCT", "KTPTBQT"]:
			return "CDSUASEG"
		if sheet == "KTPTDNT":
			return "CDSAPERM"
	if catalog == "VERSION":
		return "TCNUMVER"
	return None
# END [getColumnBySheet]


# START [getUpdateVersionQueryByTable]
def getUpdateVersionQueryByTable(table, data):
	"""
		Returns the query to execute to update the version of a table.
	"""
	# KTPT6WT is special as it doesnt need all columns
	if table == "KTPT6WT":

		tcnumverO = ""
		cdplan = "" 
		tcnumvN = "" 

		if is_integer(data[6]):
			tcnumvN = data[6]
		else:
			tcnumvN = "\"{0}\"".format(data[6])

		if is_integer(data[4]):
			cdplan = data[4]
		else:
			cdplan = "\"{0}\"".format(data[4])

		if is_integer(data[5]):
			tcnumverO = data[5]
		else:
			tcnumverO = "\"{0}\"".format(data[5])


		query = """\
		UPDATE KTPT6WT
		SET TCNUMVER = {0}
		WHERE KTPT6WT.CDPLAN = {1}  
		AND KTPT6WT.TCNUMVER = {2}
		"""
		return query.format(tcnumvN, cdplan, tcnumverO)

	else:
		tcnumverO = ""
		cdplan = "" 
		tcnumvN = ""
		cdprodco = "" 
		if is_integer(data[6]):
			tcnumvN = data[6]
		else:
			tcnumvN = "\"{0}\"".format(data[6])

		if is_integer(data[4]):
			cdplan = data[4]
		else:
			cdplan = "\"{0}\"".format(data[4])

		if is_integer(data[5]):
			tcnumverO = data[5]
		else:
			tcnumverO = "\"{0}\"".format(data[5])

		if is_integer(data[3]):
			cdprodco = data[3]
		else:
			cdprodco = "\"{0}\"".format(data[3])


		cdprodte = "\"{0}\"".format(data[2])


		query = """\
		UPDATE {0}
		SET TCNUMVER = {1}
		WHERE {0}.CDPLAN = {2}  
		AND {0}.FEVALOR = {3}  
		AND {0}.CDPRODTE = {4}  
		AND {0}.TCNUMVER = {5}  
		AND {0}.CDPRODCO = {6} 
		"""
		return query.format(data[1], tcnumvN, cdplan, data[0], cdprodte, tcnumverO, cdprodco)
# END [getUpdateVersionQueryByTable]


# START [columnToIgnoreByTable]
# Some table doesnt have some columns, so no check
def columnToIgnoreByTable(table):
	switcher = {
		"KTPT6WT": ["CDPRODCO", "CDPRODTE", "FEVALOR", "TCNUMVER"],
		"KTPTCQT": ["CDPLAN"], 
		"KTPTDNT": ["CDPLAN"],
		"KTPTBCT": ["CDPLAN"],
		"KTPTCLT": ["CDPLAN"],
		"KACTPAT": ["CDPLAN"],
		"KTPT8LT": ["CDPRODCO", "CDPRODTE"],
		"KTPTAST": ["CDPRODCO", "CDPRODTE"]
	}
	return switcher.get(table)
# END [columnToIgnoreByTable]


# START [getTableByToIgnoreComodin]
# Return tables associated to a comodin column
def getTableByToIgnoreComodin(col):
	switcher = {
		# VERSION / PRODUCTOS
		"CDPLAN": ["KTPTCPT", "KTPTDOT", "KTPTCNT", "KTPT6WT", "KTPTDMT", "KTPTCKT", "KTPTDLT"],
		"CDPRODTE": ["KTPTCPT"], 
		"CDPRODCO": ["KTPTCPT", "KTPTDOT", "KTPTDIT", "KTPTDMT"],
		# DEDUCIBLES
		"CDDEDUCI": ["KTPTCOT", "KTPTCPT", "KTPTDOT"],
		# SUMA ASEGURADA
		"VASUASEG": ["KTPTCPT"],
		"CDSUASEG": ["KTPTBCT"],
		# CM
		"INTABULA": ["KTPTCNT"],
		# REGION
		"CDREGGMM": ["KTPTCPT", "KTPTCLT", "KTPTCNT", "KTPTCOT", "KTPTDMT", "KTPTAST"],
		"CDREGION": ["KTPT6WT", "KTPTDOT", "KTPT8AT", "KTPTDIT", "KTPTBCT", "KTPT8BT"],
		"CDPARAM2": ["KTPTCKT"],
		# COASEGURO
		"CDCOAINT": ["KTPTCNT", "KTPTDJT", "KTPTCLT"],
		"TCSEGMEN": ["KTPTDIT"]
	}
	return switcher.get(col)
# END [getTableByToIgnoreComodin]


# START [getValueToIgnoreByTableAndComodin]
# Returns values to ignore for each couple (table, comodin)
# The @@@@ value is a mock to get a query acceptable by MySQL
def getValueToIgnoreByTableAndComodin(table, com):
	switcher = {
		# VERSION / PRODUCTOS
		("KTPTCPT", "CDPLAN"): ("XXXXX", "@@@@@"),
		("KTPTCPT", "CDPRODTE"): ("ZZZZZZZZZZ", "@@@@@"),
		("KTPTCPT", "CDPRODCO"): ("ZZZZZZZZZZ", "@@@@@"),
		("KTPTDOT", "CDPLAN"): ("XXXXX", "@@@@@"),
		("KTPTDOT", "CDPRODCO"): ("ZZZZZZZZZZ", "@@@@@"),
		("KTPTCNT", "CDPLAN"): ("ZZZZZ", "@@@@@"),
		("KTPT6WT", "CDPLAN"): ("ZZZZZ", "@@@@@"),
		("KTPTDMT", "CDPLAN"): ("99999", "@@@@@"),
		("KTPTDMT", "CDPRODCO"): ("ZZZZZZZZZZ", "@@@@@"),
		("KTPTCKT", "CDPLAN"): ("99999", "@@@@@"),
		("KTPTDLT", "CDPLAN"): ("ZZZZZ", "@@@@@"),
		("KTPTDIT", "CDPRODCO"): ("ZZZZZZZZZZ", "@@@@@"),
		# DEDUCIBLES
		("KTPTCOT", "CDDEDUCI"): ("ZZZZ", "XXXX"),
		("KTPTCPT", "CDDEDUCI"): ("ZZZZ", "XXXX"),
		("KTPTDOT", "CDDEDUCI"): ("ZZZZ", "XXXX"),
		# SUMA ASEGURADA
		("KTPTCPT", "VASUASEG"): ("999999999", "0.000"),
		("KTPTBCT", "CDSUASEG"): ("ZZ", "@@@@@"),
		# CM
		("KTPTCNT", "INTABULA"): ("XXXX", "ZZZZ"),
		# REGION
		("KTPTCNT", "CDREGGMM"): ("ZZZZZZZZ", "XXXXXXXX"),
		("KTPTCOT", "CDREGGMM"): ("ZZZZZZZZ", "XXXXXXXX"),
		("KTPTCPT", "CDREGGMM"): ("ZZZZZZZZ", "XXXXXXXX"),
		("KTPT6WT", "CDREGION"): ("ZZZZZZZZ", "@@@@@"),
		("KTPTDOT", "CDREGION"): ("ZZZZZZZZ", "XXXXXXXX"),
		("KTPT8AT", "CDREGION"): ("ZZZZZZZZ", "@@@@@"),
		("KTPTDIT", "CDREGION"): ("ZZZZZZZZ", "@@@@@"),
		("KTPTDMT", "CDREGGMM"): ("XXXXXXXX", "@@@@@"),
		("KTPTBCT", "CDREGGMM"): ("ZZZZZZZZ", "@@@@@"),
		("KTPTCLT", "CDREGGMM"): ("ZZZZZZZZ", "@@@@@"),
		("KTPTAST", "CDREGGMM"): ("XXXXXXXX", "@@@@@"),
		("KTPTCKT", "CDPARAM2"): ("ZZZZZZZZZZ", "@@@@@"),
		("KTPT8BT", "CDREGION"): ("ZZZZZZZZ", "@@@@@"),
		# COASEGURO
		("KTPTCNT", "CDCOAINT"): ("X", "@@@@@"),
		("KTPTDJT", "CDCOAINT"): ("Z", "@@@@@"),
		("KTPTDIT", "TCSEGMEN"): ("ZZ", "@@@@@"),
		("KTPTCLT", "CDCOAINT"): ("Z", "@@@@@")
	}
	return switcher.get((table, com))
# END (getValueToIgnoreByTableAndComodin]

def is_integer(s):
	try:
		int(s)
		return True
	except ValueError:
		return False