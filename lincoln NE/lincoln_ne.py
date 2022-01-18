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

ul = "https://orion.lancaster.ne.gov/"




def scrap(count,a0,a1,a2,a3,a4,a5,a6):
    html = driver.page_source
    resp = Selector(text=html)
    
    parcel = resp.xpath("normalize-space(//td[@id='dnn_ctr388_View_tdPropertyID']/text())").extract_first()
    property_Id = resp.xpath("normalize-space(//td[@id='dnn_ctr388_View_tdGIAccount']/text())").extract_first()
    property_class = resp.xpath("//td[@id='dnn_ctr388_View_tdGIPropertyClass']/text()").extract_first()
    Owners = resp.xpath("normalize-space(//div[@id='dnn_ctr388_View_divOwnersLabel']/text())").extract_first()
    

    site_address = resp.xpath("//td[@id='dnn_ctr388_View_tdPropertyAddress']/text()").extract_first()
    site_address = str(site_address)
    try:
        site_street_address = re.findall(r"^[^,]+,",site_address)
    except:
        site_street_address = None
    
    sew = ''
    for sew in site_street_address:
        sew = str(sew)
        site_address = site_address.replace(sew,'')
        site_address = site_address.strip()
    
    try:

        site_state = re.findall(r"\s\w\w\s",site_address)
        site_zip = re.findall(r"\d.*",site_address)
    except:
        site_state = None
        site_zip = None

    sa = ''
    for sa in site_state:
        site_address = site_address.replace(sa,'')

    si= ''
    for si in site_zip:
        site_address = site_address.replace(si,'')
        site_address = site_address.strip()



    
    mail_address = resp.xpath("//td[@id='dnn_ctr388_View_tdOIMailingAddress']/text()").extract_first()
    mail_address = str(mail_address)
    try:
        mail_street_address = re.findall(r"^[^,]+",mail_address)
    except:
        mail_street_address = None
    
    meow = ''
    for meow in mail_street_address:
        meow = str(meow)
        mail_address = mail_address.replace(meow,'')
        mail_address = mail_address.strip()
    try:
        m_city = re.findall(r"\b(\w+)$",meow)
    except:
        m_city = None
    try:   
        mail_state = re.findall(r"\s\w\w\s",mail_address)
        mail_zip = re.findall(r"\d.*",mail_address)
    except:
        mail_state = None
        mail_zip = None


    living_area = resp.xpath("normalize-space(//table[@id='resImprovementTable0']/tbody/tr[2]/td[last()]/text())").extract_first()
    built_year = resp.xpath("normalize-space(//table[@id='resImprovementTable0']/tbody/tr[2]/td[last()-1]/text())").extract_first()
    land_value = resp.xpath("//table[@id='dnn_ctr388_View_tblValueHistoryDataRP']/tbody/tr[2]/td[2]/text()").extract_first()
    bldg_value = resp.xpath("//table[@id='dnn_ctr388_View_tblValueHistoryDataRP']/tbody/tr[2]/td[3]/text()").extract_first()
    total_market_value = resp.xpath("//table[@id='dnn_ctr388_View_tblValueHistoryDataRP']/tbody/tr[2]/td[4]/text()").extract_first()
    sale_date = resp.xpath("//table[@id='dnn_ctr388_View_tblSalesHistoryData']/tbody/tr[2]/td[1]/text()").extract_first()
    sale_price = resp.xpath("//table[@id='dnn_ctr388_View_tblSalesHistoryData']/tbody/tr[2]/td[last()]/text()").extract_first()
    property_type =  resp.xpath("//table[@id='resImprovementTable0']/tbody/tr[2]/td[3]/text()").extract_first()




    
    print()
    print(f"Scraping ====>{a4}")
    print("parcel:",parcel)
    print("property_Id:",property_Id)
    print("Owners:",Owners)
    print("site_address:",sew)
    print("site_city:",site_address)
    print("site_state:",sa)
    print("mail_zip:",si)
    print("mail_address:",meow)
    print("mail_city:",m_city)
    print("mail_state:",mail_state)
    print("mail_zip:",mail_zip)
    print("property_type:",property_type)
    print("sale_date:",sale_date)
    print("sale_price:",sale_price)
    print("property_class:",property_class)
    print("land_value:",land_value)
    print("bldg_value:",bldg_value)
    print("total_market_value:",total_market_value)
    print("living_area:",living_area)    
    print("built_year:",built_year)
    print()
    
    with open('dataset_for_Lincoln NE (01-01-2015 - 04-14-2021) neglegted Building Registry.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,a6,parcel,property_Id,Owners,sew,site_address,sa,si,meow,m_city,mail_state,mail_zip,property_type,property_class,sale_date,sale_price,land_value,bldg_value,total_market_value,living_area,built_year])
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
time.sleep(10)


with open("./Lincoln NE (01-01-2015 - 04-14-2021) neglegted Building Registry.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company1 = str(i[4])
        company1 = company1.strip()
        search = driver.find_element_by_xpath("//input[@id='SearchText']")
        search.send_keys(Keys.CONTROL + "a")
        search.send_keys(Keys.DELETE)
        time.sleep(1)
        search.send_keys(company1)
        time.sleep(1)
        search.send_keys(Keys.ENTER)
        time.sleep(10)

    
        results = driver.find_elements_by_xpath("//table[@class='k-selectable']/tbody/tr")
        if results !=[]:
            for ri in range(0,len(results)):
                driver.find_elements_by_xpath("//table[@class='k-selectable']/tbody/tr")[ri].click()
                time.sleep(5)
                count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6])
                driver.back()
                time.sleep(3)
        else:
            count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6])



        driver.get(ul)
        time.sleep(3)


