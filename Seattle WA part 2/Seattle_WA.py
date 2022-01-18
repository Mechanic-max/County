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
# with open('test.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(["Parcel ID","owner_name","site_address","site_city","mail_address","mail_city","mail_state","mail_zip","land_value","bldg_value","total_market_value","property_type","Atucal_year_built","living_area","above_rooms","below_rooms","baths","sale_date","sale_price"])

ul = "https://blue.kingcounty.com/Assessor/eRealProperty/default.aspx"


def scrap(count,a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16):
    

    html = driver.page_source
    resp = Selector(text=html)

    parcel_id = resp.xpath("//td[contains(text(),'Parcel')]/following-sibling::td[1]/text()").extract_first()
    owner_name = resp.xpath("normalize-space(//td[contains(text(),'Name')]/following-sibling::td[1]/text())").extract_first()

    site_address = resp.xpath("normalize-space(//td[contains(text(),'Site Address')]/following-sibling::td[1]/text())").extract_first()
    site_address = str(site_address)
    try:
        site_zip = re.findall(r"\b(\w+)$",site_address)
    except:
        site_zip = ''
    
    for sit_zip in site_zip:
        site_address = site_address.replace(sit_zip,'')
        site_address = site_address.strip()
        sit_zip = sit_zip.strip()

    bldg_name = resp.xpath("//td[contains(text(),'Property Name')]/following-sibling::td[1]/text()").extract_first()
    property_type = resp.xpath("//td[contains(text(),'Property Type')]/following-sibling::td[1]/span/text()").extract_first()
    property_type = resp.xpath("normalize-space(//span[@id='cphContent_FormViewLegalDescription_LabelLegalDescription']/text())").extract_first()
    site_city = resp.xpath("normalize-space(//td[contains(text(),'Jurisdiction')]/following-sibling::td[1]/text())").extract_first()
    present_use = resp.xpath("normalize-space(//td[contains(text(),'Present Use')]/following-sibling::td[1]/text())").extract_first()
    land_area = resp.xpath("normalize-space(//td[contains(text(),'Land SqFt')]/following-sibling::td[1]/text())").extract_first()
    year_built = resp.xpath("normalize-space(//td[contains(text(),'Year Built')]/following-sibling::td[1]/text())").extract_first()
    Eff_built = resp.xpath("normalize-space(//td[contains(text(),'Eff. Year')]/following-sibling::td[1]/text())").extract_first()
    bldg_area = resp.xpath("normalize-space(//td[contains(text(),'Building Net Sq Ft')]/following-sibling::td[1]/text())").extract_first()
    land_value = resp.xpath("normalize-space(//th[contains(text(),'Appraised Land Value ($)')]/parent::tr/following-sibling::tr[1]/td[6]/text())").extract_first()
    bldg_value = resp.xpath("//th[contains(text(),'Appraised Land Value ($)')]/parent::tr/following-sibling::tr[1]/td[7]/text()").extract_first()
    total_value = resp.xpath("//th[contains(text(),'Appraised Land Value ($)')]/parent::tr/following-sibling::tr[1]/td[8]/text()").extract_first()
    sale_date = resp.xpath("//span[@id='cphContent_GridViewSales_lblSaleDate_0']/text()").extract_first()
    sale_price = resp.xpath("//span[@id='cphContent_GridViewSales_lblSaleDate_0']/parent::td/following-sibling::td[1]/text()").extract_first()
    
    
    print()
    print(f"Scraping=======>{a9}")
    print("parcel_id",parcel_id)
    print("Owner_Name",owner_name)
    print("site_address",site_address)
    print("site_city",site_city)
    print("site_zip",site_zip)
    print("bldg_name",bldg_name)
    print("present_use",present_use)
    print("year_built",year_built)
    print("Eff_built",Eff_built)
    print("property_type",property_type)
    print("land_area",land_area)
    print("bldg_area",bldg_area)
    print("land_value",land_value)
    print("bldg_value",bldg_value)
    print("total_value",total_value)
    print("sale_date",sale_date)
    print("sale_price",sale_price)
    print()
    
    
    
    with open('dataset_for_SEATTLE WA.csv', 'a', newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,parcel_id,owner_name,site_address,site_city,site_zip,bldg_name,present_use,year_built,Eff_built,property_type,land_area,bldg_area,land_value,bldg_value,total_value,sale_date,sale_price])
        count = count + 1
        print("Data Saved in CSV:",count)

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

with open("SEATTLE WA.csv", 'r',encoding='utf-8') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        try:
            driver.find_element_by_xpath("//input[@id='cphContent_checkbox_acknowledge']").click()
            time.sleep(5)
        except:
            print("Pop up didn't appear")
        company = str(i[9])
        company = company.strip()
        
        company1 = str(i[10])
        company1 = company1.strip()
        
        search = driver.find_element_by_xpath("//input[@id='cphContent_txtAddress']")
        search.send_keys(Keys.CONTROL + "a")
        search.send_keys(Keys.DELETE)
        time.sleep(1)
        search.send_keys(company)
        time.sleep(1)
        
        search1 = driver.find_element_by_xpath("//input[@id='cphContent_txtCity']")
        search1.send_keys(Keys.CONTROL + "a")
        search1.send_keys(Keys.DELETE)
        time.sleep(1)
        search1.send_keys(company1)
        time.sleep(1)
        
        driver.find_element_by_xpath("//input[@id='cphContent_btn_SearchAddress']").click()
        time.sleep(5)

        try:
            driver.find_element_by_xpath("//a[@id='cphContent_GridViewParcelList_LinkButtonParcel_0']").click()
            time.sleep(3)
        except:
            None

        count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16])
        driver.get(ul)
        time.sleep(7)
            
    
driver.close()
