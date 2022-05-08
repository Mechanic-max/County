
import re
import csv
import time

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


class ShelbyAlScraper():
	input_file = './input.csv'
	DELAY = 20
	i = 0

	DB_TEMP = {}
	ITEM = {   
		'baths': '',
		'beds': '',
		'bldg actual value': '',
		'land actual value': '',
		'living area': '',
		'owner address': '',
		'owner state': '',
		'owner city': '',
		'owner zip': '',
		'owner name': '',
		'property type': '',
		'sale amount': '',
		'sale date': '',
		'site address': '',
		'site state': '',
		'site city': '',
		'site zip': '',
		'total actual value': '',
		'year built': '',
		'land use code': '',

		'ParcelNo': '',
	}

	def __init__(self):
		self.options = webdriver.ChromeOptions()
		prefs = {'profile.managed_default_content_settings.images': 2}
		self.options.add_experimental_option("prefs", prefs)
		self.driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=self.options)
		self._get_data()

	def _get_data(self):
		"""
			this function read a input file
			and get "Parcel Number" column
		"""

		self.data = pd.read_csv(self.input_file, dtype={'ParcelNo': object})
		self.data['ParcelNo'] = self.data['ParcelNo'].astype(str)

	def start(self):
		length = len(self.data.iloc[:])
		self.driver.get('https://elmorerevenuecommissioner.net/')
		time.sleep(10)
		try:
			link_to_search = WebDriverWait(self.driver, self.DELAY).until(
				EC.element_to_be_clickable((By.ID, 'PropertyTaxBttn'))
			)
		except:
			self.driver.get('https://elmorerevenuecommissioner.net/')
			time.sleep(50)
			link_to_search = WebDriverWait(self.driver, self.DELAY).until(
				EC.element_to_be_clickable((By.ID, 'PropertyTaxBttn'))
			)
		link_to_search.click()
		try:
			with open('./index_1.csv', 'r') as f:
				start = f.readlines()[0].replace('\n','')
				if start:
					start = int(start)
				else:
					start = 0
		except:
			start = 0
		
		
		for index, row in self.data.iloc[start:].iterrows(): #use iloc[i:]
			self.item = self.ITEM.copy()
			self.item['ParcelNo'] = row['ParcelNo']
			# self.item['Name1'] = row['Name1']
			# self.item['Name2'] = row['Name2']
			# self.item['Address1'] = row['Address1']
			# self.item['Address2'] = row['Address2']
			# self.item['Address3'] = row['Address3']
			# self.item['City'] = row['City']
			# self.item['State'] = row['State']
			# self.item['Zip'] = row['Zip']
			# self.item['PropAddr1'] = row['PropAddr1']
			# self.item['PropCity'] =  row['PropCity']
			# self.item['AssmtClass'] =  row['AssmtClass']
			# self.item['MunCode'] =  row['MunCode']
			# self.item['TotalLandValue'] =  row['TotalLandValue']
			# self.item['TotalImpValue'] = row['TotalImpValue']
			# self.item['TotalValue'] =  row['TotalValue']
			# self.item['TotalDue'] = row['TotalDue']


			print("============ scraping... ==========  {}/{} ======== ParcelNo {}".format(
				index+1, 
				length,
				self.item['ParcelNo'])
			)

			with open('index_1.csv', 'w') as f:
				write = csv.writer(f)
				write.writerow([index])

			self.driver.switch_to_frame(self.driver.find_element_by_id("Iframe1"))
			time.sleep(10)
			input_by_parcel = WebDriverWait(self.driver, self.DELAY).until(
				EC.presence_of_element_located((By.ID, 'SearchByParcel'))
			)
			input_by_parcel.click()

			
			text_parcel = WebDriverWait(self.driver, self.DELAY).until(
				EC.presence_of_element_located((By.ID, 'SearchText'))
			)

			text_parcel.send_keys(Keys.CONTROL + "a")
			text_parcel.send_keys(Keys.DELETE)
			text_parcel.send_keys(row['ParcelNo'])
			

			search = WebDriverWait(self.driver, self.DELAY).until(
				EC.presence_of_element_located((By.ID, 'Search'))
			)
			search.click()

			tds = self.driver.find_elements_by_xpath('//*[@id="BodyTable"]/tbody/tr/td/fieldset/table/tbody/tr/td')

			for n, td in enumerate(tds):
				if 'ADDRESS:' in td.text:
					self.item['owner address'] = tds[n+1].text
				if 'CLASS:' in td.text:
					self.item['property type'] = tds[n+1].text
					break
			
			
			try:
				link_to_detail = WebDriverWait(self.driver, self.DELAY).until(
					EC.presence_of_element_located((By.XPATH, '//*[@id="BodyTable"]/tbody/tr/td/fieldset/legend/span'))
				)
			except:
				self.driver.switch_to.default_content()
				self.write_in_csv(self.item)
				continue
			link_to_detail.click()



			#self.driver.switch_to.default_content()
			self.driver.switch_to_frame(self.driver.find_element_by_id("Iframe2"))

			tds = self.driver.find_elements_by_xpath('//*[@id="MainTable"]/tbody/tr[1]/td/fieldset/table/tbody/tr/td')
			for idx, td in enumerate(tds[:-1]):
				label = tds[idx].text
				value = tds[idx+1].text

				if 'OWNER:' in label:
					self.item['owner name'] = value
					continue
				elif 'ADDRESS:' in label:
					#self.item['owner address'] = value
					continue
				elif 'LOCATION:' in label:
					self.item['site address'] = value
					continue
				elif 'Baths' in label:
					self.item['baths'] = label.replace('Baths: ','')
					continue
				elif 'Bed Rooms' in label:
					self.item['beds'] = label.replace('Bed Rooms: ','')
					continue
				elif 'H/C Sqft' in label:
					self.item['living area'] = label.replace('H/C Sqft: ','')
					continue
				elif 'Land:' in label:
					self.item['land actual value'] = label.replace('Land:','')
				elif 'Imp:' in label:
					self.item['bldg actual value'] = label.replace('Imp:','')
				elif 'Sales Info' in value:
					try:
						sale_data = [string for string in value.split(' ') if string!='']
						self.item['sale date'] = sale_data[2]
						self.item['sale amount'] = sale_data[3].replace('$','')
					except:
						pass
					continue
					
			zip_code = re.search(r'\b(\d{5})[-d{4}]?\b', self.item['owner address'].split(' ')[-1])
			address_dict = self.get_address(zip_code)
			self.item['owner city'] = address_dict['city'].upper()
			self.item['owner state'] = address_dict['state'].upper()
			self.item['owner zip'] = address_dict['zip']
			self.item['owner address'] = self.item['owner address'].replace(self.item['owner city'], '').replace(self.item['owner state'], '').replace(self.item['owner zip'], '').replace(',','').strip()

			if not self.item['sale amount'] and self.item['sale date']:
				self.item['sale amount'] = self.item['sale date'].replace('$','')
				self.item['sale date'] = ''

			time.sleep(5)
			self.driver.switch_to.default_content()
			self.driver.switch_to_frame(self.driver.find_element_by_id('Iframe1'))
			self.driver.switch_to_frame(self.driver.find_element_by_id('Iframe1'))

			trs = self.driver.find_elements_by_xpath('//*[@id="ValueFS"]/table/tbody/tr')

			for j, tr in enumerate(trs):
				value = tr.text

				if 'BLDG' in value:
					self.item['bldg actual value'] = value.split(' ')[-1].strip().replace('$','')
					continue
				elif 'TOTAL MARKET VALUE' in value:
					self.item['total actual value'] = value.split(':')[-1].strip().replace('$','')
			
			self.driver.switch_to.default_content()
			self.driver.switch_to_frame(self.driver.find_element_by_id('Iframe1'))
			self.driver.switch_to_frame(self.driver.find_element_by_id('Iframe2'))
			buildings = WebDriverWait(self.driver, self.DELAY).until(
				EC.presence_of_element_located((By.XPATH, '//*[@id="Buildings"]'))
			)
			#print(buildings)
			buildings.click()
			#time.sleep(5)

			self.driver.switch_to.default_content()
			self.driver.switch_to_frame(self.driver.find_element_by_id('Iframe1'))
			self.driver.switch_to_frame(self.driver.find_element_by_id('Iframe1'))

			trs = 	trs = self.driver.find_elements_by_xpath('//*[@id="GeneralFS"]/table/tbody/tr')
			for j, tr in enumerate(trs):
				value = tr.text

				if 'Built' in value:
					self.item['year built'] = value.replace('Built', '')
					break
			
			self.driver.switch_to.default_content()
			self.driver.switch_to_frame(self.driver.find_element_by_id('Iframe1'))
			self.driver.switch_to_frame(self.driver.find_element_by_id('Iframe2'))
			lands = WebDriverWait(self.driver, self.DELAY).until(
				EC.presence_of_element_located((By.XPATH, '//*[@id="Land"]'))
			)
			#print(buildings)
			lands.click()
			time.sleep(5)

			self.driver.switch_to.default_content()
			self.driver.switch_to_frame(self.driver.find_element_by_id('Iframe1'))
			self.driver.switch_to_frame(self.driver.find_element_by_id('Iframe1'))

			try:
				self.item['land use code'] = self.driver.find_element_by_xpath('//*[@id="TABLE1"]/tbody/tr[2]/td[3]').text
			except:
				pass
			
			zip_code = re.search(r'\b(\d{5})[-d{4}]?\b', self.item['site address'])
			address_dict = self.get_address(zip_code)
			print(self.item['site address'])
			self.item['site city'] = address_dict['city'].upper()
			self.item['site state'] = address_dict['state'].upper()
			self.item['site zip'] = address_dict['zip']


			self.item['site address'] = self.item['site address'].replace(self.item['site city'], '').replace(self.item['site state'], '').replace(self.item['site zip'], '').replace(',','').strip()

			self.write_in_csv(self.item)		
			self.driver.back()
			self.driver.back()
			self.driver.back()
			self.driver.back()

	def write_in_csv(self, item):
		pp.pprint(item)
		with open("output.csv", 'a+', newline='') as f:  # Just use 'w' mode in 3.x
			w = csv.DictWriter(f, self.ITEM.keys())
			if self.i == 0:
				w.writeheader()
			w.writerow(item)
			self.i+=1
			#print(r.text)

	def get_address(self, zip_code):
		city = ''
		state = ''
		if zip_code:
			zip_code = zip_code.groups()[0]
			while True:
				try:
					print(zip_code, 'http://api.zippopotam.us/us/{}'.format(zip_code))
					zone = requests.get('http://api.zippopotam.us/us/{}'.format(zip_code))
					break
				except:
					pass

			if zone.status_code == 200:
				data = zone.json()
				if data:
					city = data['places'][0]['place name']
					state = data['places'][0]['state abbreviation']
		else:
			zip_code = ''
		
		if not city:
			city = ''
		if not state:
			state = ''

		return {
			'zip': zip_code,
			'city': city,
			'state': state
		}


if __name__ == '__main__':
	scraper = ShelbyAlScraper()
	scraper.start()
