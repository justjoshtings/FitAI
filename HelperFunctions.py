from pandas import ExcelWriter

class HelperFunctions:
	'''
	Object to house helper methods.
	'''
	def __init__(self):
		return

	def df_to_excel(self, df, filename, sheetname):
		'''
		Funtion to save Pandas DFs to Excel file.
		'''
		self.filepath = 'DataWarehouse/' + filename + '.xlsx'
		self.writer = ExcelWriter(self.filepath)
		df.to_excel(self.writer, sheet_name = sheetname)
		self.writer.save()

	# def dates_between(self):