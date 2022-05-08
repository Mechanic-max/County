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
with open('CRAIGHEAD.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Parcel ID","owner_name","site_address","city","state","zip","mail_address","m_city","m_state","m_zip","sale_date","sale_price","land_value","bldg_value","total_accessed_value","living_area","property_type","built_year","baths"])

ul = "https://www.arcountydata.com/results.asp"

path = which("chromedriver")
options = Options()
options.add_experimental_option("detach", True)
#options.add_argument("--headless")
ua = UserAgent()
userAgent = ua.random
userAgent = ua.random
options.add_argument(f'user-agent={userAgent}')
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(executable_path=path,options=options)
driver.get(ul)
time.sleep(30)
driver.find_element_by_xpath("//span[@style='white-space: nowrap;']/a[contains(text(),'Craighead')]").click()
time.sleep(5)

with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        search = driver.find_element_by_xpath("//input[@id='ParcelNumber']")
        search.clear()
        search.send_keys(company)
        search.send_keys(Keys.ENTER)
        time.sleep(3)
        try:
            driver.find_element_by_xpath("//th[contains(text(),'Owner')]/parent::tr/following-sibling::tr/td/a").click()
            time.sleep(3)   
            html = driver.page_source
            resp = Selector(text=html)

            owner_name = resp.xpath("//td[contains(text(),'Property Address:')]/following-sibling::td/text()[1]").extract_first()
            site_address = resp.xpath("normalize-space(//td[contains(text(),'Property Address:')]/following-sibling::td/text()[2])").extract_first()
            city_state_zip = resp.xpath("normalize-space(//td[contains(text(),'Property Address:')]/following-sibling::td/text()[3])").extract_first()
            try:
                city_state_zip = str(city_state_zip)
                city = re.findall(r"^[^,]+",city_state_zip)
                state = re.findall(r"\s\w\w\s",city_state_zip)
                zip = re.findall(r"\d\d\d\d\d",city_state_zip)
            except :
                city = None
                state = None
                zip = None
            
            mail_address = resp.xpath("normalize-space(//td[contains(text(),'Mailing Address:')]/following-sibling::td/text()[2])").extract_first()
            m_city_state_zip = resp.xpath("normalize-space(//td[contains(text(),'Mailing Address:')]/following-sibling::td/text()[3])").extract_first()
            try:
                m_city_state_zip = str(m_city_state_zip)
                m_city = re.findall(r"^[^\s]+",m_city_state_zip)
                m_state = re.findall(r"\s\w\w\s",m_city_state_zip)
                m_zip = re.findall(r"\d\d\d\d\d",m_city_state_zip)
            except :
                m_city = None
                m_state = None
                m_zip = None

            try:
                sales_btn = driver.find_element_by_xpath("//a[contains(text(),'Sales')]")
                sales_btn.click()
                time.sleep(3)

                html = driver.page_source
                resp = Selector(text=html)

                sale_date = resp.xpath("(((//table[@class='table table-striped-yellow table-bordered table-condensed'])[3]//tr)[2]/td)[2]/text()").extract_first()
                sale_price = resp.xpath("(((//table[@class='table table-striped-yellow table-bordered table-condensed'])[3]//tr)[2]/td)[3]/text()").extract_first()          
            except:
                sale_date = None
                sale_price = None          

            try:
                Valuation = driver.find_element_by_xpath("//a[contains(text(),'Valuation')]")
                Valuation.click()
                time.sleep(3)

                html = driver.page_source
                resp = Selector(text=html)

                land_value = resp.xpath("(//td[contains(text(),'Land: ')]/following-sibling::td)[1]/text()").extract_first()
                bldg_value = resp.xpath("(//td[contains(text(),'Improvements: ')]/following-sibling::td)[1]/text()").extract_first()
                total_accessed_value = resp.xpath("(//td[contains(text(),'Total Value: ')]/following-sibling::td)[1]/text()").extract_first()
                
            except:
                land_value = None
                bldg_value = None
                total_accessed_value = None

            try:
                Improvements = driver.find_element_by_xpath("//a[contains(text(),'Improvements')]")
                Improvements.click()
                time.sleep(3)

                html = driver.page_source
                resp = Selector(text=html)

                living_area = resp.xpath("(//td/strong[contains(text(),'Living Area Total SF')]/parent::td/following-sibling::td/strong/text())[1]").extract_first()
                property_type = resp.xpath("//td[contains(text(),'Occupancy Type:')]/following-sibling::td/text()").extract_first()
                built_year = resp.xpath("(//td[contains(text(),'Year Built:')]/following-sibling::td)/text()").extract_first()
                baths = resp.xpath("(//td[contains(text(),'Bathrooms')]/following-sibling::td)/text()").extract_first()
            except:
                living_area = None
                property_type = None
                built_year = None
                baths = None
                beds = None
            with open('CRAIGHEAD.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([company,owner_name,site_address,city,state,zip,mail_address,m_city,m_state,m_zip,sale_date,sale_price,land_value,bldg_value,total_accessed_value,living_area,property_type,built_year,baths])
                count = count + 1
                print("Data Saved in CSV: ",count)
        except:
            print("Search results")    
        driver.get("https://www.arcountydata.com/sponsored.asp?Benton")
        time.sleep(3) 