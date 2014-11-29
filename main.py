import pandas
import datetime

#set format to currency
pandas.options.display.float_format = '${:,.2f}'.format


class MintParse():
	def __init__(self,filename='transactions.csv'):
		self.fname = filename
	def load(self):
		data = pandas.read_csv(self.fname)
		# fix columns with spaces
		cols = data.columns
		cols = cols.map(lambda x: x.replace(' ','_'))
		data.columns = cols		
		# add month and year for later aggregation
		data['year'] = [datetime.datetime.strptime(t,"%m/%d/%Y").year for t in data.Date]
		data['month'] = [datetime.datetime.strptime(t,"%m/%d/%Y").month for t in data.Date]

		self.data = data
		self.debits = data[data['Transaction_Type'].str.contains("debit")]

	def report(self):
		summarydata = self.debits[['Amount','Category','Account_Name','Date']]
		b = summarydata.groupby(['Account_Name'])

		#to do a large summary by date, need to break up dates to groupby parts
		a= self.debits[['Amount','Category','Account_Name','Date','year','month']]
		pt = pandas.pivot_table(a,
			values='Amount',
			index=['Account_Name'],
			columns=['month'],
			fill_value=0.00,
			margins=True,
			aggfunc=sum)
		return {'pivottable': pt, 'summary':b.sum()}

if __name__ == '__main__':
	run = MintParse()
