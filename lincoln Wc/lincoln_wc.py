from typing import Type
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
with open('test.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Account No","Parcel_No","owner_name","site_address","Mail Street","mail_city","mail_state","mail_zip","sub_division","lot","block","Section","Township","Range","property_type","land_value","bldg_value","total_market_value","built_year","beds","baths","Living_area"])
with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        ul = f"https://propertydetails.lcwy.org/Home/Detail/{company}?accountNumber={company}&taxYear=2021&pageSize=10"
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
        html = driver.page_source
        resp = Selector(text=html)
        
        site_address = resp.xpath("//h5[contains(text(),'Property Address')]/following-sibling::span/text()").extract_first()
        owner_name = resp.xpath("(//strong[contains(text(),'Primary Owner')]/following-sibling::span)[1]/text()").extract_first()
        street_address = resp.xpath("(//strong[contains(text(),'Primary Owner')]/following-sibling::span)[2]/text()").extract_first()
        mail_zip1 = resp.xpath("(//strong[contains(text(),'Primary Owner')]/following-sibling::span)[6]/text()").extract_first()
        mail_zip1 = str(mail_zip1)
        if '8' in mail_zip1:
            
            mail_city = resp.xpath("(//strong[contains(text(),'Primary Owner')]/following-sibling::span)[4]/text()").extract_first()
            mail_state = resp.xpath("(//strong[contains(text(),'Primary Owner')]/following-sibling::span)[5]/text()").extract_first()
            mail_zip = resp.xpath("(//strong[contains(text(),'Primary Owner')]/following-sibling::span)[6]/text()").extract_first()
        else:
            mail_city = resp.xpath("(//strong[contains(text(),'Primary Owner')]/following-sibling::span)[3]/text()").extract_first()
            mail_state = resp.xpath("(//strong[contains(text(),'Primary Owner')]/following-sibling::span)[4]/text()").extract_first()
            mail_zip = resp.xpath("(//strong[contains(text(),'Primary Owner')]/following-sibling::span)[5]/text()").extract_first()
        
        sub_division = resp.xpath("//dt[contains(text(),'Subdivision')]/following-sibling::dd/text()").extract_first()
        lot = resp.xpath("//dt[contains(text(),'Lot')]/following-sibling::dd/text()").extract_first()
        block = resp.xpath("//dt[contains(text(),'Block')]/following-sibling::dd/text()").extract_first()
        Section = resp.xpath("//dt[contains(text(),'Section')]/following-sibling::dd/text()").extract_first()
        Township = resp.xpath("//dt[contains(text(),'Township')]/following-sibling::dd/text()").extract_first()
        Range = resp.xpath("//dt[contains(text(),'Range')]/following-sibling::dd/text()").extract_first()
        
        Parcel_No = resp.xpath("//dt[contains(text(),'Parcel Number')]/following-sibling::dd/text()").extract_first()
        Living_area = resp.xpath("//dt[contains(text(),'Square Feet')]/following-sibling::dd/text()").extract_first()

        land_value = resp.xpath("((//table[@class='table table-hover'])[1]/tbody/tr/td)[3]/text()").extract_first()
        bldg_value = resp.xpath("((//table[@class='table table-hover'])[1]/tbody/tr/td)[8]/text()").extract_first()
        total_market_value = resp.xpath("(//th[contains(text(),'Totals')]/following-sibling::th)[1]/text()").extract_first()

        property_type = resp.xpath("(//dt[contains(text(),'Occupancy')]/following-sibling::dd)[1]/text()").extract_first()
        built_year = resp.xpath("(//dt[contains(text(),'Year Built')]/following-sibling::dd)[1]/text()").extract_first()
        beds = resp.xpath("(//dt[contains(text(),'Bed Rooms')]/following-sibling::dd)[1]/text()").extract_first()
        baths = resp.xpath("(//dt[contains(text(),'Baths')]/following-sibling::dd)[1]/text()").extract_first()
        with open('test.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([company,Parcel_No,owner_name,site_address,street_address,mail_city,mail_state,mail_zip,sub_division,lot,block,Section,Township,Range,property_type,land_value,bldg_value,total_market_value,built_year,beds,baths,Living_area])
            count = count + 1
            print("Data Saved in CSV",count)
        driver.close()


