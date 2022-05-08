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

count = 0
ul = "https://www.franklincountytax.us/search/CommonSearch.aspx?mode=OWNER"
path = which("chromedriver")
options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--headless")
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
    writer.writerow(["Parcel ID","Owner","Site Address","Site City","Site Zip","Mail Address","Mail City","Mail State","Mail Zip Code","Property Type","Sale Date","Sale Price","Year Built","Living Area(SQFT)","Beds","Full Bathrooms","Half Bathrooms","Land Value","BLDG Value","total_accessed_value"])

with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        search = driver.find_element_by_xpath("//input[@id='inpOwner']")
        time.sleep(3)
        search.clear()
        search.send_keys(company)
        search.send_keys(Keys.ENTER)
        time.sleep(5)
        try:

            btn = driver.find_element_by_xpath("(//tr[@class='SearchResults']/td)[1]")
            btn.click()
            time.sleep(4)

            try:

                html = driver.page_source
                resp = Selector(text=html)

                parcel_id = resp.xpath("(//tr[@class='DataletHeaderTop'])[1]/td[contains(text(),'PARCEL ID:')]/text()").extract_first()
                if parcel_id:
                    parcel_id = str(parcel_id)
                    parcel_id = parcel_id.replace("PARCEL ID:", '')
                    parcel_id = parcel_id.lstrip()

                site_address = resp.xpath("//td[contains(text(),'Physical Address')]/following-sibling::td/text()").extract_first()
                site_city = resp.xpath("(//td[contains(text(),'City')]/following-sibling::td/text())[1]").extract_first()
                site_zip = resp.xpath("(//td[contains(text(),'Zip')]/following-sibling::td/text())[1]").extract_first()
                if site_zip:
                    site_zip = str(site_zip)
                    site_zip = site_zip.replace('-', '')

                property_type = resp.xpath("(//td[contains(text(),'Land Use Code')]/following-sibling::td/text())[1]").extract_first()
                owner = resp.xpath("(//td[contains(text(),'Owner 1')]/following-sibling::td/text())[1]").extract_first()
                mail_address = resp.xpath("(//td[contains(text(),'Mailing Address')]/following-sibling::td/text())[1]").extract_first()
                st_mail_add = resp.xpath("(//td[contains(text(),'City/State/Zip')]/following-sibling::td/text())[1]").extract_first()
                if st_mail_add:
                    st_mail_add = str(st_mail_add)
                    mail_city = re.findall(r"^[A-Z]*", st_mail_add)
                    mail_state = re.findall(r"\/.*\/", st_mail_add)
                    mail_zip = re.findall(r"\d\d\d\d\d", st_mail_add)
                else:
                    mail_city = None
                    mail_state = None
                    mail_zip = None  
                
            except:
                parcel_id = None
                site_address = None
                site_city = None
                site_zip = None
                property_type = None
                owner = None
                mail_address = None
                mail_city = None
                mail_state = None
                mail_zip = None
            try:
                sales_btn = driver.find_element_by_xpath("//span[contains(text(),'Sales')]//parent::a")
                sales_btn.click()
                time.sleep(3)

                html = driver.page_source
                resp = Selector(text=html)

                sale_date = resp.xpath("(//td[contains(text(),'Sale Date')]/following-sibling::td/text())[1]").extract_first()
                sale_price = resp.xpath("(//td[contains(text(),'Sale Price')]/following-sibling::td/text())[1]").extract_first()
           
            except:
                sale_date = None
                sale_price = None
            

            try:
                Residential = driver.find_element_by_xpath("//span[contains(text(),'Residential')]//parent::a")
                Residential.click()
                time.sleep(3)

                html = driver.page_source
                resp = Selector(text=html)

                year_built = resp.xpath("(//td[contains(text(),'Year Built')]/following-sibling::td/text())[1]").extract_first()
                beds = resp.xpath("(//td[contains(text(),'Bedrooms')]/following-sibling::td/text())[1]").extract_first()
                Living_Area = resp.xpath("(//td[contains(text(),'Living Area')]/following-sibling::td/text())[1]").extract_first()
                full_bathrooms = resp.xpath("(//td[contains(text(),'Full Baths')]/following-sibling::td/text())[1]").extract_first()
                half_bathrooms = resp.xpath("(//td[contains(text(),'Half Baths')]/following-sibling::td/text())[1]").extract_first()
         
            except:
                year_built = None
                beds = None
                Living_Area = None
                full_bathrooms = None
                half_bathrooms = None
           

            try:
                Values = driver.find_element_by_xpath("//span[contains(text(),'Values')]//parent::a")
                Values.click()
                time.sleep(3)

                html = driver.page_source
                resp = Selector(text=html)

                land_value = resp.xpath("(//td[contains(text(),'Land Value')]/following-sibling::td/text())[1]").extract_first()
                bldg_value = resp.xpath("(//td[contains(text(),'Building Value')]/following-sibling::td/text())[1]").extract_first()
                total_accessed_value = resp.xpath("(//td[contains(text(),'Total Value')]/following-sibling::td/text())[1]").extract_first()
            
            except:
                land_value = None
                bldg_value = None
                total_accessed_value = None

            with open('test.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([parcel_id,owner,site_address,site_city,site_zip,mail_address,mail_city,mail_state,mail_zip,property_type,sale_date,sale_price,year_built,Living_Area,beds,full_bathrooms,half_bathrooms,land_value,bldg_value,total_accessed_value])
                count = count + 1
                print("Data Saved in CSV", count)

            driver.get(ul)
            time.sleep(3)              
        except:
            print("Search Result is empty")
            driver.get(ul)
            time.sleep(3) 
        