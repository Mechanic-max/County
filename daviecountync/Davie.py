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
from pandas import DataFrame
import wget
import re

ul = "https://maps.daviecountync.gov/itsnet/basicsearch.aspx"
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
with open('sample.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Mail Address", "Mail city","State","Zip Code","Site Address","BLDG Value","land value","Assessed Value","Sale Year","Sale Price","Year Built","Property Type","Beds","Bath(ADD Full and Hald)"])
driver.get(ul)
time.sleep(2)
driver.find_element_by_xpath("//input[@id='ctl00_contentplaceholderBasicSearch_btnNext']").click()
time.sleep(3)
with open(r"F:\projects\daviecountync\input.csv", 'r') as input_file:
    for company_name in input_file:
        company = company_name.strip()
        search = driver.find_element_by_xpath("//input[@id='ctl00_contentplaceholderBasicSearch_txtPropertyOwnerName']")
        search.send_keys(company)
        search.send_keys(Keys.ENTER)
        time.sleep(2)
        search_last = driver.find_element_by_xpath("((//tr[@class='RowStyleDefaultGridViewSkin'])[last()]/td/a)[1]")
        search_last.click()
        time.sleep(1)
        html = driver.page_source
        resp = Selector(text=html)
        bld = []
        b1 = resp.xpath("(//td)[53]/text()").get()
        b2 = resp.xpath("(//td)[55]/text()").get()
        bld.append(b1)
        bld.append(b2)
        sit =" "
        sit = resp.xpath("normalize-space((((//td[@valign='top']/table/tbody)[5]/tr/td)[2]/text())[2])").extract_first()
        sit = sit.replace("Address:","")
        sit = sit.lstrip()
        city_state_zip =""
        city_state_zip = resp.xpath("(((//td[@valign='top']/table/tbody)[3]/tr/td)[2]/text())[3]").extract_first()
        try:
            zi = re.findall(r"[\d]+", city_state_zip)
        except:
            zi = None
        try:
            state = re.findall(r"[a-zA-Z]+(?=[^,]*$)",city_state_zip)
        except:
            state = None
        try:
            mail_citi = re.findall(r"^[^,]+\s*",city_state_zip)
        except:
            mail_citi = None
        Name = resp.xpath("normalize-space((((//td[@valign='top']/table/tbody)[3]/tr/td)[2]/text())[1])").get()
        Mail_Address = resp.xpath("normalize-space((((//td[@valign='top']/table/tbody)[3]/tr/td)[2]/text())[2])").get()
        land_value = resp.xpath("(//td)[57]/text()").get()
        Assessed_Value = resp.xpath("(//td)[61]/text()").get()
        Sale_Year = resp.xpath("normalize-space((//table[@id='ctl00_contentplaceholderBasicSearch_gvSalesData']//tr/td[5])[1]/text())").get()
        Sale_Price = resp.xpath("(//table[@id='ctl00_contentplaceholderBasicSearch_gvSalesData']//tr/td[9])[1]/text()").get()
        
        goto = driver.find_element_by_xpath("(//td[@align='center']/a)[1]").get_attribute("href")
        driver.get(goto)
        time.sleep(2)
        html = driver.page_source
        resp = Selector(text=html)
        year_buit = resp.xpath("(//td[@class='AppraisalCardBorder-LT'])[12]/span/text()").get()
        property_type = resp.xpath("//span[@id='ctl04_labelImprovementTypeDescriptionValue']/text()").extract_first()
        beds_bath = resp.xpath("((//td[@class='AppraisalCardBorder-B' and @colspan='4'])/span[contains(text(),'/')])[last()]/text()").extract_first()
        try:
            beds = re.findall(r"^([0-9]+)",beds_bath)
        except:
            beds = None
        with open('sample.csv', 'a',newline='') as file:
            writer = csv.writer(file)
            writer.writerow([Name, Mail_Address, mail_citi,state,zi,sit,bld,land_value,Assessed_Value,Sale_Year,Sale_Price,year_buit,property_type,beds,beds_bath])
            print("Data Saved in CSV :")
        # dic = {
        #     'Name': Name,
        #     'Mail Address': Mail_Address,
        #     'Mail city':mail_citi,
        #     'State':state,
        #     'Zip Code':zi,
        #     'Site Address': sit,
        #     'BLDG Value': bld,
        #     'land value': land_value,
        #     'Assessed Value':Assessed_Value,
        #     'Sale Year':Sale_Year,
        #     'Sale Price':Sale_Price,
        #     'Year_built':year_buit,
        #     'Beds':beds,
        #     'Bath(ADD Full and Hald)':beds_bath,
        # }
        # print(dic)
        driver.back()
        driver.back()
        driver.back()
        time.sleep(3)
        driver.find_element_by_xpath("//input[@id='ctl00_contentplaceholderBasicSearch_btnNext']").click()
        time.sleep(3)


