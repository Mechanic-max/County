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
    writer.writerow(["year","Bill ID","owner_name","Address","total_amount_due","Status"])

ul = "https://paymadisontaxes.com/taxes.html#/WildfireSearch"
def scrap():
    html = driver.page_source
    resp = Selector(text=html)
    table = resp.xpath("//tr[@class='ng-scope']")
    for tbl in table:
        year = tbl.xpath(".//td[1]/text()").extract_first()
        bill_id = tbl.xpath(".//td[2]/text()").extract_first()
        owner_name = tbl.xpath(".//td[3]/text()").extract_first()
        address = tbl.xpath(".//td[3]/small/text()").extract_first()
        total_amount_due = tbl.xpath(".//td[4]/text()").extract_first()
        status = tbl.xpath("normalize-space(.//td[6]/span/text())").get()
        with open('test.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([year,bill_id,owner_name,address,total_amount_due,status])
            print("Data Saved in CSV:")

def next_page():
    scrap()
    try:
        driver.find_element_by_xpath("//a[@title='Next Page']").click()
        time.sleep(4)
        next_page()
    except:
        print("There is no more pages")


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
try:
    driver.find_element_by_xpath("//button[@class='btn btn-info']").click()
    time.sleep(2)
except:
    print("Pop up didn't appear")

with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        search = driver.find_element_by_xpath("//input[@id='searchBox']")
        search.clear()
        search.send_keys(company)
        driver.find_element_by_xpath("//span[@class='input-group-btn']/button").click()
        time.sleep(3)
        driver.find_element_by_xpath("//b[contains(text(),'Unpaid')]/parent::label/input").click()
        driver.find_element_by_xpath("//b[contains(text(),'Real')]/parent::label/input").click()
        driver.find_element_by_xpath("//b[contains(text(),'2020')]/parent::label/input").click()
        driver.find_element_by_xpath("//b[contains(text(),'2019')]/parent::label/input").click()
        driver.find_element_by_xpath("//b[contains(text(),'2018')]/parent::label/input").click()
        driver.find_element_by_xpath("//b[contains(text(),'2017')]/parent::label/input").click()
        time.sleep(5)
        next_page()
# driver.find_element_by_xpath("//span[@class='radiocheckmark']").click()


# time.sleep(3)
# driver.find_element_by_xpath("//span[@class='checkmark']").click()
# time.sleep(3)
# driver.find_element_by_xpath("//select[@name='tms_datatable_length']/option[@value='100']").click()
# time.sleep(3)
