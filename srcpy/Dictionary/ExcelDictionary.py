# START [firstLineOfDataDictionary]
def firstLineOfDataDictionary(sheetName):
	switcher = {
		'KTPT8AT': 17,
		'KTPTDGT': 15,
		'KTPTDIT': 19,
		'KTPTDMT': 17,
		'KTPTBCT': 17,
		'KTPTAST': 14,
		'KTPTDLT': 16,
		'KACTPAT': 17,
		'KTPT8LT': 12,
		'KTPTBQT': 14,
		'KTPTCKT': 18,
		'KTPTDJT': 17,
		'KTPTDNT': 18,
		'KTPTCNT': 22,
		'KTPTCPT': 20,
		'KTPTCOT': 18,
		'KTPTDFT': 22,
		'KTPT6WT': 17,
		'KTPTDOT': 21,
		'KTPTCQT': 13,
		'KTPTCLT': 19,
		'KTPT8BT': 17
	}
	return switcher.get(sheetName)
# END [firstLineOfDataDictionary]


# STAR [getEndColumnCatalog]
def getEndColumnCatalog(sheet):
	switcher = {
		"VERSION": 7,
		"PRODUCTOS": 5,
		"DEDUCIBLE": 4,
		"SUMA ASEGURADA": 4,
		"CM": 2,
		"REGION": 2,
		"COASEGURO": 2,
		"Concentrado": 7
	}
	return switcher.get(sheet)
# STAR [getEndColumnCatalog]