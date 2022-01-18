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
# with open('Sharp.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(["Parcel ID","owner_name","site_address","city","state","zip","mail_address","m_city","m_state","m_zip","sale_date","sale_price","land_value","bldg_value","total_accessed_value","living_area","property_type","built_year","baths"])

ul = "https://maps.indy.gov/AssessorPropertyCards/"



path = which("chromedriver")
options = Options()
options.add_experimental_option("detach", True)
#options.add_argument("--headless")
ua = UserAgent()
userAgent = ua.random
userAgent = ua.random
options.add_argument(f'user-agent={userAgent}')
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(executable_path=path,options=options)
driver.get(ul)
time.sleep(10)

try:
    driver.find_element_by_xpath("//div[@class='mblSimpleDialogCloseBtn mblDomButtonSilverCircleRedCross mblDomButton']").click()
    time.sleep(3)
except:
    print("pop up didn't appear")

driver.find_element_by_xpath("//li[@id='AddressListItem']").click()
time.sleep(3)
with open("./Indiannapolis Code viol- 3-10-2021.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        try:
            
            
            company1 = str(i[3])
            company1 = company1.strip()
            search = driver.find_element_by_xpath("//input[@id='geocoder']")
            search.send_keys(Keys.CONTROL + "a")
            search.send_keys(Keys.DELETE)
            time.sleep(1)
            search.send_keys(company1)
            time.sleep(2)
            search.send_keys(Keys.ENTER)
            time.sleep(5)
            try:
                driver.find_element_by_xpath("//div[@class='mblScrollableViewContainer unselectable']").click()
                time.sleep(3)
                driver.find_element_by_xpath("//div[contains(text(),'Click to see property card')]/parent::li").click()
                time.sleep(3)
                print(f"Downloading Pdf ====>{company1}")
            except:
                print("li pa click nai ho raha")



        except:
            None
            break
# Date,Case Number,Address,Address,,Case Type,Status



