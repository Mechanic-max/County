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

ul = "https://oktaxrolls.com/searchTaxRoll/Comanche"
def scrap():
    html = driver.page_source
    resp = Selector(text=html)
    table = resp.xpath("//tr[@class='odd' or @class='even']")
    for tbl in table:
        year = tbl.xpath(".//td[@class='sorting_1 dtr-control']/text()").extract_first()
        owner_name = tbl.xpath(".//td/a/text()").extract_first()
        parcel_id = tbl.xpath(".//td[4]/text()").extract_first()
        typ = tbl.xpath(".//td[5]/text()").get()
        total_amount_due = tbl.xpath(".//td[7]/text()").extract_first()
        print(year,owner_name,parcel_id,typ,total_amount_due)

def next_page():
    scrap()
    try:
        next_pg = driver.find_element_by_xpath("//a[contains(text(),'Next')]")
        next_pg.click()
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

driver.find_element_by_xpath("//select[@class='from-year']/option[@id='allyearsfrom']").click()
driver.find_element_by_xpath("//span[@class='radiocheckmark']").click()
search = driver.find_element_by_xpath("//input[@id='business_owner_name']")
search.send_keys("A")
search.send_keys(Keys.ENTER)
time.sleep(3)
driver.find_element_by_xpath("//span[@class='checkmark']").click()
time.sleep(3)
driver.find_element_by_xpath("//select[@name='tms_datatable_length']/option[@value='100']").click()
time.sleep(3)
next_page()