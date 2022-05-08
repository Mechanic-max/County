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
    writer.writerow(["Parcel ID","owner_name","site_address","site_city","mail_address","mail_city","mail_state","mail_zip","land_value","bldg_value","total_market_value","property_type","Atucal_year_built","living_area","above_rooms","below_rooms","baths","sale_date","sale_price"])

ul = "https://beacon.schneidercorp.com/Application.aspx?AppID=408&LayerID=6228&PageTypeID=2&PageID=3318"

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
    time.sleep(3)
except:
    print("Pop up didn't appear")

with open("input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        search = driver.find_element_by_xpath("//input[@id='ctlBodyPane_ctl04_ctl01_txtParcelID']")
        search.clear()
        time.sleep(1)
        company = str(company)
        if len(company) == 11:
            company = f"0{company}"
        search.send_keys(company)
        search.send_keys(Keys.ENTER)
        time.sleep(5)
        
        try:
            html = driver.page_source
            resp = Selector(text=html)

            owner_name = resp.xpath("normalize-space(//a[@id='ctlBodyPane_ctl01_ctl01_lnkDeedName_lnkSearch']/text())").extract_first()
            site_address = resp.xpath("normalize-space(//span[@id='ctlBodyPane_ctl00_ctl01_lblPropertyAddress']/text()[1])").extract_first()
            site_city = resp.xpath("normalize-space(//span[@id='ctlBodyPane_ctl00_ctl01_lblPropertyAddress']/text()[2])").extract_first()
            mail_address = resp.xpath("normalize-space(//span[@id='ctlBodyPane_ctl01_ctl01_lblDeedAddress']/text()[1])").extract_first()
            mail_city_state_zip = resp.xpath("normalize-space(//span[@id='ctlBodyPane_ctl01_ctl01_lblDeedAddress']/text()[2])").extract_first()
            try:
                mail_city_state_zip = str(mail_city_state_zip)
                mail_city = re.findall(r"^.*[A-Z]",mail_city_state_zip)
                mail_state = re.findall(r"\s\w\w\s",mail_city_state_zip)
                mail_zip = re.findall(r"\d\d\d\d\d",mail_city_state_zip)
            except:
                mail_city = None
                mail_state = None
                mail_zip = None

            property_type = resp.xpath("//span[@id='ctlBodyPane_ctl03_ctl01_lstResidential_ctl00_lblOccupancy']/text()").extract_first()
            Atucal_year_built = resp.xpath("//span[@id='ctlBodyPane_ctl03_ctl01_lstResidential_ctl00_lblYearBuilt']/text()").extract_first()
            living_area = resp.xpath("//span[@id='ctlBodyPane_ctl03_ctl01_lstResidential_ctl00_lblGLA']/text()").extract_first()
            above_rooms = resp.xpath("//span[@id='ctlBodyPane_ctl03_ctl01_lstResidential_ctl00_lblRoomAboveCount']/text()").extract_first()
            below_rooms = resp.xpath("//span[@id='ctlBodyPane_ctl03_ctl01_lstResidential_ctl00_lblRoomBelowCount']/text()").extract_first()
            baths = resp.xpath("//span[@id='ctlBodyPane_ctl03_ctl01_lstResidential_ctl00_lblPlumbing']/text()").extract_first()

            land_value = resp.xpath("//table[@id='ctlBodyPane_ctl09_ctl01_grdValuation']/tbody/tr[2]/td[2]/text()").extract_first()
            bldg_value = resp.xpath("//table[@id='ctlBodyPane_ctl09_ctl01_grdValuation']/tbody/tr[3]/td[2]/text()").extract_first()
            total_market_value = resp.xpath("//table[@id='ctlBodyPane_ctl09_ctl01_grdValuation']/tbody/tr[4]/td[2]/text()").extract_first()
            
            
            sale_date = resp.xpath("//table[@id='ctlBodyPane_ctl07_ctl01_gvwSales']/tbody/tr/th[1]/text()").extract_first()
            sale_price = resp.xpath("//table[@id='ctlBodyPane_ctl07_ctl01_gvwSales']/tbody/tr/td[last()]/text()").extract_first()
            with open('test.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([company,owner_name,site_address,site_city,mail_address,mail_city,mail_state,mail_zip,land_value,bldg_value,total_market_value,property_type,Atucal_year_built,living_area,above_rooms,below_rooms,baths,sale_date,sale_price])
                count = count + 1
                print("Data Saved in CSV:",count)
        except:
            print("Serch Result is empty")
        driver.get(ul)
        time.sleep(2)
            
    
driver.close()
