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

ul = "https://www2.alleghenycounty.us/RealEstate/Search.aspx"




def scrap(count,a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19):
    html = driver.page_source
    resp = Selector(text=html)
    
    parcel_id = resp.xpath("normalize-space(//span[@id='BasicInfo1_lblParcelID']/text())").extract_first()


    Owners = resp.xpath("normalize-space(//span[@id='BasicInfo1_lblOwner']/text())").extract_first()
    site_address = resp.xpath("//span[@id='BasicInfo1_lblAddress']/text()[1]").extract_first()
    site_address1 = resp.xpath("normalize-space(//span[@id='BasicInfo1_lblAddress']/text()[2])").extract_first()
    site_address1 = str(site_address1)
    try:
        site_city = re.findall(r"^[^,]+,",site_address1)
        site_state = re.findall(r"\s\w\w\s",site_address1)
        site_zip = re.findall(r"\d.*",site_address1)
    except:
        site_city = None
        site_state = None
        site_zip = None



    property_class = resp.xpath("//span[@id='lblState']/text()").extract_first()
    land_area = resp.xpath("normalize-space(//span[@id='lblLot']/text())").extract_first()
    
    mail_address = resp.xpath("normalize-space(//span[@id='lblChangeMail']/text()[1])").extract_first()
    mail_address1 = resp.xpath("normalize-space(//span[@id='lblChangeMail']/text()[2])").extract_first()
    mail_address1 = str(mail_address1)
    
    
    try:
        mail_city = re.findall(r"^[^,]+,",mail_address1)
        mail_state = re.findall(r"\s\w\w\s",mail_address1)
        mail_zip = re.findall(r"\d.*",mail_address1)
    except:
        mail_city = None
        mail_state = None
        mail_zip = None
    


    sale_date = resp.xpath("normalize-space(//span[@id='lblSaleDate']/text())").extract_first()
    sale_price = resp.xpath("normalize-space(//span[@id='lblSalePrice']/text())").extract_first()
    

    land_value = resp.xpath("//span[@id='lblFullLand']/text()[1]").extract_first()
    bldg_value = resp.xpath("//span[@id='lblCountyBuild']/text()[1]").extract_first()
    total_market_value = resp.xpath("//span[@id='lblCountyTot']/text()[1]").extract_first()

    try:
        driver.find_element_by_xpath("//input[@id='Header1_lnkBuilding']").click()
        time.sleep(3)
        html = driver.page_source
        resp = Selector(text=html)
        living_area = resp.xpath("normalize-space(//span[@id='lblResLiveArea']/text())").extract_first()
        full_baths = resp.xpath("normalize-space(//span[@id='lblResFullBath']/text())").extract_first()
        haLf_baths = resp.xpath("normalize-space(//span[@id='lblResHalfBath']/text())").extract_first()
        built_year = resp.xpath("normalize-space(//span[@id='lblResYearBuilt']/text())").extract_first()
        bedrooms = resp.xpath("normalize-space(//span[@id='lblResBedrooms']/text())").extract_first()
    except:
        bedrooms = ''
        living_area = ''
        full_baths = ''
        haLf_baths = ''
        built_year = ''


    
    print()
    print(f"Scraping ====>{a9}")
    print("parcel_id:",parcel_id)
    print("Owners:",Owners)
    print("site_address:",site_address)
    print("site_city:",site_city)
    print("site_state:",site_state)
    print("site_zip:",site_zip)
    print("mail_address:",mail_address)
    print("mail_city:",mail_city)
    print("mail_state:",mail_state)
    print("mail_zip:",mail_zip)
    print("bedrooms:",bedrooms)
    print("full_baths:",full_baths)
    print("haLf_baths:",haLf_baths)
    print("land_area:",land_area)
    print("property_class:",property_class)
    print("sale_date:",sale_date)
    print("sale_price:",sale_price)
    print("land_value:",land_value)
    print("bldg_value:",bldg_value)
    print("total_market_value:",total_market_value)
    print("living_area:",living_area)    
    print("built_year:",built_year)
    print()
    
    with open('dataset_for_pittsburgh pa2.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,parcel_id,Owners,site_address,site_city,site_state,site_zip,mail_address,mail_city,mail_state,mail_zip,land_area,property_class,sale_date,sale_price,land_value,bldg_value,total_market_value,living_area,bedrooms,full_baths,haLf_baths,built_year])
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
time.sleep(5)


with open("./pittsburgh pa2.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        try:
            driver.find_element_by_xpath("//input[@id='radio1_1']").click()
            time.sleep(3)
            company1 = str(i[9])
            company1 = company1.strip()
            search = driver.find_element_by_xpath("//input[@id='txtParcelIDFull']")
            search.send_keys(Keys.CONTROL + "a")
            search.send_keys(Keys.DELETE)
            time.sleep(1)
            search.send_keys(company1)
            time.sleep(1)
            search.send_keys(Keys.ENTER)
            time.sleep(10)
        except:
            None
        

        count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16],i[17],i[18],i[19])



        driver.get(ul)
        time.sleep(3)


