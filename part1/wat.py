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



options = webdriver.ChromeOptions()
path = which("chromedriver")
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(chrome_options=options, executable_path=path)
PROXY = "11.456.448.110:8080"
options.add_argument('--proxy-server=%s' % PROXY)

ul = "https://www.actdatascout.com/RealProperty/Arkansas/Washington"
with open('test.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Parcel ID","Owners","Mailing Address","Mailing City","Mailing State","Mailing Zip Code","Site Address","Land Value","Bldg Value","Total_accessed_value","Sale_date","Sale Price","Property Type","Living Area","Year Built"])

with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        driver.find_element_by_xpath("//a[contains(text(),'Parcel')]").click()
        time.sleep(1)
        search = driver.find_element_by_xpath("//input[@id='ParcelNumber']")
        time.sleep(1)
        search.clear()
        search.send_keys(company)
        search.send_keys(Keys.ENTER)
        time.sleep(5)
        
        try:
            driver.find_element_by_xpath("(//button[@class='publicGridButton btn btn-default'])[1]").click()
            time.sleep(2)

            html = driver.page_source
            resp = Selector(text=html)
            
            parcel_id = resp.xpath("normalize-space((//span[@class='pull-left']/text())[1])").extract_first()
            if parcel_id:
                parcel_id = str(parcel_id)
                parcel_id = parcel_id.replace("Parcel:","")
                parcel_id = parcel_id.strip()
            owners = resp.xpath("//td[contains(text(),'Name')]/following-sibling::td/text()").get()

            mailing_address = resp.xpath("normalize-space((//td[contains(text(),'Mailing Address:')]/following-sibling::td/text())[1])").get()
            mailing_city_state_zip_code = resp.xpath("normalize-space((//td[contains(text(),'Mailing Address:')]/following-sibling::td/text())[2])").extract_first()
            try:
                mailing_city_state_zip_code = str(mailing_city_state_zip_code)
                mailing_city = re.findall(r"^[^,]+",mailing_city_state_zip_code)
                mailing_state = re.findall(r"\s\w\w\s",mailing_city_state_zip_code)
                mailing_zip_code = re.findall(r"\s\d.*",mailing_city_state_zip_code)
            except:
                mailing_city = None
                mailing_state = None
                mailing_zip_code = None

            sit = []
            site_address = resp.xpath("//td[contains(text(),'Physical Address:')]/following-sibling::td")
            for i in site_address:
                abc = i.xpath("normalize-space(.//text())").get()
                sit.append(abc)
            land_value = resp.xpath("normalize-space((//strong[contains(text(),'Land')]/parent::td/following-sibling::td)[2]/text())").get()
            bldg_value = resp.xpath("normalize-space((//strong[contains(text(),'Building')]/parent::td/following-sibling::td)[2]/text())").get()
            total_accessed_value = resp.xpath("normalize-space((//td[contains(text(),'Totals')]/following-sibling::td)[2]/text())").get()
            sale_date = resp.xpath("(//tr[@id='DocumentLinks']/td)[2]/text()").get()
            sale_price = resp.xpath("(//tr[@id='DocumentLinks']/td)[7]/text()").get()
            property_type = resp.xpath("(//div[contains(text(),'Details for Residential Card 1')]/following-sibling::div/table/tbody/tr/td)[1]/text()").get()
            living_area = resp.xpath("(//div[contains(text(),'Details for Residential Card 1')]/following-sibling::div/table/tbody/tr/td)[4]/text()").get()
            year_built = resp.xpath("normalize-space((//div[contains(text(),'Details for Residential Card 1')]/following-sibling::div/table/tbody/tr/td)[7]/text())").get()
            with open('test.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([parcel_id,owners,mailing_address,mailing_city,mailing_state,mailing_zip_code,sit,land_value,bldg_value,total_accessed_value,sale_date,sale_price,property_type,living_area,year_built])
                count = count + 1
                print("Data Saved in CSV:",count)

                        
        except:
            print("Search Result is empty")

        
        driver.close()