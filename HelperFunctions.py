from pandas import ExcelWriter
import datetime as dt
from datetime import datetime, timedelta
from sqlalchemy import create_engine

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
		df.to_excel(self.writer, sheet_name = sheetname, index=False)
		self.writer.save()

	def dates_between(self, start_date, end_date, days_threshold):
		'''
		Function to break up a start and end date range by the days threshold.
		For example, 100 days limit between start and end date.
		'''
		
		start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
		end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

		marker_date = start_date + timedelta(days=int(days_threshold))
		
		start_date_list = []
		start_date_list.append(start_date)
		end_date_list = []
		end_date_list.append(marker_date)

		while marker_date < end_date:
			next_start_date = marker_date + timedelta(days=1)
			next_end_date = next_start_date + timedelta(days=int(days_threshold))

			marker_date = next_end_date
			
			start_date_list.append(next_start_date)
			if marker_date >= end_date:
				end_date_list.append(end_date)
			else:
				end_date_list.append(next_end_date)
				
		return start_date_list, end_date_list


	def df_to_db(self, df):
		'''
		Function to connect to DB and push data into
		https://www.fullstackpython.com/blog/export-pandas-dataframes-sqlite-sqlalchemy.html
		'''

		engine = create_engine('sqlite:///DataWarehouse/Personal_DB.db', echo=True)
		sqlite_connection = engine.connect()

		sqlite_table = 'sleep'
		df.to_sql(sqlite_table, sqlite_connection, if_exists='replace')
		sqlite_connection.close()
