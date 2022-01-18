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

ul = "https://payments.washco-md.net/MSS/citizens/RealEstate/Default.aspx?mode=new"




def scrap(count,a0,a1,a2,a3,a4,a5,a6,a7):
    try:
        driver.find_element_by_xpath("//a[contains(text(),'Property Detail')]").click()
        time.sleep(3)

        html = driver.page_source
        resp = Selector(text=html)
        parcel_id= resp.xpath("//span[@id='ctl00_ctl00_PrimaryPlaceHolder_ContentPlaceHolderMain_ParcelIdLabel']/text()").extract_first()
        site_address = resp.xpath("//span[@id='ctl00_ctl00_PrimaryPlaceHolder_ContentPlaceHolderMain_LocationLabel']/text()").extract_first()
        units = resp.xpath("//span[@id='ctl00_ctl00_PrimaryPlaceHolder_ContentPlaceHolderMain_UnitsLabel']/text()").extract_first()
    except:
        parcel_id = None
        site_address = None
        units = None
    
    try:
        driver.find_element_by_xpath("//a[contains(text(),'Owner Information')]").click()
        time.sleep(3)

        html = driver.page_source
        resp = Selector(text=html)
        Owners= resp.xpath("//span[@id='ctl00_ctl00_PrimaryPlaceHolder_ContentPlaceHolderMain_OwnerInformation1_OwnerInformationFormLayout_CustomerNameFormLayoutItem_ctl01_CustomerNameLabel']/text()").extract_first()
        mail_address = resp.xpath("//span[@id='ctl00_ctl00_PrimaryPlaceHolder_ContentPlaceHolderMain_OwnerInformation1_OwnerInformationFormLayout_CustomerAddressFormLayoutItem_ctl01_CustomerAddressLabel']/text()").extract_first()
        mail_address1 = resp.xpath("//span[@id='ctl00_ctl00_PrimaryPlaceHolder_ContentPlaceHolderMain_OwnerInformation1_OwnerInformationFormLayout_CityStateZipFormLayoutItem_ctl01_CityStateZipLabel']/text()").extract_first()
        mail_address1 = str(mail_address1)
        try:
            mail_city = re.findall(r"^([\w\-]+)",mail_address1)
            mail_state = re.findall(r"\s\w\w\s",mail_address1)
            mail_zip = re.findall(r"\d.*",mail_address1)
        except:
            mail_city = None
            mail_state = None
            mail_zip = None
    except:
        Owners = None
        mail_address = None
        mail_city = None
        mail_state = None
        mail_zip = None

    try:
        driver.find_element_by_xpath("//a[contains(text(),'Assessment')]").click()
        time.sleep(3)

        html = driver.page_source
        resp = Selector(text=html)
        land_value= resp.xpath("//th[contains(text(),'Land')]/following-sibling::td/text()").extract_first()
        bldg_value = resp.xpath("//th[contains(text(),'Building')]/following-sibling::td/text()").extract_first()
        TOAL_MARKET_VALUE = resp.xpath("(//th[contains(text(),'Total')]/following-sibling::td/text())[1]").extract_first()
    except:
        land_value = None
        bldg_value = None
        TOAL_MARKET_VALUE = None


    print() 
    print(f"Scraping ====>{a7}")
    print("parcel_id:",parcel_id)
    print("Owners:",Owners)
    print("units:",units)
    print("site_address:",site_address)
    print("mail_address:",mail_address)
    print("mail_city:",mail_city)
    print("mail_state:",mail_state)
    print("mail_zip:",mail_zip)
    print("land_value:",land_value)
    print("bldg_value:",bldg_value)
    print("TOAL_MARKET_VALUE:",TOAL_MARKET_VALUE)

    print()
    
    with open('Scraped_Hagerstown WV PIA List of Open Cases 1.1.2020 to 4.29.2021.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,a6,a7,parcel_id,Owners,units,site_address,mail_address,mail_city,mail_state,mail_zip,land_value,bldg_value,TOAL_MARKET_VALUE])
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

with open("./Hagerstown WV PIA List of Open Cases 1.1.2020 to 4.29.2021.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        try:            
            company1 = str(i[1])
            company1 = company1.strip()
            search = driver.find_element_by_xpath("//input[@id='ctl00_ctl00_PrimaryPlaceHolder_ContentPlaceHolderMain_Control_AddressSearchFieldLayout_ctl01_StreetNumberTextBox']")
            search.send_keys(Keys.CONTROL + "a")
            search.send_keys(Keys.DELETE)
            time.sleep(1)
            search.send_keys(company1)
            time.sleep(1)

            commpany2 = str(i[7])
            search1 = driver.find_element_by_xpath("//input[@id='ctl00_ctl00_PrimaryPlaceHolder_ContentPlaceHolderMain_Control_StreetNameSearchFieldLayout_ctl01_AddressTextBox']")
            search1.send_keys(Keys.CONTROL + "a")
            search1.send_keys(Keys.DELETE)
            time.sleep(1)
            search1.send_keys(commpany2)
            time.sleep(1)
            search.send_keys(Keys.ENTER)
            time.sleep(5)
            try:
                driver.find_element_by_xpath("//a[@id='ctl00_ctl00_PrimaryPlaceHolder_ContentPlaceHolderMain_ParcelsGridView_ctl02_ViewParcelButton']").click()
                time.sleep(3)
                driver.find_element_by_xpath("//a[@id='ctl00_ctl00_PrimaryPlaceHolder_ContentPlaceHolderMain_BillsGridView_ctl06_ViewBillLinkButton']").click()
                time.sleep(3)
                count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7])
            except:
                None
                count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7])
                
        except:
            None

        driver.get(ul)
        time.sleep(3)


