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

ul = "https://iaspublicaccess.fultoncountyga.gov/search/commonsearch.aspx?mode=address"




def scrap(count,a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11):
    html = driver.page_source
    resp = Selector(text=html)
    
    parcel_id = resp.xpath("//td[contains(text(),'Parcel ID:')]/following-sibling::td/text()").extract_first()
    site_address = resp.xpath("//td[contains(text(),'Property Location:')]/following-sibling::td/text()").extract_first()
    site_city = resp.xpath("//td[contains(text(),'City:')]/following-sibling::td/text()").extract_first()
    Property_Class = resp.xpath("//td[contains(text(),'Property Class:')]/following-sibling::td/text()").extract_first()
    land_use_code = resp.xpath("//td[contains(text(),'Land Use Code:')]/following-sibling::td/text()").extract_first()
    Owners = resp.xpath("//td[contains(text(),'Owners:')]/following-sibling::td/text()").extract_first()
    mail_address = resp.xpath("//td[contains(text(),'Address')]/parent::tr/following-sibling::tr[1]/td/text()[last()-1]").extract_first()
    mail_address1 = resp.xpath("//td[contains(text(),'Address')]/parent::tr/following-sibling::tr[1]/td/text()[last()]").extract_first()
    mail_address1 = str(mail_address1)
    try:
        mail_city = re.findall(r"^([\w\-]+)",mail_address1)
        mail_state = re.findall(r"\s\w\w\s",mail_address1)
        mail_zip = re.findall(r"\s\b(\w+)$",mail_address1)
    except:
        mail_city = None
        mail_state = None
        mail_zip = None
    # iframe = driver.find_element_by_xpath("//iframe[@id='ifrDetails']")
    # driver.switch_to.frame(iframe)
    try:
        driver.find_element_by_xpath("//span[contains(text(),'Sales')]/parent::a").click()
        time.sleep(3)
        html = driver.page_source
        resp = Selector(text=html)

        sale_date = resp.xpath("//table[@id='Sales']/tbody/tr[2]/td[1]/text()").extract_first()
        sale_price = resp.xpath("//table[@id='Sales']/tbody/tr[2]/td[2]/text()").extract_first()

        driver.back()
        time.sleep(3)
    except:
        sale_date = None
        sale_price = None
    try:
        driver.find_element_by_xpath("(//span[contains(text(),'Values')])[1]/parent::a").click()
        time.sleep(3)
        html = driver.page_source
        resp = Selector(text=html)

        tex_year = resp.xpath("//table[@id='Appraised Values']/tbody/tr[2]/td[1]/text()").extract_first()
        land_value = resp.xpath("//table[@id='Appraised Values']/tbody/tr[2]/td[2]/text()").extract_first()
        bldg_value = resp.xpath("//table[@id='Appraised Values']/tbody/tr[2]/td[3]/text()").extract_first()
        total_market_value = resp.xpath("//table[@id='Appraised Values']/tbody/tr[2]/td[4]/text()").extract_first()

        driver.back()
        time.sleep(3)
    except:
        tex_year = None
        land_value = None
        bldg_value = None
        total_market_value = None
    try:
        driver.find_element_by_xpath("//span[contains(text(),'Land')]/parent::a").click()
        time.sleep(3)
        html = driver.page_source
        resp = Selector(text=html)

        land_type = resp.xpath("//td[contains(text(),'Land Type:')]/following-sibling::td/text()").extract_first()
        living_area = resp.xpath("//td[contains(text(),'Square Feet:')]/following-sibling::td/text()").extract_first()
        acres = resp.xpath("//td[contains(text(),'Acres:')]/following-sibling::td/text()").extract_first()

        driver.back()
        time.sleep(3)
    except:
        land_type = None
        living_area = None
        acres = None

    
    
    print()
    print(f"Scraping ====>{a8} {a9} {a10} {a11}")
    print("parcel_id:",parcel_id)
    print("site_address:",site_address)
    print("site_city:",site_city)
    print("Property_Class:",Property_Class)
    print("land_use_code:",land_use_code)
    print("Owners:",Owners)
    print("mail_address:",mail_address)
    print("mail_city:",mail_city)
    print("mail_state:",mail_state)
    print("mail_zip:",mail_zip)
    print("sale_date:",sale_date)
    print("sale_price:",sale_price)
    print("tex_year:",tex_year)
    print("land_value:",land_value)
    print("bldg_value:",bldg_value)
    print("total_market_value:",total_market_value)
    print("land_type:",land_type)
    print("living_area:",living_area)
    print("acres:",acres)

    print()
    
    with open('dataset_for_atlanta.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,parcel_id,site_address,site_city,Property_Class,land_use_code,Owners,mail_address,mail_city,mail_state,mail_zip,sale_date,sale_price,tex_year,land_value,bldg_value,total_market_value,land_type,living_area,acres])
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

driver.find_element_by_xpath("//button[contains(text(),'Agree')]").click()
time.sleep(3)





with open("./input.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company1 = str(i[8])
        company1 = company1.strip()
        company2 = str(i[9])
        company2 = company2.strip()
        company3 = str(i[10])
        company4 = str(i[11])
        search = driver.find_element_by_xpath("//input[@id='inpNumber']")
        search.clear()
        search.send_keys(company1)
        time.sleep(1)
        search1 = driver.find_element_by_xpath("//input[@id='inpStreet']")
        search1.clear()
        search1.send_keys(company2)
        time.sleep(1)
        suffix = f"//option[contains(text(),'{company3}')]"
        direction = f"//option[contains(text(),'{company4}')]"
        try:
            driver.find_element_by_xpath(suffix).click()
            time.sleep(1)
        except:
            None
        try:
            driver.find_element_by_xpath(direction).click()
            time.sleep(1)
        except:
            None
        search.send_keys(Keys.ENTER)
        time.sleep(5)
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
        
