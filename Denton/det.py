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
ul = "https://denton.tx.publicsearch.us/"
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
time.sleep(7)
with open('ober.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Grantor","Doc Type","Sale Date"])




with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        company = str(company)
        company = company.strip()
        search = driver.find_element_by_xpath("//input[@class='basic-search__search-term']")
        time.sleep(3)
        search.clear()
        search.send_keys(company)
        search.send_keys(Keys.ENTER)
        time.sleep(5)
        try:

            html = driver.page_source
            resp = Selector(text=html)
            doc_link = resp.xpath("//span[contains(text(),'DEED')]")
            for doc in doc_link:
                a =  doc.xpath(".//text()").extract_first()
                b = doc.xpath(".//parent::td/following-sibling::td[1]/span/text()").extract_first()
                with open('ober.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([company,a,b])
                    count = count + 1 
                    print("Data Saved in CSV:",count)
            
            doc_link1 = resp.xpath("//span[contains(text(),'W/D')]")
            if doc_link1:
                for doc in doc_link1:
                    a =  doc.xpath(".//text()").extract_first()
                    b = doc.xpath(".//parent::td/following-sibling::td[1]/span/text()").extract_first()
                    with open('ober.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([company,a,b])
                        count = count + 1 
                        print("Data Saved in CSV:",count)
            
            doc_link2 = resp.xpath("//span[contains(text(),'QCD')]")
            if doc_link2:
                for doc in doc_link2:
                    a =  doc.xpath(".//text()").extract_first()
                    b = doc.xpath(".//parent::td/following-sibling::td[1]/span/text()").extract_first()
                    with open('ober.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([company,a,b])
                        count = count + 1 
                        print("Data Saved in CSV:",count)


            
        except:
            print("Search Result is empty")
            
        driver.get(ul)
        time.sleep(3) 

driver.close()