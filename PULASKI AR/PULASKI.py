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

# with open('owner.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(["Acc No","Owner 1","Date","Owner 2","Date"])
def scrap():
    html = driver.page_source
    resp = Selector(text=html)
    table_data = resp.xpath("//table[@id='HdrTbl1']//tr[@class]")
    for table_dat in table_data:
        parcel_id = table_dat.xpath(".//td[1]/text()").extract_first()
        Name = table_dat.xpath(".//td[2]/text()").extract_first()
        total = table_dat.xpath(".//td[3]/text()").extract_first()
        print(parcel_id,Name,total)

def next_result():
    scrap()
    try:
        pages = driver.find_elements_by_xpath("//div[@id='Over0']/table//a")
        for i in range(0,len(pages)):
            pag = driver.find_elements_by_xpath("//div[@id='Over0']/table//a")[i].click()
            time.sleep(2)
            next_result()
    except:
        print("cannot click next page")

def nxt_pages():
    next_result()
    try:
        driver.find_element_by_xpath("//div[@id='Over0']/table//td/input").click()
        time.sleep(2)
        nxt_pages()
    except:
        print("There is nothing more to scrap")

count = 0
ul = "https://public.pulaskicountytreasurer.net/"
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
time.sleep(10)
with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        try:
            try:
                time.sleep(10)
                search = driver.find_element_by_xpath("(//input[@class='x'])[2]")
                search.send_keys(company)
                time.sleep(1)
                select = Select(driver.find_element_by_xpath("//select[@name='P_3']"))
                select.select_by_visible_text('Real Estate Taxes - (General Taxes)')
                time.sleep(1)
                driver.find_element_by_xpath("//button[@value='Search Delinquents']").click()
                time.sleep(2)
                nxt_pages()




                # with open('owner.csv', 'a', newline='') as file:
                #     writer = csv.writer(file)
                #     writer.writerow([company,previous_owner1,date1,previous_owner2,date2])
                #     count = count + 1
                #     print("Data Saved in CSV",count)
            except:
                print("Search result is empty")

        except:
            print("Cannot click Delinquent Inquiry")

driver.close()