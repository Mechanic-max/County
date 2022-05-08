from socket import SIO_LOOPBACK_FAST_PATH
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
ul = "https://williamsoncountytx-web.tylerhost.net/williamsonweb/search/DOCSEARCH149S1"


with open('test.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name","ID","Doc Type","Sale Date"])
with open("input.csv","r") as f:
    data = csv.reader(f)
    for row in data:
        path = which("chromedriver")
        options = Options()
        options.add_experimental_option("detach", True)
        ua = UserAgent()
        userAgent = ua.random
        options.add_argument(f'user-agent={userAgent}')
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(executable_path=path,options=options)
        driver.get(ul)
        time.sleep(3)
        try:
            driver.find_element_by_xpath("//button[@id='submitDisclaimerAccept']").click()
            time.sleep(3)
        except:
            print("Pop up didn't appear")

        time.sleep(2)
        search = driver.find_element_by_xpath("//input[@id='field_BothNamesID']")
        search.send_keys(row[1])
        time.sleep(1)
        search.send_keys(Keys.ENTER)
        search.send_keys(Keys.ENTER)
        time.sleep(3)
        html = driver.page_source
        resp = Selector(text=html)
        data = resp.xpath("//div[@class='selfServiceSearchRowRight']/h1")
        for dat in data:
            record = dat.xpath("normalize-space(.//text())").get()
            record = str(record)
            if "DEED" in record:
                if "DEED OF TRUST" not in record:
                    doc_type = re.findall(r"\s\w\w\w\w\s",record)
                    date = re.findall(r"\d{2}\/\d{2}\/\d{4}",record)
                    with open('test.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([row[1],row[0],doc_type,date])
                        count = count +1
                        print("Data Saved in CSV:",count)
        time.sleep(1)
        driver.close()