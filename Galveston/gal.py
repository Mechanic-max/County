from typing import Text
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

ul = "https://ava.fidlar.com/txgalveston/avaweb/#!/search"



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
time.sleep(5)

with open("./input.csv", 'r') as input_file:
    try:
        reader = csv.reader(input_file,delimiter=",")
        for i in reader:
            search1 = driver.find_element_by_xpath("//input[@id='last-name']")
            search1.clear()
            search = driver.find_element_by_xpath("//input[@id='docnumber']")
            search.clear()
            search.send_keys(i[0])        
            time.sleep(1)
            search.send_keys(Keys.ENTER)
            time.sleep(15)
            try:
                btn = driver.find_element_by_xpath("//button[@class='btn btn-custom' and contains(text(),'OK')]").click()
                time.sleep(3)
                search = driver.find_element_by_xpath("//input[@id='docnumber']")
                search.clear()
                time.sleep(2)
                search1 = driver.find_element_by_xpath("//input[@id='last-name']")
                search1.clear()
                search1.send_keys(i[1])        
                time.sleep(1)
                search1.send_keys(Keys.ENTER)
                time.sleep(15)
            except:
                btn = None


            html = driver.page_source
            resp = Selector(text=html)
            doc = resp.xpath("//label[@class='span2 resultHeaderText trim-info ng-binding' and contains(text(),'DEED')]")
            for d in doc:
                doc_type = d.xpath(".//text()").extract_first()
                date = d.xpath(".//following-sibling::label[1]/text()").extract_first()
                scraped_id = d.xpath(".//preceding-sibling::label/text()").extract_first()
                scraped_name = d.xpath(".//following-sibling::label[2]/text()").extract_first()
                with open('test.csv','a',newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([i[0],i[1],doc_type,date,scraped_id,scraped_name])
                    count = count + 1
                    print("Data saved in CSV: ",count)
            driver.get(ul)
            time.sleep(4)
    except:
        driver.get(ul)
        time.sleep(10)
