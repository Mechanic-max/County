from types import prepare_class
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
ul = "http://asp.rutherfordcountytn.gov/apps/propertydata/RealPropertySearch2.aspx"
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
    writer.writerow(["Account No","parcel_id","owner1","owner2","mailing_address1","mailing_address2","site_address","mail_city","mail_state","mail_zip","property_class_type","land_value","bldg_value","total_acccessed_value","sale_date","sale_price","year_built","living_area"])

with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        search = driver.find_element_by_xpath("//input[@id='MainContent_TextBox5']")
        time.sleep(1)
        search.clear()
        search.send_keys(company)
        search.send_keys(Keys.ENTER)
        time.sleep(2)
        
        try:
            driver.find_element_by_xpath("//td/a[contains(text(),'View')]").click()
            time.sleep(3)
            html = driver.page_source
            resp = Selector(text=html)
            
            owner1 = resp.xpath("//span[@id='TabContainer1_TabPanel1_lblownername']/text()").extract_first()
            owner2 = resp.xpath("//span[@id='TabContainer1_TabPanel1_lblownername2']/text()").extract_first()
            mailing_address1 = resp.xpath("//span[@id='TabContainer1_TabPanel1_lblowneraddr']/text()").extract_first()
            mailing_address2 = resp.xpath("//span[@id='TabContainer1_TabPanel1_lblowneraddr2']/text()").extract_first()

            site_city_state_zip = resp.xpath("//span[@id='TabContainer1_TabPanel1_lblcity']/text()").extract_first()
            try:
                site_city_state_zip = str(site_city_state_zip)
                site_city = re.findall(r"^[^,]+",site_city_state_zip)
                site_state = re.findall(r"\s\S\S\s",site_city_state_zip)
                site_zip = re.findall(r"\d.*",site_city_state_zip)
            except:
                site_city = None
                site_state = None
                site_zip = None
            
            site_address = resp.xpath("//span[@id='TabContainer1_TabPanel1_lblpropaddr']/text()").extract_first()
            
            parcel_id = resp.xpath("normalize-space(//span[@id='TabContainer1_TabPanel1_lblparcel']/text())").extract_first()

            property_class_type = resp.xpath("//span[@id='TabContainer1_TabPanel1_lblclass']/text()").extract_first()    
            
            land_value = resp.xpath("//span[@id='TabContainer1_TabPanel1_lbllandval']/text()").extract_first()
            bldg_value = resp.xpath("//span[@id='TabContainer1_TabPanel1_lblimpval']/text()").extract_first()
            total_acccessed_value = resp.xpath("//span[@id='TabContainer1_TabPanel1_lbltotval']/text()").extract_first()
            
            living_area = resp.xpath("//th[contains(text(),'SQFT')]/parent::tr/following-sibling::tr/td[last()]/text()").extract_first()

            sale_date = resp.xpath("(//th[contains(text(),'SaleDate')])[1]/parent::tr/following-sibling::tr/td[1]/text()").extract_first()
            sale_price = resp.xpath("(//th[contains(text(),'SaleDate')])[1]/parent::tr/following-sibling::tr/td[2]/text()").extract_first()
            year_built = resp.xpath("(//th[contains(text(),'YearBuilt')])[1]/parent::tr/following-sibling::tr/td[6]/text()").extract_first()

            with open('test.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([company,parcel_id,owner1,owner2,mailing_address1,mailing_address2,site_address,site_city,site_state,site_zip,property_class_type,land_value,bldg_value,total_acccessed_value,sale_date,sale_price,year_built,living_area])
                count = count + 1
                print("Data Saved in CSV:",count)
                        
        except:
            print("Search Result is empty")
        driver.get(ul)
        time.sleep(3) 
    
driver.close()