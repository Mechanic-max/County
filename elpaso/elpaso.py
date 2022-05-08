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

ul = "https://property.spatialest.com/co/elpaso/#/"
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
count = 0
with open('test.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Parcel ID","Site Address","Owner Name","Mail Address","Zip Code","Property Type","Living Area","Land Value","BLDG Value","Total Accessed Value","Sale Date","Sale Amount","Year Built","Beds","Baths"])

with open("input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        search = driver.find_element_by_id("primary_search")
        time.sleep(3)
        try:
            driver.find_element_by_id("primary_search").send_keys(Keys.CONTROL + "a")
            driver.find_element_by_id("primary_search").send_keys(Keys.DELETE)
        except:
            print("there is nothing to delete in seach box")
        time.sleep(1)
        search.send_keys(company)
        search.send_keys(Keys.ENTER)
        time.sleep(10)
        try:
            try:
                site_address = driver.find_element_by_xpath("//div[@class='location text-highlight']/span").text
            except:
                site_address = None
            try:
                owners = driver.find_element_by_xpath("((//select[@class='value '])[1]/option)[1]").text
            except:
                owners = None
            try:
                mailing_address = driver.find_element_by_xpath("(//p[@class='clearfix data-list-item with-title with-value col-sm-12 col-xs-12'])[2]/span[@class='value ']").text
                try:
                    mailing_address = str(mailing_address)
                    add = re.findall(r"^[^,]+",mailing_address)
                    zip_code = re.findall(r",\s\S.*",mailing_address)
                except:
                    add = None
                    zip_code
            except:
                mailing_address = None
                add = None
                zip_code
            try:
                land_value = driver.find_element_by_xpath("(//p[@class='clearfix data-list-item with-value col-xs-4'])[1]/span[@class='value ']").text
            except:
                land_value = None
            try:
                bldg_value = driver.find_element_by_xpath("(//p[@class='clearfix data-list-item with-value col-xs-4'])[3]/span[@class='value ']").text
            except:
                bldg_value = None
            try:
                total_accessed_value = driver.find_element_by_xpath("(//p[@class='clearfix data-list-item with-value col-xs-4'])[5]/span[@class='value ']").text
            except:
                total_accessed_value = None
            try:
                property_type = driver.find_element_by_xpath("((//table[@class='table table-striped table-nolines ']/tbody/tr)[1]/td)[2]").text
            except:
                property_type = None
            try:
                Living_Area = driver.find_element_by_xpath("(//p[@class='clearfix data-list-item with-title with-value col-sm-6 col-xs-12'])[4]/span[@class='value ']").text
            except:
                Living_Area = None
            try:
                year_built = driver.find_element_by_xpath("(//p[@class='clearfix data-list-item with-title with-value col-sm-6 col-xs-12'])[9]/span[@class='value ']").text
            except:
                year_built = None
            try:
                beds = driver.find_element_by_xpath("(//p[@class='clearfix data-list-item with-title with-value col-sm-6 col-xs-12' or @class='clearfix data-list-item with-title col-sm-6 col-xs-12'])[15]/span[@class='value ']").text
            except:
                beds = None
            try:
                baths = driver.find_element_by_xpath("(//p[@class='clearfix data-list-item with-title with-value col-sm-6 col-xs-12' or @class='clearfix data-list-item with-title col-sm-6 col-xs-12'])[17]/span[@class='value ']").text
            except:
                baths = None
            try:
                sale_date = driver.find_element_by_xpath("((//table[@class='table table-striped table-nolines '])[2]/tbody/tr/td)[2]").text
            except:
                sale_date = None
            try:
                sale_amount = driver.find_element_by_xpath("((//table[@class='table table-striped table-nolines '])[2]/tbody/tr/td)[3]").text
            except:
                sale_amount = None

            with open('test.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([company,site_address,owners,add,zip_code,property_type,Living_Area,land_value,bldg_value,total_accessed_value,sale_date,sale_amount,year_built,beds,baths])
                count = count + 1
                print("Data Saved in CSV",count)

        except:
            print("Search Result is empty")
  