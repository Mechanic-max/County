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
ul = "file:///C:/Users/nabeel/Desktop/c7bbccc6-d2ab-11eb-a980-0cc47a792c0a_id_c7bbccc6-d2ab-11eb-a980-0cc47a792c0a.html"

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

parcel_ids = resp.xpath("//div[contains(@style,'position:absolute;left:10')]/span")
for i in parcel_ids:
    Name = i.xpath(".//text()").extract_first()
    with open('input2.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([Name])
        count = count + 1
        print("Data Saved in CSV:",count)
driver.close()