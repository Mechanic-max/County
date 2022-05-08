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

ul = "https://publicaccess.columbusga.org/search/commonsearch.aspx?mode=address"




def scrap(count,a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11):
    html = driver.page_source
    resp = Selector(text=html)

    parcel_id = resp.xpath("//td[contains(text(),'Parcel ID')]/following-sibling::td/text()").extract_first()
    site_address = resp.xpath("//td[contains(text(),'Situs')]/following-sibling::td/text()").extract_first()
    site_city = resp.xpath("normalize-space(//td[contains(text(),'Situs')]/parent::tr/following-sibling::tr/td[contains(text(),'City')]/following-sibling::td/text())").extract_first()
    site_zip_code = resp.xpath("normalize-space(//td[contains(text(),'Situs')]/parent::tr/following-sibling::tr/td[contains(text(),'Zip Code')]/following-sibling::td/text())").extract_first()
    Property_Class = resp.xpath("//td[contains(text(),'Class')]/following-sibling::td/text()").extract_first()
    Owners = resp.xpath("(//td[contains(text(),'Owner')])[2]/following-sibling::td/text()").extract_first()
    mail_address = resp.xpath("//td[contains(text(),'Address')]/following-sibling::td/text()").extract_first()
    mail_city = resp.xpath("normalize-space(//td[contains(text(),'Owner')]/parent::tr/following-sibling::tr/td[contains(text(),'City')]/following-sibling::td/text())").extract_first()
    mail_state = resp.xpath("//td[contains(text(),'Owner')]/parent::tr/following-sibling::tr/td[contains(text(),'State')]/following-sibling::td/text()").extract_first()
    mail_zip = resp.xpath("//td[contains(text(),'Owner')]/parent::tr/following-sibling::tr/td[contains(text(),'Zip Code')]/following-sibling::td/text()").extract_first()

    try:
        driver.find_element_by_xpath("//span[contains(text(),'Sales Information')]/parent::a").click()
        time.sleep(3)
        html = driver.page_source
        resp = Selector(text=html)

        sale_date = resp.xpath("//td[contains(text(),'Sale Date')]/following-sibling::td[@class='DataletData']/text()").extract_first()
        sale_price = resp.xpath("//td[contains(text(),'Sale Price')]/following-sibling::td[@class='DataletData']/text()").extract_first()

        driver.back()
        time.sleep(3)
    except:
        sale_date = None
        sale_price = None
    try:
        driver.find_element_by_xpath("(//span[contains(text(),'Property Values')])[1]/parent::a").click()
        time.sleep(3)
        html = driver.page_source
        resp = Selector(text=html)

        tex_year = resp.xpath("//td[contains(text(),'Tax Year')]/following-sibling::td/text()").extract_first()
        asmt = resp.xpath("//td[contains(text(),'Final ASMT')]/following-sibling::td/text()[1]").extract_first()

        driver.back()
        time.sleep(3)
    except:
        tex_year = None
        asmt = None
    try:
        driver.find_element_by_xpath("//span[contains(text(),'Residential')]/parent::a").click()
        time.sleep(3)
        html = driver.page_source
        resp = Selector(text=html)

        year_built = resp.xpath("//td[contains(text(),'Year Built')]/following-sibling::td/text()[1]").extract_first()
        living_area = resp.xpath("//td[contains(text(),'Living Area')]/following-sibling::td/text()").extract_first()
        bedrooms = resp.xpath("//td[contains(text(),'Bedrooms')]/following-sibling::td/text()").extract_first()
        half_bath = resp.xpath("//td[contains(text(),'Half Baths')]/following-sibling::td/text()").extract_first()
        full_bath = resp.xpath("//td[contains(text(),'Full Baths')]/following-sibling::td/text()").extract_first()

        driver.back()
        time.sleep(3)
    except:
        year_built = None
        living_area = None
        bedrooms = None
        half_bath = None
        full_bath = None

    
    
    print()
    print(f"Scraping ====>{a9} {a10} {a11}")
    print("parcel_id:",parcel_id)
    print("site_address:",site_address)
    print("site_city:",site_city)
    print("site_zip_code:",site_zip_code)
    print("Property_Class:",Property_Class)
    print("Owners:",Owners)
    print("mail_address:",mail_address)
    print("mail_city:",mail_city)
    print("mail_state:",mail_state)
    print("mail_zip:",mail_zip)
    print("sale_date:",sale_date)
    print("sale_price:",sale_price)
    print("tex_year:",tex_year)
    print("asmt:",asmt)
    print("year_built:",year_built)
    print("bedrooms:",bedrooms)
    print("living_area:",living_area)
    print("half_bath:",half_bath)
    print("full_bath:",full_bath)

    print()
    
    with open('dataset_for_columbus.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,parcel_id,Owners,site_address,site_city,site_zip_code,Property_Class,mail_address,mail_city,mail_state,mail_zip,sale_date,sale_price,tex_year,asmt,year_built,living_area,bedrooms,full_bath,half_bath])
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
    driver.find_element_by_xpath(("//button[contains(text(),'Agree')]")).click()
    time.sleep(3)
except:
    print("Pop up didn't appear")
with open("./input.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company1 = str(i[9])
        company1 = company1.strip()
        company2 = str(i[10])
        company2 = company2.strip()
        search = driver.find_element_by_xpath("//input[@id='inpNumber']")
        search.clear()
        search.send_keys(company1)
        time.sleep(1)
        search1 = driver.find_element_by_xpath("//input[@name='inpStreet']")
        search1.clear()
        search1.send_keys(company2)
        time.sleep(1)
        search.send_keys(Keys.ENTER)
        time.sleep(5)
        i[11] = str(i[11])
        i[11] = i[11].strip()
        suffix = f"//option[contains(text(),'{i[11]}')]"
        try:
            driver.find_element_by_xpath(suffix).click()
        except:
            None
        try:
            results = driver.find_elements_by_xpath("//tr[@class='SearchResults']")
            if len(results) != 0:
                for ri in range(0,len(results)):
                    driver.find_elements_by_xpath("//tr[@class='SearchResults']")[ri].click()
                    time.sleep(3)
                    count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11])
                    driver.back()
                    time.sleep(3)

            else:
                count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11])


        except:
            print("Search result is empty")
        
        driver.get(ul)
        time.sleep(2)
        
