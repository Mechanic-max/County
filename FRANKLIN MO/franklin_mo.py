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
with open('test.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["paid","parcel_id","owner_name1","owner_name2","situs","texyear","Acct_no"])

ul = "http://collector.franklinmo.net/"
def scrap():
    pages = driver.find_elements_by_xpath("(//table[@border='0'])[last()]//tbody/tr/td/a[not(contains(text(),'...'))]")
    for i in range(0,len(pages)):
        driver.find_elements_by_xpath("(//table[@border='0'])[last()]//tbody/tr/td/a[not(contains(text(),'...'))]")[i].click()
        time.sleep(4)
        html = driver.page_source
        resp = Selector(text=html)
        table = resp.xpath("//table[@id='gvCollSearchNew']/tbody/tr[not(contains(@style,'color:White;background-color:#1C5E55;font-weight:bold;')) and not(contains(@style,'color:White;background-color:#666666;'))]")
        for tbl in table:
            year = tbl.xpath(".//td[2]/span/input[@checked='checked']").get()
            if year:
                paid = True
            else:
                paid = False
            parcel_id = tbl.xpath(".//td[3]/text()").extract_first()
            owner_name1 = tbl.xpath(".//td[4]/text()").extract_first()
            owner_name2 = tbl.xpath(".//td[5]/text()").extract_first()
            situs = tbl.xpath(".//td[6]/text()").extract_first()
            texyear = tbl.xpath(".//td[7]/text()").extract_first()
            Acct_no = tbl.xpath(".//td[14]/text()").extract_first()
            with open('test.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([paid,parcel_id,owner_name1,owner_name2,situs,texyear,Acct_no])
                print("Data Saved in CSV:")

def scrap1():
    html = driver.page_source
    resp = Selector(text=html)
    table = resp.xpath("//table[@id='gvCollSearchNew']/tbody/tr[not(contains(@style,'color:White;background-color:#1C5E55;font-weight:bold;')) and not(contains(@style,'color:White;background-color:#666666;'))]")
    for tbl in table:
        year = tbl.xpath(".//td[2]/span/input[@checked='checked']").get()
        if year:
            paid = True
        else:
            paid = False
        parcel_id = tbl.xpath(".//td[3]/text()").extract_first()
        owner_name1 = tbl.xpath(".//td[4]/text()").extract_first()
        owner_name2 = tbl.xpath(".//td[5]/text()").extract_first()
        situs = tbl.xpath(".//td[6]/text()").extract_first()
        texyear = tbl.xpath(".//td[7]/text()").extract_first()
        Acct_no = tbl.xpath(".//td[14]/text()").extract_first()
        with open('test.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([paid,parcel_id,owner_name1,owner_name2,situs,texyear,Acct_no])
            print("Data Saved in CSV:")

def next_tenpages():
    scrap()
    try:
        driver.find_element_by_xpath("((//table[@border='0'])[last()]//tbody/tr/td/a[(contains(text(),'...'))])[last()]").click()
        time.sleep(4)
        next_tenpages()
    except:
        print("There are no more pages")
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

with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        search = driver.find_element_by_xpath("//input[@id='txtTaxYrCNew']")
        search.clear()
        search.send_keys(company)
        driver.find_element_by_xpath("//input[@id='btnSearchCNew']").click()
        time.sleep(3)
        driver.find_element_by_xpath("//a[contains(text(),'Paid')]").click()
        time.sleep(5)
        scrap1()
        next_tenpages()


driver.close()