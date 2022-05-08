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
ul = "https://obrien.iowaassessors.com/search.php"
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
with open('ober.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Parcel ID","Sale Date"])

try:
    driver.find_element_by_xpath("//input[contains(@value,'Yes, I Agree')]").click()
    time.sleep(3)
except:
    print("Pop up didn't appear")


with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        if len(company) == 4:
            company = str(company)
            company = f"000000{company}"
        elif len(company) == 5:
            company = str(company)
            company = f"00000{company}"
        elif len(company) == 6:
            company = str(company)
            company = f"0000{company}"
        elif len(company) == 7:
            company = str(company)
            company = f"000{company}"
        elif len(company) == 8:
            company = str(company)
            company = f"00{company}"
        else:
            company = company
        search = driver.find_element_by_xpath("//input[@id='iparcelNumber']")
        time.sleep(3)
        search.clear()
        search.send_keys(company)
        search.send_keys(Keys.ENTER)
        time.sleep(5)
        try:

            html = driver.page_source
            resp = Selector(text=html)

            
            Parcel_id = resp.xpath("//td[contains(text(),'Parcel Number')]/following-sibling::td/text()").extract_first()
            sale_date = resp.xpath("//div[@id='sale0']/div[@class='saleColumn']/text()").extract_first()
            

                  

            with open('ober.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([Parcel_id,sale_date])
                count = count + 1 
                print("Data Saved in CSV:",count)
            driver.get(ul)
            time.sleep(3) 
        except:
            print("Search Result is empty")
            driver.get(ul)
            time.sleep(3) 
        

driver.close()