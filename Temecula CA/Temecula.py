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

ul = "https://ca-riverside-acr.publicaccessnow.com/Search.aspx"




def scrap(count,a0,a1,a2,a3,a4,a5,a6):
    html = driver.page_source
    resp = Selector(text=html)
    
    Parcel = resp.xpath("normalize-space(//th[contains(text(),'Assessment No. (PIN) ')]/following-sibling::td[1]/text())").extract_first()
    Parcel = str(Parcel)
    Parcel = Parcel.strip()
    if Parcel:
        Parcel = f"P{Parcel}"


    
    site_address = resp.xpath("//th[contains(text(),'Property Address')]/following-sibling::td[1]/text()[last()-1]").extract_first()
    site_address1 = resp.xpath("//th[contains(text(),'Property Address')]/following-sibling::td[1]/text()[last()]").extract_first()
    site_address1 = str(site_address1)
    try:
        site_city = re.findall(r"^[^,]+,",site_address1)
        site_state = re.findall(r"\s\w\w\s",site_address1)
        site_zip = re.findall(r"\d.*",site_address1)
    except:
        site_city = None
        site_state = None
        site_zip = None




    property_type = resp.xpath("//th[contains(text(),'Property Type')]/following-sibling::td[1]/text()").extract_first()
    land_area = resp.xpath("normalize-space(//th[contains(text(),'Acreage')]/following-sibling::td[1]/text())").extract_first()
    sale_date = resp.xpath("normalize-space(//th[contains(text(),'Sale Price')]/parent::tr/following-sibling::tr[1]/td[1]/text())").extract_first()
    sale_price = resp.xpath("normalize-space(//th[contains(text(),'Sale Price')]/parent::tr/following-sibling::tr[1]/td[last()]/text())").extract_first()
    living_area = resp.xpath("normalize-space(//th[contains(text(),'Total Area')]/following-sibling::th[1]/text())").extract_first()

    built_year = resp.xpath("normalize-space(//th[contains(text(),'Year Built')]/following-sibling::td[1]/text())").extract_first()


    try:
        driver.find_element_by_xpath("//a[@id='nav-units-costs-tab']").click()
        time.sleep(3)
        html = driver.page_source
        resp = Selector(text=html)
        baths = resp.xpath("normalize-space(//strong[contains(text(),'Number of Baths:')]/parent::li/text())").extract_first()
        if baths:
            None
        else:
            baths = resp.xpath("normalize-space(//td[contains(text(),'Bath - Full')]/preceding-sibling::td[last()]/text())").extract_first()
        
        bedroomms = resp.xpath("//strong[contains(text(),'Number of Beds:')]/parent::li/text()").extract_first()
        if bedroomms:
            None
        else:
            bedroomms = resp.xpath("//td[contains(text(),'Bedroom')]/preceding-sibling::td[last()]/text()").extract_first()
    except:
        baths = None
        bedroomms = None

    Owners = ''
    owner_link = resp.xpath("//a[contains(text(),'View Tax Info')]/@href").extract_first()
    if owner_link:
        driver.get(owner_link)
        time.sleep(15)
        html = driver.page_source
        resp = Selector(text=html)
        Owners = resp.xpath("normalize-space(//b[contains(text(),'Current Owner: ')]/parent::h2/text()[last()])").extract_first()


    print()
    print(f"Scraping ====>{a2}")
    print("Parcel:",Parcel)
    print("Owners:",Owners)
    print("site_address:",site_address)
    print("site_city:",site_city)
    print("site_state:",site_state)
    print("site_zip:",site_zip)
    print("bedrooms:",bedroomms)
    print("baths:",baths)
    print("land_area:",land_area)
    print("property_type:",property_type)
    print("sale_date:",sale_date)
    print("sale_price:",sale_price)
    print("living_area:",living_area)    
    print("built_year:",built_year)
    print()
    
    with open('dataset_for_Temecula CA (01-01-2020 - 04-07-2021) Code Enforcement.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,a6,Parcel,Owners,site_address,site_city,site_state,site_zip,land_area,property_type,sale_date,sale_price,living_area,bedroomms,baths,built_year])
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
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(executable_path=path,options=options)
driver.get(ul)
time.sleep(20)

with open("./Temecula CA (01-01-2020 - 04-07-2021) Code Enforcement.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:

        company1 = str(i[2])
        company1 = company1.strip()
        search = driver.find_element_by_xpath("//input[@class='form-control ng-untouched ng-pristine ng-valid']")
        search.send_keys(Keys.CONTROL + "a")
        search.send_keys(Keys.DELETE)
        time.sleep(2)
        search.send_keys(company1)
        time.sleep(2)
        search.send_keys(Keys.ENTER)
        time.sleep(10)

        try:
            driver.find_element_by_xpath("//a[contains(text(),'View Property')]").click()
            time.sleep(3)
            
        except:
            None
        
        count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6])
        driver.get(ul)
        time.sleep(7)
