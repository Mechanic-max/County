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
ul = "https://tccsearch.org/RealEstate/SearchEntry.aspx"
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
time.sleep(6)

try:
    driver.find_element_by_xpath("//a[contains(text(),'Click here to acknowledge the disclaimer and enter the site.')]").click()
    time.sleep(3)
except:
    print("Pop didn't appear")
with open('test.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name","Doc_type","Date","Associated Name","ID"])


with open("./input.csv", 'r') as input_file:
    reader = csv.reader(input_file, delimiter=",")
    for i in reader:
        search = driver.find_element_by_xpath("//input[@id='cphNoMargin_f_txtParty']")
        time.sleep(3)
        search.clear()
        search.send_keys(i[0])
        search.send_keys(Keys.ENTER)
        time.sleep(4)
        try:
            html = driver.page_source
            resp = Selector(text=html)
            doc_types = resp.xpath("//td[@class='igede12b91' and contains(text(),'DEED')]")
            for doc in doc_types:
                a = doc.xpath(".//text()").extract_first()
                b = doc.xpath(".//preceding-sibling::td[contains(text(),'/')]/text()").extract_first()
                c = doc.xpath(".//following-sibling::td[1]/span[2]/text()").extract_first()
                with open('test.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([i[0],a,b,c,i[1]])
                    count = count + 1
                    print("Data Saved in CSV",count)
            
            doc_1 = resp.xpath("//td[@class='igede12b91' and contains(text(),'QCD')]")
            if doc_1:
                for doc in doc_1:
                    a = doc.xpath(".//text()").extract_first()
                    b = doc.xpath("./preceding-sibling::td[contains(text(),'/')]/text()").extract_first()
                    c = doc.xpath(".//following-sibling::td[1]/span[2]/text()").extract_first()
                    with open('test.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([i[0],a,b,c,i[1]])
                        count = count + 1
                        print("Data Saved in CSV",count)
            
            doc_2 = resp.xpath("//td[@class='igede12b91' and contains(text(),'QCD')]")
            if doc_2:
                for doc in doc_2:
                    a = doc.xpath(".//text()").extract_first()
                    b = doc.xpath("./preceding-sibling::td[contains(text(),'/')]/text()").extract_first()
                    c = doc.xpath(".//following-sibling::td[1]/span[2]/text()").extract_first()
                    with open('test.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([i[0],a,b,c,i[1]])
                        count = count + 1
                        print("Data Saved in CSV",count)
            
        except:
            print("Search result is empty")
        driver.get(ul)
        time.sleep(5)
        