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
