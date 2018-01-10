# START [getColumnBySheet]
def getColumnBySheet(catalog, sheet):
	if catalog == "DEDUCIBLES":
		return "CDDEDUCI"
	if catalog == "SUMAASEGURADA":
		if sheet in ["KTPTCPT", "KTPTBCT", "KTPTBQT"]:
			return "CDSUASEG"
		if sheet == "KTPTDNT":
			return "CDSAPERM"
	if catalog == "VERSION":
		return "TCNUMVER"
# END [getColumnBySheet]


# START [getUpdateVersionQueryByTable]
def getUpdateVersionQueryByTable(table, data):
	"""
		Returns the query to execute to update the version of a table.
	"""
	# KTPT6WT is special as it doesnt need all columns
	if table == "KTPT6WT":
		query = """
		UPDATE KTPT6WT
		SET TCNUMVER = {data[6]}
		WHERE {data[4]} = KTPT6WT.CDPLAN
		AND {data[5]} = KTPT6WT.TCNUMVER
		"""
		return query.format(data = data)

	else:
		query = """
		UPDATE {d[1]}
		SET TCNUMVER = {d[6]}
		WHERE {d[4]} = {d[1]}.CDPLAN
		AND {d[0]} = {d[1]}.FEVALOR
		AND {d[2]} = {d[1]}.CDPRODTE
		AND {d[5]} = {d[1]}.TCNUMVER
		AND {d[3]} = {d[1]}.CDPRODCO
		"""
		return query.format(d = data)
# END [getUpdateVersionQueryByTable]


# START [getQueryByCatalogAndTable]
def getQueryByCatalogAndTable(catalog, table):
	"""
		Returns the query to execute to get the intersection of catalog and table
	"""
	if catalog == "PRODUCTOS":
		# These tables only have CDPRODCO and CDPRODTE
		if table in ["KTPTCQT", "KTPTDNT", "KTPTBCT", "KTPTCLT", "KACTPAT"]:
			query = """
			SELECT {table}.* 
			FROM PRODUCTOS RIGHT JOIN {table} 
			ON PRODUCTOS.PRODUCTOTECNICO = {table}.CDPRODTE
			AND PRODUCTOS.PRODUCTOCOMERCIAL = {table}.CDPRODCO
			WHERE PRODUCTOS.PRODUCTOTECNICO IS NULL
			"""
			return query.format(table = table)

		# These tables only have CDPLAN
		elif table in ["KTPT6WT", "KTPT8LT", "KTPTAST"]:
			query = """
			SELECT {table}.*
			FROM PRODUCTOS RIGHT JOIN {table} 
			ON PRODUCTOS.CODIGODELPLAN = {table}.CDPLAN
			WHERE PRODUCTOS.CODIGODELPLAN IS NULL
			"""
			return query.format(table = table)

		# Complete tables
		else:
			query = """
			SELECT {table}.*
			FROM PRODUCTOS RIGHT JOIN {table} 
			ON PRODUCTOS.PRODUCTOTECNICO = {table}.CDPRODTE
			AND PRODUCTOS.PRODUCTOCOMERCIAL = {table}.CDPRODCO
			AND PRODUCTOS.CODIGODELPLAN = {table}.CDPLAN
			WHERE PRODUCTOS.CODIGODELPLAN IS NULL
			"""
			return query.format(table = table)
	elif catalog == "DEDUCIBLES":
		query= """
		SELECT {table}.*
		FROM DEDUCIBLE RIGHT JOIN {table}
		ON DEDUCIBLE.CDELEMEN = {table}.CDDEDUCI
		WHERE DEDUCIBLE.CDELEMEN IS NULL
		"""
		return query.format(table = table)
	elif catalog == "SUMAASEGURADA":
		# These tables have CDSUASEG, VASUASEG
		if table in ["KTPTCPT", "KTPTBCT"]:
			query = """
			SELECT {table}.*
			FROM SUMA_ASEGURADA RIGHT JOIN {table}
			ON SUMA_ASEGURADA.CDELEMEN = {table}.CDSUASEG
			AND SUMA_ASEGURADA.DSELEMEN = {table}.VASUASEG
			WHERE SUMA_ASEGURADA.CDELEMEN IS NULL
			"""
			return query.format(table = table)
		# These table only have VASUASEG
		elif table in ["KTPT8LT"]:
			query = """
			SELECT {table}.*
			FROM SUMA_ASEGURADA RIGHT JOIN {table}
			ON SUMA_ASEGURADA.DSELEMEN = {table}.VASUASEG
			WHERE SUMA_ASEGURADA.DSELEMEN IS NULL
			"""
			return query.format(table = table)
		# These table have CDSAPERM, CPASEGUR
		elif table in ["KTPTDNT"]:
			query = """
			SELECT {table}.*
			FROM SUMA_ASEGURADA RIGHT JOIN {table}
			ON SUMA_ASEGURADA.CDELEMEN = {table}.CDSAPERM
			AND SUMA_ASEGURADA.DSELEMEN = {table}.CPASEGUR
			WHERE SUMA_ASEGURADA.CDELEMEN IS NULL
			"""
			return query.format(table = table)

	


		# KTPTBQT   A DEFINIR
		# KTPTCKT   A DEFINIR

	elif catalog == "CM":
		query = """
		SELECT {table}.*
		FROM REGION RIGHT JOIN {table}
		ON CM.CDELEMEN = {table}.INTABULA
		WHERE CM.CDELEMEN IS NULL
		"""
		return query.format(table = table)		
	elif catalog == "REGION":
		# These tables have CDREGGMM
		if table in ["KTPTCNT", "KTPTCOT", "KTPTCPT", "KTPTDMT", "KTPTBCT", "KTPTCLT"]:
			query = """
			SELECT {table}.*
			FROM CM RIGHT JOIN {table}
			ON CM.CDELEMEN = {table}.CDREGMM
			WHERE CM.CDELEMEN IS NULL
			"""
			return query.format(table = table)
		# These tables have CDREGION
		elif table ["KTPT6WT", "KTPTDOT", "KTPT8AT", "KTPTDIT", "KTPTAST", "KTPT8BT"]:
			query = """
			SELECT {table}.*
			FROM CM RIGHT JOIN {table}
			ON CM.CDELEMEN = {table}.CDREGION
			WHERE CM.CDELEMEN IS NULL
			"""
			return query.format(table = table)
		# These tables have CDPARAM2
		elif table ["KTPTCKT"]:
			query = """
			SELECT {table}.*
			FROM CM RIGHT JOIN {table}
			ON CM.CDELEMEN = {table}.CDPARAM2
			WHERE CM.CDELEMEN IS NULL
			"""
			return query.format(table = table)
	elif catalog == "COASEGURO":
		# CDCOAINT
		if table in ["KTPTCNT", "KTPTCOT", "KTPTDJT", "KTPTCLT"]:
			query = """
			SELECT {table}.*
			FROM COASEGURO RIGHT JOIN {table}
			ON COASEGURO.CDELEMEN = {table}.CDCOAINT
			WHERE COASEGURO.CDELEMEN IS NULL
			"""
			return query.format(table = table)
		# TCSEGMEN
		elif table in ["KTPTDIT"]:
			query = """
			SELECT {table}.*
			FROM COASEGURO RIGHT JOIN {table}
			ON COASEGURO.CDELEMEN = {table}.TCSEGMEN
			WHERE COASEGURO.CDELEMEN IS NULL
			"""
			return query.format(table = table)
# END [getQueryByCatalogAndTable]

		

