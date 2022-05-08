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
    writer.writerow(["Sourcce Parcel ID","parcel_id","owner_name","site_address","site_city","site_state","site_zip","owner_address","owner_city","owner_state","owner_zip","property_type","Atucal_year_built","living_area","sale_date","sale_price","above_Bedrooms","below_Bedrooms","bathrooms","text_year1","land_value1","bldg_value1","total_market_value1","text_year2","land_value2","bldg_value2","total_market_value2","text_year3","land_value3","bldg_value3","total_market_value3","text_year4","land_value4","bldg_value4","total_market_value4","text_year5","land_value5","bldg_value5","total_market_value5"])

ul = "https://beacon.schneidercorp.com/Application.aspx?AppID=12&LayerID=93&PageTypeID=2&PageID=143"

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

with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        company = str(company)
        if len(company) == 9:
            company = f"0{company}"
        search = driver.find_element_by_xpath("//input[@id='ctlBodyPane_ctl02_ctl01_txtParcelID']")
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
                site_city = re.findall(r"^[\dA-Z_]+ [^\(\s]+.",site_city_state_zip)
                site_state = re.findall(r"\s\w\w\s",site_city_state_zip)
                site_zip = re.findall(r"\d.*",site_city_state_zip)
            except:
                site_city = None
                site_state = None
                site_zip = None
            
            owner_name = resp.xpath("//span[@id='ctlBodyPane_ctl02_ctl01_lstDeed_ctl01_lblDeedName_lblSearch']/text()").extract_first()
            owner_address = resp.xpath("//span[@id='ctlBodyPane_ctl02_ctl01_lstDeed_ctl01_lblAddress1']/text()").extract_first()
            owner_city_state_zip = resp.xpath("normalize-space(//span[@id='ctlBodyPane_ctl02_ctl01_lstDeed_ctl01_lblAddress3']/text())").extract_first()
            try:
                owner_city_state_zip = str(owner_city_state_zip)
                owner_city = re.findall(r"^[\dA-Z_]+ [^\(\s]+.",owner_city_state_zip)
                owner_state = re.findall(r"\s\w\w\s",owner_city_state_zip)
                owner_zip = re.findall(r"\d.*",owner_city_state_zip)
            except:
                owner_city = None
                owner_state = None
                owner_zip = None
            
            property_type = resp.xpath("//span[@id='ctlBodyPane_ctl00_ctl01_lblClass']/text()[1]").extract_first()
            Atucal_year_built = resp.xpath("//span[@id='ctlBodyPane_ctl04_ctl01_lstResidential_ctl00_lblYearBuilt']/text()[1]").extract_first()
            
            
            
            living_area = resp.xpath("//span[@id='ctlBodyPane_ctl04_ctl01_lstResidential_ctl00_lblGLA']/text()[1]").extract_first()
            above_Bedrooms = resp.xpath("//span[@id='ctlBodyPane_ctl04_ctl01_lstResidential_ctl00_lblBedroomAboveCount']/text()[1]").extract_first()
            below_Bedrooms = resp.xpath("//span[@id='ctlBodyPane_ctl04_ctl01_lstResidential_ctl00_lblBedroomBelowCount']/text()[1]").extract_first()
            bathrooms = resp.xpath("//span[@id='ctlBodyPane_ctl04_ctl01_lstResidential_ctl00_lblPlumbing']/text()[1]").extract_first()
            sale_date = resp.xpath("//table[@id='ctlBodyPane_ctl08_ctl01_gvwSales']/tbody/tr[1]/th/text()").extract_first()
            sale_price = resp.xpath("//table[@id='ctlBodyPane_ctl08_ctl01_gvwSales']/tbody/tr[1]/td[last()]/text()").extract_first()
            
            text_year1 = resp.xpath("//table[@id='ctlBodyPane_ctl11_ctl01_grdValuation']/thead/tr[1]/th[1]/text()").extract_first()
            land_value1 = resp.xpath("//table[@id='ctlBodyPane_ctl11_ctl01_grdValuation']/tbody/tr[2]/td[2]/text()").extract_first()
            bldg_value1 = resp.xpath("//table[@id='ctlBodyPane_ctl11_ctl01_grdValuation']/tbody/tr[3]/td[2]/text()").extract_first()
            total_market_value1 = resp.xpath("//table[@id='ctlBodyPane_ctl11_ctl01_grdValuation']/tbody/tr[5]/td[2]/text()").extract_first()
            
            text_year2 = resp.xpath("//table[@id='ctlBodyPane_ctl11_ctl01_grdValuation']/thead/tr[1]/th[2]/text()").extract_first()
            land_value2 = resp.xpath("//table[@id='ctlBodyPane_ctl11_ctl01_grdValuation']/tbody/tr[2]/td[3]/text()").extract_first()
            bldg_value2 = resp.xpath("//table[@id='ctlBodyPane_ctl11_ctl01_grdValuation']/tbody/tr[3]/td[3]/text()").extract_first()
            total_market_value2 = resp.xpath("//table[@id='ctlBodyPane_ctl11_ctl01_grdValuation']/tbody/tr[5]/td[3]/text()").extract_first()
            
            text_year3 = resp.xpath("//table[@id='ctlBodyPane_ctl11_ctl01_grdValuation']/thead/tr[1]/th[3]/text()").extract_first()
            land_value3 = resp.xpath("//table[@id='ctlBodyPane_ctl11_ctl01_grdValuation']/tbody/tr[2]/td[4]/text()").extract_first()
            bldg_value3 = resp.xpath("//table[@id='ctlBodyPane_ctl11_ctl01_grdValuation']/tbody/tr[3]/td[4]/text()").extract_first()
            total_market_value3 = resp.xpath("//table[@id='ctlBodyPane_ctl11_ctl01_grdValuation']/tbody/tr[5]/td[4]/text()").extract_first()
            
            text_year4 = resp.xpath("//table[@id='ctlBodyPane_ctl11_ctl01_grdValuation']/thead/tr[1]/th[4]/text()").extract_first()
            land_value4 = resp.xpath("//table[@id='ctlBodyPane_ctl11_ctl01_grdValuation']/tbody/tr[2]/td[5]/text()").extract_first()
            bldg_value4 = resp.xpath("//table[@id='ctlBodyPane_ctl11_ctl01_grdValuation']/tbody/tr[3]/td[5]/text()").extract_first()
            total_market_value4 = resp.xpath("//table[@id='ctlBodyPane_ctl11_ctl01_grdValuation']/tbody/tr[5]/td[5]/text()").extract_first()
            
            text_year5 = resp.xpath("//table[@id='ctlBodyPane_ctl11_ctl01_grdValuation']/thead/tr[1]/th[5]/text()").extract_first()
            land_value5 = resp.xpath("//table[@id='ctlBodyPane_ctl11_ctl01_grdValuation']/tbody/tr[2]/td[6]/text()").extract_first()
            bldg_value5 = resp.xpath("//table[@id='ctlBodyPane_ctl11_ctl01_grdValuation']/tbody/tr[3]/td[6]/text()").extract_first()
            total_market_value5 = resp.xpath("//table[@id='ctlBodyPane_ctl11_ctl01_grdValuation']/tbody/tr[5]/td[6]/text()").extract_first()
            
            
            with open('test.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([company,parcel_id,owner_name,site_address,site_city,site_state,site_zip,owner_address,owner_city,owner_state,owner_zip,property_type,Atucal_year_built,living_area,sale_date,sale_price,above_Bedrooms,below_Bedrooms,bathrooms,text_year1,land_value1,bldg_value1,total_market_value1,text_year2,land_value2,bldg_value2,total_market_value2,text_year3,land_value3,bldg_value3,total_market_value3,text_year4,land_value4,bldg_value4,total_market_value4,text_year5,land_value5,bldg_value5,total_market_value5])
                count = count + 1
                print("Data Saved in CSV:",count)
        except:
            print("Search results is empty")
            break

        driver.get(ul)
        time.sleep(5)