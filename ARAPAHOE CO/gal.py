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
    writer.writerow(["Parcel ID","owner_name","site_address","site_city","owner_address","owner_city","owner_state","owner_zip_code","land_value","bldg_value","total_accessed_value","sale_date","sale_price","Bedrooms","Bathrooms","year_built","living_area","property_type"])

ul = "https://www.arapahoegov.com/1084/Residential-Commercial-Ag-and-Vacant-Lan"



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

with open("./input.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
            
        driver.switch_to_frame(driver.find_element_by_xpath("//iframe"))
        search = driver.find_element_by_xpath("//input[@id='txtPIN']")
        search.clear()
        company = str(i[0])
        company = f"0{company}"
        search.send_keys(company)        
        time.sleep(1)
        search.send_keys(Keys.ENTER)
        time.sleep(3)
        html = driver.page_source
        resp = Selector(text=html)

        site_address = resp.xpath("//span[@id='ucParcelHeader_lblSitusAddressTxt']/text()").extract_first()
        site_city = resp.xpath("//span[@id='ucParcelHeader_lblSitusCityTxt']/text()").extract_first()
        owner_name = resp.xpath("//span[@id='ucParcelHeader_lblFullOwnerListTxt']/text()").extract_first()
        owner_address = resp.xpath("//span[@id='ucParcelHeader_lblOwnerAddressTxt']/text()").extract_first()
        owner_city_state_zip = resp.xpath("//span[@id='ucParcelHeader_lblOwnerCSZTxt']/text()").extract_first()
        try:
            owner_city_state_zip = str(owner_city_state_zip)
            owner_city = re.findall(r"^[^,]+",owner_city_state_zip)
            owner_state = re.findall(r",\s\w\w\s",owner_city_state_zip)
            owner_zip_code = re.findall(r"\d.*",owner_city_state_zip)

        except:
            owner_city = None
            owner_state = None
            owner_zip_code = None
        
        land_value = resp.xpath("//span[@id='ucParcelValue_lblApprTotal']/text()").extract_first()
        bldg_value = resp.xpath("//span[@id='ucParcelValue_lblApprBuilding']/text()").extract_first()
        total_accessed_value = resp.xpath("//span[@id='ucParcelValue_lblApprLand']/text()").extract_first()
        sale_date = resp.xpath("(//div[contains(text(),'-')])[1]/text()").extract_first()
        sale_price = resp.xpath("(//div[contains(text(),'-')])[1]/parent::td/following-sibling::td/div/text()").extract_first()
        bedrooms = resp.xpath("//span[@id='ucParcelResdBuild_rptrResdBuild_lblBedroomTitle_0']/parent::div/parent::td/following-sibling::td/div/text()").extract_first()
        bathrooms = resp.xpath("//span[@id='ucParcelResdBuild_rptrResdBuild_Label4_0']/parent::div/parent::td/following-sibling::td/div/text()").extract_first()
        year_built = resp.xpath("//span[@id='ucParcelResdBuild_rptrResdBuild_lblYearBuiltTitle_0']/parent::div/parent::td/following-sibling::td/div/text()").extract_first()
        living_area = resp.xpath("//b[contains(text(),'Bldg Total Area:')]/parent::td/following-sibling::td/div/text()").extract_first()
        property_type = resp.xpath("//th[contains(text(),'Land Use')]/parent::tr/parent::thead/following-sibling::tbody/tr[1]/td[last()]/text()").extract_first()
        with open('test.csv','a',newline='') as file:
            writer = csv.writer(file)
            writer.writerow([company,owner_name,site_address,site_city,owner_address,owner_city,owner_state,owner_zip_code,land_value,bldg_value,total_accessed_value,sale_date,sale_price,bedrooms,bathrooms,year_built,living_area,property_type])
            count = count + 1
            print("Data saved in CSV: ",count)
        driver.get(ul)
        time.sleep(4)
