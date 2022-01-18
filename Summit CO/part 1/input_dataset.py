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
ul = "https://s3.pdfconvertonline.com/convert/p3r68-cdx67/klvmr-q8sft.html"


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

add = resp.xpath("//tr")
for address in add:
    id = address.xpath(".//td[@style='border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000']/b/font/text()").extract_first()
    sie_address = address.xpath(".//font[contains(text(),'SITE ADDRESS:')]/text()").extract_first()
    date = address.xpath(".//font[contains(text(),'OPENED:')]/text()").extract_first()
    status = address.xpath(".//font[contains(text(),'STATUS:')]/text()").extract_first()
    OFFICER = address.xpath(".//font[contains(text(),'OFFICER:')]/text()").extract_first()
    SUBTYPE = address.xpath(".//font[contains(text(),'SUBTYPE:')]/text()").extract_first()
    SITE_APN = address.xpath(".//font[contains(text(),'SITE APN:')]/text()").extract_first()

    print()
    print("ID",id)
    print("sie_address",sie_address)
    print("date",date)
    print("status",status)
    print("OFFICER",OFFICER)
    print("SUBTYPE",SUBTYPE)
    print("SITE_APN",SITE_APN)
    print()
    with open('input.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([id,sie_address,date,status,OFFICER,SUBTYPE,SITE_APN])
        count = count + 1
        print("Data saved in CSV: ",count)


driver.close()
