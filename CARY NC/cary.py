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

ul = "http://services.wakegov.com/realestate/"




def scrap(count,a0,a1,a2,a3,a4,a5,a6,a7,a8,a9):
    html = driver.page_source
    resp = Selector(text=html)
    
    parcel_id = resp.xpath("normalize-space(//font[contains(text(),'Real Estate ID ')]/following-sibling::b/font/text())").extract_first()
    pin = resp.xpath("//font[contains(text(),'PIN #')]/following-sibling::b/font/text()").extract_first()
    Owners = resp.xpath("//font[contains(text(),'Property Owner')]/ancestor::tr/following-sibling::tr[1]/td/b/font/text()").extract_first()

    site_address = resp.xpath("//font[contains(text(),'Mailing Address')]/ancestor::tr/following-sibling::tr[1]/td/b/font/text()").extract_first()
    site_city_state_zip = resp.xpath("//font[contains(text(),'Mailing Address')]/ancestor::tr/following-sibling::tr[2]/td/b/font/text()").extract_first()
    site_city_state_zip = str(site_city_state_zip)
    try:
        site_city = re.findall(r"^([\w\-]+)",site_city_state_zip)
        site_state = re.findall(r"\s\w\w\s",site_city_state_zip)
        site_zip = re.findall(r"\b(\w+)$",site_city_state_zip)
    except:
        site_city = None
        site_state = None
        site_zip = None

    land_value = resp.xpath("//font[contains(text(),'Land Value Assessed')]/parent::td/following-sibling::td/div/b/font/text()").extract_first()
    bldg_value = resp.xpath("//font[contains(text(),'Bldg. Value Assessed')]/parent::td/following-sibling::td/div/b/font/text()").extract_first()
    total_market_value = resp.xpath("//font[contains(text(),'Total Value Assessed')]/parent::td/following-sibling::td/div/b/font/text()").extract_first()

    
    mail_address = resp.xpath("//font[contains(text(),'Property Location Address')]/ancestor::tr/following-sibling::tr[1]/td/b/font/text()").extract_first()
    mail_address1 = resp.xpath("//font[contains(text(),'Property Location Address')]/ancestor::tr/following-sibling::tr[2]/td/b/font/text()").extract_first()
    mail_address1 = str(mail_address1)
    try:
        mail_city = re.findall(r"^([\w\-]+)",mail_address1)
        mail_state = re.findall(r"\s\w\w\s",mail_address1)
        mail_zip = re.findall(r"\b(\w+)$",mail_address1)
    except:
        mail_city = None
        mail_state = None
        mail_zip = None

    try:
        driver.find_element_by_xpath("//b[contains(text(),'Sales')]/parent::font/parent::a").click()
        time.sleep(3)
        html = driver.page_source
        resp = Selector(text=html)

        sale_date = resp.xpath("//font[contains(text(),'Sale')]/ancestor::tr/following-sibling::tr[1]/td[last()-1]/b//text()").extract_first()
        sale_price = resp.xpath("//font[contains(text(),'Sale')]/ancestor::tr/following-sibling::tr[1]/td[last()]/b//text()").extract_first()

        driver.back()
        time.sleep(3)
    except:
        sale_date = None
        sale_price = None
    

    try:
        driver.find_element_by_xpath("//b[contains(text(),'Buildings')]/parent::font/parent::a").click()
        time.sleep(3)
        html = driver.page_source
        resp = Selector(text=html)

        Property_TYPE = resp.xpath("normalize-space(//font[contains(text(),'Bldg Type')]/parent::td/following-sibling::td/b/font/text())").extract_first()
        living_area = resp.xpath("//font[contains(text(),'Heated Area')]/parent::td/following-sibling::td/b/font/text()").extract_first()
        baths = resp.xpath("//font[contains(text(),'Plumbing')]/parent::td/following-sibling::td/b/font/text()").extract_first()
        built_year = resp.xpath("//font[contains(text(),'Year Blt')]/parent::td/following-sibling::td[1]/b/font/text()").extract_first()
        eff_year = resp.xpath("//font[contains(text(),'Eff Year')]/parent::td/following-sibling::td[1]/b/font/text()").extract_first()

        driver.back()
        time.sleep(3)
    except:
        Property_TYPE = None
        living_area = None
        baths = None
        built_year = None
        eff_year = None

    
    
    print()
    print(f"Scraping ====>{a8} {a9}")
    print("parcel_id:",parcel_id)
    print("pin:",pin)
    print("Owners:",Owners)
    print("site_address:",site_address)
    print("site_city:",site_city)
    print("site_state:",site_state)
    print("site_zip:",site_zip)
    print("land_value:",land_value)
    print("bldg_value:",bldg_value)
    print("total_market_value:",total_market_value)
    print("mail_address:",mail_address)
    print("mail_city:",mail_city)
    print("mail_state:",mail_state)
    print("mail_zip:",mail_zip)
    print("sale_date:",sale_date)
    print("sale_price:",sale_price)
    print("Property_TYPE:",Property_TYPE)
    print("living_area:",living_area)    
    print("baths:",baths)
    print("built_year:",built_year)
    print("eff_year:",eff_year)

    print()
    
    with open('dataset_for_carry.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,parcel_id,pin,Owners,site_address,site_city,site_state,site_zip,mail_address,mail_city,mail_state,mail_zip,land_value,bldg_value,total_market_value,sale_date,sale_price,Property_TYPE,living_area,baths,built_year,eff_year])
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







with open("./input.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company1 = str(i[8])
        company1 = company1.strip()
        company2 = str(i[9])
        company2 = company2.strip()
        search = driver.find_element_by_xpath("//input[@name='stnum']")
        search.clear()
        search.send_keys(company1)
        time.sleep(1)
        search1 = driver.find_element_by_xpath("//input[@name='stname']")
        search1.clear()
        search1.send_keys(company2)
        time.sleep(1)
        search.send_keys(Keys.ENTER)
        time.sleep(5)
        try:
            results = driver.find_elements_by_xpath("//a[contains(@href,'Acc')]")
            if len(results) != 0:
                for ri in range(0,len(results)):
                    driver.find_elements_by_xpath("//a[contains(@href,'Acc')]")[ri].click()
                    time.sleep(3)
                    count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9])
                    driver.back()
                    time.sleep(3)

            else:
                count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9])


        except:
            print("Search result is empty")
        
        driver.get(ul)
        time.sleep(2)
        
