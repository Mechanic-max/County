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

ul = "https://sdat.dat.maryland.gov/RealProperty/Pages/default.aspx"




def scrap(count,a0,a1,a2,a3):
    html = driver.page_source
    resp = Selector(text=html)
    
    Account_No = resp.xpath("normalize-space(//strong[contains(text(),'Account Number - ')]/parent::span/text()[last()])").extract_first()
    Owners = resp.xpath("normalize-space(//span[@id='MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucDetailsSearch_dlstDetaisSearch_lblOwnerName_0']/text())").extract_first()

    Parcel = resp.xpath("normalize-space(//span[@id='MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucDetailsSearch_dlstDetaisSearch_Label7_0']/text())").extract_first()
    Parcel = str(Parcel)
    Parcel = Parcel.strip()
    if Parcel:
        Parcel = f"P{Parcel}"


    
    site_address = resp.xpath("//span[@id='MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucDetailsSearch_dlstDetaisSearch_lblPremisesAddress_0']/text()[1]").extract_first()
    site_address1 = resp.xpath("//span[@id='MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucDetailsSearch_dlstDetaisSearch_lblPremisesAddress_0']/text()[2]").extract_first()
    site_address1 = str(site_address1)
    try:
        site_zip = re.findall(r"\d.*",site_address1)
    except:
        site_zip = None

    sit_zip = ''

    for sit_zip in site_zip:
        sit_state = str(sit_zip)
        site_address1 = site_address1.replace(sit_zip,'')
        site_address1 = site_address1.strip()


    mail_address = resp.xpath("normalize-space(//span[@id='MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucDetailsSearch_dlstDetaisSearch_lblMailingAddress_0']/text())").extract_first()
    mail_address1 = resp.xpath("normalize-space(//span[@id='MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucDetailsSearch_dlstDetaisSearch_lblMailingAddress_0']/text()[2])").extract_first()
    mail_address1 = str(mail_address1)
    try:
        mail_state = re.findall(r"\s\w\w\s",mail_address1)
        mail_zip = re.findall(r"\d.*",mail_address1)
    except:
        mail_state = None
        mail_zip = None

    ma_zip = ''
    ma_state = ''

    for ma_state in mail_state:
        ma_state = str(ma_state)
        mail_address1 = mail_address1.replace(ma_state,' ')
        mail_address1 = mail_address1.strip()
    
    for ma_zip in mail_zip:
        ma_zip = str(mail_zip)
        ma_zip = ma_zip.replace('[','')
        ma_zip = ma_zip.replace(']','')
        ma_zip = ma_zip.replace("'","")
        mail_address1 = mail_address1.replace(ma_zip,'')

    property_use = resp.xpath("//span[@id='MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucDetailsSearch_dlstDetaisSearch_lblUse_0']/text()").extract_first()
    
    property_type = resp.xpath("//th[contains(text(),'Property Type')]/following-sibling::td[1]/text()").extract_first()
    land_value = resp.xpath("normalize-space(//span[@id='MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucDetailsSearch_dlstDetaisSearch_lblBaseLand_0']/text())").extract_first()
    bldg_value = resp.xpath("normalize-space(//span[@id='MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucDetailsSearch_dlstDetaisSearch_lblBaseImprove_0']/text())").extract_first()
    market_value = resp.xpath("normalize-space(//span[@id='MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucDetailsSearch_dlstDetaisSearch_lblBaseTotal_0']/text())").extract_first()
    sale_date = resp.xpath("normalize-space(//span[@id='MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucDetailsSearch_dlstDetaisSearch_Label40_0']/text())").extract_first()
    sale_price = resp.xpath("normalize-space(//span[@id='MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucDetailsSearch_dlstDetaisSearch_Label39_0']/text())").extract_first()
    living_area = resp.xpath("normalize-space(//span[@id='MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucDetailsSearch_dlstDetaisSearch_Label20_0']/text())").extract_first()

    built_year = resp.xpath("normalize-space(//span[@id='MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucDetailsSearch_dlstDetaisSearch_Label18_0']/text())").extract_first()



    baths = resp.xpath("normalize-space(//span[@id='MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucDetailsSearch_dlstDetaisSearch_Label34_0']/text())").extract_first()



    

    print()
    print(f"Scraping ====>{a0}")
    print("Parcel:",Parcel)
    print("Account_No:",Account_No)
    print("Owners:",Owners)
    print("mail_address:",mail_address)
    print("MAIL CIITY:",mail_address1)
    print("ma_state:",ma_state)
    print("ma_zip:",ma_zip)
    print("site_address:",site_address)
    print("site_city:",site_address1)
    print("site_zip:",sit_zip)
    print("baths:",baths)
    print("property_type:",property_type)
    print("sale_date:",sale_date)
    print("sale_price:",sale_price)
    print("living_area:",living_area)    
    print("built_year:",built_year)
    print("property_use:",property_use)
    print("land_value:",land_value)
    print("bldg_value:",bldg_value)
    print("market_value:",market_value)
    print()
    
    with open('dataset_for_montgomery county md.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,Parcel,Account_No,Owners,mail_address,mail_address1,ma_state,ma_zip,site_address,site_address1,sit_zip,property_type,sale_date,sale_price,living_area,baths,built_year,property_use,land_value,bldg_value,market_value])
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
time.sleep(20)
try:
    driver.find_element_by_xpath("//select/option[contains(text(),'MONTGOMERY COUNTY')]").click()
    time.sleep(2)
except: None
try:
    driver.find_element_by_xpath("//select/option[contains(text(),'STREET ADDRESS')]").click()
    time.sleep(2)
except: None
try:
    driver.find_element_by_xpath("//input[@id='MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_StartNavigationTemplateContainerID_btnContinue']").click()
    time.sleep(5)
except: None
with open("./input1.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        try:
            company1 = str(i[1])
            company1 = company1.strip()
            search = driver.find_element_by_xpath("//input[@id='MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucEnterData_txtStreenNumber']")
            search.send_keys(Keys.CONTROL + "a")
            search.send_keys(Keys.DELETE)
            search.send_keys(company1)
            time.sleep(1)

            company2 = str(i[2])
            company2 = company2.strip()
            search1 = driver.find_element_by_xpath("//input[@id='MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucEnterData_txtStreetName']")
            search1.send_keys(Keys.CONTROL + "a")
            search1.send_keys(Keys.DELETE)
            time.sleep(1)
            search1.send_keys(company2)
            time.sleep(1)

            driver.find_element_by_xpath("//input[@id='MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_StepNavigationTemplateContainerID_btnStepNextButton']").click()
            time.sleep(5)
            
            count = scrap(count,i[0],i[1],i[2],i[3])
            driver.find_element_by_xpath("//input[@id='MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_StepNavigationTemplateContainerID_btnStepPreviousButton']").click()
            time.sleep(10)
        except:
            driver.get(ul)
            time.sleep(3)
            try:
                driver.find_element_by_xpath("//select/option[contains(text(),'MONTGOMERY COUNTY')]").click()
                time.sleep(2)
            except: None
            try:
                driver.find_element_by_xpath("//select/option[contains(text(),'STREET ADDRESS')]").click()
                time.sleep(2)
            except: None
            try:
                driver.find_element_by_xpath("//input[@id='MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_StartNavigationTemplateContainerID_btnContinue']").click()
                time.sleep(5)
            except: None
            company1 = str(i[1])
            company1 = company1.strip()
            search = driver.find_element_by_xpath("//input[@id='MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucEnterData_txtStreenNumber']")
            search.send_keys(Keys.CONTROL + "a")
            search.send_keys(Keys.DELETE)
            search.send_keys(company1)
            time.sleep(1)

            company2 = str(i[2])
            company2 = company2.strip()
            search1 = driver.find_element_by_xpath("//input[@id='MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucEnterData_txtStreetName']")
            search1.send_keys(Keys.CONTROL + "a")
            search1.send_keys(Keys.DELETE)
            time.sleep(1)
            search1.send_keys(company2)
            time.sleep(1)

            driver.find_element_by_xpath("//input[@id='MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_StepNavigationTemplateContainerID_btnStepNextButton']").click()
            time.sleep(5)
            
            count = scrap(count,i[0],i[1],i[2],i[3])
            driver.find_element_by_xpath("//input[@id='MainContent_MainContent_cphMainContentArea_ucSearchType_wzrdRealPropertySearch_StepNavigationTemplateContainerID_btnStepPreviousButton']").click()
            time.sleep(10)