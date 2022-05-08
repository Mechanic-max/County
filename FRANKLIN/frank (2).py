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



def scrap():
    html = driver.page_source
    resp = Selector(text=html)

    parcel_ID = resp.xpath("//td[contains(text(),'Parcel ID')]/text()").extract_first()
    year_built = resp.xpath("//td[contains(text(),'Yr Built')]/parent::tr/following-sibling::tr[1]/td[1]/text()").extract_first()
    sale_date  = resp.xpath("//td[contains(text(),'Transfer Date')]/following-sibling::td/text()").extract_first()
    SALE_PRICE = resp.xpath("//td[contains(text(),'Transfer Price')]/following-sibling::td/text()").extract_first()
    Owner_name = resp.xpath("//td[contains(text(),'Owner')]/following-sibling::td/a/text()").extract_first()
    mail_address = resp.xpath("normalize-space(//td[contains(text(),'Owner Mailing')]/following-sibling::td/text())").extract_first()
    city_state_zip = resp.xpath("//td[contains(text(),'Contact Address')]/following-sibling::td/text()").extract_first()
    try:
        city_state_zip = str(city_state_zip)
        mail_city = re.findall(r"^[^\s]+",city_state_zip)
        mail_state = re.findall(r"\s\w\w\s",city_state_zip)
        mail_zip = re.findall(r"\d.*",city_state_zip)
    except:
        mail_city = None
        mail_state = None
        mail_zip = None
    property_type = resp.xpath("//td[contains(text(),'Property Class')]/following-sibling::td/text()").extract_first()
    property_class = resp.xpath("//td[contains(text(),'Land Use')]/following-sibling::td/text()").extract_first()
    site_address = resp.xpath("//td[contains(text(),'Site (Property) Address')]/following-sibling::td/text()").extract_first()
    living_area = resp.xpath("//td[contains(text(),'Sq Ft')]/parent::tr/following-sibling::tr[1]/td[5]/text()").extract_first()
    if living_area:
        baths = None
        bedroms = None
    else:
        living_area = resp.xpath("//td[contains(text(),'Tot Fin Area')]/parent::tr/following-sibling::tr[1]/td[2]/text()").extract_first()
        bedroms = resp.xpath("//td[contains(text(),'Tot Fin Area')]/parent::tr/following-sibling::tr[1]/td[4]/text()").extract_first()
        baths = resp.xpath("//td[contains(text(),'Tot Fin Area')]/parent::tr/following-sibling::tr[1]/td[5]/text()").extract_first()
    land_value = resp.xpath("//table[@id='2020 Auditor']//tr/td[contains(text(),'Total')and @class='DataletData']/following-sibling::td[1]/text()").extract_first()
    bldg_value = resp.xpath("//table[@id='2020 Auditor']//tr/td[contains(text(),'Total')and @class='DataletData']/following-sibling::td[2]/text()").extract_first()
    total_accessed_value  = resp.xpath("//table[@id='2020 Auditor']//tr/td[contains(text(),'Total')and @class='DataletData']/following-sibling::td[3]/text()").extract_first()
    with open('test.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([parcel_ID,year_built,sale_date,SALE_PRICE,Owner_name,mail_address,mail_city,mail_state,mail_zip,property_type,property_class,site_address,living_area,baths,bedroms,land_value,bldg_value,total_accessed_value])

count = 0
with open('test.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["parcel_ID","year_built","sale_date","SALE_PRICE","Owner_name","mail_address","mail_city","mail_state","mail_zip","property_type","property_class","site_address","living_area","baths","bedroms","land_value","bldg_value","total_accessed_value"])

ul = "https://property.franklincountyauditor.com/_web/search/commonsearch.aspx?mode=address"



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

with open("./input1.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        search1 = driver.find_element_by_xpath("//input[@id='inpNumber']")
        search1.clear()
        search1.send_keys(i[0]) 
        time.sleep(2)
        search = driver.find_element_by_xpath("//input[@id='inpStreet']")
        search.clear()
        search.send_keys(i[1]) 
        time.sleep(1)
        search.send_keys(Keys.ENTER)
        time.sleep(4)
        count = count +1
        print("Data saved in CSV: ",count)
        try:
            results = driver.find_elements_by_xpath("//tr[@class='SearchResults']")
            if results == []:
                scrap()
            else:
                for i in range(0,len(results)):
                    result = driver.find_elements_by_xpath("//tr[@class='SearchResults']")[i].click()
                    time.sleep(3)
                    scrap()
                    driver.back()
                    time.sleep(3)
        except:
            results = None

        driver.get(ul)
        time.sleep(3)
