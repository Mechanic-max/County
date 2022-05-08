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
    writer.writerow(["site_address","owner_name","address","State","zip","total_market_value","property_use","land_value","bldg_value","use_code","Bedrooms","full_bath","half_bath","year_built","sale_date","sale_price"])


try:
    driver.find_element_by_xpath("//button[contains(text(),'I Understand')]").click()
    time.sleep(2)
except:
    print("Pop up didn't appear")

with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        company = str(company)
        if len(company)==2:
            company = f"000{company}"
        elif len(company) == 3:
            company = f"00{company}"
        elif len(company) == 4:
            company = f"0{company}"
        else:
            company = company
        ul = f"https://property.spatialest.com/nc/pitt#/property/{company}"
        try:
            driver.get(ul)
            time.sleep(2)
            html = driver.page_source
            resp = Selector(text=html)
            
            site_address = resp.xpath("//div[@class='location text-highlight']/span/text()").extract_first()
            owner_name = resp.xpath("//div[@class='mailing']/div[@class='value']/text()[1]").extract_first()
            owner_address = resp.xpath("//div[@class='mailing']/div[@class='value']/text()[2]").extract_first()
            try:
                owner_address = str(owner_address)
                zip = re.findall(r"\b\w+\W*$",owner_address)
                State = re.findall(r"\s\w\w\s\d",owner_address)
                address = re.sub(r"\s\w+\s+\w+\s*\Z",'',owner_address)
            except:
                zip = None
                State = None
                address = None
            total_market_value = resp.xpath("//span[@class='value text-highlight']/text()").extract_first()
            property_use = resp.xpath("//span[contains(text(),'Property Use')]/following-sibling::span/text()").extract_first()
            land_value = resp.xpath("//span[contains(text(),'Land Value')]/following-sibling::span/text()").extract_first()
            bldg_value = resp.xpath("//span[contains(text(),'Building Value')]/following-sibling::span/text()").extract_first()
            use_code = resp.xpath("//span[contains(text(),'Style')]/following-sibling::span/text()").extract_first()
            Bedrooms = resp.xpath("//span[contains(text(),'Bedrooms')]/following-sibling::span/text()").extract_first()
            full_bath = resp.xpath("//span[contains(text(),'Full Baths')]/following-sibling::span/text()").extract_first()
            half_bath = resp.xpath("//span[contains(text(),'Half Baths')]/following-sibling::span/text()").extract_first()
            year_built = resp.xpath("//span[contains(text(),'Year Built')]/following-sibling::span/text()").extract_first()
            sale_date = resp.xpath("//th[@title='Sale Date']/parent::tr/parent::thead/following-sibling::tbody/tr/td[1]/text()").extract_first()
            sale_price = resp.xpath("//th[@title='Sale Date']/parent::tr/parent::thead/following-sibling::tbody/tr/td[2]/text()").extract_first()
            with open('test.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([site_address,owner_name,address,State,zip,total_market_value,property_use,land_value,bldg_value,use_code,Bedrooms,full_bath,half_bath,year_built,sale_date,sale_price])
                count = count + 1
                print("Data Saved in CSV:",count)
        
        except:
            print("Search result is empty")
