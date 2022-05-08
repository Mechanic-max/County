
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


class WilliamsonTxScraper():
	input_file = './WILLIAMSON TX - Sarah.csv'
	DELAY = 20
	i = 0

	DB_TEMP = {}
	ITEM = {
		'OWNER1': '',
	}

	def __init__(self):
		self.os_str = platform.system()
		self.options = webdriver.ChromeOptions()
		prefs = {'profile.managed_default_content_settings.images': 2}
		self.options.add_experimental_option("prefs", prefs)
		if 'Linux' in self.os_str:
			self.driver = webdriver.Chrome(executable_path='./chromedriver', options=self.options)
		else:
			self.driver = webdriver.Chrome(executable_path='./chromedriver.exe',options=self.options)

		self._get_data()
		#self.login()

	def _get_data(self):
		"""
			this function read a input file
			and get "Parcel Number" column
		"""

		self.data = pd.read_csv(self.input_file, delimiter=';', dtype={'OWNER1': object,'LegalDescription1':object, 'LegalDescription2': object})
		self.data = self.data.fillna('')
		#self.data = self.data.drop_duplicates(subset=['OWNER1', 'LegalDescription1', 'LegalDescription2'])
		#self.data = self.data.loc[self.data['OWNER1']!=''].reset_index(drop=True)

	def search(self, owner, lot, block):
		owner = owner.split('&')[0]

		url_base = "https://dallas.tx.publicsearch.us/results?department=RP&block={}&lot={}&parties=%5B%7B%22term%22%3A%22{}%22%2C%22types%22%3A%5B%22grantee%22%5D%7D%5D&recordedDateRange=17991231%2C20210414&searchType=advancedSearch".format(block, lot, owner)	
		self.driver.get(url_base)

		while True:
			try:
				table = WebDriverWait(self.driver, 4).until(
					EC.presence_of_element_located((By.CLASS_NAME, "a11y-table"))
				)
				break
			except:
				if "Error" in self.driver.title:
					self.driver.get(url_base)
				else:
					self.write_in_csv(self.item)
					return None

			

		trs = table.find_elements_by_tag_name('tr')[2:]
		i = 1
		for tr in trs:
			element = {}
			file_str = 'file date {}'.format(i)
			type_str = 'type {}'.format(i)
			tds = tr.find_elements_by_tag_name('td')
			element['doc_type'] = tds[5].text.strip()
			print(element)
			match = False
			for t in ['W/D','QCD', 'DEED']:
				if t in element['doc_type']:
					match = True
					break
			if not match:
				continue
			element['recorded_date'] = tds[6].text.strip()
			self.item[file_str] = element['recorded_date']
			self.item[type_str] = element['doc_type']
			i+=1
		
		self.write_in_csv(self.item)
		#exit()

	def start(self):
		length = len(self.data.iloc[:])
		try:
			with open('./index_1.csv', 'r') as f:
				start = f.readlines()[0].replace('\n','')
				if start:
					start = int(start)
				else:
					start = 0
		except:
			start = 0
		
		self.driver.get('https://williamsoncountytx-web.tylerhost.net/williamsonweb/user/disclaimer')
		accept_disclaimer = WebDriverWait(self.driver, 4).until(
			EC.presence_of_element_located((By.ID, "submitDisclaimerAccept"))
		)
		accept_disclaimer.click()
		while True:
			if 'user/disclaimer' in self.driver.current_url:
				pass
			else:
				break
			
		for index, row in self.data.iloc[start:].iterrows(): #use iloc[i:]
			with open('index_1.csv', 'w') as f:
					write = csv.writer(f)
					write.writerow([index])
			self.item = {}
			self.item['OWNER1'] = row['OWNER1'].strip()
			self.item['LegalDescription1'] = str(row['LegalDescription1']).strip()
			self.item['LegalDescription2'] = str(row['LegalDescription2']).strip()

			data = {}
			data['grantee'] = self.item['OWNER1']

			
			
			print("============ scraping... ==========  {}/{} ======== owner: {} legal desc #: {} ".format(
				index+1, 
				length,
				self.item['OWNER1'],
				self.item['LegalDescription1'], 
			))
			#self.search(self.item['OWNER1'], self.item['lot'], self.item['block'])

			self.driver.get("https://williamsoncountytx-web.tylerhost.net/williamsonweb/search/DOCSEARCH149S1")
			
			try:
				unselect = WebDriverWait(self.driver, 4).until(
					EC.presence_of_element_located((By.XPATH, '//li[@class="cblist-input-list transition-background"]'))
				)
				unselect.click()
			except:
				pass
			
			input_field = WebDriverWait(self.driver, 4).until(
				EC.presence_of_element_located((By.ID, "field_GranteeID"))
			)
			input_field.send_keys(self.item['OWNER1'].split('&')[0])

			self.driver.execute_script("window.scrollTo(0, 400)")

			btn_submit = WebDriverWait(self.driver, 4).until(
				EC.presence_of_element_located((By.ID, "searchButton"))
			)
			
			btn_submit.click()
			time.sleep(4)
			#568847321
			source  = self.driver.page_source
			soup = BeautifulSoup(source, 'html.parser')
			rows = soup.find_all('div', {'class': 'selfServiceSearchRowRight'})
			number_match = 0
			i = 1
			for row in rows:
				file_str = 'file date {}'.format(i)
				type_str = 'type {}'.format(i)
				desc = 'legal desc {}'.format(i)
				legal_desc  = row.find_all('div', {'class': 'searchResultFourColumn'})[-1]
				
				h1 = row.find('h1')
				h1 = h1.text.replace('\n',' ').replace('\t',' ').split()
				header = " ".join(h1).split(' • ')
				id_property, type_, date = header
				match = False
				for t in ['W/D','QCD', 'DEED']:
					if t in type_:
						match = True
						break
				
				if match:
					
					data[type_str] = type_
					data[file_str] = date
					data[desc] = legal_desc.text.replace('\n','').replace('Legal Description','').strip()
					i+=1

				else:
					continue
			
			self.write_in_csv(data)

			"""
			self.driver.close()
			if 'Linux' in self.os_str:
				self.driver = webdriver.Chrome(executable_path='./chromedriver', options=self.options)
			else:
				self.driver = webdriver.Chrome(executable_path='./chromedriver.exe',options=self.options)
			
			self.driver.get('https://williamsoncountytx-web.tylerhost.net/williamsonweb/user/disclaimer')
			accept_disclaimer = WebDriverWait(self.driver, 4).until(
				EC.presence_of_element_located((By.ID, "submitDisclaimerAccept"))
			)
			accept_disclaimer.click()
			while True:
				if 'user/disclaimer' in self.driver.current_url:
					pass
				else:
					break
			"""

	def write_in_csv(self, item):
		pp.pprint(item)
		with open("WILLIAMSON_results_1.csv", 'a+', newline='') as f:  # Just use 'w' mode in 3.x
			# using csv.writer method from CSV package
			write = csv.writer(f)
			
			write.writerow(item.values())



if __name__ == '__main__':
	scraper = WilliamsonTxScraper()
	#scraper.login()
	scraper.start()
