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

with open('owner.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Acc No","Owner 1","Date","Owner 2","Date"])

count = 0
ul = ""
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
with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        company = str(company)
        if len(company) == 4:
            company = f"0000{company}"
        elif len(company) == 5:
            company = f"000{company}"
        elif len(company) == 6:
            company = f"00{company}"
        elif len(company) == 7:
            company = f"0{company}"
        else:
            company = company
        ul = f"https://www.tad.org/property/{company}/"
        try:
            driver.get(ul)
            time.sleep(1)
            html = driver.page_source
            resp = Selector(text=html)
            previous_owner1 = resp.xpath("(//tr/td[@data-label='Name'])[1]/text()").extract_first()
            date1 = resp.xpath("(//tr/td[@data-label='Date'])[1]/text()").extract_first()
            previous_owner2 = resp.xpath("(//tr/td[@data-label='Name'])[2]/text()").extract_first()
            date2 = resp.xpath("(//tr/td[@data-label='Date'])[2]/text()").extract_first()
            with open('owner.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([company,previous_owner1,date1,previous_owner2,date2])
                count = count + 1
                print("Data Saved in CSV",count)
        except:
            print("Search result is empty")



driver.close()