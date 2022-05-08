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

ul = "https://beacon.schneidercorp.com/Application.aspx?AppID=979&LayerID=19792&PageTypeID=2&PageID=8661"


def scrap(count,a0,a1,a2,a3,a4,a5,a6,a7,a8):

    html = driver.page_source
    resp = Selector(text=html)

    owner_name = resp.xpath("normalize-space(//a[@id='ctlBodyPane_ctl01_ctl01_sprLnkOwnerName1_lnkUpmSearchLinkSuppressed_lnkSearch']/text())").extract_first()
    if owner_name:
        None
    else:
        owner_name = resp.xpath("normalize-space(//span[@id='ctlBodyPane_ctl01_ctl01_sprLnkOwnerName1_lnkUpmSearchLinkSuppressed_lblSearch']/text())").extract_first()
    site_address = resp.xpath("normalize-space(//span[@id='ctlBodyPane_ctl00_ctl01_lblLocationAddress']/text())").extract_first()
    mail_address =resp.xpath("//span[@id='ctlBodyPane_ctl01_ctl01_lblAddress2']/text()").extract_first()
    if mail_address:
        None
    else:
        mail_address = resp.xpath("normalize-space(//span[@id='ctlBodyPane_ctl01_ctl01_lblAddress1']/text())").extract_first()
    mail_city_state_zip = resp.xpath("normalize-space(//span[@id='ctlBodyPane_ctl01_ctl01_lblCityStZip']/text())").extract_first()
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
    property_type = resp.xpath("//span[@id='ctlBodyPane_ctl00_ctl01_lblPropertyClass']/text()").extract_first()
    land_area = resp.xpath("normalize-space(//span[@id='ctlBodyPane_ctl00_ctl01_lblLandArea']/text())").extract_first()
    tex_bill_no = resp.xpath("//span[@id='ctlBodyPane_ctl00_ctl01_lblTaxBillNumber']/text()").extract_first()
    living_area = resp.xpath("//span[@id='ctlBodyPane_ctl00_ctl01_lblBuildingArea']/text()").extract_first()
    lot_folio = resp.xpath("//span[@id='ctlBodyPane_ctl00_ctl01_lblLotFolio']/text()").extract_first()
    land_value = resp.xpath("//table[@id='ctlBodyPane_ctl04_ctl01_grdValuation']/tbody/tr[1]/td[2]/text()").extract_first()
    bldg_value = resp.xpath("//table[@id='ctlBodyPane_ctl04_ctl01_grdValuation']/tbody/tr[2]/td[2]/text()").extract_first()
    total_market_value = resp.xpath("//table[@id='ctlBodyPane_ctl04_ctl01_grdValuation']/tbody/tr[3]/td[2]/text()").extract_first()
    sale_date = resp.xpath("//table[@id='ctlBodyPane_ctl06_ctl01_gvwSales']/tbody/tr/th[1]/text()").extract_first()
    sale_price = resp.xpath("//table[@id='ctlBodyPane_ctl06_ctl01_gvwSales']/tbody/tr/td[1]/text()").extract_first()
    
    print()
    print(f"Scraping=======>{a3}")
    print("Owner_Name",owner_name)
    print("site_address",site_address)
    print("mail_address",mail_address)
    print("mail_city",mail_city)
    print("mail_state",ma_state)
    print("mail_zip",ma_zip)
    print("property_type",property_type)
    print("land_area",land_area)
    print("living_area",living_area)
    print("tex_bill_no",tex_bill_no)
    print("lot_folio",lot_folio)
    print("land_value",land_value)
    print("bldg_value",bldg_value)
    print("total_market_value",total_market_value)
    print("sale_date",sale_date)
    print("sale_price",sale_price)
    print()
    
    
    
    with open('dataset_for_New Orleans LA1.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,a6,a7,a8,owner_name,site_address,mail_address,mail_city,ma_state,ma_zip,land_value,bldg_value,total_market_value,property_type,land_area,living_area,tex_bill_no,lot_folio,sale_date,sale_price])
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
time.sleep(15)

try:
    driver.find_element_by_xpath("//a[contains(text(),'Agree')]").click()
    time.sleep(3)
except:
    print("Pop up didn't appear")

with open("New Orleans LA.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company = str(i[3])
        company = company.strip()
        search = driver.find_element_by_xpath("//input[@id='ctlBodyPane_ctl01_ctl01_txtAddress']")
        search.send_keys(Keys.CONTROL + "a")
        search.send_keys(Keys.DELETE)
        time.sleep(1)
        search.send_keys(company)
        time.sleep(1)
        search.send_keys(Keys.ENTER)
        time.sleep(15)
        results= driver.find_elements_by_xpath("//table[@id='ctlBodyPane_ctl00_ctl01_gvwParcelResults']/tbody/tr/th/label/a")
        if results!=[]:
            driver.find_elements_by_xpath("//table[@id='ctlBodyPane_ctl00_ctl01_gvwParcelResults']/tbody/tr/th/label/a")[0].click()
            time.sleep(4)
        count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8])
        driver.get(ul)
        time.sleep(20)
            
    
driver.close()
