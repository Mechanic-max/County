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
import wget

count = 0
with open('test.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["text_year","owner1","owner2","owner_address","owner_city","owner_state","owner_zip","site_address","mp_id","parcel_no","property_class","land_value","bldg_value","total_market_value","year_built","sale_date","sale_price"])

ul = f"https://inigo.williamson-tn.org/property_search/#"

path = which("chromedriver")
options = Options()
options.add_experimental_option("detach", True)
#options.add_argument("--headless")
ua = UserAgent()
userAgent = ua.random
userAgent = ua.random
options.add_argument(f'user-agent={userAgent}')
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(executable_path=path,options=options)
driver.get(ul)
time.sleep(3)


with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        search = driver.find_element_by_xpath("//input[@id='owner_name']")
        search.clear()
        search.send_keys(company)
        search.send_keys(Keys.ENTER)
        time.sleep(5)

        try:
            results = driver.find_elements_by_xpath("//table[@id='results_table']/tbody/tr")
            for i in range(0,len(results)):
                driver.find_elements_by_xpath("//table[@id='results_table']/tbody/tr")[i].click()
                time.sleep(3)


                html = driver.page_source
                resp = Selector(text=html)

                text_year = resp.xpath("//dt[contains(text(),'Current Tax Year')]/following-sibling::dd/text()").extract_first()
                owner1 = resp.xpath("(//dt[contains(text(),'Owner')]/following-sibling::dd/text())[1]").extract_first()
                owner2 = resp.xpath("(//dt[contains(text(),'Owner')]/following-sibling::dd/text())[2]").extract_first()
                owner_address = resp.xpath("(//dt[contains(text(),'Address')]/following-sibling::dd/text())[1]").extract_first()
                owner_city_state_zip = resp.xpath("normalize-space((//dt[contains(text(),'Address')]/following-sibling::dd/text())[2])").extract_first()
                try:
                    owner_city_state_zip = str(owner_city_state_zip)
                    owner_city = re.findall(r"^[^,]+,",owner_city_state_zip)
                    owner_state = re.findall(r"\s\w\w\s",owner_city_state_zip)
                    owner_zip = re.findall(r"\d\d\d\d\d",owner_city_state_zip)
                except:
                    owner_city = None
                    owner_state = None
                    owner_zip = None

                site_address = resp.xpath("//dl[@id='prop_street']/dd/text()").extract_first()
                mp_id = resp.xpath("//dl[@id='map']/dd/text()").extract_first()
                parcel_no = resp.xpath("//dl[@id='parcel']/dd/text()").extract_first()
                
                land_value = resp.xpath("//th[contains(text(),'Land Market Value')]/following-sibling::td/text()").extract_first()
                bldg_value   = resp.xpath("//th[contains(text(),'Improvement Value')]/following-sibling::td/text()").extract_first()
                total_market_value = resp.xpath("//th[contains(text(),'Total Market Appraisal')]/following-sibling::td/text()").extract_first()
                property_class = resp.xpath("//dl[@id='property_class']/dd/text()").extract_first()
                year_built = resp.xpath("//dl[@id='year_built_R01']/dd/text()").extract_first()
                sale_date = resp.xpath("//section[@id='sales_information']/table/tbody/tr[1]/td[1]/text()").extract_first()
                sale_price = resp.xpath("//section[@id='sales_information']/table/tbody/tr[1]/td[2]/text()").extract_first()
                
            
                with open('test.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([text_year,owner1,owner2,owner_address,owner_city,owner_state,owner_zip,site_address,mp_id,parcel_no,property_class,land_value,bldg_value,total_market_value,year_built,sale_date,sale_price])
                    count = count + 1
                    print("Data Saved in CSV:",count)

                driver.back()
                time.sleep(2)
        except:
            print("Search results is empty")
            break

        driver.get(ul)
        time.sleep(5)