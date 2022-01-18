

import re
import csv
import time
import platform

# to read data
import pandas as pd

# web automator
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# parse html content
from bs4 import BeautifulSoup

#print pretty format 
import pprint

# requests
import requests

pp = pprint.PrettyPrinter(indent=4)


class SebastianArScraper():
	input_file = './input.csv'
	DELAY = 20
	i = 0

	DB_TEMP = {}
	ITEM = {   
		'full baths': '',
		'half baths': '',
		'bldg actual value': '',
		'land actual value': '',
		'living area': '',
		'owner address': '',
		'owner state': '',
		'owner city': '',
		'owner zip': '',
		'owner name': '',
		'parcel No.': '',
		'property type': '',
		'property use': '',
		'sale price': '',
		'sale date': '',
		'site address': '',
		'site state': '',
		'site city': '',
		'site zip': '',
		'total actual value': '',
		'year built': '',

		'Full_Address': '',
		'Street_Address': '',
		'Street_No': '',
		'Street_Name': '',
		'Suffix': '',
	}

	def __init__(self):
		self.driver = webdriver.Chrome(executable_path='./chromedriver.exe')
		self._get_data()
		#self.login()

	def _get_data(self):
		"""
			this function read a input file
			and get "Parcel Number" column
		"""

		self.data = pd.read_csv(self.input_file, dtype={'Street_No': object})
		self.data = pd.read_csv(self.input_file, dtype={'Street_Name': object})


	def start(self):
		length = len(self.data.iloc[:])
		
		try:
			with open('./index.csv', 'r') as f:
				start = f.readlines()[0].replace('\n','')
				if start:
					start = int(start)
				else:
					start = 0
		except:
			start = 0
		
		
		for index, row in self.data.iloc[start:].iterrows(): #use iloc[i:]
			time.sleep(5)
			self.item = self.ITEM.copy()
			self.item['Full_Address'] = row['Full_Address']
			self.item['Street_Address'] = row['Street_Address']
			self.item['Street_No'] = row['Street_No']
			self.item['Street_Name'] = row['Street_Name']
			self.item['Suffix'] = row['Suffix']

			print("Scraping ============== {}/{} ======== parcel {}".format(
				index,
				length,
				self.item['parcel No.']
			))

			print(self.item['parcel No.'])

			self.driver.get('https://www.actdatascout.com/RealProperty/Arkansas/Garland')
			while True:
				try:
					parcel = self.driver.find_element_by_xpath("//a[contains(text(),'Physical Address')]")
					parcel.click()
					break
				except:
					pass

			time.sleep(3)

			input_parcel = self.driver.find_element_by_id('StreetNumber')
			input_parcel.send_keys(Keys.CONTROL + "a")
			input_parcel.send_keys(Keys.DELETE)
			time.sleep(1)
			input_parcel.send_keys(self.item['Street_No'])
			input_parcel1 = self.driver.find_element_by_id('StreetName')
			input_parcel1.send_keys(Keys.CONTROL + "a")
			input_parcel1.send_keys(Keys.DELETE)
			input_parcel1.send_keys(self.item['Street_Name'])
			time.sleep(3)
			submit = self.driver.find_element_by_id('RPAddressSubmit')
			submit.click()

			time.sleep(20)
			
			while True:
				try:
					trs = self.driver.find_elements_by_xpath('//*[@id="RealPropertyResultsTable"]/tbody/tr')
					if trs != []:
						tds = trs[0].find_elements_by_tag_name('td')
						tds[0].find_element_by_tag_name('button').click()
						break
					else:
						print("There is nothing to scrrap")
						break
				except:
					pass
					time.sleep(4)
			
			

			sections = self.driver.find_elements_by_xpath('//div[@class="panel panel-generic"]')
			try:
				building = [self.driver.find_element_by_xpath('//div[@class="panel panel-residentialMain"]')]
			except:
				building = []
			sections = sections + building
			for section in sections:
				value = section.find_element_by_class_name('panel-heading').text
				print(value)
				if 'Property Owner' in value:
					trs = section.find_elements_by_tag_name('tr')
					for tr in trs:
						data = tr.find_elements_by_tag_name('td')
						label = data[0].text
						value = data[1]

						if 'Name:' in label:
							self.item['owner name'] = value.text
						elif 'Mailing Address:' in label:
							owner_address = value.text.split('\n')

							if len(owner_address) == 2:
								self.item['owner address'] = owner_address[0]
								self.item['owner city'] = " ".join(owner_address[1].split(' ')[:-2])
								self.item['owner state'] = owner_address[1].split(' ')[-2]
								self.item['owner zip'] = owner_address[1].split(' ')[-1]
							elif len(owner_address) == 3:
								owner_address = owner_address[1:]
								self.item['owner address'] = owner_address[0]
								self.item['owner city'] = " ".join(owner_address[1].split(' ')[:-2])
								self.item['owner state'] = owner_address[1].split(' ')[-2]
								self.item['owner zip'] = owner_address[1].split(' ')[-1]
							elif len(owner_address) == 4:
								owner_address = owner_address[2:]
								self.item['owner address'] = owner_address[0]
								self.item['owner city'] = " ".join(owner_address[1].split(' ')[:-2])
								self.item['owner state'] = owner_address[1].split(' ')[-2]
								self.item['owner zip'] = owner_address[1].split(' ')[-1]
							else:
								print(owner_address)
								exit()
						elif 'Type:' in label:
							self.item['property type'] = value.text
				
				elif 'Property Information' in value:
					trs = section.find_elements_by_tag_name('tr')
					for tr in trs:
						data = tr.find_elements_by_tag_name('td')
						label = data[0].text
						value = data[1].text

						if 'Physical Address:' in label:
							self.item['site address'] = value
							break
				
				elif 'Market and Assessed Values' in value:
					#parce Owner details
					trs = section.find_elements_by_tag_name('tr')[1:]
					for tr in trs:
						data = tr.find_elements_by_tag_name('td')
						type_value = data[0].text
						value = data[1].text

						if 'Land' in type_value:
							self.item['land actual value'] = value
						elif 'Building' in type_value:
							self.item['bldg actual value'] = value
						elif 'Totals' in type_value:
							self.item['total actual value'] = value

				elif 'Deed Transfers' in value:
					trs = section.find_elements_by_tag_name('tr')[1:]
					tr = trs[0]
					tds = tr.find_elements_by_tag_name('td')

					self.item['sale date'] = tds[0].text
					self.item['sale price'] = tds[5].text.replace('$','')
				
				elif 'Details for Residential Card 1' in value:
					trs = section.find_elements_by_tag_name('tr')[1:]
					for tr in trs:
						data = tr.find_elements_by_tag_name('td')
						self.item['property use'] = data[0].text
						self.item['living area'] = data[3].text
						self.item['year built'] = data[6].text
						break
					
					table = section.find_elements_by_tag_name('table')[1]
					trs = table.find_elements_by_tag_name('tr')
					tds = trs[0].find_elements_by_tag_name('td')
					td = tds[3].text
					baths_data = td.split('Half:')
					self.item['full baths'] = baths_data[0].replace('Full: ','')
					self.item['half baths'] = baths_data[1].strip()
			

			self.write_in_csv(self.item, index)

	def write_in_csv(self, item, index):
		pp.pprint(item)
		with open("SEBASTIAN_AR_results_details.csv", 'a+', newline='') as f:  # Just use 'w' mode in 3.x
			w = csv.DictWriter(f, self.ITEM.keys())
			if self.i == 0:
				w.writeheader()
			w.writerow(item)
			self.i+=1
		
		with open('index.csv', 'w') as f:
			write = csv.writer(f)
			write.writerow([index])

if __name__ == '__main__':
	scraper = SebastianArScraper()
	scraper.start()
