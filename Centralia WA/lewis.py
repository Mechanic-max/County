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

ul = "https://parcels.lewiscountywa.gov/"




def scrap(count,a0,a1,a2,a3,a4):
    html = driver.page_source
    resp = Selector(text=html)
    
    parcel_id = resp.xpath("normalize-space(//dl[@id='top-information']/dt[contains(text(),'Parcel Number')]/following-sibling::dd/strong/text())").extract_first()
    Owners = resp.xpath("//dl[@id='top-information']/dt[contains(text(),'Owner')]/following-sibling::dd[1]/a/text()").extract_first()
    Account_id = resp.xpath("//dl[@id='top-information']/dt[contains(text(),'Account #')]/following-sibling::dd[1]/a/text()").extract_first()
    site_address = resp.xpath("normalize-space(//dl[@id='top-information']/dt[contains(text(),'Address')]/following-sibling::dd/text())").extract_first()
    site_address = str(site_address)
    try:
        site_city = re.findall(r"\b(\w+)$",site_address)
    except:
        None

    si = ''
    for si in site_city:
        si = str(si)
        site_address = site_address.replace(si,'')
        site_address = site_address.strip()

    mail_address = resp.xpath("normalize-space(//dt[contains(text(),'Owner')]/following-sibling::dd[@class='text-capitalize']/text()[last()-1])").extract_first()
    mail_address1 = resp.xpath("normalize-space(//dt[contains(text(),'Owner')]/following-sibling::dd[@class='text-capitalize']/text()[last()])").extract_first()
    mail_address1 = str(mail_address1)
    try:
        mail_city = re.findall(r"^([\w\-]+)",mail_address1)
        mail_state = re.findall(r"\s\w\w\s",mail_address1)
        mail_zip = re.findall(r"\b(\w+)$",mail_address1)
    except:
        mail_city = None
        mail_state = None
        mail_zip = None

    try:
        driver.find_element_by_xpath("//a[contains(text(),'Property Values')]/parent::li/a").click()
        time.sleep(3)
        html = driver.page_source
        resp = Selector(text=html)
        tex_year = resp.xpath("//th[contains(text(),'Tax Year')]/ancestor::thead/following-sibling::tbody/tr[1]/td[1]/text()").extract_first()
        land_value = resp.xpath("//th[contains(text(),'Tax Year')]/ancestor::thead/following-sibling::tbody/tr[1]/td[3]/text()").extract_first()
        bldg_value = resp.xpath("//th[contains(text(),'Tax Year')]/ancestor::thead/following-sibling::tbody/tr[1]/td[4]/text()").extract_first()
        total_market_value = resp.xpath("//th[contains(text(),'Tax Year')]/ancestor::thead/following-sibling::tbody/tr[1]/td[6]/text()").extract_first()
    except:
        tex_year = None
        land_value = None
        bldg_value = None
        total_market_value = None
    try:
        driver.find_element_by_xpath("//a[contains(text(),'Sales History')]").click()
        time.sleep(3)
        html = driver.page_source
        resp = Selector(text=html)
        sale_date = resp.xpath("//th[contains(text(),'Buyer')]/ancestor::thead/following-sibling::tbody/tr[1]/td[1]/text()").extract_first()
        sale_price = resp.xpath("//th[contains(text(),'Buyer')]/ancestor::thead/following-sibling::tbody/tr[1]/td[2]/text()").extract_first()
    except:
        sale_date = None
        sale_price = None
    try:
        driver.find_element_by_xpath("//a[contains(text(),'Building/Land')]").click()
        time.sleep(3)
        html = driver.page_source
        resp = Selector(text=html)
        property_type = resp.xpath("//th[contains(text(),'Building Type')]/ancestor::thead/following-sibling::tbody/tr[1]/td[1]/text()").extract_first()
        if property_type:
            living_area = resp.xpath("//th[contains(text(),'Building Type')]/ancestor::thead/following-sibling::tbody/tr[1]/td[last()]/text()").extract_first()
            baths = None
            built_year = resp.xpath("//th[contains(text(),'Building Type')]/ancestor::thead/following-sibling::tbody/tr[1]/td[4]/text()").extract_first()
            bedrooms = None
        else:
            living_area = resp.xpath("//dt[contains(text(),'Main Finished Area')]/following-sibling::dd/text()[1]").extract_first()
            baths = resp.xpath("normalize-space(//dt[contains(text(),'Bathrooms')]/following-sibling::dd/text()[1])").extract_first()
            built_year = resp.xpath("//dt[contains(text(),'Year Built')]/following-sibling::dd/text()[1]").extract_first()
            bedrooms = resp.xpath("normalize-space(//dt[contains(text(),'Bedrooms')]/following-sibling::dd/text()[1])").extract_first()
    except:
        property_type = None
        living_area = None
        baths = None
        built_year = None
        bedrooms = None







    
    print()
    print(f"Scraping ====>{a2}")
    print("parcel_id:",parcel_id)
    print("Account_id:",Account_id)
    print("Owners:",Owners)
    print("site_address:",site_address)
    print("site_city:",si)
    print("mail_address:",mail_address)
    print("mail_city:",mail_city)
    print("mail_state:",mail_state)
    print("mail_zip:",mail_zip)
    print("tex_year:",tex_year)
    print("land_value:",land_value)
    print("bldg_value:",bldg_value)
    print("total_market_value:",total_market_value)
    print("sale_date:",sale_date)
    print("sale_price:",sale_price)
    print("Property_TYPE:",property_type)
    print("living_area:",living_area)
    print("baths:",baths)
    print("built_year:",built_year)
    print("bedrooms:",bedrooms)
    print()
    
    with open('dataset_for_canton.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,parcel_id,Account_id,Owners,site_address,si,mail_address,mail_city,mail_state,mail_zip,tex_year,land_value,bldg_value,total_market_value,sale_date,sale_price,property_type,living_area,bedrooms,baths,built_year])
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
time.sleep(5)


with open("./input.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company1 = i[2]
        company1 = str(company1)
        search = driver.find_element_by_xpath("//input[@id='q']")
        search.send_keys(Keys.CONTROL + "a")
        search.send_keys(Keys.DELETE)
        time.sleep(1)
        search.send_keys(company1)
        time.sleep(1)
        search.send_keys(Keys.ENTER)
        time.sleep(5)
        try:
            result = driver.find_elements_by_xpath("//th[contains(text(),'Parcel Number')]/parent::tr/parent::thead/following-sibling::tbody/tr")
            if len(result) != 0:
                driver.find_elements_by_xpath("//th[contains(text(),'Parcel Number')]/parent::tr/parent::thead/following-sibling::tbody/tr")[0].click()
                count = scrap(count,i[0],i[1],i[2],i[3],i[4])
            else:
                count = scrap(count,i[0],i[1],i[2],i[3],i[4])
        except:
            print("Search result is empty")
        
        driver.get(ul)
        time.sleep(4)
        