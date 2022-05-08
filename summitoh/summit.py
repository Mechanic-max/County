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

with open('test.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Parcel ID","Site Address","Site City","Site State","Site Zip","Owner","Mail Address","Mail City","Mail State","Mail Zip","Property Type","Land value","Bldg Value","Total Accessed Value","Sale Date","Sale Amount","Year Built","Bedrooms","Baths"])

with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        if len(company) == 6:
            company = str(company)
            company = f"0{company}"
        a = f"https://fiscaloffice.summitoh.net/pls/apex/thothrefstrt.do_one?parcel={company}&print=1&lienyear=2020&doland=ON&docard=ON&cardnum=ALL&dosales=ON&dopermits=ON&dotaxes=ON&doassess=ON&docauv=OFF&donotes=ON&dogeninf=OFF"
        driver.get(a)
        time.sleep(2)
        try:
            html = driver.page_source
            resp = Selector(text=html)
            
            parcel_id = resp.xpath("(//font/b[contains(text(),'PARCEL')]/parent::font/parent::td/following-sibling::td)[1]/font/text()").extract_first()
            owner = resp.xpath("(//font/b[contains(text(),'OWNER')]/parent::font/parent::td/following-sibling::td)[1]//text()").extract_first()
            site_address = resp.xpath("(//font/b[contains(text(),'ADDR.')]/parent::font/parent::td/following-sibling::td)[1]//text()").extract_first()
            try:
                site_address = str(site_address)
                site_street = re.findall(r"^[^,]+,",site_address)
                site_city = re.findall(r",\s\w.*\s",site_address)
                site_zip = re.findall(r"\s\d.*",site_address)
            except:
                site_street = None
                site_city = None
                site_zip = None
            

            mail_address = resp.xpath("(//b[contains(text(),'MAILING ADDRESS')]/parent::font/following-sibling::font/text())[2]").extract_first()
            mail_city_zip = resp.xpath("(//b[contains(text(),'MAILING ADDRESS')]/parent::font/following-sibling::font/text())[3]").extract_first()
            
            try:
                mail_city_zip = str(mail_city_zip)
                mail_city = re.findall(r"^[^,]+",mail_city_zip)
                mail_state = re.findall(r"\s\w\w\s",mail_city_zip)
                mail_zip = re.findall(r"\d.*",mail_city_zip)
            except:
                mail_city = None
                mail_state = None
                mail_zip = None  

            property_type = resp.xpath("//font[contains(text(),' - ')]/text()").extract_first()
            land_value = resp.xpath("(//font/b[contains(text(),'LAND:')]/parent::font/parent::td/following-sibling::td)[1]//text()").extract_first()
            bldg_value = resp.xpath("(//font/b[contains(text(),'BUILDING:')]/parent::font/parent::td/following-sibling::td)[1]//text()").extract_first()
            total_accessed_value = resp.xpath("(//font/b[contains(text(),'TOTAL:')]/parent::font/parent::td/following-sibling::td)[1]//text()").extract_first()
            
            sale_date = resp.xpath("//b[contains(text(),'DATE')]/parent::font/text()").extract_first()
            sale_amount = resp.xpath("//b[contains(text(),'AMT')]/parent::font/text()").extract_first()
            
            year_built = resp.xpath("(//font/b[contains(text(),'YR BUILT')]/parent::font/parent::td/following-sibling::td)[1]/font/text()").extract_first()
            Bedrooms = resp.xpath("(//font/b[contains(text(),'BEDRM')]/parent::font/parent::td/following-sibling::td)[1]/font/text()").extract_first()
            baths = resp.xpath("(//font/b[contains(text(),'FULL/BTH')]/parent::font/parent::td/following-sibling::td)[1]/font/text()").extract_first()
            

            with open('test.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([parcel_id,site_address,site_street,site_city,site_zip,owner,mail_address,mail_city,mail_state,mail_zip,property_type,land_value,bldg_value,total_accessed_value,sale_date,sale_amount,year_built,Bedrooms,baths])
                count = count + 1
                print("Data Saved in CSV",count)
            
        except:
            print("Search result is empty")