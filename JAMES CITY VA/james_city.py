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
# with open('test.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(["Source Address","owner_name","Mailing_address","mail_city","mail_state","mail_zip","property_class","site_address","site_city","site_state","site_zip","land_value","bldg_value","total_market_value","Atucal_year_built","living_area","Bedrooms","full_baths","half_baths","sale_date","sale_price"])

ul = "https://property.jamescitycountyva.gov/JamesCity/"

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
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(executable_path=path,options=options)
driver.get(ul)
time.sleep(10)



with open("input.csv", 'r') as input_file:
    for code in input_file:
        try:
            driver.find_element_by_xpath("//span[@id='cbNewCheckbox']").click()
            time.sleep(3)
            driver.find_element_by_xpath("//input[@id='btnEnterSite']").click()
            time.sleep(3)
        except:
            print("Pop up didn't appear")
        company = code.strip()
        search = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "acName"))
        )
        #search = driver.find_element_by_xpath("//input[@id='']")
        # time.sleep(2)
        # search.clear()
        time.sleep(1)
        search.send_keys(company)
        search.send_keys(Keys.ENTER)
        time.sleep(6)
        
        try:
            html = driver.page_source
            resp = Selector(text=html)

            owner_name = resp.xpath("normalize-space(//strong[contains(text(),'Name')]/parent::td/following-sibling::td/text())").extract_first()
            Mailing_address = resp.xpath("normalize-space(//strong[contains(text(),'Mailing Address')]/parent::td/following-sibling::td/text()[1])").extract_first()
            mail_city_state_zip = resp.xpath("normalize-space(//strong[contains(text(),'Mailing Address')]/parent::td/following-sibling::td/text()[2])").extract_first()
            try:
                mail_city_state_zip = str(mail_city_state_zip)
                mail_city = re.findall(r"^[^,]+",mail_city_state_zip)
                mail_state = re.findall(r",\s\w\w\s",mail_city_state_zip)
                mail_zip = re.findall(r"\d.*",mail_city_state_zip)
            except:
                mail_city = None
                mail_state = None
                mail_zip = None

            property_class = resp.xpath("normalize-space(//strong[contains(text(),'Property Class:')]/parent::td/following-sibling::td/text())").extract_first()
            site_address = resp.xpath("normalize-space(//strong[contains(text(),'Property Address')]/parent::td/following-sibling::td/text()[1])").extract_first()

            site_address_city = resp.xpath("normalize-space(//strong[contains(text(),'Property Address')]/parent::td/following-sibling::td/text()[2])").extract_first()
            try:
                site_address_city = str(site_address_city)
                site_city = re.findall(r"^[^,]+",site_address_city)
                site_state = re.findall(r",\s\w\w\s",site_address_city)
                site_zip = re.findall(r"\d.*",mail_city_state_zip)
            except:
                site_state = None
                site_city = None
                site_zip = None

            try:
                driver.find_element_by_xpath("//span[contains(text(),'Improvements')]/parent::a").click()
                time.sleep(4)
                html = driver.page_source
                resp = Selector(text=html)
            
                Atucal_year_built = resp.xpath("//strong[contains(text(),'Year Built:')]/parent::td/following-sibling::td/text()[1]").extract_first()
                living_area = resp.xpath("//strong[contains(text(),'Finished')]/parent::td/following-sibling::td/text()[1]").extract_first()
                Bedrooms = resp.xpath("//strong[contains(text(),'Bedrooms')]/parent::td/following-sibling::td/text()[1]").extract_first()
                full_baths = resp.xpath("//strong[contains(text(),'Full Baths:')]/parent::td/following-sibling::td/text()[1]").extract_first()
                half_baths = resp.xpath("//strong[contains(text(),'Half Baths:')]/parent::td/following-sibling::td/text()[1]").extract_first()
            except:
                Atucal_year_built = None
                living_area = None
                Bedrooms = None
                full_baths = None
                half_baths = None

                

            try:
                driver.find_element_by_xpath("//span[contains(text(),'Ownership History')]/parent::a").click()
                time.sleep(4)
                html = driver.page_source
                resp = Selector(text=html)
            
                sale_date = resp.xpath("//div[@id='OwnershipHistory']/table/tbody/tr[2]/td[3]/text()").extract_first()
                sale_price = resp.xpath("//div[@id='OwnershipHistory']/table/tbody/tr[2]/td[5]/text()").extract_first()

            except:
                sale_date = None
                sale_price = None

            try:
                driver.find_element_by_xpath("//span[contains(text(),'Assessment')]/parent::a").click()
                time.sleep(4)
                html = driver.page_source
                resp = Selector(text=html)
            
                land_value = resp.xpath("//div[@id='Assessment']/table/tbody/tr[last()-2]/td[last()-1]/text()").extract_first()
                bldg_value = resp.xpath("//div[@id='Assessment']/table/tbody/tr[last()-1]/td[last()-1]/text()").extract_first()
                total_market_value = resp.xpath("//div[@id='Assessment']/table/tbody/tr[last()]/td[last()-1]/text()").extract_first()

            except:
                land_value = None
                bldg_value = None
                total_market_value = None


        except:
            print("Search result is empty")


            
            
        print()
        print("Scraping=======>",company)
        print("Owner_Name", owner_name)
        print("Mailing_address", Mailing_address)
        print("mail_city", mail_city)
        print("mail_state", mail_state)
        print("mail_zip", mail_zip)
        print("property_class", property_class)
        print("site_address", site_address)
        print("site_city", site_city)
        print("site_state", site_state)
        print("site_zip", site_zip)
        print("Atucal_year_built", Atucal_year_built)
        print("living_area", living_area)
        print("Bedrooms", Bedrooms)
        print("full_baths", full_baths)
        print("half_baths", half_baths)
        print("sale_date", sale_date)
        print("sale_price", sale_price)
        print("land_value", land_value)
        print("bldg_value", bldg_value)
        print("total_market_value", total_market_value)
        print()
        with open('test.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([company,owner_name,Mailing_address,mail_city,mail_state,mail_zip,property_class,site_address,site_city,site_state,site_zip,land_value,bldg_value,total_market_value,Atucal_year_built,living_area,Bedrooms,full_baths,half_baths,sale_date,sale_price])
            count = count + 1
            print("Data Saved in CSV:",count)

        driver.get(ul)
        time.sleep(10)
            
    
driver.close()
