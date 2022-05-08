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
import re

count = 0
ul = "https://realestate.starkcountyohio.gov/search/commonsearch.aspx?mode=realprop"
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
time.sleep(2)

with open('test.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Owner","Site Address","Site City","Site State","Site Zip Code","Mail Address","Mail City","Mail State","Mail Zip Code","Property Type","Land Value","BLDG Value","Total Accessed Value","Sale Date","Sale Amount","Living Area","Year Built","Bedrooms","Full Baths","Half Baths"])


try:
    driver.find_element_by_xpath("//button[@id='btAgree']").click()
    time.sleep(2)
except:
    print("Pop up didn't appear")

with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        search = driver.find_element_by_xpath("//input[@id='inpParid']")
        time.sleep(1)
        search.clear()
        search.send_keys(company)
        search.send_keys(Keys.ENTER)
        time.sleep(3)
        try:
            html = driver.page_source
            resp = Selector(text=html)
            
            owner = resp.xpath("(//td[@class='DataletHeaderBottom'])[1]/text()").extract_first()
            site_address = resp.xpath("(//td[contains(text(),'Address')]/following-sibling::td)[1]/text()").extract_first()
            site_city_state_zip = resp.xpath("(//td[contains(text(),'City, State, Zip')]/following-sibling::td)[1]/text()").extract_first()
            try:
                site_city_state_zip = str(site_city_state_zip)
                site_city = re.findall(r"^[^\s]+",site_city_state_zip)
                site_state = re.findall(r"\s\w\w\s",site_city_state_zip)
                site_zip = re.findall(r"\s\d.*",site_city_state_zip)
            except:
                site_city = None
                site_state = None
                site_zip = None

            property_type = resp.xpath("(//td[contains(text(),'Land Use Code')]/following-sibling::td)[1]/text()").extract_first()
            
            mail_address = resp.xpath("(//td[contains(text(),'Address 1')]/following-sibling::td)[1]/text()").extract_first()
            mail_city_state_zip = resp.xpath("(//td[contains(text(),'Address 3')]/following-sibling::td)[1]/text()").extract_first()
            try:
                mail_city_state_zip = str(mail_city_state_zip)
                mail_city = re.findall(r"^[^\s]+",mail_city_state_zip)
                mail_state = re.findall(r"\s\w\w\s",mail_city_state_zip)
                mail_zip = re.findall(r"\s\d.*",mail_city_state_zip)
            except:
                mail_city = None
                mail_state = None
                mail_zip = None
            try:
                driver.find_element_by_xpath("//span[contains(text(),'Values History')]//parent::a").click()
                time.sleep(2)
                
                html = driver.page_source
                resp = Selector(text=html)

                land_value = resp.xpath("((//tr)[11]/td)[2]/text()").extract_first()
                bldg_value = resp.xpath("((//tr)[11]/td)[3]/text()").extract_first()
                total_accessed_value = resp.xpath("((//tr)[11]/td)[4]/text()").extract_first()

            except:
                land_value = None
                bldg_value = None
                total_accessed_value = None
            
            try:
                driver.find_element_by_xpath("//span[contains(text(),'Sales')]//parent::a").click()
                time.sleep(2)
                
                html = driver.page_source
                resp = Selector(text=html)

                sale_date = resp.xpath("(//td[contains(text(),'Sale Date')]/following-sibling::td)[1]/text()").extract_first()
                sale_value = resp.xpath("(//td[contains(text(),'Sale Price')]/following-sibling::td)[1]/text()").extract_first()
                
            except:
                sale_date = None
                sale_value = None
            
            try:
                driver.find_element_by_xpath("//span[contains(text(),'Residential')]//parent::a").click()
                time.sleep(2)
                
                html = driver.page_source
                resp = Selector(text=html)

                living_area = resp.xpath("(//td[contains(text(),'Square Feet')]/following-sibling::td)[1]/text()").extract_first()
                year_built = resp.xpath("(//td[contains(text(),'Year Built')]/following-sibling::td)[1]/text()").extract_first()
                Bedrooms = resp.xpath("(//td[contains(text(),'Bedrooms')]/following-sibling::td)[1]/text()").extract_first()
                full_bath = resp.xpath("(//td[contains(text(),'Full Baths')]/following-sibling::td)[1]/text()").extract_first()
                half_bath = resp.xpath("(//td[contains(text(),'Half Baths')]/following-sibling::td)[1]/text()").extract_first()
                
            except:
                living_area = None
                year_built = None
                Bedrooms = None
                full_bath = None
                half_bath = None
            
            with open('test.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([owner,site_address,site_city,site_state,site_zip,mail_address,mail_city,mail_state,mail_zip,property_type,land_value,bldg_value,total_accessed_value,sale_date,sale_value,living_area,year_built,Bedrooms,full_bath,half_bath])
                count = count + 1
                print("Data Saved in CSV:",count)
        
        
        except:
            print("Search Result is empty")
            
        driver.get(ul)
        time.sleep(2)