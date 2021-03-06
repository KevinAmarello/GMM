# START [_getCreateTableQuery]
# Used to create tables
def _getCreateTableQuery(title):
	switcher = {
		'CONTROL_CIFRAS': "CREATE TABLE CONTROL_CIFRAS(TABLENAME CHAR(7), CIFRAS INT)",
		'KTPT8AT': "CREATE TABLE KTPT8AT(FEVALOR DEC(8,0), CDPRODTE CHAR(10), CDPRODCO CHAR(10), TCNUMVER DEC(4), CDPLAN CHAR(5), CDREGION CHAR(8), CDESTAN CHAR(1), CDZONCEE CHAR(1), IMPRIMTA DEC(15,3))",
		'KTPTDGT': "CREATE TABLE KTPTDGT(FEVALOR DEC(8,0), CDPRODTE CHAR(10), CDPRODCO CHAR(10), CDMCT CHAR(10), CDPLAN CHAR(5), EDEDAD DEC(5,0), VAPRICOB DEC(15,3))",
		'KTPTDIT': "CREATE TABLE KTPTDIT(FEVALOR DEC(8,0), CDPRODTE CHAR(10), CDPRODCO CHAR(10), CDMCT CHAR(10), TCSEGMEN CHAR(2), CDPLAN CHAR(5), INTABULA CHAR(4), CDDEDUCI CHAR(4), CDREGION CHAR(8), EDEDAD DEC(5,0), VAPRICOB DEC(15,3))",
		'KTPTDMT': "CREATE TABLE KTPTDMT(FETARIFA DEC(8,0), CDPRODTE CHAR(10), CDPRODCO CHAR(10), CDMCT CHAR(10), CDPLAN CHAR(5), CDREGGMM CHAR(8), CDDESTIN CHAR(1), CDESTAN CHAR(1), VAFACTAR DEC(15,3))",
		'KTPTBCT': "CREATE TABLE KTPTBCT(FETARIFA DEC(8,0), CDPRODTE CHAR(10), CDPRODCO CHAR(10), CDMCT CHAR(10), TCSEGPLA CHAR (2), CDREGGMM CHAR(8), CDSUASEG CHAR(3), VASUASEG DEC(15,3), VAFCTTAR DEC(7,6))",
		'KTPTAST': "CREATE TABLE KTPTAST(FEVALOR DEC(8,0), CDPLAN CHAR(5), CDREGGMM CHAR(8), TCSEXOA CHAR(1), EDEDAD DEC(5,0), VAPRICO DEC(15,3))",
		'KTPTDLT': "CREATE TABLE KTPTDLT(FEVALOR DEC(8,0), CDPRODTE CHAR(10), CDPRODCO CHAR(10), TCTIPMOV CHAR(1), CDPLAN CHAR(5), TCCDMODE CHAR(3), NUASGTIT DEC(8), IMPRIMA DEC(15,3))",
		'KACTPAT': "CREATE TABLE KACTPAT(FEVALOR DEC(8,0), CDPRODTE CHAR(10), CDPRODCO CHAR(10), CTNUANIN DEC(3), CTNUANFI DEC(3), IMSANAC DEC(15,3), CDMOSANA CHAR(3), IMSAEXT DEC(15,3), CDMOSAEX CHAR(3))",
		'KTPT8LT': "CREATE TABLE KTPT8LT(FECDESDE DEC(8,0), CDTIPNEG CHAR(1), CDPLAN CHAR(5), VASUASEG DEC(15,3))",
		'KTPTBQT': "CREATE TABLE KTPTBQT(TCNUMVER DEC(4), CDTIPNEG CHAR(1), CDMCT CHAR(10), CDSUASEG CHAR(3), VASAEGNA DEC(15,3), VASAEGIN DEC(15,3))",
		'KTPTCKT': "CREATE TABLE KTPTCKT(FEVALOR DEC(8,0), CDPRODTE CHAR(10), CDPRODCO CHAR(10), CDPARAM1 CHAR(10), CDPLAN CHAR(5), CDTIPPOL CHAR(2), CDPARAM2 CHAR(10), AAVIGENC DEC(4), CPASLINN DEC(17,3), CPASLINI DEC(17,3))",
		'KTPTDJT': "CREATE TABLE KTPTDJT(FEVALOR DEC(8,0), CDPRODTE CHAR(10), CDPRODCO CHAR(10), CDMCT CHAR(10), CDPLAN CHAR(5), CDCOAINT CHAR(1), VACOSEGU DEC(15,3), VACOAINT DEC(17,3), VALIMCCI DEC(17,3))",
		'KTPTDNT': "CREATE TABLE KTPTDNT(CDPRODTE CHAR(10), CDPRODCO CHAR(10), INTIPLAN CHAR(5), FETARIFA DEC(8,0), CDMCT CHAR(10), INNIORIG CHAR(5), INNICONT CHAR(5), CDSAPERM CHAR(3), CPASEGUR DEC(15,3), CPTARIF DEC(15,3))",
		'KTPTCNT': "CREATE TABLE KTPTCNT(FEVALOR DEC(8,0), CDPRODTE CHAR(10), CDPRODCO CHAR(10), TCNUMVER DEC(4), INTABULA CHAR(4), EDEDAD DEC(5,0), CDGRDEDU DEC(4), CDCOAINT CHAR(1), CDREGGMM CHAR(8), TCSEXO CHAR(1), CDPLAN CHAR(5), INCONTMM CHAR(1), VAPRICOB DEC(15,3))",
		'KTPTCPT': "CREATE TABLE KTPTCPT(FEVALOR DEC(8,0), CDPRODTE CHAR(10), CDPRODCO CHAR(10), TCNUMVER DEC(4), CDPLAN CHAR(5), CDREGGMM CHAR (8), TCTISUAS CHAR(1), CDSUASEG CHAR(3), CDDEDUCI CHAR(4), EDAD DEC(5,0), VASUASEG DEC(15,3), VAFCTTAR DEC(7,6))",
		'KTPTCOT': "CREATE TABLE KTPTCOT(FEVALOR DEC(8,0), CDPRODTE CHAR(10), CDPRODCO CHAR(10), TCNUMVER DEC(4), CDREGGMM CHAR (8), CDPLAN CHAR(5), INTABULA CHAR(4), CDDEDUCI CHAR(4), EDAD DEC(5,0), VAFCTTAR DEC(7,6))",
		'KTPTDFT': "CREATE TABLE KTPTDFT(FEVALOR DEC(8,0), CDPRODTE CHAR(10), CDPRODCO CHAR(10), TCNUMVER DEC(4), CDPLAN CHAR(5), TCSEXO CHAR(1), EDEDAD DEC(5,0), TCTIDEDU CHAR(1), CDDEDUCI CHAR(4), VADEDUNA DEC(17,3), VADEDUIN DEC(17,3), VAFCTTAR DEC(7,6), CDUNDENA CHAR(3), CDUNDEIN CHAR(3))",
		'KTPT6WT': "CREATE TABLE KTPT6WT(TCNUMVER DEC(4), CDPLAN CHAR(5), CDREGION CHAR(8), CDDEDUCI CHAR(4), VADEDUNA DEC(17,3), VADEDUIN DEC(17,3), VAFCTTAR DEC(7,6), CDUNDENA CHAR(3), CDUNDEIN CHAR(3))",
		'KTPTDOT': "CREATE TABLE KTPTDOT(FEVALOR DEC(8,0), CDPRODTE CHAR(10), CDPRODCO CHAR(10), TCNUMVER DEC(4), CDPLAN CHAR(5), CDREGION CHAR(8), CDCOAINT CHAR(1), CDDEDUCI CHAR(4), EDAD DEC(5,0), VACOANAC DEC(17,3), VACOAINT DEC(17,3), VAFCTTAR DEC(7,6), VACOASVI DEC(17,3))",
		'KTPTCQT': "CREATE TABLE KTPTCQT(FEVALOR DEC(8,0), CDPRODTE CHAR(10), CDPRODCO CHAR(10), CDDEDUCI CHAR(4), CDGRDEDU DEC(4))",
		'KTPTCLT': "CREATE TABLE KTPTCLT(FEVALOR DEC(8,0), CDPRODTE CHAR(10), CDPRODCO CHAR(10), CDMCT CHAR(10), CDTIPPOL CHAR(2), EDEDAD DEC(5,0), CDCOAINT CHAR(1), CDDEDUCI CHAR(4), INTABULA CHAR(4), CDREGGMM CHAR(8), VAPRICOB DEC(15,3))",
		'KTPT8BT': "CREATE TABLE KTPT8BT(CDPRODTE CHAR(10), CDPRODCO CHAR(10), CDMCT CHAR(10), FEVALOR DEC(8,0), CDPLAN CHAR(5), CDTIPPOL CHAR(2), CDREGION CHAR(8), CPASLINN DEC(17,3), CPASLINI DEC(17,3))"
	}
	return switcher.get(title)
# END [_getCreateTableQuery]


# START [_getCatalogCreateTableQuery]
# Used to create tables
def _getCatalogCreateTableQuery(title):
	switcher = {
		"VERSION": "CREATE TABLE VERSION(FECHA CHAR(8), TABLA CHAR(7), PRODUCTOTECNICO CHAR(10), PRODUCTOCOMERCIAL CHAR(10), CODIGODELPLAN CHAR(5), VERSIONACTUAL CHAR(4), VERSIONNUEVA CHAR(4))",
		"PRODUCTOS": "CREATE TABLE PRODUCTOS(PRODUCTOTECNICO CHAR(10), PRODUCTOCOMERCIAL CHAR(10), NOMBRE CHAR(20), CODIGODELPLAN CHAR(5), DESCRIPCIONDELPLAN CHAR(20))",
		"DEDUCIBLE": "CREATE TABLE DEDUCIBLE(CDELEMEN CHAR(4), DSELEMEN DEC(17,3), TIPO CHAR(20), NCODIGO CHAR(4))",
		"SUMA ASEGURADA": "CREATE TABLE SUMA_ASEGURADA(CDELEMEN CHAR(3), DSELEMEN DEC(17,3), TIPO CHAR(20), NCODIGO CHAR(3))",
		"CM": "CREATE TABLE CM(CDELEMEN CHAR(4), DSELEMEN CHAR(20))",
		"REGION": "CREATE TABLE REGION(CDELEMEN CHAR(10), DSELEMEN CHAR(20))",		
		"COASEGURO": "CREATE TABLE COASEGURO(CDELEMEN CHAR(3), DSELEMEN CHAR(15))",
		"Concentrado": "CREATE TABLE Concentrado(VERSION CHAR(7), PRODUCTOS CHAR(7), DEDUCIBLES CHAR(7), SUMA_ASEGURADA CHAR(7), CM CHAR(7), REGION CHAR(7), COASEGURO CHAR(7))"
	}
	return switcher.get(title)
# END [_getCatalogCreateTableQuery]


# START [_getInsertTableQuery]
# Used to insert values in the table 
def _getInsertTableQuery(title):
	switcher = {	
		'CONTROL_CIFRAS': "INSERT INTO CONTROL_CIFRAS VALUES({table}, {value})",
		'KTPT8AT': "INSERT INTO {title} VALUES({v[0]}, {v[1]}, {v[2]}, {v[3]}, {v[4]}, {v[5]}, {v[6]}, {v[7]}, {v[8]})",
		'KTPTDGT': "INSERT INTO {title} VALUES({v[0]}, {v[1]}, {v[2]}, {v[3]}, {v[4]}, {v[5]}, {v[6]})",
		'KTPTDIT': "INSERT INTO {title} VALUES({v[0]}, {v[1]}, {v[2]}, {v[3]}, {v[4]}, {v[5]}, {v[6]}, {v[7]}, {v[8]}, {v[9]}, {v[10]})",
		'KTPTDMT': "INSERT INTO {title} VALUES({v[0]}, {v[1]}, {v[2]}, {v[3]}, {v[4]}, {v[5]}, {v[6]}, {v[7]}, {v[8]})",
		'KTPTBCT': "INSERT INTO {title} VALUES({v[0]}, {v[1]}, {v[2]}, {v[3]}, {v[4]}, {v[5]}, {v[6]}, {v[7]}, {v[8]})",
		'KTPTAST': "INSERT INTO {title} VALUES({v[0]}, {v[1]}, {v[2]}, {v[3]}, {v[4]}, {v[5]})",
		'KTPTDLT': "INSERT INTO {title} VALUES({v[0]}, {v[1]}, {v[2]}, {v[3]}, {v[4]}, {v[5]}, {v[6]}, {v[7]})",
		'KACTPAT': "INSERT INTO {title} VALUES({v[0]}, {v[1]}, {v[2]}, {v[3]}, {v[4]}, {v[5]}, {v[6]}, {v[7]}, {v[8]})",
		'KTPT8LT': "INSERT INTO {title} VALUES({v[0]}, {v[1]}, {v[2]}, {v[3]})",
		'KTPTBQT': "INSERT INTO {title} VALUES({v[0]}, {v[1]}, {v[2]}, {v[3]}, {v[4]}, {v[5]})",
		'KTPTCKT': "INSERT INTO {title} VALUES({v[0]}, {v[1]}, {v[2]}, {v[3]}, {v[4]}, {v[5]}, {v[6]}, {v[7]}, {v[8]}, {v[9]})",
		'KTPTDJT': "INSERT INTO {title} VALUES({v[0]}, {v[1]}, {v[2]}, {v[3]}, {v[4]}, {v[5]}, {v[6]}, {v[7]}, {v[8]})",
		'KTPTDNT': "INSERT INTO {title} VALUES({v[0]}, {v[1]}, {v[2]}, {v[3]}, {v[4]}, {v[5]}, {v[6]}, {v[7]}, {v[8]}, {v[9]})",
		'KTPTCNT': "INSERT INTO {title} VALUES({v[0]}, {v[1]}, {v[2]}, {v[3]}, {v[4]}, {v[5]}, {v[6]}, {v[7]}, {v[8]}, {v[9]}, {v[10]}, {v[11]}, {v[12]})",
		'KTPTCPT': "INSERT INTO {title} VALUES({v[0]}, {v[1]}, {v[2]}, {v[3]}, {v[4]}, {v[5]}, {v[6]}, {v[7]}, {v[8]}, {v[9]}, {v[10]}, {v[11]})",
		'KTPTCOT': "INSERT INTO {title} VALUES({v[0]}, {v[1]}, {v[2]}, {v[3]}, {v[4]}, {v[5]}, {v[6]}, {v[7]}, {v[8]}, {v[9]})",
		'KTPTDFT': "INSERT INTO {title} VALUES({v[0]}, {v[1]}, {v[2]}, {v[3]}, {v[4]}, {v[5]}, {v[6]}, {v[7]}, {v[8]}, {v[9]}, {v[10]}, {v[11]}, {v[12]}, {v[13]})",
		'KTPT6WT': "INSERT INTO {title} VALUES({v[0]}, {v[1]}, {v[2]}, {v[3]}, {v[4]}, {v[5]}, {v[6]}, {v[7]}, {v[8]})",
		'KTPTDOT': "INSERT INTO {title} VALUES({v[0]}, {v[1]}, {v[2]}, {v[3]}, {v[4]}, {v[5]}, {v[6]}, {v[7]}, {v[8]}, {v[9]}, {v[10]}, {v[11]}, {v[12]})",
		'KTPTCQT': "INSERT INTO {title} VALUES({v[0]}, {v[1]}, {v[2]}, {v[3]}, {v[4]})",
		'KTPTCLT': "INSERT INTO {title} VALUES({v[0]}, {v[1]}, {v[2]}, {v[3]}, {v[4]}, {v[5]}, {v[6]}, {v[7]}, {v[8]}, {v[9]}, {v[10]})",
		'KTPT8BT': "INSERT INTO {title} VALUES({v[0]}, {v[1]}, {v[2]}, {v[3]}, {v[4]}, {v[5]}, {v[6]}, {v[7]}, {v[8]})"
	}
	return switcher.get(title)
# END [_getInsertTableQuery]



# START [_getCatalogInsertTableQuery]
# Used to insert values in the table 
def _getCatalogInsertTableQuery(title):
	switcher = {
		"VERSION": "INSERT INTO VERSION VALUES({v[0]}, {v[1]}, {v[2]}, {v[3]}, {v[4]}, {v[5]}, {v[6]})",
		"PRODUCTOS": "INSERT INTO PRODUCTOS VALUES({v[0]}, {v[1]}, {v[2]}, {v[3]}, {v[4]})",
		"DEDUCIBLE": "INSERT INTO DEDUCIBLE VALUES({v[0]}, {v[1]}, {v[2]}, {v[3]})",
		"SUMA ASEGURADA": "INSERT INTO SUMA_ASEGURADA VALUES({v[0]}, {v[1]}, {v[2]}, {v[3]})",
		"CM": "INSERT INTO CM VALUES({v[0]}, {v[1]})",
		"REGION": "INSERT INTO REGION VALUES({v[0]}, {v[1]})",		
		"COASEGURO": "INSERT INTO COASEGURO VALUES({v[0]}, {v[1]})",
		"Concentrado": "INSERT INTO Concentrado VALUES({v[0]}, {v[1]}, {v[2]}, {v[3]}, {v[4]}, {v[5]}, {v[6]})"
	}
	return switcher.get(title)
# END [_getInsertTableQuery]