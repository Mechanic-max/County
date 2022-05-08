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

ul = "https://www.leonpa.org/pt/search/commonsearch.aspx?mode=parid"


def scrap(count,a0,a1,a2,a3,a4,a5,a6,a7):

    html = driver.page_source
    resp = Selector(text=html)
    
    Parcel = resp.xpath("normalize-space(//td[contains(text(),'Parcel: ')]/text())").extract_first()
    
    owner_name = resp.xpath("normalize-space(//td[contains(text(),'Owner:')]/text())").extract_first()
    mail_address = resp.xpath("normalize-space(//div[contains(text(),'Mailing Addr:')]/parent::td/following-sibling::td/div/text())").extract_first()
    mail_city_state_zip = resp.xpath("normalize-space((//div[contains(text(),' FL ')])[1]/text())").extract_first()
    mail_zip = ''
    mail_state = ''
    mail_city_state_zip = str(mail_city_state_zip)
    try:
        ma_zip = re.findall(r"\d.*",mail_city_state_zip)
        ma_state = re.findall(r"\s\w\w\s",mail_city_state_zip)
    except:
        ma_zip = ''
        ma_state = ''


    for mail_zip in ma_zip:
        mail_city_state_zip = mail_city_state_zip.replace(mail_zip,'')
        mail_city_state_zip = mail_city_state_zip.strip()

    for mail_state in ma_state:
        mail_state = str(mail_state)
        mail_state = mail_state.strip()
        mail_city_state_zip = mail_city_state_zip.replace(mail_state,'')
        mail_city_state_zip = mail_city_state_zip.strip()

    site_address = resp.xpath("normalize-space(//td[contains(text(),'Owner: ')]/following-sibling::td/text())").extract_first()

    property_use = resp.xpath("normalize-space(//td[contains(text(),'Property Use:')]/text())").extract_first()
    land_area = resp.xpath("normalize-space((//div[contains(text(),'Acreage:')])[1]/parent::td/following-sibling::td/div/text())").extract_first()
    Legal_Desc = resp.xpath("normalize-space(//div[contains(text(),'Legal Desc:')]/parent::td/following-sibling::td/div/text())").extract_first()


    land_value = resp.xpath("normalize-space(//td[contains(text(),'Land Value')]/parent::tr/following-sibling::tr[1]/td[2]/text())").extract_first()

    total_market_value = resp.xpath("normalize-space(//td[contains(text(),'Land Value')]/parent::tr/following-sibling::tr[1]/td[4]/text())").extract_first()
    bld_value = resp.xpath("normalize-space(//td[contains(text(),'Land Value')]/parent::tr/following-sibling::tr[1]/td[3]/text())").extract_first()


    sale_date = resp.xpath("normalize-space(//td[contains(text(),'Sale Date')]/parent::tr/following-sibling::tr[1]/td[1]/text())").extract_first()
    sale_price = resp.xpath("normalize-space(//td[contains(text(),'Sale Date')]/parent::tr/following-sibling::tr[1]/td[2]/text())").extract_first()


    print()
    print(f"Scraping ====>{a4}")
    print("Parcel:",Parcel)
    print("owner_name:",owner_name)
    print("site_address:",site_address)
    print("mail_address:",mail_address)
    print("mail_city:",mail_city_state_zip)
    print("mail_state:",mail_state)
    print("mail_zip:",mail_zip)
    print("property_use:",property_use)
    print("Legal_Desc:",Legal_Desc)
    print("land_area:",land_area)
    print("land_value:",land_value)
    print("bld_value:",bld_value)
    print("total_market_value:",total_market_value)
    print("sale_date:",sale_date)
    print("sale_price:",sale_price)
    print()
    
    with open('dataset_for_Tallahassee FL 210405 Active Code Enforcement Cases (4 files merged).csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,a6,a7,Parcel,owner_name,site_address,mail_address,mail_city_state_zip,mail_state,mail_zip,property_use,Legal_Desc,land_area,land_value,bld_value,total_market_value,sale_date,sale_price])
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
time.sleep(7)
try:
    driver.find_element_by_xpath("//button[@id='btAgree']").click()
    time.sleep(3)
except:
    None

with open("./Tallahassee FL 210405 Active Code Enforcement Cases (4 files merged).csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company = str(i[4])
        company = company.replace('Parcel ID','')
        company = company.strip()
        
        search = driver.find_element_by_xpath("//input[@id='inpParid']")
        search.send_keys(Keys.CONTROL + "a")
        search.send_keys(Keys.DELETE)
        time.sleep(1)
        search.send_keys(company)
        time.sleep(2)
        driver.find_element_by_xpath("//button[@id='btSearch']").click()
        time.sleep(8)

        count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7])
        driver.get(ul)
        time.sleep(10)
