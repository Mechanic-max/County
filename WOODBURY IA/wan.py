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
import wget

count = 0
with open('test.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["parcel_id","owner_name","site_address","site_city","site_state","site_zip","property_usage","owner_address","owner_city","owner_state","owner_zip","property_type","Atucal_year_built","text_year","living_area","sale_date","sale_price","land_value","bldg_value","total_market_value"])

ul = "https://beacon.schneidercorp.com/Application.aspx?AppID=10&LayerID=108&PageTypeID=2&PageID=204"

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
time.sleep(2)
try:
    driver.find_element_by_xpath("//a[contains(text(),'Agree')]").click()
    time.sleep(2)
except:
    print("Button not Found")

with open("./a.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        search = driver.find_element_by_xpath("//input[@id='ctlBodyPane_ctl04_ctl01_txtParcelID']")
        search.clear()
        time.sleep(1)
        search.send_keys(company)
        search.send_keys(Keys.ENTER)
        time.sleep(5)


        try:
            html = driver.page_source
            resp = Selector(text=html)
            
            parcel_id = resp.xpath("//span[@id='ctlBodyPane_ctl00_ctl01_lblParcelID']/text()").extract_first()
            site_address = resp.xpath("//span[@id='ctlBodyPane_ctl00_ctl01_lblPropertyAddress']/text()[1]").extract_first()
            site_city_state_zip = resp.xpath("//span[@id='ctlBodyPane_ctl00_ctl01_lblPropertyAddress']/text()[2]").extract_first()
            try:
                site_city_state_zip = str(site_city_state_zip)
                site_city = re.findall(r"^[\w\-]+",site_city_state_zip)
                site_state = re.findall(r"\s\w\w\s",site_city_state_zip)
                site_zip = re.findall(r"\d\d\d\d\d",site_city_state_zip)
            except:
                site_city = None
                site_state = None
                site_zip = None
            property_usage = resp.xpath("//span[@id='ctlBodyPane_ctl00_ctl01_lblZone']/text()").extract_first()
            owner_name = resp.xpath("//a[@id='ctlBodyPane_ctl01_ctl01_lstDeed_ctl01_lblDeedName_lnkSearch']/text()").extract_first()
            owner_address = resp.xpath("//a[@id='ctlBodyPane_ctl01_ctl01_lstDeed_ctl01_lnkAddress1']/text()").extract_first()
            owner_city_state_zip = resp.xpath("normalize-space(//span[@id='ctlBodyPane_ctl01_ctl01_lstDeed_ctl01_lblAddress3']/text())").extract_first()
            try:
                owner_city_state_zip = str(owner_city_state_zip)
                owner_city = re.findall(r"^[\w\-]+",owner_city_state_zip)
                owner_state = re.findall(r"\s\w\w\s",owner_city_state_zip)
                owner_zip = re.findall(r"\d\d\d\d\d",owner_city_state_zip)
            except:
                owner_city = None
                owner_state = None
                owner_zip = None
            
            property_type = resp.xpath("//span[@id='ctlBodyPane_ctl03_ctl01_lstResidential_ctl00_lblOccupancy']/text()[1]").extract_first()
            Atucal_year_built = resp.xpath("//span[@id='ctlBodyPane_ctl03_ctl01_lstResidential_ctl00_lblYearBuilt']/text()[1]").extract_first()
            text_year = resp.xpath("//table[@id='ctlBodyPane_ctl09_ctl01_grdValuation']/thead/tr/th[1]/text()").extract_first()
            living_area = resp.xpath("//span[@id='ctlBodyPane_ctl03_ctl01_lstResidential_ctl00_lblGLA']/text()[1]").extract_first()
            sale_date = resp.xpath("//table[@id='ctlBodyPane_ctl07_ctl01_gvwSales']/tbody/tr[1]/th/text()").extract_first()
            sale_price = resp.xpath("//table[@id='ctlBodyPane_ctl07_ctl01_gvwSales']/tbody/tr[1]/td[last()]/text()").extract_first()
            land_value = resp.xpath("//th[contains(text(),'Assessed Land Value')]/following-sibling::td[1]/text()").extract_first()
            bldg_value = resp.xpath("//th[contains(text(),'Assessed Dwelling Value')]/following-sibling::td[1]/text()").extract_first()
            total_market_value = resp.xpath("//th[contains(text(),'Gross Assessed Value')]/following-sibling::td[1]/text()").extract_first()
            
            
            with open('test.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([parcel_id,owner_name,site_address,site_city,site_state,site_zip,property_usage,owner_address,owner_city,owner_state,owner_zip,property_type,Atucal_year_built,text_year,living_area,sale_date,sale_price,land_value,bldg_value,total_market_value])
                count = count + 1
                print("Data Saved in CSV:",count)
        except:
            print("Search results is empty")
            break

        driver.get(ul)
        time.sleep(5)