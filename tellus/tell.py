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
import re

ul = "http://tellus.co.forsyth.nc.us/lrcpwa/SearchProperty.aspx"
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
with open('davidson_sample.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Owner","Site Address","Site City", "Mail Address", "Mail city","Mail State","Zip Code","Property Type","Living Area(SQFT)","Package Sale Date","Sale Amount","BLDG Value","land value","Assessed Value","Year Built","Beds","Bath(ADD Full and Hald)"])
pin_btn = driver.find_element_by_xpath("(//ul[@id='panelSummary']/li)[4]/a")
pin_btn.click()
time.sleep(1)
with open(r"F:/projects/tellus/input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        pin_btn = driver.find_element_by_xpath("//a[contains(text(),'PIN')]")
        pin_btn.click()
        time.sleep(2.5)
        search = driver.find_element_by_xpath("//input[@id='ctl00_ContentPlaceHolder1_PINNumberTextBox']")
        search.clear()
        search.send_keys(company)
        search.send_keys(Keys.ENTER)
        time.sleep(5)

        try:
            not_found = driver.find_element_by_xpath("//span[contains(text(),'No Records Found')]")
        except:

            html = driver.page_source
            resp = Selector(text=html)

            owner = resp.xpath("//table[@id='ctl00_PageHeader1_DetailsView1']//td[@class='h5']/text()").extract_first()
            site_address = resp.xpath("//span[@id='ctl00_PageHeader1_LocationAddressLabelInfo']/text()").extract_first()
            mail_address = resp.xpath("//span[@id='ctl00_PageHeader1_DetailsView4_Mail1']/text()").extract_first()
            mail_city = resp.xpath("//span[@id='ctl00_PageHeader1_DetailsView4_City']/text()").extract_first()
            mail_state = resp.xpath("//span[@id='ctl00_PageHeader1_DetailsView4_Label1']/text()").extract_first()
            zip_code = resp.xpath("//span[@id='ctl00_PageHeader1_DetailsView4_Label2']/text()").extract_first()
            site_city = resp.xpath("//span[@id='ctl00_ContentPlaceHolder1_DetailsView5_Label3']/text()").extract_first()
            package_sale_date = resp.xpath("//span[@id='ctl00_ContentPlaceHolder1_DetailsView6_Label5']/text()").extract_first()
            package_sale_amount = resp.xpath("//span[@id='ctl00_ContentPlaceHolder1_DetailsView6_Label6']/text()").extract_first()
            try:
                link = driver.find_element_by_xpath("//a[@id='ctl00_PageHeader1_BuildingsHyperLink']")
                link.click()
                time.sleep(2)

                html = driver.page_source
                resp = Selector(text=html)

                property_type  = resp.xpath("//span[@id='ctl00_ContentPlaceHolder1_DetailsView3_Label1']/text()").extract_first()
                Living_Area_SQFT  = resp.xpath("//span[@id='ctl00_ContentPlaceHolder1_DetailsView3_Label3']/text()").extract_first()
                year_built  = resp.xpath("//span[@id='ctl00_ContentPlaceHolder1_DetailsView4_Label1']/text()").extract_first()
                baths = resp.xpath("//span[@id='ctl00_ContentPlaceHolder1_DetailsView3_Label34']/text()").extract_first()
                bedrooms  = resp.xpath("//span[@id='ctl00_ContentPlaceHolder1_DetailsView3_Label12']/text()").extract_first()
                total_accessed_amount  = resp.xpath("//span[@id='ctl00_ContentPlaceHolder1_lblTotalValueAssessed']/text()").extract_first()
                bld  = resp.xpath("(//span[@id='ctl00_ContentPlaceHolder1_DetailsView7_Label7']/text())[2]").extract_first()
                land_value  = resp.xpath("//span[@id='ctl00_ContentPlaceHolder1_lblLandValueAssessed']/text()").extract_first()
                with open('davidson_sample.csv', 'a',newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([owner, site_address,site_city,mail_address, mail_city,mail_state,zip_code,property_type,Living_Area_SQFT,package_sale_date,package_sale_amount,bld,land_value,total_accessed_amount,year_built,bedrooms,baths])
                    print("Data Saved in CSV :")
                driver.back()
                time.sleep(2)
            except:
                link = None
                    
        driver.get(ul)
        time.sleep(5)