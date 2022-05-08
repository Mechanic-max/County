from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from shutil import which
import time
from scrapy.selector import Selector
from selenium.webdriver.common.action_chains import ActionChains
import csv
import pandas as pd
import re
import undetected_chromedriver as uc

with open('lincoln.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Site Address","Owner", "Mail Address","Mail City","Mail State","Zip Code","Living Area","Land Value","BLDG Value","Total Assessed Value","Sale Date","Sale price"])

count = 0

ul = "https://arcgisserver.lincolncounty.org/taxparcelviewer/"
path = which("chromedriver")
options = Options()
options.add_experimental_option("detach", True)
#options.add_argument("--headless")
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
driver = uc.Chrome(executable_path=path,options=options)
driver.get(ul)
time.sleep(60)
pin_btn = driver.find_element_by_xpath("//button[contains(text(),'Accept')]")
pin_btn.click()
time.sleep(2)
with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        if len(company) == 3:
            company = f"00{company}"
        elif len(company) == 4:
            company = f"0{company}"
        else:
            company = company
        btn = driver.find_element_by_xpath("(//div[@role='presentation'])[1]")
        btn.click()
        time.sleep(2)
        search = driver.find_element_by_xpath("//div[@class='input-group']/input[@class='form-control ags-clearable ui-autocomplete-input' and @name='pin']")
        search.clear()
        time.sleep(0.5)
        search.send_keys(company)
        search.send_keys(Keys.ENTER)
        time.sleep(4)
        try:
            try:
                first = driver.find_element_by_xpath("(//tr[@class='results-record'])[1]")
                first.click()
                time.sleep(2)
            except:
                first = None
            try:
                address = driver.find_element_by_xpath("(//td[@class='tdWordBreak'])[3]").text
            except:
                address = None
            try:
                owners = driver.find_element_by_xpath("(//td[@class='tdParcelDisplayText' and contains(text(),'Owner(s)')]/following-sibling::td)[1]").text
            except:
                owners = None
            try:
                mail_address = driver.find_element_by_xpath("(//td[@class='tdWordBreak']/div[contains(text(),'')])[4]").text
            except:
                mail_address = None
            try:
                mai_city_state_zip = driver.find_element_by_xpath("(//td[@class='tdParcelDisplayText' and contains(text(),'Mailing City, State Zip:')]/following-sibling::td)[1]").text
                mai_city_state_zip = str(mai_city_state_zip)

                zip_code = re.findall(r"....\d$", mai_city_state_zip)
                Mail_State = re.findall(r"\s\S*.", mai_city_state_zip)
                mail_city = re.findall(r"^\S*", mai_city_state_zip)
            except:
                mail_city = None
                zip_code = None
                Mail_State = None
            try:
                living_area = driver.find_element_by_xpath("(//td[@class='tdParcelDisplayText' and contains(text(),'Acres:')]/following-sibling::td)[1]").text
            except:
                living_area = None
            try:
                land_value = driver.find_element_by_xpath("(//td[@class='tdParcelDisplayText' and contains(text(),'Land Value:')]/following-sibling::td)[1]").text
            except:
                land_value = None
            try:
                bldg_value = driver.find_element_by_xpath("(//td[@class='tdParcelDisplayText' and contains(text(),'Improved Value:')]/following-sibling::td)[1]").text
            except:
                bldg_value = None
            try:
                total_accessed_value = driver.find_element_by_xpath("(//td[@class='tdParcelDisplayText' and contains(text(),'Total Value:')]/following-sibling::td)[1]").text
            except:
                total_accessed_value = None
            try:
                sale_date =  driver.find_element_by_xpath("(//td[@class='tdParcelDisplayText' and contains(text(),'Last Recorded Date:')]/following-sibling::td)[1]").text
            except:
                sale_date = None
            try:
                sale_price = driver.find_element_by_xpath("(//td[@class='tdParcelDisplayText' and contains(text(),'Last Sale Price:')]/following-sibling::td)[1]").text
            except:
                sale_price = None
                
            with open('lincoln.csv', 'a',newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([address,owners,mail_address,mail_city,Mail_State,zip_code,living_area,land_value,bldg_value,total_accessed_value,sale_date,sale_price])
                        count = count + 1
                        print("Data Saved in CSV :",count)
                        
        except:
            print("There is nothing to scrape ie serch is empty")
        
        
        

