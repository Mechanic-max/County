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
ul = "https://hockingoh-auditor-classic.ddti.net/Search.aspx"
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

with open('ho.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["owner","Site Address","Site City","Site State","Site Zip Code","Mail Address","Mail City","Mail State"," Mail Zip Code","Land Value","BLDG Value","Total Accessed Value","Year Built","Living Area","Property Type","Beds","Baths","Sale Date", "Sale Price"])

try:
    driver.find_element_by_xpath("//input[@id='ContentPlaceHolder1_btnDisclaimerAccept']").click()
    time.sleep(3)
except:
    print("Pop up didn't appear")

with open('input.txt','r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        search = driver.find_element_by_xpath("//input[@id='ContentPlaceHolder1_Parcel_tbParcelNumber']")
        time.sleep(1)
        search.clear()
        ct = f"0{line}"
        search.send_keys(ct)
        search.send_keys(Keys.ENTER)
        time.sleep(2)
        try:

            btn = driver.find_element_by_xpath("((//tr[@class='rowstyle'])[1]/td/a)[1]")
            btn.click()
            time.sleep(3)
            try:
                site_address = driver.find_element_by_xpath("//span[@id='ContentPlaceHolder1_Base_FormView1_OwnerAddressLine2Label']").text
            except:
                site_address = None
            try:
                site_zip_st = driver.find_element_by_xpath("//span[@id='ContentPlaceHolder1_Base_FormView1_OwnerAddressLine3Label']").text
                try:
                    site_zip_st = str(site_zip_st)
                    site_city = re.findall(r"^[A-Z]*", site_zip_st)
                    site_state = re.findall(r"\s.*\s", site_zip_st)
                    site_zip = re.findall(r"\d\d\d\d\d", site_zip_st)
                except:
                    site_city = None
                    site_state = None
                    site_zip = None
            except:
                site_zip_st = None
                site_city = None
                site_state = None
                site_zip = None
            try:
                owner = driver.find_element_by_xpath("//span[@id='ContentPlaceHolder1_Base_fvDataProfileOwner_OwnerLabel']").text
            except:
                owner = None
            try:
                mail_address = driver.find_element_by_xpath("//span[@id='ContentPlaceHolder1_Base_fvDataProfileOwner_AddressLabel']").text
            except:
                mail_address = None
            try:
                st_mail_add = driver.find_element_by_xpath("//span[@id='ContentPlaceHolder1_Base_fvDataProfileOwner_Label1']").text
                try:
                    st_mail_add = str(st_mail_add)
                    mail_city = re.findall(r"^[A-Z]*", st_mail_add)
                    mail_state = re.findall(r"\s.*\s", st_mail_add)
                    mail_zip = re.findall(r"\d\d\d\d\d", st_mail_add)
                except:
                    mail_city = None
                    mail_state = None
                    mail_zip = None
            except:
                st_mail_add = None
                mail_city = None
                mail_state = None
                mail_zip = None

            try:
                Valuation = driver.find_element_by_xpath("//a[contains(text(),'Valuation')]")
                Valuation.click()
                time.sleep(3)

                html = driver.page_source
                resp = Selector(text=html)

                land_value = resp.xpath("//span[@id='ContentPlaceHolder1_Valuation_fvDataValuation_AppraisedLandValueLabel']/text()").extract_first()
                Building_value = resp.xpath("//span[@id='ContentPlaceHolder1_Valuation_fvDataValuation_AppraisedImprovementsValueLabel']/text()").extract_first()
                total_accessed_value = resp.xpath("//span[@id='ContentPlaceHolder1_Valuation_fvDataValuation_AppraisedTotalValueLabel']/text()").extract_first()
            
            except:
                land_value = None
                Building_value = None
                total_accessed_value = None
            

            try:
                Residential = driver.find_element_by_xpath("//a[contains(text(),'Residential')]")
                Residential.click()
                time.sleep(3)

                html = driver.page_source
                resp = Selector(text=html)

                propert_type = resp.xpath("//span[@id='ContentPlaceHolder1_Residential_fvDataResidential_OccupancyLabel']/text()").extract_first()
                year_built = resp.xpath("//span[@id='ContentPlaceHolder1_Residential_fvDataResidential_Label91']/text()").extract_first()
                beds = resp.xpath("//span[@id='ContentPlaceHolder1_Residential_fvDataResidential_TotalBedroomsLabel']/text()").extract_first()
                Living_Area = resp.xpath("//span[@id='ContentPlaceHolder1_Residential_fvDataResidential_TotalSquareFeetLabel']/text()").extract_first()
                
                baths = resp.xpath("//span[@id='ContentPlaceHolder1_Residential_fvDataResidential_TotalBathsLabel']/text()").extract_first()
           
            except:
                year_built = None
                beds = None
                Living_Area = None
                propert_type = None
                baths = None
           

            try:
                Sales = driver.find_element_by_xpath("//a[contains(text(),'Sales')]")
                Sales.click()
                time.sleep(3)

                html = driver.page_source
                resp = Selector(text=html)

                sale_date = resp.xpath("(//table[@id='ContentPlaceHolder1_Sales_gvDataSales']/tbody/tr/td)[2]/text()").extract_first()
                sale_price = resp.xpath("(//table[@id='ContentPlaceHolder1_Sales_gvDataSales']/tbody/tr/td)[3]/text()").extract_first()
                 
           
            except:
                sale_date = None
                sale_price = None


            with open('ho.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([owner,site_address,site_city,site_state,site_zip,mail_address,mail_city,mail_state,mail_zip,land_value,Building_value,total_accessed_value,year_built,Living_Area,propert_type,beds,baths,sale_date,sale_price])
                count = count + 1
                print("Data Saved in CSV ", count)
            
            driver.get(ul)
            time.sleep(3)              
        except:
            print("Search Result is empty")
            driver.get(ul)
            time.sleep(3)