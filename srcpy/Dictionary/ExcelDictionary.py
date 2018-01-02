# START [firstLineOfDataDictionary]
def firstLineOfDataDictionary(sheetName):
	switcher = {
		'KTPT8AT': 75,
		'KTPTDGT': 48,
		'KTPTDIT': 100,
		'KTPTDMT': 35,
		'KTPTBCT': 18,
		'KTPTAST': 18,
		'KTPTDLT': 74,
		'KACTPAT': 23,
		'KTPT8LT': 43,
		'KTPTBQT': 23,
		'KTPTCKT': 60,
		'KTPTDJT': 67,
		'KTPTDNT': 37,
		'KTPTCNT': 92,
		'KTPTCPT': 174,
		'KTPTCOT': 91,
		'KTPTDFT': 63,
		'KTPT6WT': 159,
		'KTPTDOT': 95,
		'KTPTCQT': 120
	}
	return switcher.get(sheetName)
# END [firstLineOfDataDictionary]


# START [_registryNumberCell]
def registryNumberCell(sheetName):
	switcher = {
		'KTPT8AT': 'I71',
		'KTPTDGT': 'I44',
		'KTPTDIT': 'J96',
		'KTPTDMT': 'I30',
		'KTPTBCT': 'I14',
		'KTPTAST': 'I14',
		'KTPTDLT': 'I68',
		'KACTPAT': 'I18',
		'KTPT8LT': 'I39',
		'KTPTBQT': 'I17',
		'KTPTCKT': 'J56',
		'KTPTDJT': 'I63',
		'KTPTDNT': 'I33',
		'KTPTCNT': 'I88',
		'KTPTCPT': 'I170',
		'KTPTCOT': 'I87',
		'KTPTDFT': 'I57',
		'KTPT6WT': 'I156',
		'KTPTDOT': 'J91',
		'KTPTCQT': 'I116'
	}
	return switcher.get(sheetName)
# END [_registryNumberCell]