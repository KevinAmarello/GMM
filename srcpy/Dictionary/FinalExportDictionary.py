import datetime

def getFormatByTable(table):
	switcher = {
		"KTPTCNT": (("DEC", 8, 0), ("CHAR", 10), ("CHAR", 10), ("DEC", 4, 0), ("CHAR", 4), ("DEC", 5, 0), ("DEC", 4, 0), ("CHAR", 1), ("CHAR", 8), ("CHAR", 1), ("CHAR", 5), ("CHAR", 1), ("DEC", 15, 3)),
		"KTPTCOT": (("DEC", 8, 0), ("CHAR", 10), ("CHAR", 10), ("DEC", 4, 0), ("CHAR", 8), ("CHAR", 5), ("CHAR", 4), ("CHAR", 4), ("DEC", 5, 0), ("DEC", 7, 6)),
		"KTPT6WT": (("DEC", 4, 0), ("CHAR", 5), ("CHAR", 8), ("CHAR", 4), ("DEC", 17, 3), ("DEC", 17, 3), ("DEC", 7, 6), ("CHAR", 3), ("CHAR", 3)),
		"KTPTCPT": (("DEC", 8, 0), ("CHAR", 10), ("CHAR", 10), ("DEC", 4, 0), ("CHAR", 5), ("CHAR", 8), ("CHAR", 1), ("CHAR", 3), ("CHAR", 4), ("DEC", 5, 0), ("DEC", 15, 3), ("DEC", 7, 6)),
		"KTPTDFT": (("DEC", 8, 0), ("CHAR", 10), ("CHAR", 10), ("DEC", 4, 0), ("CHAR", 5), ("CHAR", 1), ("DEC", 5, 0), ("CHAR", 1), ("CHAR", 4), ("DEC", 17, 3), ("DEC", 17, 3), ("DEC", 7, 6), ("CHAR", 3), ("CHAR", 3)),
		"KTPTDOT": (("DEC", 8, 0), ("CHAR", 10), ("CHAR", 10), ("DEC", 4, 0), ("CHAR", 5), ("CHAR", 8), ("CHAR", 1), ("CHAR", 4), ("DEC", 5, 0), ("DEC", 17, 3), ("DEC", 17, 3), ("DEC", 7, 6), ("DEC", 17, 3)),
		"KTPTCQT": (("DEC", 8, 0), ("CHAR", 10), ("CHAR", 10), ("CHAR", 4), ("DEC", 4, 0)),
		"KTPTDJT": (("DEC", 8, 0), ("CHAR", 10), ("CHAR", 10), ("CHAR", 10), ("CHAR", 5), ("CHAR", 1), ("DEC", 15, 3), ("DEC", 17, 3), ("DEC", 17, 3)),
		"KTPTDNT": (("CHAR", 10), ("CHAR", 10), ("CHAR", 5), ("DEC", 8, 0), ("CHAR", 10), ("CHAR", 5), ("CHAR", 5), ("CHAR", 3), ("DEC", 15, 3), ("DEC", 15, 3)),
		"KTPT8AT": (("DEC", 8, 0), ("CHAR", 10), ("CHAR", 10), ("DEC", 4, 0), ("CHAR", 5), ("CHAR", 8), ("CHAR", 1), ("CHAR", 1), ("DEC", 15, 3)),
		"KTPTDGT": (("DEC", 8, 0), ("CHAR", 10), ("CHAR", 10), ("CHAR", 10), ("CHAR", 5), ("DEC", 5, 0), ("DEC", 15, 3)),
		"KTPTDIT": (("DEC", 8, 0), ("CHAR", 10), ("CHAR", 10), ("CHAR", 10), ("CHAR", 2), ("CHAR", 5), ("CHAR", 4), ("CHAR", 4), ("CHAR", 8), ("DEC", 5, 0), ("DEC", 15, 3)),
		"KTPTDMT": (("DEC", 8, 0), ("CHAR", 10), ("CHAR", 10), ("CHAR", 10), ("CHAR", 5), ("CHAR", 8), ("CHAR", 1), ("CHAR", 1), ("DEC", 15, 3)),
		"KTPTBCT": (("DEC", 8, 0), ("CHAR", 10), ("CHAR", 10), ("CHAR", 10), ("CHAR", 2), ("CHAR", 8), ("CHAR", 3), ("DEC", 15, 3), ("DEC", 7, 6)),
		"KACTPAT": (("DEC", 8, 0), ("CHAR", 10), ("CHAR", 10), ("DEC", 3, 0), ("DEC", 3, 0), ("DEC", 15, 3), ("CHAR", 3), ("DEC", 15, 3), ("CHAR", 3)),
		"KTPTCLT": (("DEC", 8, 0), ("CHAR", 10), ("CHAR", 10), ("CHAR", 10), ("CHAR", 2), ("DEC", 5, 0), ("CHAR", 1), ("CHAR", 4), ("CHAR", 4), ("CHAR", 8), ("DEC", 15, 3)),
		"KTPTDLT": (("DEC", 8, 0), ("CHAR", 10), ("CHAR", 10), ("CHAR", 1), ("CHAR", 5), ("CHAR", 3), ("DEC", 8, 0), ("DEC", 15, 3)),
		"KTPT8LT": (("DEC", 8, 0), ("CHAR", 1), ("CHAR", 5), ("DEC", 15, 3)),
		"KTPTAST": (("DEC", 8, 0), ("CHAR", 5), ("CHAR", 8), ("CHAR", 1), ("DEC", 5, 0), ("DEC", 15, 3)),
		"KTPTBQT": (("DEC", 4, 0), ("CHAR", 1), ("CHAR", 10), ("CHAR", 3), ("DEC", 15, 3), ("DEC", 15, 3)),
		"KTPTCKT": (("DEC", 8, 0), ("CHAR", 10), ("CHAR", 10), ("CHAR", 10), ("CHAR", 5), ("CHAR", 2), ("CHAR", 10), ("DEC", 4, 0), ("DEC", 17, 3), ("DEC", 17, 3)),
		"KTPT8BT": (("CHAR", 10), ("CHAR", 10), ("CHAR", 10), ("DEC", 8, 0), ("CHAR", 5), ("CHAR", 2), ("CHAR", 8), ("DEC", 17, 3), ("DEC", 17, 3))
	}
	return switcher.get(table)


def commonDataEndLine():
	usuario = "OCGOMEZ"
	empusu = "0001"
	prog = "KTCLMMGE"
	date = datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S.%f")
	return usuario + empusu + prog + str(date) + "\r\n"