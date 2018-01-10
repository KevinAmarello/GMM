# START [getSheetWithComodin]
# Returns the list of sheets that contain comodines
def getSheetWithComodin():
	return ["KTPTCNT", "KTPTCOT", "KTPTCPT", "KTPTDOT", "KTPT6WT", "KTPTDIT", "KTPTBCT", "KTPTDJT", "KTPTDMT", "KTPTDLT"] #
	# Add 6WT
	#"KTPTCLT"
# END [getSheetWithComodin]


# START [getComodinColumnBySheet]
# Returns the comodin columns for each sheet
def getComodinColumnBySheet(sheetName):
	switcher = {
		"KTPTCNT": ["INTABULA", "CDCOAINT", "CDREGGMM", "INCONTMM", "CDPLAN"],
		"KTPTCOT": ["CDREGGMM", "CDDEDUCI"],
		"KTPTCPT": ["CDPLAN", "CDREGGMM", "CDDEDUCI", "CDPRODCO"],
		"KTPTDOT": ["CDPLAN", "CDREGION", "CDDEDUCI", "CDPRODCO"],
		"KTPTDJT": ["VACOSEGU", "VALIMCCI", "CDPLAN", "CDCOAINT"],
		"KTPTDIT": ["CDPRODCO", "TCSEGMEN", "INTABULA"],
		"KTPTDMT": ["CDPRODCO"],
		"KTPTBCT": ["TCSEGPLA"], 
		"KTPT6WT": ["CDPLAN"],
		#"KTPTCLT": ["CDPRODCO", "TCSEGMEN", "INTABULA"],
		"KTPTDLT": ["CDPLAN"]
	}
	return switcher.get(sheetName)
# END [getComodinColumnBySheet]


# START [getComodinColumnBySheet]
# Returns the comodin columns for each sheet
def getConditionedComodinColumnBySheet(sheetName):
	switcher = {
		"KTPTCNT": ["INTABULA", "CDCOAINT", "CDREGGMM", "INCONTMM"],
		"KTPTCOT": ["CDREGGMM", "CDDEDUCI"],
		"KTPTCPT": ["CDPLAN", "CDREGGMM", "CDDEDUCI"],
		"KTPTDOT": ["CDPLAN", "CDREGION", "CDDEDUCI"],
		"KTPTDJT": ["VACOSEGU", "VALIMCCI"]
		# Add 6WT
	}
	return switcher.get(sheetName)
# END [getComodinColumnBySheet]


# START [getComodinValueBySheet]
# Returns the value that takes the comodin for each sheet
def getComodinValueBySheet(sheetName, comodin):
	switcher = {
		("KTPTCNT", "CDPLAN"): "ZZZZZ",
		("KTPTCNT", "CDCOAINT"): "X",
		("KTPTCNT", "CDREGGMM"): "ZZZZZZZZ",
		("KTPTCNT", "INCONTMM"): "X",
		("KTPTCNT", "INTABULA"): "ZZZZ",
		("KTPTCOT", "CDREGGMM"): "ZZZZZZZZ",
		("KTPTCOT", "CDDEDUCI"): "ZZZZ",
		("KTPTCPT", "CDPLAN"): "XXXXX",
		("KTPTCPT", "CDREGGMM"): "ZZZZZZZZ",
		("KTPTCPT", "CDDEDUCI"): "ZZZZ",
		("KTPTCPT", "CDPRODCO"): "ZZZZZZZZZZ",
		("KTPTDOT", "CDPLAN"): "XXXXX",
		("KTPTDOT", "CDREGION"): "XXXXXXXX",
		("KTPTDOT", "CDDEDUCI"): "XXXX",
		("KTPTDOT", "CDPRODCO"): "ZZZZZZZZZZ",
		("KTPTDJT", "VACOSEGU"): "999999999999",
		("KTPTDJT", "VALIMCCI"): "999999999999",
		("KTPTDJT", "CDPLAN"): "ZZZZZ",
		("KTPTDJT", "CDCOAINT"): "Z",
		("KTPTDIT", "CDPRODCO"): "ZZZZZZZZZZ",
		("KTPTDIT", "TCSEGMEN"): "ZZ",
		("KTPTDIT", "INTABULA"): "ZZ",
		("KTPTDMT", "CDPRODCO"): "ZZZZZZZZZZ",
		("KTPTBCT", "TCSEGPLA"): "ZZ",
		("KTPT6WT", "CDPLAN"): "ZZZZZ",
		("KTPTDLT", "CDPLAN"): "ZZZZZ"
		# TODO KTPTCLT
	}
	return switcher.get((sheetName, comodin))
# END [getComodinValueBySheet]


# START [getComodinValueBySheet]
# Returns the value that takes the comodin for each sheet fittin with the conditions
def getConditionedComodinValueBySheet(sheetName, comodin):
	switcher = {
		("KTPTCNT", "INTABULA"): "XXXX",
		("KTPTCNT", "CDCOAINT"): "X",
		("KTPTCNT", "CDREGGMM"): "XXXXXXXX",
		("KTPTCNT", "INCONTMM"): "X",
		("KTPTCOT", "CDREGGMM"): "XXXXXXXX",
		("KTPTCOT", "CDDEDUCI"): "XXXX",
		("KTPTCPT", "CDPLAN"): "XXXXX",
		("KTPTCPT", "CDREGGMM"): "ZZZZZZZZ",
		("KTPTCPT", "CDDEDUCI"): "ZZZZ",
		("KTPTDOT", "CDPLAN"): "XXXXX",
		("KTPTDOT", "CDREGION"): "XXXXXXXX",
		("KTPTDOT", "CDDEDUCI"): "XXXX",
		("KTPTDJT", "VACOSEGU"): "999999999999",
		("KTPTDJT", "VALIMCCI"): "999999999999"
		#TODO 6WT 
	}
	return switcher.get((sheetName, comodin))
# END [getComodinValueBySheet]


# START [getConditionColumnBySheet]
# Returns the conditions whom depend the comodines for each sheet
def getConditionColumnBySheet(sheetName):
	switcher = {
		"KTPTCNT": ["CDPRODCO", "CDPLAN"],
		"KTPTCOT": ["CDPRODCO", "CDPLAN"],
		"KTPTCPT": ["CDPRODCO"],
		"KTPTDOT": ["CDPRODCO"],
		"KTPTDJT": ["CDPRODCO"]
	}
	return switcher.get(sheetName)
# END [getConditionColumnBySheet]


# START [getConditionValueBySheet]
# Return the value for each condition for each sheet
def getConditionValueBySheet(sheetName, cond):
	switcher = {
		("KTPTCNT", "CDPRODCO"): (1,4),
		("KTPTCNT", "CDPLAN"): (20,21,22,23,24,32),
		("KTPTCOT", "CDPRODCO"): (1,4),
		("KTPTCOT", "CDPLAN"): (20,21,22,23,24),
		("KTPTCPT", "CDPRODCO"): (1,4),
		("KTPTDOT", "CDPRODCO"): (1,4),
		("KTPTDJT", "CDPRODCO"): (7,-1)
	}
	return switcher.get((sheetName, cond))
# END [getConditionValueBySheet]


# START [getIntegerColumnBySheet]
def getIntegerColumnBySheet(sheetName):
	switcher = {
		"KTPTCNT": ["CDCOAINT", "CDPLAN"],
		"KTPTCPT": ["CDPLAN", "CDPRODCO"],
		"KTPTDOT": ["CDPLAN", "CDPRODCO"],
		"KTPTDJT": ["CDPLAN", "CDCOAINT"],
		"KTPTDIT": ["CDPRODCO", "TCSEGMEN", "INTABULA"],
		"KTPTDMT": ["CDPRODCO"],
		"KTPTBCT": ["TCSEGPLA"], 
		"KTPT6WT": ["CDPLAN"],
		#"KTPTCLT": ["CDPRODCO", "TCSEGMEN", "INTABULA"],
		"KTPTDLT": ["CDPLAN"]
	}
	return switcher.get(sheetName)
# END [getIntegerColumnBySheet]


# START [getDecimalColumnBySheet]
def getDecimalColumnBySheet(sheetName):
	switcher = {
		"KTPTDJT": ["VACOSEGU", "VALIMCCI"]
	}
	return switcher.get(sheetName)
# END [getDecimalColumnBySheet]	