import csv
import pprint

import pandas as pd

class BaseScraper(object):
	ITEM = {}
	base_cols = [
		'baths',  
		'site address', 
		'total value', 
		'property type', 
		'owner zip', 
		'owner address', 
		'sale price', 
		'owner state', 
		'property class', 
		'owner city', 
		'beds', 
		'owner name', 
		'parcel id', 
		'half baths', 
		'year built', 
		'sale date', 
		'land value', 
		'living area',
		'bldg value', 
		'url', 
		'full bath', 
		'half bath',
		'building value',
		'site zip', 
		'legal desc', 
		'mail zip', 
		'market value', 
		'property use code', 
		'property id', 
		'assessed value', 
		'mail state', 
		'site state', 
		'mail city', 
		'mail address', 
		'property use desc', 
		'geographic id', 
		'appraised value', 
		'site city',
		'land_area',
	]
	pp = pprint.PrettyPrinter(indent=4)
	i = 0

	def __init__(self):
		self.input_file_path = 'Santa Rosa CA Acella (01-01-2020 - 03-23-2021) Enforcement (1).csv'
		self.output_file_path = 'Results_Santa Rosa CA Acella (01-01-2020 - 03-23-2021) Enforcement (1).csv'
		self.buid_base_item()
		self.read_input_file()
	
	def buid_base_item(self):
		"""
			Build base item based
			on file cols
		"""
		for col in self.inputs_cols:
			self.ITEM[col] = ''
		
		for col in self.base_cols:
			self.ITEM[col] = ''
	
	def read_input_file(self):
		"""
			Reads the input file and returns a pandas dataframe
		"""
		self.data = pd.read_csv(self.input_file_path, dtype=object)
		self.data = self.data.fillna('')

	def write_in_csv(self, item):
		self.pp.pprint(item)
		with open(self.output_file_path, 'a+', newline='', encoding='utf-8') as f:  # Just use 'w' mode in 3.x
			w = csv.DictWriter(f, self.ITEM.keys())
			if self.i == 0:
				w.writeheader()
			w.writerow(item)
			self.i = self.i + 1
