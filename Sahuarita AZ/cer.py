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
# with open('test.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(["Parcel ID","owner_name","site_address","site_city","mail_address","mail_city","mail_state","mail_zip","land_value","bldg_value","total_market_value","property_type","Atucal_year_built","living_area","above_rooms","below_rooms","baths","sale_date","sale_price"])

ul = "https://www.asr.pima.gov/Parcel/Search"


def scrap(count,a0,a1,a2,a3,a4,a5,a6):

    html = driver.page_source
    resp = Selector(text=html)

    parcel_id = resp.xpath("normalize-space(//strong[contains(text(),'Parcel Number:')]/parent::p/text()[2])").extract_first()
    owner_name = resp.xpath("normalize-space(//th[contains(text(),'Contact Information')]/ancestor::thead/following-sibling::tbody/tr[1]/td[1]/text()[1])").extract_first()

    site_address = resp.xpath("normalize-space(//th[contains(text(),'Contact Information')]/ancestor::thead/following-sibling::tbody/tr[1]/td[1]/text()[2])").extract_first()
    site_address1 = resp.xpath("normalize-space(//th[contains(text(),'Contact Information')]/ancestor::thead/following-sibling::tbody/tr[1]/td[1]/text()[3])").extract_first()
    site_address1 = str(site_address1)
    site_address1 = site_address1.strip()
    try:
        site_state = re.findall(r"\b(\w+)$",site_address1)
        site_city = re.findall(r"^[^,]+",site_address1)
    except:
        site_state = ''
        site_city = ''
    
    site_zip = resp.xpath("normalize-space(//th[contains(text(),'Contact Information')]/ancestor::thead/following-sibling::tbody/tr[1]/td[1]/text()[last()])").extract_first()
    
    
    
    mail_street_no =resp.xpath("normalize-space(//th[contains(text(),'Property Address')]/ancestor::thead/following-sibling::tbody/tr[1]/td[1]/text())").extract_first()
    mail_dir =resp.xpath("normalize-space(//th[contains(text(),'Property Address')]/ancestor::thead/following-sibling::tbody/tr[1]/td[2]/text())").extract_first()
    mail_name =resp.xpath("normalize-space(//th[contains(text(),'Property Address')]/ancestor::thead/following-sibling::tbody/tr[1]/td[3]/text())").extract_first()
    mail_location =resp.xpath("normalize-space(//th[contains(text(),'Property Address')]/ancestor::thead/following-sibling::tbody/tr[1]/td[4]/text())").extract_first()
    mail_address = f"{mail_street_no} {mail_dir} {mail_name}, {mail_location}"
    
    land_price = resp.xpath("normalize-space((//th[contains(text(),'Land FCV')]/ancestor::thead)[1]/following-sibling::tbody/tr[1]/td[last()-4]/text())").extract_first()
    bldg_price = resp.xpath("normalize-space((//th[contains(text(),'Imp FCV')]/ancestor::thead)[1]/following-sibling::tbody/tr[1]/td[last()-3]/text())").extract_first()
    total_fcv = resp.xpath("normalize-space((//th[contains(text(),'Total FCV')]/ancestor::thead)[1]/following-sibling::tbody/tr[1]/td[last()-2]/text())").extract_first()
    limited_value  = resp.xpath("normalize-space((//th[contains(text(),'Total FCV')]/ancestor::thead)[1]/following-sibling::tbody/tr[1]/td[last()-1]/text())").extract_first()
    try:
        driver.find_element_by_xpath("//span[contains(text(),'Property Information')]/parent::div").click()
        time.sleep(3)
        html = driver.page_source
        resp = Selector(text=html)
        land_area = resp.xpath("normalize-space((//b[contains(text(),'Land Measure:')]/parent::td/following-sibling::td)[1]/text())").extract_first()
        land_use_code = resp.xpath("normalize-space((//b[contains(text(),'Use Code:')]/parent::td/following-sibling::td)[1]/text())").extract_first()
    except:
        land_area = ''
        land_use_code = ''
    
    try:
        driver.find_element_by_xpath("//span[contains(text(),'Sales Information')]/parent::div").click()
        time.sleep(3)
        html = driver.page_source
        resp = Selector(text=html)
        sale_date = resp.xpath("normalize-space((//th[contains(text(),'Sale Date')]/ancestor::thead)[1]/following-sibling::tbody/tr[1]/td[3]/text())").extract_first()
        sale_price = resp.xpath("normalize-space((//th[contains(text(),'Sale Date')]/ancestor::thead)[1]/following-sibling::tbody/tr[1]/td[5]/text())").extract_first()
        property_type = resp.xpath("normalize-space((//th[contains(text(),'Sale Date')]/ancestor::thead)[1]/following-sibling::tbody/tr[1]/td[4]/text())").extract_first()
    except:
        sale_date = ''
        sale_price = ''
        property_type = ''

    
    try:
        driver.find_element_by_xpath("//span[contains(text(),'Residential Characteristics')]/parent::div").click()
        time.sleep(3)
        html = driver.page_source
        resp = Selector(text=html)
        living_area = resp.xpath("normalize-space(//b[contains(text(),'Total Living Area')]/parent::td/following-sibling::td[1]/text())").extract_first()
        built_year = resp.xpath("normalize-space(//b[contains(text(),'Effective Construction Year')]/parent::td/following-sibling::td[1]/text())").extract_first()
        baths = resp.xpath("normalize-space(//b[contains(text(),'Bath Fixtures:')]/parent::td/following-sibling::td[1]/text())").extract_first()
        rooms = resp.xpath("normalize-space(//b[contains(text(),'Rooms')]/parent::td/following-sibling::td[1]/text())").extract_first()
    except:
        living_area = ''
        built_year = ''
        baths = ''
        rooms = ''
    
    
    

    print()
    print(f"Scraping=======>{a2}")
    print("parcel_id",parcel_id)
    print("Owner_Name",owner_name)
    print("site_address",mail_address)
    print("mail_address",site_address)
    print("mail_city",site_city)
    print("mail_state",site_state)
    print("mail_zip",site_zip)
    print("land_price",land_price)
    print("bldg_price",bldg_price)
    print("total_fcv",total_fcv)
    print("limited_value",limited_value)
    print("property_type",property_type)
    print("land_area",land_area)
    print("land_use_code",land_use_code)
    print("living_area",living_area)
    print("built_year",built_year)
    print("rooms",rooms)
    print("baths",baths)
    print("sale_date",sale_date)
    print("sale_price",sale_price)
    print()
    
    
    
    with open('dataset_for_Sahuarita AZ Acella (01-01-2020 - 03-23-2021) Code Enforcement.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,a6,parcel_id,owner_name,mail_address,site_address,site_city,site_state,site_zip,mail_address,land_price,bldg_price,total_fcv,limited_value,property_type,land_area,land_use_code,living_area,built_year,rooms,baths,sale_date,sale_price])
        count = count + 1
        print("Data Saved in CSV:",count)

    return count


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



with open("Sahuarita AZ Acella (01-01-2020 - 03-23-2021) Code Enforcement.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company = str(i[4])
        company1 = str(i[6])
        company = company.strip()
        company1 = company1.strip()
        try:
            driver.find_element_by_xpath("//a[contains(text(),'Address')]").click()
            time.sleep(3)
        except:
            print("Pop up didn't appear")

        search = driver.find_element_by_xpath("//input[@id='address1']")
        search.send_keys(Keys.CONTROL + "a")
        search.send_keys(Keys.DELETE)
        time.sleep(1)
        search.send_keys(company)
        time.sleep(1)

        direction_xpath = str(i[5])
        direction = f"//select[@id='selectedDirection']/option[contains(text(),'{direction_xpath}')]"

        try:
            driver.find_element_by_xpath(direction).click()
            time.sleep(2)
        except:None


        search1 = driver.find_element_by_xpath("//input[@id='strName']")
        search1.send_keys(Keys.CONTROL + "a")
        search1.send_keys(Keys.DELETE)
        time.sleep(1)
        search1.send_keys(company1)
        time.sleep(2)
        try:
            street_xpath =f"//strong[contains(text(),'{company1}')]/parent::a"
            driver.find_element_by_xpath(street_xpath).click()
            time.sleep(2)
    
            driver.find_element_by_xpath("//button[@class='btn btn-default button_link fa fa-search' and @title='Search by property address']").click()
            time.sleep(15)
        except: None
        count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6])
        driver.get(ul)
        time.sleep(7)
            
    
driver.close()
