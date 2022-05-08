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

with open('test.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["owner_name","year","Address","Account"])

def scrap(html):
    resp = Selector(text=html)
    table_data = resp.xpath("//tr[@class='ng-scope']")
    for tb in table_data:
        owner_name = tb.xpath("(.//td[@class='hidden-xs ng-binding'])[1]/text()").extract_first()
        year = tb.xpath("(.//td[@class='hidden-xs ng-binding'])[2]/text()").extract_first()
        Address = tb.xpath(".//td[@class='hidden-xs ng-binding'][3]/text()").extract_first()
        Account = tb.xpath(".//td[@class='ng-binding'][2]/text()").extract_first()
        with open('test.csv', '+a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([owner_name,year,Address,Account])
            print("Data Saved in CSV")

def nextPage():
    html = driver.page_source
    scrap(html)
    try:
        last_pg = driver.find_element_by_xpath("(//li[@class='pagination-next ng-scope disabled'])[1]")
    except:
        last_pg = None
    if last_pg == None:
        try:
            driver.find_element_by_xpath("(//a[@title='Next Page'])[1]").click()
            time.sleep(7)
            nextPage()
        except:
            print("cannot click more next pages")
count = 0
ul = "https://rcchancery.com/payments/delinquent-taxes.html#/WildfireSearch"
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
time.sleep(4)
try:
    driver.find_element_by_xpath("(//button[@class='btn btn-primary'])[1]").click()
    time.sleep(3)
except:
    print("Pop up didn't appear")

with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        search = driver.find_element_by_xpath("(//input[@id='searchBox'])[1]")
        time.sleep(1)
        search.clear()
        search.send_keys(company)
        time.sleep(2)
        search.send_keys(Keys.ENTER)


        try:
            time.sleep(8)
            driver.find_element_by_xpath("//b[contains(text(),'Unpaid')]/preceding-sibling::input").click()
            driver.find_element_by_xpath("//b[contains(text(),'Real Property')]/preceding-sibling::input").click()
            driver.find_element_by_xpath("//b[contains(text(),'2019')]/preceding-sibling::input").click()
            driver.find_element_by_xpath("//b[contains(text(),'2018')]/preceding-sibling::input").click()
            driver.find_element_by_xpath("//b[contains(text(),'2017')]/preceding-sibling::input").click()
            driver.find_element_by_xpath("//b[contains(text(),'2016')]/preceding-sibling::input").click()
            time.sleep(10)
            nextPage()
        except:
            print("Cannot click radio button")

        
        driver.get(ul)
        time.sleep(3) 
        
driver.close()