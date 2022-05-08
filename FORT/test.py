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
ul = "http://ccweb.co.fort-bend.tx.us/RealEstate/SearchEntry.aspx"
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
driver.get(ul)
time.sleep(2)
with open('ober.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name","Doc Type","Sale Date","ID"])
with open("input.csv","r") as f:
    data = csv.reader(f)
    for row in data:
        search = driver.find_element_by_xpath("//input[@id='cphNoMargin_f_txtParty']")
        search.send_keys(row[0])
        search1 = driver.find_element_by_xpath("//input[@id='cphNoMargin_f_txtLDLot']")
        search1.send_keys(row[1])
        search2 = driver.find_element_by_xpath("//input[@id='cphNoMargin_f_txtLDBook']")
        search2.send_keys(row[2])
        search.send_keys(Keys.ENTER)
        time.sleep(2)
        try:
            html = driver.page_source
            resp = Selector(text=html)
            doc_types = resp.xpath("//td[contains(text(),'DEED') and not(contains(text(),'DEED OF TRUST'))]")
            for doc in doc_types:
                a = doc.xpath(".//text()").extract_first()
                b = doc.xpath(".//preceding-sibling::td[contains(text(),'/')]/text()").extract_first()
                with open('ober.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([row[0],a,b,row[3]])
                    count = count + 1 
                    print("Data Saved in CSV:",count)
            doc_types = resp.xpath("//td[contains(text(),'WD')]")
            for doc in doc_types:
                a = doc.xpath(".//text()").extract_first()
                b = doc.xpath(".//preceding-sibling::td[contains(text(),'/')]/text()").extract_first()
                with open('ober.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([row[0],a,b,row[3]])
                    count = count + 1 
                    print("Data Saved in CSV:",count)
            doc_types = resp.xpath("//td[contains(text(),'QCD')]")
            for doc in doc_types:
                a = doc.xpath(".//text()").extract_first()
                b = doc.xpath(".//preceding-sibling::td[contains(text(),'/')]/text()").extract_first()
                with open('ober.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([row[0],a,b,row[3]])
                    count = count + 1 
                    print("Data Saved in CSV:",count)
        except:
            print("Search result is empty")
        driver.get(ul)
        time.sleep(3)

