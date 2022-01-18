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

ul = "https://atip.piercecountywa.gov/#/app/parcelSearch/search"


def scrap(count,a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14):

    html = driver.page_source
    resp = Selector(text=html)
    
    Parcel = resp.xpath("normalize-space((//h3[@class='inline ng-binding'])[1]/text())").extract_first()
    owner_name = resp.xpath("normalize-space(//td[contains(text(),'Taxpayer Name')]/following-sibling::td[1]/text())").extract_first()
    mail_address = resp.xpath("normalize-space(//td[contains(text(),'Mailing Address')]/following-sibling::td[1]/text()[2])").extract_first()
    mail_city_state_zip = resp.xpath("normalize-space(//td[contains(text(),'Mailing Address')]/following-sibling::td/text()[last()-1])").extract_first()
    mail_zip = resp.xpath("normalize-space(//td[contains(text(),'Mailing Address')]/following-sibling::td/text()[last()])").extract_first()
    mail_state = ''
    mail_city_state_zip = str(mail_city_state_zip)
    try:
        ma_state = re.findall(r"\s\w\w",mail_city_state_zip)
    except:
        ma_state = ''




    for mail_state in ma_state:
        mail_state = str(mail_state)
        mail_state = mail_state.strip()
        mail_city_state_zip = mail_city_state_zip.replace(mail_state,'')
        mail_city_state_zip = mail_city_state_zip.strip()

    site_address = resp.xpath("normalize-space(//td[contains(text(),'Site Address')]/following-sibling::td[1]/text())").extract_first()
    taxable_value = resp.xpath("normalize-space(//td[contains(text(),'Taxable Value')]/following-sibling::td[1]/text())").extract_first()
    assessed_value = resp.xpath("normalize-space(//td[contains(text(),'Assessed Value')]/following-sibling::td[1]/text())").extract_first()

    property_use = resp.xpath("normalize-space(//td[contains(text(),'Use Code')]/following-sibling::td[1]/text())").extract_first()
    

    try:
        driver.find_element_by_xpath("//a[contains(text(),'Taxes/Values')]").click()
        time.sleep(5)
        html = driver.page_source
        resp = Selector(text=html)
        land_value = resp.xpath("//td[contains(text(),'Assessed Land')]/following-sibling::td[1]/text()").extract_first()
        bldg_value = resp.xpath("//td[contains(text(),'Assessed Improvements')]/following-sibling::td[1]/text()").extract_first()
    except:
        land_value = ''
        bldg_value = ''

    try:
        driver.find_element_by_xpath("//a[contains(text(),'Land')]").click()
        time.sleep(5)
        html = driver.page_source
        resp = Selector(text=html)
        acers = resp.xpath("//td[contains(text(),'Acres')]/following-sibling::td[1]/text()").extract_first()
        
    except:
        acers = ''
    
    try:
        driver.find_element_by_xpath("//a[contains(text(),'Building')]").click()
        time.sleep(5)
        html = driver.page_source
        resp = Selector(text=html)
        
        property_type = resp.xpath("//label[contains(text(),'Occupancy')]/parent::div/following-sibling::div/text()").extract_first()
        built_year = resp.xpath("//td[@data-label='Year Built']/text()").extract_first()
        living_area = resp.xpath("//td[@data-label='Square Feet']/text()").extract_first()
        Bedrooms = resp.xpath("//td[@data-label='Bedrooms']/text()").extract_first()
        Bathrooms = resp.xpath("//td[@data-label='Bathrooms']/text()").extract_first()
        
    except:
        built_year = ''
        living_area = ''
        property_type = ''
        Bedrooms = ''
        Bathrooms = ''


    try:
        driver.find_element_by_xpath("//a[contains(text(),'Sales')]").click()
        time.sleep(5)
        html = driver.page_source
        resp = Selector(text=html)
        sale_date = resp.xpath("normalize-space(//td[@data-label='Sale Date']/text())").extract_first()
        sale_price = resp.xpath("normalize-space(//td[@data-label='Sale Price']/text())").extract_first()
        
    except:
        sale_date = ''
        sale_price = ''

    print()
    print(f"Scraping ====>{a3}")
    print("Parcel:",Parcel)
    print("owner_name:",owner_name)
    print("site_address:",site_address)
    print("mail_address:",mail_address)
    print("mail_city:",mail_city_state_zip)
    print("mail_state:",mail_state)
    print("mail_zip:",mail_zip)
    print("property_use:",property_use)
    print("taxable_value:",taxable_value)
    print("land_value:",land_value)
    print("bldg_value:",bldg_value)
    print("assessed_value:",assessed_value)
    print("acers:",acers)
    print("living_area:",living_area)    
    print("property_type:",property_type)    
    print("built_year:",built_year)
    print("Bedrooms:",Bedrooms)
    print("Bathrooms:",Bathrooms)
    print("sale_date:",sale_date)
    print("sale_price:",sale_price)
    print()
    
    with open('dataset_for_TACOMA WA.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,Parcel,owner_name,site_address,mail_address,mail_city_state_zip,mail_state,mail_zip,property_use,taxable_value,land_value,bldg_value,assessed_value,acers,living_area,property_type,built_year,Bedrooms,Bathrooms,sale_date,sale_price])
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

with open("./TACOMA WA.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:

        company = str(i[3])
        company = company.strip()
        search = driver.find_element_by_xpath("//input[@name='searchInput']")
        search.send_keys(Keys.CONTROL + "a")
        search.send_keys(Keys.DELETE)
        time.sleep(1)
        search.send_keys(company)
        time.sleep(1)
        search.send_keys(Keys.ENTER)
        time.sleep(15)

        count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14])
        driver.get(ul)
        time.sleep(7)
