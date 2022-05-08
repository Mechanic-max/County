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
ul = "https://yorkcountypa.maps.arcgis.com/apps/webappviewer/index.html?id=5774257ab4fb4aee9cf318e7313049ee"
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
time.sleep(100)

with open('test.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Parcel ID","Site Address","Owner Name","Property Type","Living Area","Land Value","BLDG Value","Total Accessed Value","Sale Date","Sale Amount"])
try:
    driver.find_element_by_xpath("//div[@class='checkbox jimu-float-leading jimu-icon jimu-icon-checkbox']").click()
    time.sleep(2)
    driver.find_element_by_xpath("//button[contains(text(),'OK')]").click()
    time.sleep(2)
except:
    print("Pop up didn't appear")

with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        search = driver.find_element_by_xpath("//input[@class='searchInput']")
        time.sleep(3)
        search.clear()
        search.send_keys(company)
        search.send_keys(Keys.ENTER)
        time.sleep(4)
        try:
            try:
                parcel_id = driver.find_element_by_xpath("//td[contains(text(),'PARCEL ID NUMBER')]/following-sibling::td").text
            except:
                parcel_id = None
            
            try:
                site_address = driver.find_element_by_xpath("//td[contains(text(),'PROPERTY ADDRESS')]/following-sibling::td").text
            except:
                site_address = None
            
            try:
                owner_name = driver.find_element_by_xpath("//td[contains(text(),'OWNER INFORMATION')]/following-sibling::td").text
            except:
                owner_name = None
            
            try:
                property_type = driver.find_element_by_xpath("//td[contains(text(),'LAND USE CODE')]/following-sibling::td").text
            except:
                property_type = None

            try:
                living_area = driver.find_element_by_xpath("//td[contains(text(),'ACRES')]/following-sibling::td/span").text
            except:
                living_area = None

            try:
                land_value = driver.find_element_by_xpath("//td[contains(text(),'ASSESSED LAND VALUE ($)')]/following-sibling::td/span").text
            except:
                land_value = None
            
            try:
                bldg_value = driver.find_element_by_xpath("//td[contains(text(),'ASSESSED BUILDING VALUE ($)')]/following-sibling::td/span").text
            except:
                bldg_value = None
            
            try:
                total_accessed_value = driver.find_element_by_xpath("//td[contains(text(),'TOTAL ASSESSED VALUE ($)')]/following-sibling::td/span").text
            except:
                total_accessed_value = None
            
            try:
                sale_date = driver.find_element_by_xpath("//td[contains(text(),'SALE DATE')]/following-sibling::td").text
            except:
                sale_date = None
            
            try:
                sale_amount = driver.find_element_by_xpath("//td[contains(text(),'SALE PRICE ($)')]/following-sibling::td/span").text
            except:
                sale_amount = None

        
            with open('test.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([parcel_id,site_address,owner_name,property_type,living_area,land_value,bldg_value,total_accessed_value,sale_date,sale_amount])
                count = count + 1
                print("Data Saved in CSV",count)
                        
        except:
            print("Search Result is empty")
            time.sleep(3)