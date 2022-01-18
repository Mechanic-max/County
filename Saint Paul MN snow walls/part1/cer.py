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

ul = "https://beacon.schneidercorp.com/application.aspx?AppID=959&LayerID=18852&PageTypeID=2&PageID=8395&KeyValue=262922120035"


def scrap(count,a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15):

    html = driver.page_source
    resp = Selector(text=html)

    parcel_id = resp.xpath("//span[@id='ctlBodyPane_ctl01_ctl01_lblParcelID']/text()").extract_first()
    owner_name = resp.xpath("normalize-space(//th[contains(text(),'Owner')]/following-sibling::td[1]/text())").extract_first()

    site_address = resp.xpath("normalize-space(//span[@id='ctlBodyPane_ctl01_ctl01_lblPropertyAddress']/text()[1])").extract_first()
    site_address1 = resp.xpath("normalize-space(//span[@id='ctlBodyPane_ctl01_ctl01_lblPropertyAddress']/text()[2])").extract_first()
    site_address1 = str(site_address1)
    try:
        site_state = re.findall(r"\s\w\w\s",site_address1)
        site_city = re.findall(r"^[^,]+",site_address1)
        site_zip = re.findall(r"\d.*",site_address1)
    except:
        site_state = ''
        site_city = ''
        site_zip = ''
    

    mail_address =resp.xpath("normalize-space(//th[contains(text(),'Owner')]/following-sibling::td[2]/text()[1])").extract_first()

    mail_city_state_zip = resp.xpath("normalize-space(//th[contains(text(),'Owner')]/following-sibling::td[2]/text()[2])").extract_first()
    mail_city_state_zip = str(mail_city_state_zip)
    try:
        mail_state = re.findall(r"\s\w\w\s",mail_city_state_zip)
        mail_zip = re.findall(r"\d.*",mail_city_state_zip)
    except:
        mail_state = None
        mail_zip = None

    mail_city = ''
    ma_state = ''
    ma_zip = ''
    for ma_state in mail_state:
        ma_state = str(ma_state)
        mail_city_state_zip = mail_city_state_zip.replace(ma_state,'')
        mail_city_state_zip = mail_city_state_zip.strip()
    for ma_zip in mail_zip:
        ma_zip = str(ma_zip)
        mail_city_state_zip = mail_city_state_zip.replace(ma_zip,'')
        mail_city_state_zip = mail_city_state_zip.strip()
    mail_city = mail_city_state_zip
    
    
    property_type = resp.xpath("//span[@id='ctlBodyPane_ctl01_ctl01_lblRollType']/text()").extract_first()
    land_area = resp.xpath("normalize-space(//span[@id='ctlBodyPane_ctl01_ctl01_lblParcelArea']/text())").extract_first()
    land_use_code = resp.xpath("normalize-space(//span[@id='ctlBodyPane_ctl01_ctl01_lblLandUse']/text()[1])").extract_first()
    Estimated_market_value = resp.xpath("//th[contains(text(),'Estimated Market Value')]/following-sibling::td[1]/text()").extract_first()
    Taxable_market_value = resp.xpath("//th[contains(text(),'Taxable Market Value')]/following-sibling::td[1]/text()").extract_first()
    sale_date = resp.xpath("//table[@id='ctlBodyPane_ctl09_ctl01_gvwSales']/tbody/tr[1]/th[1]/text()").extract_first()
    sale_price = resp.xpath("//table[@id='ctlBodyPane_ctl09_ctl01_gvwSales']/tbody/tr[1]/td[2]/text()").extract_first()
    
    print()
    print(f"Scraping=======>{a3}")
    print("parcel_id",parcel_id)
    print("Owner_Name",owner_name)
    print("site_address",site_address)
    print("site_city",site_city)
    print("site_state",site_state)
    print("site_zip",site_zip)
    print("mail_address",mail_address)
    print("mail_city",mail_city)
    print("mail_state",ma_state)
    print("mail_zip",ma_zip)
    print("property_type",property_type)
    print("land_area",land_area)
    print("land_use_code",land_use_code)
    print("Estimated_market_value",Estimated_market_value)
    print("Taxable_market_value",Taxable_market_value)
    print("sale_date",sale_date)
    print("sale_price",sale_price)
    print()
    
    
    
    with open('dataset_for_Saint Paul MN snow_walks_2020.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,parcel_id,owner_name,site_address,site_city,site_state,site_zip,mail_address,mail_city,ma_state,ma_zip,property_type,land_area,land_use_code,Estimated_market_value,Taxable_market_value,sale_date,sale_price])
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

try:
    driver.find_element_by_xpath("//a[contains(text(),'Agree')]").click()
    time.sleep(3)
except:
    print("Pop up didn't appear")

with open("Saint Paul MN snow_walks_2020.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company = str(i[2])
        company = company.strip()
        search = driver.find_element_by_xpath("//input[@id='ctlBodyPane_ctl01_ctl01_txtAddress']")
        search.send_keys(Keys.CONTROL + "a")
        search.send_keys(Keys.DELETE)
        time.sleep(1)
        search.send_keys(company)
        time.sleep(1)
        search.send_keys(Keys.ENTER)
        time.sleep(15)
        try:
            driver.find_element_by_xpath("//th[contains(text(),'Parcel ID')]/ancestor::thead/following-sibling::tbody/tr[1]//a[@id='ctlBodyPane_ctl00_ctl01_gvwParcelResults_ctl02_lnkParcelID']").click()
            time.sleep(3)
        except:
            None
        count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15])
        driver.get(ul)
        time.sleep(7)
            
    
driver.close()
