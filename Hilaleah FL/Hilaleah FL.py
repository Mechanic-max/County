from os import replace
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

ul = "https://www.miamidade.gov/Apps/PA/propertysearch/#/"




def scrap(count,a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14):
    html = driver.page_source
    resp = Selector(text=html)
    
    parcel_id = resp.xpath("normalize-space(//strong[contains(text(),'Folio:')]/parent::td/text())").extract_first()
    Owners = resp.xpath("normalize-space(//strong[contains(text(),'Owner')]/following-sibling::div/div/div/text()[1])").extract_first()
    Owners1 = resp.xpath("normalize-space(//strong[contains(text(),'Owner')]/following-sibling::div/div/div/text()[2])").extract_first()
    site_addres = resp.xpath("//div[@class='property-add']/span")
    site_address = []
    for sa in site_addres:
        add = sa.xpath("normalize-space(.//text())").get()
        site_address.append(add)
    
    mail_address = resp.xpath("normalize-space(//strong[contains(text(),'Mailing Address')]/following-sibling::div/span[1]/text())").extract_first()

    mail_city = resp.xpath("//strong[contains(text(),'Mailing Address')]/following-sibling::div/span[contains(text(),',')]/text()").extract_first()
    mail_state = resp.xpath("//strong[contains(text(),'Mailing Address')]/following-sibling::div/span[contains(text(),',')]/following-sibling::span[1]/text()").extract_first()
    mail_zip = resp.xpath("//strong[contains(text(),'Mailing Address')]/following-sibling::div/span[contains(text(),',')]/following-sibling::span[2]/text()").extract_first()
    
    sale_date = resp.xpath("normalize-space((//td[contains(text(),'Previous Sale')])[1]/parent::tr/following-sibling::tr[1]/td[1]/text())").extract_first()
    sale_price = resp.xpath("normalize-space((//td[contains(text(),'Previous Sale')])[1]/parent::tr/following-sibling::tr[1]/td[2]/text())").extract_first()
    
    land_value = resp.xpath("normalize-space((//td[contains(text(),'Year')])[1]/parent::tr/following-sibling::tr[1]/td[2]/text())").extract_first()
    bldg_value = resp.xpath("normalize-space((//td[contains(text(),'Year')])[1]/parent::tr/following-sibling::tr[2]/td[2]/text())").extract_first()
    TOAL_MARKET_VALUE = resp.xpath("normalize-space((//td[contains(text(),'Year')])[1]/parent::tr/following-sibling::tr[last()]/td[2]/text())").extract_first()

    living_area = resp.xpath("normalize-space(//strong[contains(text(),'Living Area')]/parent::td/following-sibling::td/text())").extract_first()

    land_use_code = resp.xpath("normalize-space(//strong[contains(text(),'Primary Land Use')]/following-sibling::div/text())").extract_first()
    beds_baths_half_bath = resp.xpath("//strong[contains(text(),'Beds / Baths / Half')]/parent::td/following-sibling::td/text()").extract_first()
    land_sq_area = resp.xpath("//strong[contains(text(),'Lot Size')]/parent::td/following-sibling::td/text()").extract_first()
    beds_baths_half_bath = str(beds_baths_half_bath)
    bdo = re.findall(r"^([\w\-]+)",beds_baths_half_bath)
    bedroomms = ''
    for bedroomms in bdo:
        bedroomms = str(bedroomms)
        beds_baths_half_bath = beds_baths_half_bath.replace(bedroomms,'')

    hb = re.findall(r"\b(\w+)$",beds_baths_half_bath)
    half_baths = ''
    for half_baths in hb:
        half_baths = str(half_baths)
        beds_baths_half_bath = beds_baths_half_bath.replace(half_baths,'')

    built_year = resp.xpath("normalize-space((//td[contains(text(),'Sub Area')]/parent::tr/following-sibling::tr)[1]/td[3]/text())").extract_first()


    beds_baths_half_bath = beds_baths_half_bath.replace('/','')
    full_baths = beds_baths_half_bath.strip()


    print() 
    print(f"Scraping ====>{a5}")
    print("parcel_id:",parcel_id)
    print("Owners:",Owners)
    print("Owners1:",Owners1)
    print("site_address:",site_address)
    print("mail_address:",mail_address)
    print("mail_city:",mail_city)
    print("mail_state:",mail_state)
    print("mail_zip:",mail_zip)
    print("land_value:",land_value)
    print("bldg_value:",bldg_value)
    print("TOAL_MARKET_VALUE:",TOAL_MARKET_VALUE)
    print("land_use_code:",land_use_code)
    print("bedrooms:",bedroomms)
    print("full_baths:",full_baths)
    print("half_baths:",half_baths)
    print("sale_date:",sale_date)
    print("sale_price:",sale_price)
    print("living_area:",living_area) 
    print("land_sq_area:",land_sq_area) 
    print("built_year:",built_year)
    print()
    
    with open('Scraped_Hilaleah FL (01-01-2020 - 4-12-2021) Violation status.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,parcel_id,Owners,Owners1,site_address,mail_address,mail_city,mail_state,mail_zip,land_value,bldg_value,TOAL_MARKET_VALUE,sale_date,sale_price,built_year,living_area,land_use_code,land_sq_area,bedroomms,full_baths,half_baths])
        count = count + 1
        print("Data saved in CSV: ",count)

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

driver.find_element_by_xpath("//a[@id='t-folio']").click()
time.sleep(3)
with open("./Hilaleah FL (01-01-2020 - 4-12-2021) Violation status.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        try:      
            company1 = str(i[5])
            company1 = company1.strip()
            search = driver.find_element_by_xpath("//input[@id='search_box' and @value='Folio']")
            search.send_keys(Keys.CONTROL + "a")
            search.send_keys(Keys.DELETE)
            time.sleep(1)
            search.send_keys(company1)
            time.sleep(1)
            search.send_keys(Keys.ENTER)
            time.sleep(5)
        except:
            None

        count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14])
