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

ul = "https://www.tad.org/property-search/"




def scrap(count,a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,a20,a21):
    html = driver.page_source
    resp = Selector(text=html)
    
    parcel_id = resp.xpath("normalize-space(//span[@class='account']/text())").extract_first()

    Owners = resp.xpath("normalize-space(//div[@class='ownerInfo']/p[2]/a/text())").extract_first()
    site_address = resp.xpath("normalize-space(//strong[contains(text(),'Property Address:')]/following-sibling::span/text())").extract_first()
    site_city = resp.xpath("//strong[contains(text(),'City:')]/following-sibling::span/text()").extract_first()
    site_zip_code = resp.xpath("//strong[contains(text(),'Zipcode:')]/following-sibling::span/text()").extract_first()
    property_type = resp.xpath("//strong[contains(text(),'State Code:')]/parent::p/text()").extract_first()
    built_year = resp.xpath("//strong[contains(text(),'Year Built:')]/parent::p/text()").extract_first()
    mail_address = resp.xpath("//div[@class='ownerInfo']/p/following-sibling::div/span/a/text()").extract_first()
    mail_city = resp.xpath("//div[@class='ownerInfo']/p/following-sibling::div/span[2]/text()").extract_first()
    mail_state = resp.xpath("//div[@class='ownerInfo']/p/following-sibling::div/span[3]/text()").extract_first()
    mail_zip = resp.xpath("//div[@class='ownerInfo']/p/following-sibling::div/span[4]/text()").extract_first()
    land_value = resp.xpath("(//td[@data-label='Land Market'])[1]/text()").extract_first()
    bldg_value = resp.xpath("(//td[@data-label='Improvement Market'])[1]/text()").extract_first()
    total_market_value = resp.xpath("(//td[@data-label='Total Market'])[1]/text()").extract_first()
    living_area = resp.xpath("normalize-space(//strong[contains(text(),'Land Sqft ')]/parent::p/text())").extract_first()
    sale_date = resp.xpath("normalize-space(//strong[contains(text(),'Deed Date:')]/parent::p/text())").extract_first()


    print()
    print(f"Scraping ====>{a6}")
    print("parcel_id:",parcel_id)
    print("Owners:",Owners)
    print("site_address:",site_address)
    print("site_city:",site_city)
    print("mail_zip:",site_zip_code)
    print("property_type:",property_type)
    print("mail_address:",mail_address)
    print("mail_city:",mail_city)
    print("mail_state:",mail_state)
    print("mail_zip:",mail_zip)
    print("land_value:",land_value)
    print("bldg_value:",bldg_value)
    print("total_market_value:",total_market_value)
    print("sale_date:",sale_date)
    print("living_area:",living_area)    
    print("built_year:",built_year)
    print()
    
    with open('dataset_for_fort_worth.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,a20,a21,parcel_id,Owners,site_address,site_city,site_zip_code,mail_address,mail_city,mail_state,mail_zip,land_value,bldg_value,total_market_value,sale_date,living_area,built_year])
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
        company1 = str(i[6])
        company1 = company1.strip()
        search = driver.find_element_by_xpath("//input[@class='ardent-html-input simple_search_field ardent-html-input-text']")
        search.send_keys(Keys.CONTROL + "a")
        search.send_keys(Keys.DELETE)
        time.sleep(1)
        search.send_keys(company1)
        time.sleep(1)
        search.send_keys(Keys.ENTER)
        time.sleep(3)



        res = driver.find_elements_by_xpath("//td[@data-label='Account #']/a")
        if len(res) !=0:
            for ri in range(0,len(res)):
                driver.find_elements_by_xpath("//td[@data-label='Account #']/a")[ri].click()
                time.sleep(10)
                count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16],i[17],i[18],i[19],i[20],i[21])
                driver.back()
                time.sleep(3)
        else:
            count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16],i[17],i[18],i[19],i[20],i[21])



        driver.get(ul)
        time.sleep(3)


