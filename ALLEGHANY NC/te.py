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
# with open('test.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(["Last Name","First Name","Full Name","Input Parcel_ID","Input Price","land_use","Scraped parcel_id","account_no","owner_name","bldg_value","land_value","total_market_value","built_year","site_address","use_code_description","lving_area","sale_date","sale_price","owner_name1","owner_address1","owner_name2","owner_address2"])

ul = "https://www.webgis.net/nc/alleghany/"

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
time.sleep(10)

with open("input.csv","r") as f:
    data = csv.reader(f)
    for row in data:
        search = driver.find_element_by_xpath("//input[@id='searchParcelOwner']")
        search.clear()
        search.send_keys(row[0])
        time.sleep(1)
        search.send_keys(Keys.ENTER)
        time.sleep(10)
        try:
            results = driver.find_elements_by_xpath("//div[@class='dgrid-content ui-widget-content']/div/table/tr/td[1]")
            for i in range(0,len(results)):
                driver.find_elements_by_xpath("//div[@class='dgrid-content ui-widget-content']/div/table/tr/td[1]")[i].click()
                time.sleep(10)
                html = driver.page_source
                resp = Selector(text=html)

                pin = resp.xpath("//span[contains(text(),'PIN:')]/following-sibling::span[1]/text()").extract_first()
                owner_name = resp.xpath("//span[contains(text(),'Owner:')]/following-sibling::span[1]/text()").extract_first()
                
                with open('test.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([pin,owner_name])
                    count = count + 1
                    print("Data Saved in CSV:",count) 

                driver.find_element_by_xpath("//a[@id='resultsPanelCtrlBtn']").click()
                time.sleep(3)
            
            driver.find_element_by_xpath("//button[@id='searchButton']").click()
            time.sleep(7)

        except:
            print("Search is empty")
            driver.get(ul)
            time.sleep(10)
        
