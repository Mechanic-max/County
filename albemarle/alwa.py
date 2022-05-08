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

ul = "https://gisweb.albemarle.org/gpv_51/Viewer.aspx#"
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
with open('albemarle.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Parcel ID","Site Address","Description","Owner","address","Zip Code","Land Value", "Improvements value", "Total Value","Sale Date","Sale Price","Card Level Use Code","Year Built","Living Area(SQFT)"])

with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        pin_btn = driver.find_element_by_xpath("//li[@id='tabSearch']/a")
        pin_btn.click()
        time.sleep(1)
        search = driver.find_element_by_xpath("//input[@name='ucSearchPanel$ctl27']")
        time.sleep(3)
        search.clear()
        search.send_keys(company)
        search.send_keys(Keys.ENTER)
        time.sleep(5)

        try:
            select = Select(driver.find_element_by_xpath("//select[@id='ddlDataTheme']"))
            select.select_by_index(0)
            time.sleep(5)


            html = driver.page_source
            resp = Selector(text=html)

            parcel_id = resp.xpath("(//div[@class='Value'])[1]/text()").get()
            previous_property_address = resp.xpath("(//div[@class='Value'])[2]/text()").get()
            description = resp.xpath("(//div[@class='Value'])[6]/text()").get()
            owner = resp.xpath("(//div[@class='Value'])[10]/text()").extract_first()
            address = resp.xpath("normalize-space((//div[@class='ValueSet'])[11]/div[@class='Value']/text())").extract_first()
            address = str(address)

            state = re.findall(r".?.?,", address)
            state = str(state)
            add = re.findall(r".*?,", address)
            add = str(add)
            add = add.replace(state, '')
            state = state.replace(",", '')
            zip_code = re.findall(r"[^,]*$", address)
            
            land_value = resp.xpath("(//div[@class='Value'])[15]/text()").extract_first()
            improvements_value = resp.xpath("(//div[@class='Value'])[17]/text()").extract_first()
            total_value = resp.xpath("(//div[@class='Value'])[18]/text()").extract_first()

            sale_date = resp.xpath("(//div[@class='Value'])[21]/text()").extract_first()
            sale_price = resp.xpath("(//div[@class='Value'])[22]/text()").extract_first()


            select = Select(driver.find_element_by_xpath("//select[@id='ddlDataTheme']"))
            select.select_by_index(1)
            time.sleep(5)

            html = driver.page_source
            resp = Selector(text=html)

            card_level_use_code = resp.xpath("((//div[contains(text(),'Primary Building Details')])[2]/parent::*/div[@class='ValueSet'])[1]/div[@class='Value']/text()").extract_first()
            year_built = resp.xpath("((//div[contains(text(),'Primary Building Details')])[2]/parent::*/div[@class='ValueSet'])[2]/div[@class='Value']/text()").extract_first()
            finshed_sq_root = resp.xpath("((//div[contains(text(),'Primary Building Details')])[2]/parent::*/div[@class='ValueSet'])[8]/div[@class='Value']/text()").extract_first()

            with open('albemarle.csv', 'a',newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([parcel_id,previous_property_address,description,owner,add,zip_code,land_value,improvements_value,total_value,sale_date,sale_price,card_level_use_code,year_built,finshed_sq_root])
                        print("Data Saved in CSV :")
        except:
            driver.get(ul)
            time.sleep(2)