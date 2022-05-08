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

ul = "https://wedge.hcauditor.org/"




def scrap(count,a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,a20,a21,a22,a23,a24):
    html = driver.page_source
    resp = Selector(text=html)

    parcel_id = resp.xpath("normalize-space(//span[contains(text(),'Parcel ID')]/parent::div/text()[2])").extract_first()
    site_address = resp.xpath("normalize-space(//span[contains(text(),'Address')]/parent::div/text()[2])").extract_first()
    Tax_Year = resp.xpath("normalize-space(//span[contains(text(),'Tax Year')]/parent::div/text()[2])").extract_first()
    Property_Class = resp.xpath("//div[contains(text(),'Land Use')]/following-sibling::div/text()").extract_first()

    Owners = resp.xpath("(//div[contains(text(),'Owner Name and Address')]/following-sibling::div/text())[1]").extract_first()
    Owners = str(Owners)
    Owners = Owners.strip()
    owner_name = re.findall(r"\A.*",Owners)
    ow = ''
    for ow in owner_name:
        ow = str(ow)
        Owners = Owners.replace(ow,'')
        Owners = Owners.strip()
    
    mail_address = re.findall(r"\A.*",Owners)
    ma = ''
    for ma in mail_address:
        ma = str(ma)
        Owners = Owners.replace(ma,'')
        Owners = Owners.strip()

    
    mail_state = re.findall(r"\s\w\w\s",Owners)
    me = ''
    for me in mail_state:
        me = str(me)
        Owners = Owners.replace(me,' ')
        Owners = Owners.strip()
    
    mail_zip = re.findall(r"\b(\w+)$",Owners)
    zip = ''
    for zip in mail_zip:
        zip = str(zip)
        Owners = Owners.replace(zip,'')
        Owners = Owners.strip()

    Owners = Owners.replace("\n",' ')
    year_built = resp.xpath("//td[contains(text(),'Year Built')]/following-sibling::td/text()").extract_first()
    living_area = resp.xpath("//td[contains(text(),'Acreage')]/following-sibling::td/text()").extract_first()
    bedrooms = resp.xpath("//td[contains(text(),'# Bedrooms')]/following-sibling::td/text()").extract_first()
    half_bath = resp.xpath("//td[contains(text(),'# Half Bathrooms')]/following-sibling::td/text()").extract_first()
    full_bath = resp.xpath("//td[contains(text(),'# Full Bathrooms')]/following-sibling::td/text()").extract_first()
    sale_date = resp.xpath("//td[contains(text(),'Last Transfer Date')]/following-sibling::td/text()").extract_first()
    sale_price = resp.xpath("//td[contains(text(),'Last Sale Amount')]/following-sibling::td/text()").extract_first()
    land_value = resp.xpath("//td[contains(text(),'Market Land Value')]/following-sibling::td/text()").extract_first()
    bldg_value = resp.xpath("//td[contains(text(),'Market Improvement Value')]/following-sibling::td/text()").extract_first()
    total_market_value = resp.xpath("//td[contains(text(),'Market Total Value')]/following-sibling::td/text()").extract_first()
    
    print()
    print(f"Scraping ====>{a1}")
    print("parcel_id:",parcel_id)
    print("site_address:",site_address)
    print("Property_Class:",Property_Class)
    print("Owners:",ow)
    print("mail_address:",ma)
    print("mail_city:",Owners)
    print("mail_state:",me)
    print("mail_zip:",zip)
    print("sale_date:",sale_date)
    print("sale_price:",sale_price)
    print("tex_year:",Tax_Year)
    print("year_built:",year_built)
    print("bedrooms:",bedrooms)
    print("living_area:",living_area)
    print("half_bath:",half_bath)
    print("full_bath:",full_bath)
    print("land_value:",land_value)
    print("bldg_value:",bldg_value)
    print("total_market_value:",total_market_value)
    print()
    
    with open('dataset_for_Cincinnati_OH.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,a20,a1,a22,a23,a24,parcel_id,ow,site_address,Property_Class,ma,Owners,me,zip,sale_date,sale_price,Tax_Year,year_built,living_area,bedrooms,full_bath,half_bath,land_value,bldg_value,total_market_value])
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
        company1 = str(i[2])
        company1 = company1.strip()
        company2 = str(i[3])
        company2 = company2.strip()
        search = driver.find_element_by_xpath("//input[@id='house_number_low']")
        search.clear()
        search.send_keys(company1)
        time.sleep(1)
        search1 = driver.find_element_by_xpath("//input[@id='street_name']")
        search1.clear()
        search1.send_keys(company2)
        time.sleep(1)
        search.send_keys(Keys.ENTER)
        time.sleep(5)
        count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16],i[17],i[18],i[19],i[20],i[21],i[22],i[23],i[24])
        driver.get(ul)
        time.sleep(2)
        
