from io import BytesIO
import logging 
import openpyxl

from srcpy.Dictionary import ExcelDictionary



class ExcelManagerClass:
	def __init__ (self, file, rop):
		logging.debug("ExcelManagerClass init")
		self.wb = openpyxl.load_workbook(filename = BytesIO(file.read()), data_only = True, read_only=rop)


	# START [getListSheetNames]
	# Returns a list of all the sheet names.
	# Those names are future tables'titles
	def _getListSheetNames(self):
		# Get sheet's names
		listSheetNames = self.wb.get_sheet_names() 

		return listSheetNames
	# END [getListSheetNames]

	# START [_getSheetByName]
	# Returns Sheet object
	def _getSheetByName(self, sheetName):
		return self.wb.get_sheet_by_name(sheetName)
	# END [_getSheetByName]


	# START [getWB]
	# Returns Workbook
	def getWB(self):
		return self.wb
	# END [getWB]

# START [setCell]
# Set the specified cell with the value
def setCell(sheet, row, col, value):
	sheet.cell(row = row, column = col, value = value)
# END [setCell]


# START [getFirstLineOfData]
# Set the line to start filling with data
def getFirstLineOfData(tableName):
	return ExcelDictionary.firstLineOfDataDictionary(tableName)
# END [getFirstLineOfData]