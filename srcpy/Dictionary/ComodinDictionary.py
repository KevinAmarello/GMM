# START [getTableWithComodin]
# Returns the list of table that contain comodines
# We consider table with comodin a table that presents a column where:
# - An alphanumeric value is expected in a numeric column
# - A column's value depends on other ones
def getTableWithComodin():
	return ["KTPTCNT", "KTPTCOT", "KTPTCPT", "KTPT6WT", "KTPTDOT", "KTPTDJT", "KTPTDIT", "KTPTDMT", "KTPTCLT", "KTPTDLT"]
# END [getTableWithComodin]


# START [getComodinColumnByTable]
# Returns the comodin columns for each table, these columns 
# present default or conditioned comodin value
def getComodinColumnByTable(table):
	switcher = {
		"KTPTCNT": ["INTABULA", "CDCOAINT", "CDREGGMM", "CDPLAN", "INCONTMM"],
		"KTPTCOT": ["CDREGGMM", "CDDEDUCI"],
		"KTPTCPT": ["CDPRODTE", "CDPRODCO", "CDPLAN", "CDREGGMM", "TCTISUAS", "CDDEDUCI"],
		"KTPT6WT": ["CDPLAN"],
		"KTPTDOT": ["CDPRODCO", "CDPLAN", "CDREGION", "CDDEDUCI"],		
		"KTPTDJT": ["CDPLAN", "CDCOAINT", "VACOSEGU", "VALIMCCI"],
		"KTPTDIT": ["CDPRODCO", "TCSEGMEN", "INTABULA"],
		"KTPTDMT": ["CDPRODCO"],
		"KTPTCLT": ["CDCOAINT"],
		"KTPTDLT": ["CDPLAN"],
		"KTPTCLT": ["CDCOAINT"],
		"KTPTDLT": ["CDPLAN"]
	}
	return switcher.get(table)
# END [getComodinColumnByTable]


# START [getDefaultComodinColumnByTable]
# Returns columns that present a default comodin value
def getDefaultComodinColumnByTable(table):
	switcher = {
		"KTPTCNT": ["INTABULA", "CDREGGMM", "CDPLAN"],
		"KTPTCOT": ["CDREGGMM", "CDDEDUCI"],
		"KTPTCPT": ["CDPRODTE", "CDPRODCO", "TCTISUAS", "CDDEDUCI", "VASUASEG"],
		"KTPT6WT": ["CDPLAN"],
		"KTPTDOT": ["CDPRODCO", "CDREGION", "CDDEDUCI"],
		"KTPTDJT": ["CDPLAN", "CDCOAINT", "VACOSEGU", "VALIMCCI"],
		"KTPTDIT": ["CDPRODCO", "TCSEGMEN", "INTABULA"],
		"KTPTDMT": ["CDPRODCO"],
		"KTPTCLT": ["CDCOAINT"],
		"KTPTDLT": ["CDPLAN"]
	}
	return switcher.get(table)
# END [getDefaultComodinColumnByTable]


# START [getConditionedComodinColumnByTable]
# Returns columns that present a conditioned comodin value
# It means that this value depends on others ones
def getConditionedComodinColumnByTable(table):
	switcher = {
		"KTPTCNT": ["INTABULA", "CDCOAINT", "CDREGGMM", "INCONTMM"],
		"KTPTCOT": ["CDREGGMM", "CDDEDUCI"],
		"KTPTCPT": ["CDPLAN", "CDREGGMM", "CDDEDUCI"],
		"KTPTDOT": ["CDPLAN", "CDREGION", "CDDEDUCI"],
		"KTPTDJT": ["VACOSEGU", "VALIMCCI"]
	}
	return switcher.get(table)
# END [getConditionedComodinColumnByTable]


# START [getDefaultComodinValueByTableAndComodin]
# Returns the default comodin value for each couple (table, comodinColumn)
def getDefaultComodinValueByTableAndComodin(table, comodin):
	switcher = {
		("KTPTCNT", "INTABULA"): "ZZZZ",
		("KTPTCNT", "CDREGGMM"): "ZZZZZZZZ",
		("KTPTCNT", "CDPLAN"): "ZZZZZ",
		("KTPTCOT", "CDREGGMM"): "ZZZZZZZZ",
		("KTPTCOT", "CDDEDUCI"): "ZZZZ",
		("KTPTCPT", "CDPRODTE"): "ZZZZZZZZZZ",
		("KTPTCPT", "CDPRODCO"): "ZZZZZZZZZZ",
		("KTPTCPT", "TCTISUAS"): "Z",
		("KTPTCPT", "CDDEDUCI"): "ZZZZ",
		("KTPTCPT", "VASUASEG"): "999999999",
		("KTPT6WT", "CDPLAN"): "ZZZZZ",
		("KTPT6WT", "CDREGION"): "ZZZZZZZZ",
		("KTPTDOT", "CDPRODCO"): "ZZZZZZZZZZ",
		("KTPTDOT", "CDREGION"): "ZZZZZZZZ",
		("KTPTDOT", "CDDEDUCI"): "ZZZZ",		
		("KTPTDJT", "CDPLAN"): "ZZZZZ",
		("KTPTDJT", "CDCOAINT"): "Z",
		("KTPTDJT", "VACOSEGU"): "999999999",
		("KTPTDJT", "VALIMCCI"): "999999999",
		("KTPTDIT", "CDPRODCO"): "ZZZZZZZZZZ",
		("KTPTDIT", "TCSEGMEN"): "ZZ",
		("KTPTDIT", "INTABULA"): "ZZZZ",
		("KTPTDMT", "CDPRODCO"): "ZZZZZZZZZZ",
		("KTPTBCT", "TCSEGPLA"): "ZZ",
		("KTPTCLT", "CDCOAINT"): "Z" ,
		("KTPTDLT", "CDPLAN"): "ZZZZZ"
	}
	return switcher.get((table, comodin))
# END [getDefaultComodinValueByTableAndComodin]


# START [getConditionedComodinValueByTableAndComodin]
# Returns the conditioned comdine value for each couple (table, comodinColumn)
def getConditionedComodinValueByTableAndComodin(table, comodin):
	switcher = {
		("KTPTCNT", "INTABULA"): "XXXX",
		("KTPTCNT", "CDCOAINT"): "X",
		("KTPTCNT", "CDREGGMM"): "XXXXXXXX",
		("KTPTCNT", "INCONTMM"): "X",
		("KTPTCOT", "CDREGGMM"): "XXXXXXXX",
		("KTPTCOT", "CDDEDUCI"): "XXXX",
		("KTPTCPT", "CDPLAN"): "XXXXX",
		("KTPTCPT", "CDREGGMM"): "XXXXXXXX",
		("KTPTCPT", "CDDEDUCI"): "XXXX",
		("KTPTDOT", "CDPLAN"): "XXXXX",
		("KTPTDOT", "CDREGION"): "XXXXXXXX",
		("KTPTDOT", "CDDEDUCI"): "XXXX",
		("KTPTDJT", "VACOSEGU"): "999999999999",
		("KTPTDJT", "VALIMCCI"): "999999999999"
	}
	return switcher.get((table, comodin))
# END [getConditionedComodinValueByTableAndComodin]


# START [getConditionColumnByTable]
# Returns the conditions whom depend the comodines for each sheet
def getConditionColumnByTable(table):
	switcher = {
		"KTPTCNT": ["CDPRODCO", "CDPLAN"],
		"KTPTCOT": ["CDPRODCO", "CDPLAN"],
		"KTPTCPT": ["CDPRODCO"],
		"KTPTDOT": ["CDPRODCO"],
		"KTPTDJT": ["CDPRODCO"]
	}
	return switcher.get(table)
# END [getConditionColumnByTable]


# START [getConditionValueByTableAndColumn]
# Return the value for each condition for each couple (table, conditionColumn)
def getConditionValueByTableAndColumn(table, cond):
	switcher = {
		("KTPTCNT", "CDPRODCO"): ['00001','00004'],
		("KTPTCNT", "CDPLAN"): ['20','21','22','23','24','32'],
		("KTPTCOT", "CDPRODCO"): ['00001','00004'],
		("KTPTCOT", "CDPLAN"): ['20','21','22','23','24'],
		("KTPTCPT", "CDPRODCO"): ['00001','00004'],
		("KTPTCPT", "CDPLAN"): ['XXXXX'],
		("KTPTDOT", "CDPRODCO"): ['00001','00004'],
		("KTPTDJT", "CDPRODCO"): ['00001','00004']
	}
	return switcher.get((table, cond))
# END [getConditionValueByTableAndColumn]


# START [getIntegerColumnByTable]
def getIntegerColumnByTable(table):
	switcher = {
		"KTPTCNT": ["CDCOAINT", "CDPLAN", "INTABULA"],
		"KTPTCPT": ["CDPRODCO", "CDPLAN", "TCTISUAS"],
		"KTPT6WT": ["CDPLAN"],
		"KTPTDOT": ["CDPRODCO", "CDPLAN"],
		"KTPTDJT": ["CDPLAN", "CDCOAINT"],
		"KTPTDIT": ["CDPRODCO", "TCSEGMEN", "INTABULA"],
		"KTPTDMT": ["CDPRODCO"],
		"KTPTCLT": ["CDCOAINT"],
		"KTPTDLT": ["CDPLAN"]
	}
	return switcher.get(table)
# END [getIntegerColumnByTable]


# START [getDecimalColumnByTable]
def getDecimalColumnByTable(table):
	switcher = {
		"KTPTDJT": ["VACOSEGU", "VALIMCCI"]
	}
	return switcher.get(table)
# END [getDecimalColumnByTable]	


# START [getAlphaNumericColumnByTable]
def getAlphaNumericColumnByTable(table):
	switcher = {
		"KTPTCNT": ["CDREGGMM", "INCONTMM"],
		"KTPTCOT": ["CDREGGMM", "CDDEDUCI"],
		"KTPTCPT": ["CDPRODTE", "CDREGGMM", "CDDEDUCI"],
		"KTPT6WT": ["CDREGION"],
		"KTPTDOT": ["CDREGION", "CDDEDUCI"]
	}
	return switcher.get(table)
# END [getAlphaNumericColumnByTable]
