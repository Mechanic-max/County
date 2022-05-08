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
ul = "http://nyenv-assessor.devnetwedge.com/"
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
    writer.writerow(["Parcel ID","Owner","Site Address","Site State","Site Zip","Mail Address","Mail State","Mail Zip Code","Property Type","Sale Date","Sale Price","Year Built","Living Area(SQFT)","Beds","Bathrooms","Land Value","BLDG Value","total_accessed_value"])

with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        search = driver.find_element_by_xpath("//input[@id='property-key']")
        time.sleep(1)
        search.clear()
        search.send_keys(company)
        search.send_keys(Keys.ENTER)
        time.sleep(5)
        try:
            try:
                parcel_id = driver.find_element_by_xpath("//div[contains(text(),'Parcel ID')]/following-sibling::div").text
            except:
                parcel_id = None
            
            try:
                site_address = driver.find_element_by_xpath("//div[contains(text(),'Site Address')]/following-sibling::div").text 
                try:
                    site_address = str(site_address)
                    site_city = re.findall(r"([\w\s]+)", site_address)
                    site_state = re.findall(r",\s\w\w", site_address)
                    if site_state:
                        site_state = str(site_state)
                        site_state = site_state.replace(',','')
                        site_state = site_state.lstrip()
                    site_zip = re.findall(r"\d\d\d\d\d", site_address)
                except:
                    site_city = None
                    site_state = None
                    site_zip = None  
                      
            except:
                site_address = None
                site_city = None
                site_state = None
                site_zip = None   

            try:
                property_type = driver.find_element_by_xpath("(//div[contains(text(),'Land Use')]/following-sibling::div)[2]").text
            except:
                property_type = None
            
            try:
                owner = driver.find_element_by_xpath("(//div[contains(text(),'Name')]/following-sibling::div)[1]").text
            except:
                owner = None
            
            try:
                land_value = driver.find_element_by_xpath("((//td[contains(text(),'Residential')])[1]/following-sibling::td)[1]").text
            except:
                land_value = None
            
            try:
                bldg_value = driver.find_element_by_xpath("((//td[contains(text(),'Residential')])[1]/following-sibling::td)[2]").text
            except:
                bldg_value = None
            
            try:
                total_accessed_value = driver.find_element_by_xpath("((//td[contains(text(),'Residential')])[1]/following-sibling::td)[4]").text
            except:
                total_accessed_value = None
            
            try:
                mail_address = driver.find_element_by_xpath("(//div[contains(text(),'Mailing Address')]/following-sibling::div)[1]").text 
                try:
                    mail_address = str(mail_address)
                    mail_city = re.findall(r"^[^,]*", mail_address)
                    mail_state = re.findall(r",\s\w\w,", mail_address)
                    if mail_state:
                        mail_state = str(mail_state)
                        mail_state = mail_state.replace(",",'')
                        mail_state = mail_state.lstrip()

                    mail_zip = re.findall(r",\s\d.*", mail_address)
                except:
                    mail_city = None
                    mail_state = None
                    mail_zip = None  
                      
            except:
                mail_address = None
                mail_city = None
                mail_state = None
                mail_zip = None  

            try:
                sale_date = driver.find_element_by_xpath("((//table[@class='table table-bordered table-hover text-center']/tbody/tr)[1]/td)[4]").text
            except:
                sale_date = None
            
            try:
                sale_price =driver.find_element_by_xpath("((//table[@class='table table-bordered table-hover text-center']/tbody/tr)[1]/td)[7]").text
            except:
                sale_price = None
            
            try:
                driver.find_element_by_xpath("//span[@id='images-collapse-toggle-1']").click()
                time.sleep(2)

                try:
                    year_built = driver.find_element_by_xpath("(//table[@class='table table-bordered']//tr[@class='text-center'])[3]/td[last()]").text
                except:
                    year_built = None
                
                try:
                    beds = driver.find_element_by_xpath("//td[contains(text(),'# of Bedrooms')]/following-sibling::td").text
                except:
                    beds = None
                
                try:
                    bathrooms = driver.find_element_by_xpath("//td[contains(text(),'# of Bathrooms')]/following-sibling::td").text
                except:
                    bathrooms = None
                
                try:
                    Living_Area = driver.find_element_by_xpath("((//table[@class='table table-bordered']//tr[@class='text-center'])[3]/td)[last()-1]").text
                except:
                    Living_Area = None
            
            except:
                print("Btn nai chala")
                year_built= None
                beds = None
                bathrooms = None
                Living_Area = None
                
                
            with open('test.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([parcel_id,owner,site_city,site_state,site_zip,mail_city,mail_state,mail_zip,property_type,sale_date,sale_price,year_built,Living_Area,beds,bathrooms,land_value,bldg_value,total_accessed_value])
                count = count + 1
                print("Data Saved in CSV", count)

            driver.get(ul)
            time.sleep(3)              
        except:
            print("Search Result is empty")
            driver.get(ul)
            time.sleep(3) 
        