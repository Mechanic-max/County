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
ul = "file:///C:/Users/Nabeel/Downloads/JAMES%20CITY%20COUNTY%20VA%20DELINQUENT%20TAX%20REPORT%20DOWNLOAD.html"

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

html = driver.page_source
resp = Selector(text=html)

parcel_ids = resp.xpath("//tr")
for i in parcel_ids:
    Name = i.xpath(".//td[contains(@class,' td23') and not(contains(@class,'tr td23'))]/p[1]/text()").extract_first()
    Name = str(Name)
    parcel_id = re.findall(r"\d.*",Name)
    # print(parcel_id)
    with open('input.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([parcel_id])
        count = count + 1
        print("Data Saved in CSV:",count)
driver.close()