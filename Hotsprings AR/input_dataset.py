

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
ul = "file:///E:/projects/Working/Hotsprings%20AR/Hotsprings%20AR%2001-01-2020%20-%20current%20CaseListingReport.html"


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

html = driver.page_source
resp = Selector(text=html)

add = resp.xpath("//p[contains(text(),'HOT SPRINGS') or contains(text(),' AR ')]")
for address in add:
    searching_address = address.xpath(".//text()").extract_first()
    with open('input.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([searching_address])
        count = count + 1
        print("Data saved in CSV: ",count)


driver.close()

