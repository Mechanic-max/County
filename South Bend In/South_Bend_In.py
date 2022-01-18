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

ul = "http://in-stjoseph-assessor.governmax.com/propertymax/search_property.asp?l_nm=streetaddress&form=searchform&formelement=0&sid=7DFA83635C534A74B81F48C09531FA88"


def scrap(count,a0,a1,a2,a3,a4,a5,a6):

    html = driver.page_source
    resp = Selector(text=html)
    
    Parcel = resp.xpath("normalize-space((//font[contains(text(),'-')])[1]/text())").extract_first()
    owner_name = resp.xpath("normalize-space(//b[contains(text(),'Owner Name')]/ancestor::td[1]/following-sibling::td[1]/font/text())").extract_first()
    mail_address = resp.xpath("normalize-space(//b[contains(text(),'Owner Address')]/ancestor::td[1]/following-sibling::td[1]/font/text()[1])").extract_first()
    mail_city_state_zip = resp.xpath("normalize-space(//b[contains(text(),'Owner Address')]/ancestor::td[1]/following-sibling::td[1]/font/text()[last()])").extract_first()
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

    site_address = resp.xpath("normalize-space((//b[contains(text(),'Parcel Address')])[2]/ancestor::td[1]/following-sibling::td[1]/font/text())").extract_first()

    property_use_code = resp.xpath("normalize-space(//b[contains(text(),'Property Class Code')]/ancestor::td[1]/following-sibling::td[1]/font/text())").extract_first()

    Legal_Description = resp.xpath("normalize-space(//b[contains(text(),'Legal Desc.')]/ancestor::td[1]/following-sibling::td[1]/font/text())").extract_first()
    
    land_value = resp.xpath("normalize-space(//b[contains(text(),'Current AV - Total Land')]/ancestor::td[1]/following-sibling::td[1]/font/text())").extract_first()

    total_market_value = resp.xpath("normalize-space((//b[contains(text(),'AV - Total Land & Improv.')])[2]/ancestor::td[1]/following-sibling::td/font/text())").extract_first()
    bld_value = resp.xpath("normalize-space(//b[contains(text(),'Current AV - Total Improv.')]/ancestor::td[1]/following-sibling::td[1]/font/text())").extract_first()

    try:
        driver.find_element_by_xpath("//a[contains(text(),'Sales History')]").click()
        time.sleep(3)
        html = driver.page_source
        resp = Selector(text=html)
        sale_date = resp.xpath("normalize-space(//b[contains(text(),'Date of Sale')]/ancestor::td[1]/following-sibling::td[1]/font/text())").extract_first()
        sale_price = resp.xpath("normalize-space(//b[contains(text(),'Total Sale')]/ancestor::td[1]/following-sibling::td[1]/font/text())").extract_first()

    except:
        sale_date = ''
        sale_price = ''



    print()
    print(f"Scraping ====>{a4}")
    print("Parcel:",Parcel)
    print("owner_name:",owner_name)
    print("site_address:",site_address)
    print("mail_address:",mail_address)
    print("mail_city:",mail_city_state_zip)
    print("mail_state:",mail_state)
    print("mail_zip:",mail_zip)
    print("property_use_code:",property_use_code)
    print("Legal_Description:",Legal_Description)
    print("land_value:",land_value)
    print("bld_value:",bld_value)    
    print("total_market_value:",total_market_value)
    print("sale_date:",sale_date)
    print("sale_price:",sale_price)
    print()
    
    with open('dataset_for_South Bend In Acella (01-01-2020 - 04-09-2021) Code Enforcement.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,a6,Parcel,owner_name,site_address,mail_address,mail_city_state_zip,mail_state,mail_zip,property_use_code,Legal_Description,land_value,bld_value,total_market_value,sale_date,sale_price])
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
    driver.find_element_by_xpath("//font[contains(text(),'I accept, continue')]").click()
    time.sleep(3)
except:
    None

with open("./South Bend In Acella (01-01-2020 - 04-09-2021) Code Enforcement.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        
        try:
            driver.find_element_by_xpath("//a[contains(@href,'ttp://in-stjoseph-assessor')]").click()
            time.sleep(3)
        except:
            None
        try:
            driver.find_element_by_xpath("//option[contains(text(),'Contains')]").click()
            time.sleep(3)
        except:
            None
        company = str(i[4])
        company = company.strip()
        
        search = driver.find_element_by_xpath("//input[@name='p.address']")
        search.send_keys(Keys.CONTROL + "a")
        search.send_keys(Keys.DELETE)
        time.sleep(1)
        search.send_keys(company)
        time.sleep(1)
        search.send_keys(Keys.ENTER)
        time.sleep(4)

        count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6])
        driver.get(ul)
        time.sleep(7)
