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

ul = "https://property.spatialest.com/nc/mecklenburg#/"




def scrap(count,a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11):
    html = driver.page_source
    resp = Selector(text=html)
    
    parcel_id = resp.xpath("normalize-space(//span[contains(text(),'PARCEL ')]/text())").extract_first()
    Owners = resp.xpath("//div[@class='mailing']/div/text()[1]").extract_first()
    site_address = resp.xpath("//div[@class='location text-highlight']/span/text()").extract_first()
    site_address = str(site_address)
    try:
        site_state = re.findall(r"\b(\w+)$",site_address)
    except:
        site_state = None
    
    for j in site_state:
        j = str(j)
        site_address = site_address.replace(j,'')
        site_address = site_address.strip()
    try:
        site_city = re.findall(r"\b(\w+)$",site_address)
    except:
        site_city = None
    
    for j1 in site_city:
        j1 = str(j1)
        site_address = site_address.replace(j1,'')
        site_address = site_address.strip()
    
    Property_TYPE = resp.xpath("//span[contains(text(),'Land Use Desc')]/following-sibling::span/text()").extract_first()

    land_value = resp.xpath("//span[contains(text(),'Land Value')]/following-sibling::span/text()").extract_first()
    bldg_value = resp.xpath("//span[contains(text(),'Building Value')]/following-sibling::span/text()").extract_first()
    total_market_value = resp.xpath("(//span[contains(text(),'Total')]/following-sibling::span/text())[1]").extract_first()

    
    mail_address = resp.xpath("//div[@class='mailing']/div/text()[last()-1]").extract_first()
    mail_address1 = resp.xpath("//div[@class='mailing']/div/text()[last()]").extract_first()
    mail_address1 = str(mail_address1)
    try:
        mail_city = re.findall(r"^([\w\-]+)",mail_address1)
        mail_state = re.findall(r"\s\w\w\s",mail_address1)
        mail_zip = re.findall(r"\b(\w+)$",mail_address1)
    except:
        mail_city = None
        mail_state = None
        mail_zip = None



    sale_date = resp.xpath("//span[contains(text(),'Last Sale Date')]/following-sibling::span/text()").extract_first()
    sale_price = resp.xpath("//span[contains(text(),'Last Sale Price')]/following-sibling::span/text()").extract_first()

    living_area = resp.xpath("//span[contains(text(),'Total (SqFt)')]/following-sibling::span/text()").extract_first()
    baths = resp.xpath("//span[contains(text(),'Full Bath(s)')]/following-sibling::span/text()").extract_first()
    half_baths = resp.xpath("//span[contains(text(),'Half Bath(s)')]/following-sibling::span/text()").extract_first()
    built_year = resp.xpath("//span[contains(text(),'Year Built')]/following-sibling::span/text()").extract_first()
    bedrooms = resp.xpath("//span[contains(text(),'Bedroom(s)')]/following-sibling::span/text()").extract_first()


    
    print()
    print(f"Scraping ====>{a4}")
    print("parcel_id:",parcel_id)
    print("Owners:",Owners)
    print("site_address:",site_address)
    print("site_city:",site_city)
    print("site_state:",site_state)
    print("mail_address:",mail_address)
    print("mail_city:",mail_city)
    print("mail_state:",mail_state)
    print("mail_zip:",mail_zip)
    print("land_value:",land_value)
    print("bldg_value:",bldg_value)
    print("total_market_value:",total_market_value)
    print("sale_date:",sale_date)
    print("sale_price:",sale_price)
    print("Property_TYPE:",Property_TYPE)
    print("living_area:",living_area)    
    print("Full baths:",baths)
    print("half_baths:",half_baths)
    print("built_year:",built_year)
    print("bedrooms:",bedrooms)
    print()
    
    with open('dataset_for_canton.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,parcel_id,Owners,site_address,site_city,site_state,mail_address,mail_city,mail_state,mail_zip,land_value,bldg_value,total_market_value,sale_date,sale_price,Property_TYPE,living_area,bedrooms,baths,half_baths,built_year])
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
        company1 = i[4]
        company1 = str(company1)
        if len(company1) == 7:
            company1 = f"0{company1}"
        search = driver.find_element_by_xpath("//input[@id='primary_search']")
        search.send_keys(Keys.CONTROL + "a")
        search.send_keys(Keys.DELETE)
        time.sleep(1)
        search.send_keys(company1)
        time.sleep(1)
        search.send_keys(Keys.ENTER)
        time.sleep(20)
        count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11])