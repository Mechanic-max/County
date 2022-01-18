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

ul = "https://taxcama.guilfordcountync.gov/camapwa/"




def scrap(count,a0,a1,a2,a3):
    html = driver.page_source
    resp = Selector(text=html)
    
    parcel_id = resp.xpath("normalize-space(//span[@id='ctl00_PageHeader1_PinLabelInfo']/text())").extract_first()
    Owners = resp.xpath("normalize-space(//table[@id='ctl00_PageHeader1_DetailsView1']/tbody/tr[1]/td/text())").extract_first()
    site_address = resp.xpath("//span[@id='ctl00_PageHeader1_LocationAddressLabelInfo']/text()").extract_first()
    mail_address = resp.xpath("//span[@id='ctl00_PageHeader1_DetailsView4_Mail1']/text()").extract_first()
    mail_city = resp.xpath("//span[@id='ctl00_PageHeader1_DetailsView4_City']/text()").extract_first()
    mail_state = resp.xpath("//span[@id='ctl00_PageHeader1_DetailsView4_Label1']/text()").extract_first()
    mail_zip = resp.xpath("//span[@id='ctl00_PageHeader1_DetailsView4_Label2']/text()").extract_first()
    sale_date = resp.xpath("normalize-space(//span[@id='ctl00_ContentPlaceHolder1_DetailsView6_Label5']/text())").extract_first()
    sale_price = resp.xpath("normalize-space(//span[@id='ctl00_ContentPlaceHolder1_DetailsView6_Label6']/text())").extract_first()
    land_value = resp.xpath("normalize-space(//span[@id='ctl00_ContentPlaceHolder1_DetailsView8_TotalLandValueAssessed']/text())").extract_first()
    bldg_value = resp.xpath("normalize-space(//span[@id='ctl00_ContentPlaceHolder1_DetailsView8_TotalBldgValueAssessed']/text())").extract_first()
    TOAL_MARKET_VALUE = resp.xpath("normalize-space(//span[@id='ctl00_ContentPlaceHolder1_DetailsView8_CostValue']/text())").extract_first()
    living_area = resp.xpath("normalize-space(//span[@id='ctl00_ContentPlaceHolder1_DetailsView7_Label4']/text())").extract_first()

    land_class = resp.xpath("//span[@id='ctl00_ContentPlaceHolder1_DetailsView5_Label12']/text()").extract_first()


    try:
        driver.find_element_by_xpath("//a[contains(text(),'Buildings')]").click()
        time.sleep(3)
        html = driver.page_source
        resp = Selector(text=html)
        
        bedroomms = resp.xpath("normalize-space(//span[@id='ctl00_ContentPlaceHolder1_DetailsView3_Label12']/text())").extract_first()
        full_baths = resp.xpath("normalize-space(//span[@id='ctl00_ContentPlaceHolder1_DetailsView3_Label34']/text())").extract_first()
        half_baths = resp.xpath("normalize-space(//span[@id='ctl00_ContentPlaceHolder1_DetailsView3_Label35']/text())").extract_first()
        built_year = resp.xpath("normalize-space(//span[@id='ctl00_ContentPlaceHolder1_DetailsView4_Label1']/text())").extract_first()
        property_type = resp.xpath("normalize-space(//span[@id='ctl00_ContentPlaceHolder1_DetailsView3_Label1']/text())").extract_first()

        driver.back()
        time.sleep(3)
    except:
        bedroomms = None
        full_baths = None
        half_baths = None
        built_year = None
        property_type = None


    print() 
    print(f"Scraping ====>{a0}")
    print("parcel_id:",parcel_id)
    print("Owners:",Owners)
    print("site_address:",site_address)
    print("mail_address:",mail_address)
    print("mail_city:",mail_city)
    print("mail_state:",mail_state)
    print("mail_zip:",mail_zip)
    print("land_value:",land_value)
    print("bldg_value:",bldg_value)
    print("TOAL_MARKET_VALUE:",TOAL_MARKET_VALUE)
    print("land_class:",land_class)
    print("property_type:",property_type)
    print("bedrooms:",bedroomms)
    print("full_baths:",full_baths)
    print("half_baths:",half_baths)
    print("sale_date:",sale_date)
    print("sale_price:",sale_price)
    print("living_area:",living_area)    
    print("built_year:",built_year)
    print()
    
    with open('Scraped_greensboro nc.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,parcel_id,Owners,site_address,mail_address,mail_city,mail_state,mail_zip,land_value,bldg_value,TOAL_MARKET_VALUE,sale_date,sale_price,built_year,living_area,land_class,property_type,bedroomms,full_baths,half_baths])
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







with open("./greensboro nc.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        try:
            driver.find_element_by_xpath("//a[contains(@href,'loca')]").click()
            time.sleep(3)
            
            company1 = str(i[1])
            company1 = company1.strip()
            search = driver.find_element_by_xpath("//input[@id='ctl00_ContentPlaceHolder1_StreetNumberTextBox']")
            search.send_keys(Keys.CONTROL + "a")
            search.send_keys(Keys.DELETE)
            time.sleep(1)
            search.send_keys(company1)
            time.sleep(1)
            commpany2 = str(i[2])
            search1 = driver.find_element_by_xpath("//input[@id='ctl00_ContentPlaceHolder1_StreetNameTextBox']")
            search1.send_keys(Keys.CONTROL + "a")
            search1.send_keys(Keys.DELETE)
            time.sleep(1)
            search1.send_keys(commpany2)
            time.sleep(1)
            search.send_keys(Keys.ENTER)
            time.sleep(5)
        except:
            None

        try:
            driver.find_element_by_xpath("//input[@id='ctl00_ContentPlaceHolder1_streetDictionaryResultsGridView_ctl02_CheckBox1']").click()
            time.sleep(3)
            driver.find_element_by_xpath("//input[@id='ctl00_ContentPlaceHolder1_StreetDictionarySearchButton']").click()
            time.sleep(3)
        except:None
        results = driver.find_elements_by_xpath("//table[@id='ctl00_ContentPlaceHolder1_ParcelStreetsGridView']/tbody/tr/td/a")
        if len(results)!=0:
            for ri in range(0,len(results)):
                driver.find_elements_by_xpath("//table[@id='ctl00_ContentPlaceHolder1_ParcelStreetsGridView']/tbody/tr/td/a")[ri].click()
                time.sleep(5)
                count = scrap(count,i[0],i[1],i[2],i[3])
                driver.back()
                time.sleep(3)
        else:
            count = scrap(count,i[0],i[1],i[2],i[3])



        driver.get(ul)
        time.sleep(3)


