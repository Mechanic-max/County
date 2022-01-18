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

ul = "https://www.countyoffice.org/ca-orange-county-property-records/"




def scrap(count,a0,a1,a2,a3,a4,a5,a6):
    html = driver.page_source
    resp = Selector(text=html)
    
    Census_Tract = resp.xpath("normalize-space(//th[contains(text(),'Census Tract')]/following-sibling::td/text()[1])").extract_first()


    Owners = resp.xpath("normalize-space(//dt[contains(text(),'Name')]/following-sibling::dd[1]/text())").extract_first()
    site_address = resp.xpath("//th[contains(text(),'Address')]/following-sibling::td/text()[1]").extract_first()
    site_address1 = resp.xpath("//th[contains(text(),'Address')]/following-sibling::td/text()[2]").extract_first()
    site_address1 = str(site_address1)
    try:
        site_state = re.findall(r"\s\w\w\s",site_address1)
        site_zip = re.findall(r"\d.*",site_address1)
    except:
        site_state = None
        site_zip = None

    for sa in site_state:
        site_address1 = site_address1.replace(sa,'')

    for si in site_zip:
        site_address1 = site_address1.replace(si,'')
        site_address1 = site_address1.strip()



    
    mail_address = resp.xpath("//dt[contains(text(),'Address')]/following-sibling::dd[1]/text()[1]").extract_first()
    mail_address1 = resp.xpath("//dt[contains(text(),'Address')]/following-sibling::dd[1]/text()[last()]").extract_first()
    mail_address1 = str(mail_address1)
    try:
        mail_state = re.findall(r"\s\w\w\s",mail_address1)
        mail_zip = re.findall(r"\d.*",mail_address1)
    except:
        mail_state = None
        mail_zip = None

    for mo in mail_zip:
        mail_address1 = mail_address1.replace(mo,'')

    for ma in mail_state:
        mail_address1 = mail_address1.replace(ma,'')
        mail_address1 = mail_address1.strip()


    land_use_code = resp.xpath("normalize-space(//th[contains(text(),'Land Use Code')]/following-sibling::td/text())").getall()
    land_use_Category = resp.xpath("normalize-space(//th[contains(text(),'Land Use Category')]/following-sibling::td/text())").extract_first()
    sale_date = resp.xpath("normalize-space((//dt[contains(text(),'Details')])[1]/following-sibling::dd/b[contains(text(),'Recording Date')]/following::text()[1])").extract_first()
    sale_price = resp.xpath("normalize-space((//dt[contains(text(),'Details')])[1]/following-sibling::dd/b[contains(text(),'Sale Price')]/following::text()[1])").extract_first()
    land_area = resp.xpath("normalize-space(//th[contains(text(),'Area')]/following-sibling::td/text())").extract_first()
    living_area = resp.xpath("normalize-space(//th[contains(text(),'Total Area')]/following-sibling::td[1]/text())").extract_first()
    baths = resp.xpath("normalize-space(//th[contains(text(),'Bathrooms')]/following-sibling::td[1]/text())").extract_first()
    built_year = resp.xpath("normalize-space(//th[contains(text(),'Year')]/following-sibling::td[1]/text())").extract_first()
    bedroomms = resp.xpath("//th[contains(text(),'Bedrooms')]/following-sibling::td[1]/text()").extract_first()
    land_value = resp.xpath("//th[contains(text(),'Land Value')]/ancestor::thead/following-sibling::tbody/tr[1]/td[2]/text()").extract_first()
    bldg_value = resp.xpath("//th[contains(text(),'Land Value')]/ancestor::thead/following-sibling::tbody/tr[1]/td[3]/text()").extract_first()
    total_market_value = resp.xpath("//th[contains(text(),'Land Value')]/ancestor::thead/following-sibling::tbody/tr[1]/td[4]/text()").extract_first()






    
    print()
    print(f"Scraping ====>{a3}")
    print("Census_Tract:",Census_Tract)
    print("Owners:",Owners)
    print("site_address:",site_address)
    print("site_city:",site_address1)
    print("site_state:",site_state)
    print("mail_zip:",site_zip)
    print("mail_address:",mail_address)
    print("mail_city:",mail_address1)
    print("mail_state:",mail_state)
    print("mail_zip:",mail_zip)
    print("bedrooms:",bedroomms)
    print("baths:",baths)
    print("land_area:",land_area)
    print("land_use_code:",land_use_code)
    print("land_use_Category:",land_use_Category)
    print("sale_date:",sale_date)
    print("sale_price:",sale_price)
    print("land_value:",land_value)
    print("bldg_value:",bldg_value)
    print("total_market_value:",total_market_value)
    print("living_area:",living_area)    
    print("built_year:",built_year)
    print()
    
    with open('dataset_for_Huntington CA code enforcement.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,a6,Census_Tract,Owners,site_address,site_address1,site_state,site_zip,mail_address,mail_address1,mail_state,mail_zip,land_area,land_use_code,land_use_Category,sale_date,sale_price,land_value,bldg_value,total_market_value,living_area,bedroomms,baths,built_year])
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



with open("./Huntington CA code enforcement.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        driver.get(ul)
        time.sleep(10)
        company1 = str(i[3])
        company1 = company1.strip()
        company1 = f"{company1}, Huntington Beach, CA, USA"
        search = driver.find_element_by_xpath("//input[@id='addressauto']")
        search.send_keys(Keys.CONTROL + "a")
        search.send_keys(Keys.DELETE)
        time.sleep(1)
        search.send_keys(company1)
        time.sleep(1)
        search.send_keys(Keys.ENTER)
        time.sleep(10)
        i[3] = company1


        count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6])



        driver.get(ul)
        time.sleep(3)


