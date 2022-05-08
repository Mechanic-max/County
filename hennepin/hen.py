from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from shutil import which
from fake_useragent import UserAgent
import time
from scrapy.selector import Selector
from selenium.webdriver.common.action_chains import ActionChains
import csv
from selenium.webdriver.support.ui import Select
import re

ul = "https://gis.hennepin.us/property/map/default.aspx?"
path = which("chromedriver")
options = Options()
options.add_experimental_option("detach", True)
#options.add_argument("--headless")
ua = UserAgent()
userAgent = ua.random
options.add_argument(f'user-agent={userAgent}')
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(executable_path=path,options=options)
driver.get(ul)
time.sleep(4)
count = 0
with open('sample.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Owners","Site Address", "Site City","Site State","Site Zip Code","Mail Address", "Mail city","Mail State","Zip Code","Previous Year Market Value","Current Year Market Value","Property Type","Year Built","Sale Price","Sale Date"])



with open('input1.txt','r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if len(line) == 12:
            line = f"0{line}"
        search = driver.find_element_by_xpath("//input[@id='search-input']")
        time.sleep(1)
        search.clear()
        search.send_keys(line)
        search.send_keys(Keys.ENTER)
        time.sleep(3)
        try:
            html = driver.page_source
            resp = Selector(text=html)
            site_address = resp.xpath("(//div[@class='resultSubTitle']/text())[1]").extract_first()
            city_state_zip = resp.xpath("(//div[@class='resultSubTitle']/text())[2]").extract_first()
            try:
                city_state_zip = str(city_state_zip)
                site_city = re.findall(r"^[^,]*",city_state_zip)
                site_state = re.findall(r"\s\w\w\s",city_state_zip)
                site_zip_code = re.findall(r"\d.*$",city_state_zip)
            except:
                site_city = None
                site_state = None
                site_zip_code = None
            
            owners = resp.xpath("//td[@id='owner']/text()").extract_first()
            owners_address = resp.xpath("(//td[@id='taxpayer']/text())[last()-1]").extract_first()
            owners_city_state_zip = resp.xpath("(//td[@id='taxpayer']/text())[last()]").extract_first()
            try:
                owners_city_state_zip = str(owners_city_state_zip)
                mail_city = re.findall(r"^[A-Z].*\s",owners_city_state_zip)
                mail_state = re.findall(r"\s\w\w\s",owners_city_state_zip)
                mail_zip_code = re.findall(r"\d.*$",owners_city_state_zip)
            except:
                mail_city = None
                mail_state = None
                mail_zip_code = None

            previous_year_market_value = resp.xpath("(//td[@id='marketvalue']/text())[last()-1]").extract_first()
            Property_Type = resp.xpath("(//td[@id='propertytype']/text())[1]").extract_first()
            year_built = resp.xpath("(//td[@id='buildyear']/text())[1]").extract_first()
            current_year_market_value = resp.xpath("(//td[@id='marketvalue']/text())[last()]").extract_first()
            sale_price = resp.xpath("(//td[@id='saleprice'])[1]/text()").extract_first()
            sale_date = resp.xpath("(//td[@id='saledate'])[1]/text()").extract_first()
            with open('sample.csv', 'a',newline='') as file:
                writer = csv.writer(file)
                writer.writerow([owners,site_address,site_city,site_state,site_zip_code,owners_address,mail_city,mail_state,mail_zip_code,previous_year_market_value,current_year_market_value,Property_Type,year_built,sale_price,sale_date])
                count = count + 1
                print("Data Saved in CSV :",count)
            driver.get(ul)
            time.sleep(3)         
        except:
            print("Search Result is empty")
            driver.get(ul)
            time.sleep(3) 
        