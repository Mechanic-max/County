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
ul = "http://vance.ustaxdata.com/"
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
    writer.writerow(["Parcel ID","Owner 1","Owner 2","Site Address","Site State","Site City","Site Zip","Mail Address","Mail State","Mail City","Mail Zip Code","Property Type","Sale Date","Sale Price","Year Built","Living Area(SQFT)","Beds","Bathrooms","Land Value","BLDG Value"])

with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        search = driver.find_element_by_xpath("//input[@id='StreetName']")
        time.sleep(1)
        search.clear()
        search.send_keys(company)
        search.send_keys(Keys.ENTER)
        time.sleep(3)
        try:
            driver.find_element_by_xpath("(//a[@class='style16'])[1]").click()
            time.sleep(2)
            html = driver.page_source
            resp = Selector(text=html)

            owners_1 = resp.xpath("((//table[@width='100%' and @border='1'])[1]//table[@bgcolor='a9a9a9']/tbody/tr)[1]/td/b//text()").get()
            owners_2 = resp.xpath("((//table[@width='100%' and @border='1'])[1]//table[@bgcolor='a9a9a9']/tbody/tr)[2]/td/b//text()").get()

            mailing_address = resp.xpath("((//table[@width='100%' and @border='1'])[1]//table[@bgcolor='a9a9a9']/tbody/tr)[3]/td/b//text()").get()
            mailing_city_state_zip_code = resp.xpath("((//table[@width='100%' and @border='1'])[1]//table[@bgcolor='a9a9a9']/tbody/tr)[4]/td/b//text()").extract_first()
            try:
                
                mailing_city_state_zip_code = str(mailing_city_state_zip_code)
                mailing_city = re.findall(r"^[^,]+",mailing_city_state_zip_code)
                mailing_state = re.findall(r"\s\w\w\s",mailing_city_state_zip_code)
                mailing_zip_code = re.findall(r"\d.*$",mailing_city_state_zip_code)
            except:
                mailing_city = None
                mailing_state = None
                mailing_zip_code = None

            site_address = resp.xpath("((//table[@width='100%' and @border='1'])[1]//table[@bgcolor='a9a9a9']/tbody/tr)[5]/td/b//text()").get()
            site_city_state_zip = resp.xpath("((//table[@width='100%' and @border='1'])[1]//table[@bgcolor='a9a9a9']/tbody/tr)[6]/td/b//text()").get()
            try:
                    site_city_state_zip = str(site_city_state_zip)
                    site_city = re.findall(r"^[^,]+",site_city_state_zip)
                    site_state = re.findall(r"\s\w\w\s",site_city_state_zip)
                    site_zip_code = re.findall(r"\d.*$",site_city_state_zip)
            except:
                site_city = None
                site_state = None
                site_zip_code = None

            sale_date = resp.xpath("((((//table[@width='100%' and @border='1'])[3]//table)[2]//tr)[3]/td)[2]/div/text()").get()
            sale_price = resp.xpath("((((//table[@width='100%' and @border='1'])[3]//table)[2]//tr)[3]/td)[6]/div[@class='a1']/div/text()").get()
            try:
                driver.find_element_by_xpath("//font[contains(text(),'Buildings')]//parent::a").click()
                time.sleep(2)
                html = driver.page_source
                resp = Selector(text=html)

                year_built = resp.xpath("//font[contains(text(),'Year Built')]//parent::td/following-sibling::td/b/font/text()").get()
                property_type = resp.xpath("//font[contains(text(),'Built Use/Style')]//parent::td/following-sibling::td/b/font/text()").get()
                bathrooms = resp.xpath("normalize-space(//font[contains(text(),' Bathroom(s) ')]//parent::td/following-sibling::td/font/strong/text())").get()
                bedrooms = resp.xpath("normalize-space(//font[contains(text(),' Bedroom(s) ')]//parent::td/following-sibling::td//strong/font/text())").get()
                living_area = resp.xpath("(//tr[@class='a1']/td[@bgcolor='DFEBF9'])[3]/text()").get()
                bldg_value = resp.xpath("((//font[contains(text(),'Total Improvement')]//parent::div//parent::td//parent::tr/following-sibling::tr)[1]/td/div/font/strong)[1]/text()").get()

            except:
                year_built = None
                property_type = None
                bathrooms = None
                bedrooms = None
                living_area = None
                bldg_value = None
            try:
                driver.find_element_by_xpath("//font[contains(text(),'Land')]//parent::a").click()
                time.sleep(2)
                html = driver.page_source
                resp = Selector(text=html)
                land_value = resp.xpath("(((//div[contains(text(),'Land')])[3]//parent::td/parent::tr/following-sibling::tr)[1]/td)[3]/div/font/strong/text()").get()
            except:
                land_value = None
            
        
            with open('test.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([company,owners_1,owners_2,site_address,site_state,site_city,site_zip_code,mailing_address,mailing_state,mailing_city,mailing_zip_code,property_type,sale_date,sale_price,year_built,living_area,bedrooms,bathrooms,land_value,bldg_value])
                count = count + 1
                print("Data Saved in CSV",count)
            driver.get(ul)
            time.sleep(3)
                        
        except:
            print("Search Result is empty")
            driver.get(ul)
            time.sleep(3) 
        