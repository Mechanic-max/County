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
    writer.writerow(["Parcel ID","owner_name","site_address","site_city","land_value","bldg_value","total_market_value","property_type","Atucal_year_built","living_area","sale_date","sale_price"])

ul = "https://clay.iowaassessors.com/search.php"

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
time.sleep(2)

with open('input.txt','r') as f:
    lines = f.readlines()
    for line in lines:
        company = line.strip()
        search = driver.find_element_by_xpath("//input[@id='iparcelNumber']")
        search.clear()
        time.sleep(1)
        search.send_keys(company)
        search.send_keys(Keys.ENTER)
        time.sleep(5)

        html = driver.page_source
        resp = Selector(text=html)

        owner_name = resp.xpath("normalize-space(//td[contains(text(),'Deed Holder:')]/following-sibling::td/text())").extract_first()
        site_address = resp.xpath("normalize-space(//td[contains(text(),'Property Address:')]/following-sibling::td/text()[1])").extract_first()
        site_city = resp.xpath("normalize-space(//td[contains(text(),'Property Address:')]/following-sibling::td/text()[2])").extract_first()
        land_value = resp.xpath("//th[contains(text(),'Land')]/parent::tr/following-sibling::tr/td[1]/text()").extract_first()
        bldg_value = resp.xpath("//th[contains(text(),'Land')]/parent::tr/following-sibling::tr/td[2]/text()").extract_first()
        total_market_value = resp.xpath("//th[contains(text(),'Land')]/parent::tr/following-sibling::tr/td[3]/text()").extract_first()
        property_type = resp.xpath("//img[@id='res0img']/parent::div/text()").extract_first()
        Atucal_year_built = resp.xpath("//img[@id='res0img']/parent::div/following-sibling::div[2]/text()").extract_first()
        living_area = resp.xpath("//img[@id='res0img']/parent::div/following-sibling::div[3]/text()").extract_first()
        sale_date = resp.xpath("(//div[@id='sale0']/div/text())[1]").extract_first()
        sale_price = resp.xpath("(//div[@id='sale0']/div/text())[2]").extract_first()
        with open('test.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([company,owner_name,site_address,site_city,land_value,bldg_value,total_market_value,property_type,Atucal_year_built,living_area,sale_date,sale_price])
            count = count + 1
            print("Data Saved in CSV:",count)

        driver.get(ul)
        time.sleep(2)
            
    
driver.close()
