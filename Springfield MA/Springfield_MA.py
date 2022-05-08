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

ul = "https://www.springfield-ma.gov/finance/assessors-search/"


def scrap(count,a0,a1,a2,a3,a4,a5,a6,a7):

    html = driver.page_source
    resp = Selector(text=html)
    
    Parcel = resp.xpath("normalize-space(//strong[contains(text(),'Map ID:')]/parent::td/a/text())").extract_first()
    
    owner_name = resp.xpath("normalize-space(//td[contains(text(),'Assessed Owner')]/parent::tr/following-sibling::tr[1]/td/div/text()[1])").extract_first()
    mail_address = resp.xpath("normalize-space(//td[contains(text(),'Assessed Owner')]/parent::tr/following-sibling::tr[1]/td/div/text()[last()-1])").extract_first()
    mail_city_state_zip = resp.xpath("normalize-space(//td[contains(text(),'Assessed Owner')]/parent::tr/following-sibling::tr[1]/td/div/text()[last()])").extract_first()
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

    site_address = resp.xpath("normalize-space(//strong[contains(text(),'Situs:')]/parent::td/text())").extract_first()

    property_class = resp.xpath("normalize-space(//b[contains(text(),'Property Class Code')]/ancestor::td[1]/following-sibling::td[1]/font/text())").extract_first()
    land_area = resp.xpath("normalize-space(//strong[contains(text(),'Total Acres:')]/parent::td/text())").extract_first()


    land_value = resp.xpath("normalize-space(//strong[contains(text(),'Assessed')]/ancestor::tr[1]/following-sibling::tr[1]/td[2]/text())").extract_first()

    total_market_value = resp.xpath("normalize-space(//strong[contains(text(),'Assessed')]/ancestor::tr[1]/following-sibling::tr[3]/td[2]/text())").extract_first()
    bld_value = resp.xpath("normalize-space(//strong[contains(text(),'Assessed')]/ancestor::tr[1]/following-sibling::tr[2]/td[2]/text())").extract_first()


    sale_date = resp.xpath("normalize-space(//strong[contains(text(),'Transfer Date')]/ancestor::tr[1]/following-sibling::tr[1]/td[1]/text())").extract_first()
    sale_price = resp.xpath("normalize-space(//strong[contains(text(),'Transfer Date')]/ancestor::tr[1]/following-sibling::tr[1]/td[2]/text())").extract_first()
    built_year = resp.xpath("normalize-space(//strong[contains(text(),'Year Built/Eff Year:')]/parent::td/following-sibling::td[last()]/text())").extract_first()
    beds = resp.xpath("//strong[contains(text(),'Beds')]/ancestor::tr[1]/following-sibling::tr[2]/td[5]/text()").extract_first()
    baths = resp.xpath("//strong[contains(text(),'Beds')]/ancestor::tr[1]/following-sibling::tr[2]/td[6]/text()").extract_first()
    living_area = resp.xpath("//b[contains(text(),'Total Gross Bldg Area')]/parent::td/following-sibling::td[1]/text()").extract_first()




    print()
    print(f"Scraping ====>{a5}")
    print("Parcel:",Parcel)
    print("owner_name:",owner_name)
    print("site_address:",site_address)
    print("mail_address:",mail_address)
    print("mail_city:",mail_city_state_zip)
    print("mail_state:",mail_state)
    print("mail_zip:",mail_zip)
    print("property_class:",property_class)
    print("built_year:",built_year)
    print("beds:",beds)
    print("baths:",baths)
    print("living_area:",living_area)
    print("land_area:",land_area)
    print("land_value:",land_value)
    print("bld_value:",bld_value)
    print("total_market_value:",total_market_value)
    print("sale_date:",sale_date)
    print("sale_price:",sale_price)
    print()
    
    with open('dataset_for_Springfield MA Acella (01-01-2020 - 04-12-2021) Code Enforcement.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,a6,a7,Parcel,owner_name,site_address,mail_address,mail_city_state_zip,mail_state,mail_zip,property_class,land_area,living_area,land_value,bld_value,total_market_value,built_year,beds,baths,sale_date,sale_price])
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


with open("./Springfield MA Acella (01-01-2020 - 04-12-2021) Code Enforcement.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company = str(i[5])
        company = company.strip()
        
        search = driver.find_element_by_xpath("//input[@id='streetSearch']")
        search.send_keys(Keys.CONTROL + "a")
        search.send_keys(Keys.DELETE)
        time.sleep(1)
        search.send_keys(company)
        time.sleep(2)
        driver.find_element_by_xpath("//input[@id='form-btn']").click()
        time.sleep(8)
        
        results = driver.find_elements_by_xpath("//a[contains(@href,'detail.php')]")
        if results != []:
            driver.find_elements_by_xpath("//a[contains(@href,'detail.php')]")[0].click()
            time.sleep(3)

        count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7])
        driver.get(ul)
        time.sleep(20)
