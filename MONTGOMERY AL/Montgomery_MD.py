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

ul = "https://revco.mc-ala.org/CAPortal/CAPortal_MainPage.aspx"




def scrap(count,a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13):
    
    iframe = driver.find_elements_by_xpath("//iframe[contains(@id,'')]")
    for io in range(0,len(iframe)):
        driver.switch_to.frame(driver.find_elements_by_xpath("//iframe[contains(@id,'')]")[io])
    html = driver.page_source
    resp = Selector(text=html)
    
    Parcel_no = resp.xpath("normalize-space(//b[contains(text(),'PARCEL #:')]/parent::td/following-sibling::td[1]/b/text())").extract_first()
    Owners = resp.xpath("normalize-space(//b[contains(text(),'OWNER:')]/parent::td/following-sibling::td[1]/span/text())").extract_first()
    
    site_address = resp.xpath("normalize-space(//b[contains(text(),'LOCATION:')]/parent::td/following-sibling::td[1]//text())").extract_first()
    site_address = str(site_address)

    site_address1 = resp.xpath("normalize-space(//b[contains(text(),'ADDRESS:')]/parent::td/following-sibling::td[1]//text())").extract_first()
    site_address1 = str(site_address1)
    site_address = site_address.replace(site_address1,'')
    try:
        site_zip = re.findall(r"\d.*",site_address1)
        site_state = re.findall(r"\s\w\w\s",site_address1)
    except:
        site_zip = None
        site_state = None

    sit_zip = ''
    sit_state = ''
    
    for sit_zip in site_zip:
        sit_state = str(sit_zip)
        site_address1 = site_address1.replace(sit_zip,'')

    for sit_zip in site_state:
        sit_state = str(sit_state)
        site_address1 = site_address1.replace(sit_state,'')
        site_address1 = site_address1.strip()


    # mail_address = resp.xpath("normalize-space(//span[@id='MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucDetailsSearch_dlstDetaisSearch_lblMailingAddress_0']/text())").extract_first()
    # mail_address1 = resp.xpath("normalize-space(//span[@id='MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucDetailsSearch_dlstDetaisSearch_lblMailingAddress_0']/text()[2])").extract_first()
    # mail_address1 = str(mail_address1)
    # try:
    #     mail_state = re.findall(r"\s\w\w\s",mail_address1)
    #     mail_zip = re.findall(r"\d.*",mail_address1)
    # except:
    #     mail_state = None
    #     mail_zip = None

    # ma_zip = ''
    # ma_state = ''

    # for ma_state in mail_state:
    #     ma_state = str(ma_state)
    #     mail_address1 = mail_address1.replace(ma_state,' ')
    #     mail_address1 = mail_address1.strip()
    
    # for ma_zip in mail_zip:
    #     ma_zip = str(mail_zip)
    #     ma_zip = ma_zip.replace('[','')
    #     ma_zip = ma_zip.replace(']','')
    #     ma_zip = ma_zip.replace("'","")
    #     mail_address1 = mail_address1.replace(ma_zip,'')

    property_class = resp.xpath("//td[contains(text(),'PROPERTY CLASS:')]/following-sibling::td[1]/text()").extract_first()
    land_value = resp.xpath("normalize-space(//td[contains(text(),'Land:')]/b/text())").extract_first()
    bldg_value = resp.xpath("normalize-space(//td[contains(text(),'Imp')]/b/text())").extract_first()
    market_value = resp.xpath("normalize-space(//td[contains(text(),'Total:')]/b/text())").extract_first()
    sale_date = resp.xpath("normalize-space(//td[contains(text(),'INSTRUMENT NUMBER')]/parent::tr/following-sibling::tr[1]/td[2]/text())").extract_first()
    sale_price = resp.xpath("normalize-space(//td[contains(text(),'Sales Info:')]/b/text())").extract_first()
    living_area = resp.xpath("normalize-space(//td[contains(text(),'H/C Sqft:')]/b/text())").extract_first()
    land_area = resp.xpath("normalize-space(//td[contains(text(),'Acres:')]/b/text())").extract_first()
    baths = resp.xpath("normalize-space(//td[contains(text(),'Baths:')]/b/text())").extract_first()
    bedrooms = resp.xpath("normalize-space(//td[contains(text(),'Bed Rooms:')]/b/text())").extract_first()


    

    print()
    print(f"Scraping ====>{a4}")
    print("Parcel_no:",Parcel_no)
    print("Owners:",Owners)
    # print("mail_address:",mail_address)
    # print("MAIL CIITY:",mail_address1)
    # print("ma_state:",ma_state)
    # print("ma_zip:",ma_zip)
    print("site_address:",site_address)
    print("site_city:",site_address1)
    print("sit_state:",sit_state)
    print("site_zip:",sit_zip)
    print("baths:",baths)
    print("bedrooms:",bedrooms)
    print("property_class:",property_class)
    print("sale_date:",sale_date)
    print("sale_price:",sale_price)
    print("land_area:",land_area)    
    print("living_area:",living_area)  
    print("land_value:",land_value)
    print("bldg_value:",bldg_value)
    print("market_value:",market_value)
    print()
    
    with open('dataset_for_montgomery county al.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,Parcel_no,Owners,site_address,site_address1,sit_state,sit_zip,property_class,sale_date,sale_price,land_area,living_area,baths,bedrooms,land_value,bldg_value,market_value])
        count = count + 1
        print("Data saved in CSV: ",count)

    driver.switch_to.default_content()
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
time.sleep(10)
with open("./montgomery al.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company1 = str(i[4])
        company1 = company1.strip()
        try:
            driver.find_element_by_xpath("//input[@id='PropertyTaxBttn']").click()
            time.sleep(5)
        except: None

        iframe = driver.find_element_by_xpath("//iframe[@id]")
        driver.switch_to.frame(iframe)
        try:
            driver.find_element_by_xpath("//input[@id='SearchByParcel']").click()
            time.sleep(5)
        except: print("nai select hua")
        time.sleep(2)
        search = driver.find_element_by_xpath("//input[@id='SearchText']")
        search.send_keys(Keys.CONTROL + "a")
        search.send_keys(Keys.DELETE)
        search.send_keys(company1)
        time.sleep(1)
        search.send_keys(Keys.ENTER)
        time.sleep(5)

        try:
            driver.find_element_by_xpath("//span[@class='Header1Font']").click()
            time.sleep(5)
            count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13])
        except:
            count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13])
            
        driver.get(ul)
        time.sleep(5)
