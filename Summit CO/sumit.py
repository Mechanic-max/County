import re
import csv
import time
import requests
from itertools import cycle
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from base import BaseScraper
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from shutil import which
from fake_useragent import UserAgent
import time
from scrapy.selector import Selector
from selenium.webdriver.common.action_chains import ActionChains

proxies = [
	'69.30.240.226:15002',
	'69.30.197.122:15002',
	'173.208.239.10:15002',
	'173.208.136.2:15002',
	'195.154.255.118:15002',
	'195.154.222.228:15002',
	'195.154.255.34:15002',
	'195.154.222.26:15002',
	'63.141.241.98:16001',
	'173.208.209.42:16001',
	'163.172.36.211:16001',
	'163.172.61.67:16001',
]

proxy_pool = cycle(proxies)

class RichmondUt(BaseScraper):
	name = 'richmond_ut_cache_00002'
	inputs_cols = [
		'Key Field',
		'STATUS',
		'Case Type',
		'CLOSED',
		'ASSIGNED_TO',
		'PREFIX',
		'Case Sub Type',
		'Address',
		'city',
		'state',
		'zip',
		'MAIN_TABLE_TYPE',
		'MAIN_TABLE_SUBTYPE',
		'MAIN_TABLE_STATUS',
		'COORD_X',
		'COORD_Y',
		'LAT',
		'LON',
		'GIS_SITE_GEO_TYPE',
		'GIS_SITE_ALTERNATE_ID',
	]

	base_url = 'https://www.countyoffice.org/ca-alameda-county-property-records/'
	detail_url = 'https://www.countyoffice.org/property-records-search/?q={}'

	def start(self):
		self.driver = webdriver.Chrome(executable_path='./chromedriver.exe')
		self.driver.get(self.base_url)

		try:
			with open(f'index.csv', 'r') as f:
				start = f.readlines()[0].replace('\n','')
				if start:
					start = int(start)
				else:
					start = 0
		except:
			start = 0
		proxy = next(proxy_pool)
		for index, row in self.data.iloc[start:,:].iterrows():
			time.sleep(5)
			item = self.ITEM.copy()
			for key, value in row.items():
				item[key] = value
			
			extra = ''
			item['Address'] = str(item['Address'])
			extra = re.findall(r"\s\(.*?\)",item['Address'])
			extra = str(extra)
			extra = extra.replace("'","")
			extra = extra.replace("[","")
			extra = extra.replace("]","")
			extra = extra.strip()
			item['Address'] = item['Address'].replace(extra,'')
			item['Address'] = item['Address'].strip()
			ade = f"{item['Address']}, Breckenridge"
			item['Address'] = ade
			print(item['Address'])
			print('Scraping =================== {}/{} ========= address {}'.format(
				index,
				len(self.data),
				item['Address'].upper()
			))

			input_address = self.driver.find_element_by_id('addressauto')
			input_address.clear()
			input_address.send_keys(item['Address'])
			time.sleep(1.5)

			try:
				result = self.driver.find_element_by_xpath('//div[@class="pac-item"]')
				address_match = BeautifulSoup(result.get_attribute('innerHTML'), 'html.parser').find_all(text=True)
				address_match = ''.join(address_match).replace(', Breckenridge',', Breckenridge, CO')
			except:
				print('No results found')
				self.write_in_csv(item)
				with open(f'index.csv', 'w') as f:
					write = csv.writer(f)
					write.writerow([index])	
				continue
			
			while True:
				try:
					
					url = self.detail_url.format(address_match.replace(' ','+').replace(',','%2C')).replace('Breckenridge','%2C+Breckenridge')
					print(url)
					response = requests.get(url, proxies={"http": proxy, "https": proxy})
					print(response.status_code)
					if "You've hit the daily limit of 5 searches, " in response.text:
						proxy = next(proxy_pool)
					else:
						break
						
					
				except Exception as e:
					print(e)
			#we need to use proxy
			
			soup = BeautifulSoup(response.text, 'html.parser')
			resp = Selector(text=response.content)
			site_address_label = soup.find('th', text='Address')
			if site_address_label:
				site_address = site_address_label.find_next_sibling('td').find_all(text=True)
				item['site address'] = site_address[0]
				item['site state'] = ' '.join(site_address[1].split(' ')[:-2])
				item['site city'] = site_address[1].split(' ')[-2]
				item['site zip'] = site_address[1].split(' ')[-1]
				print(site_address)

			owner_name_label = soup.find('dt', text='Name')
			if owner_name_label:
				owner_name = owner_name_label.find_next_sibling('dd').text
				item['owner name'] = owner_name
			
			owner_address_label = soup.find('dt', text='Address')
			if owner_address_label:
				owner_address = owner_address_label.find_next_sibling('dd').find_all(text=True)
				item['owner address'] = owner_address[0]
				try:
					item['owner state'] = ' '.join(owner_address[1].split(' ')[:-2])
					item['owner city'] = owner_address[1].split(' ')[-2]
					item['owner zip'] = owner_address[1].split(' ')[-1]
					print(owner_address)
				except:
					pass
			
			
			
			
			item['total value'] = resp.xpath("//th[contains(text(),'Land Value')]/ancestor::thead/following-sibling::tbody/tr[1]/td[4]/text()").extract_first()
			item['land value'] = resp.xpath("//th[contains(text(),'Land Value')]/ancestor::thead/following-sibling::tbody/tr[1]/td[2]/text()").extract_first()
			item['bldg value'] = resp.xpath("//th[contains(text(),'Land Value')]/ancestor::thead/following-sibling::tbody/tr[1]/td[3]/text()").extract_first()

			
			item['geographic id'] = resp.xpath("normalize-space(//th[contains(text(),'Census Tract')]/following-sibling::td/text()[1])").extract_first()
			item['property use code'] = resp.xpath("normalize-space(//th[contains(text(),'Land Use Code')]/following-sibling::td/text())").extract_first()
			item['property use code'] = str(item['property use code'])
			item['property use code'] = item['property use code'].replace('(','')
			item['property use code'] = item['property use code'].strip()
			item['property class'] = resp.xpath("normalize-space(//th[contains(text(),'Land Use Category')]/following-sibling::td/text())").extract_first()
			item['sale date'] = resp.xpath("normalize-space((//dt[contains(text(),'Details')])[1]/following-sibling::dd/b[contains(text(),'Recording Date')]/following::text()[1])").extract_first()
			item['sale price'] = resp.xpath("normalize-space((//dt[contains(text(),'Details')])[1]/following-sibling::dd/b[contains(text(),'Sale Price')]/following::text()[1])").extract_first()
			item['land_area'] = resp.xpath("normalize-space(//th[contains(text(),'Area')]/following-sibling::td/text())").extract_first()
			item['living area'] = resp.xpath("normalize-space(//th[contains(text(),'Total Area')]/following-sibling::td[1]/text())").extract_first()
			item['baths'] = resp.xpath("normalize-space(//th[contains(text(),'Bathrooms')]/following-sibling::td[1]/text())").extract_first()
			item['year built'] = resp.xpath("normalize-space(//th[contains(text(),'Year')]/following-sibling::td[1]/text())").extract_first()
			item['beds'] = resp.xpath("//th[contains(text(),'Bedrooms')]/following-sibling::td[1]/text()").extract_first()
			item['property type'] = resp.xpath("//th[contains(text(),'Land Use Category')]/following-sibling::td//text()").extract_first()
			item['property type'] = str(item['property type'])
			item['property type'] = item['property type'].replace('(','')
			item['property type'] = item['property type'].strip()
	

			self.write_in_csv(item)
			with open(f'index.csv', 'w') as f:
				write = csv.writer(f)
				write.writerow([index])	

if __name__ == '__main__':
   scraper = RichmondUt()
   scraper.start()