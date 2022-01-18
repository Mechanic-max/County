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

ul = "https://jcgis.jacksongov.org/apps/parcelviewer/WebMap1.aspx"




def scrap(count,a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,a20,a21,a22):
    html = driver.page_source
    resp = Selector(text=html)
    
    parcel_id = resp.xpath("normalize-space(//div[@id='lblParcelNum']/text())").extract_first()
    site_address = resp.xpath("//div[@id='lblSitusAddr']/text()").extract_first()
    site_address1 = resp.xpath("//div[@id='lblSitusCityStateZip']/text()").extract_first()
    site_address1 = str(site_address1)
    try:
        site_city = re.findall(r"^[^,]+",site_address1)
        site_state = re.findall(r"\s\w\w\s",site_address1)
        site_zip = re.findall(r"\d.*",site_address1)
    except:
        site_city = None
        site_state = None
        site_zip = None
    
    land_size = resp.xpath("//div[@id='lblLotSize']/text()").extract_first()
    living_area = resp.xpath("normalize-space(//div[@id='lblBldgSqFt']/text())").extract_first()
    beds = resp.xpath("//div[@id='lblNumBR']/text()").extract_first()
    baths = resp.xpath("//div[@id='lblNumBaths']/text()").extract_first()
    built_year = resp.xpath("normalize-space(//div[@id='lblYearBuilt']/text())").extract_first()
    land_use_code = resp.xpath("normalize-space(//div[@id='lblusecode']/text())").extract_first()
    land_value = resp.xpath("normalize-space(//div[@id='lblYear0ResLand']/text())").extract_first()
    bldg_value = resp.xpath("normalize-space(//div[@id='lblYear0ResImp']/text())").extract_first()
    TOAL_MARKET_VALUE = resp.xpath("normalize-space(//div[@id='lblYear0TMV']/text())").extract_first()

    



    try:
        driver.find_element_by_xpath("//a[contains(text(),'OWNERSHIP')]").click()
        time.sleep(3)
        html = driver.page_source
        resp = Selector(text=html)
        
        Owners = resp.xpath("normalize-space(//td[@id='lblowner1name']/text())").extract_first()
        mail_address = resp.xpath("//td[@id='lblowner1address']/text()").extract_first()
        mail_address1 = resp.xpath("//td[@id='lblowner1citystatezipcountry']/text()").extract_first()
        mail_address1 = str(mail_address1)
        try:
            mail_city = re.findall(r"^[^,]+",mail_address1)
            mail_state = re.findall(r"\s\w\w\s",mail_address1)
            mail_zip = re.findall(r"\d.*",mail_address1)
        except:
            mail_city = None
            mail_state = None
            mail_zip = None

    except:
        Owners = None
        mail_address = None
        mail_city = None
        mail_state = None
        mail_zip = None


    print() 
    print(f"Scraping ====>{a1}")
    print("parcel_id:",parcel_id)
    print("Owners:",Owners)
    print("site_address:",site_address)
    print("site_city:",site_city)
    print("site_state:",site_state)
    print("site_zip:",site_zip)
    print("mail_address:",mail_address)
    print("mail_city:",mail_city)
    print("mail_state:",mail_state)
    print("mail_zip:",mail_zip)
    print("land_value:",land_value)
    print("bldg_value:",bldg_value)
    print("TOAL_MARKET_VALUE:",TOAL_MARKET_VALUE)
    print("land_use_code:",land_use_code)
    print("land_size:",land_size)
    print("beds:",beds)
    print("baths:",baths)
    print("living_area:",living_area)    
    print("built_year:",built_year)
    print()
    
    with open('Scraped_Jackson county MO.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,a20,a21,a22,parcel_id,Owners,site_address,site_city,site_state,site_zip,mail_address,mail_city,mail_state,mail_zip,land_value,bldg_value,TOAL_MARKET_VALUE,built_year,living_area,beds,baths,land_size,land_use_code])
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
try:
    btn = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'I Agree')]")))
    btn.click()
except:
    print("Could n't click Agree")


with open("./Jackson county MO.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        try:
            company1 = str(i[1])
            company1 = company1.strip()
            search = driver.find_element_by_xpath("//input[@class='esri-input esri-search__input']")
            search.send_keys(Keys.CONTROL + "a")
            search.send_keys(Keys.DELETE)
            time.sleep(1)
            search.send_keys(company1)
            time.sleep(1)

            search.send_keys(Keys.ENTER)
            time.sleep(5)
            try:
                btns = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='esri-popup__button esri-popup__action']")))
                btns.click()
                time.sleep(2)
                count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16],i[17],i[18],i[19],i[20],i[21],i[22])
            except:
                count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16],i[17],i[18],i[19],i[20],i[21],i[22])
                None
        except:
            None
