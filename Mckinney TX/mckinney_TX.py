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

ul = "https://www.collincad.org/propertysearch"




def scrap(count,a0,a1,a2,a3,a4,a5,a6,a7,a8,a9):
    html = driver.page_source
    resp = Selector(text=html)
    
    parcel = resp.xpath("normalize-space(//dt[contains(text(),'Geographic ID')]/following-sibling::dd[1]/text())").extract_first()
    property_Id = resp.xpath("normalize-space(//dt[contains(text(),'Property ID')]/following-sibling::dd[1]/text())").extract_first()
    DBA_NAME = resp.xpath("normalize-space(//dt[contains(text(),'DBA Name')]/following-sibling::dd[1]/text()[1])").extract_first()
    Owners = resp.xpath("normalize-space(//dt[contains(text(),'Owner Name(s)')]/following-sibling::dd[1]//text()[1])").extract_first()
    

    site_address = resp.xpath("//dt[contains(text(),'Property Address')]/following-sibling::dd[1]/text()[1]").extract_first()
    site_address1 = resp.xpath("//dt[contains(text(),'Property Address')]/following-sibling::dd[1]/text()[2]").extract_first()
    site_address1 = str(site_address1)

    
    try:

        site_state = re.findall(r"\s\w\w\s",site_address1)
        site_zip = re.findall(r"\d.*",site_address1)
    except:
        site_state = None
        site_zip = None

    sa = ''
    for sa in site_state:
        site_address1 = site_address1.replace(sa,'')

    si= ''
    for si in site_zip:
        site_address1 = site_address1.replace(si,'')
        site_address1 = site_address1.strip()



    
    mail_address = resp.xpath("//dt[contains(text(),'Mailing Address')]/following-sibling::dd[1]//text()[1]").extract_first()
    mail_address1 = resp.xpath("//dt[contains(text(),'Mailing Address')]/following-sibling::dd[1]//text()[2]").extract_first()
    mail_address1 = str(mail_address1)

    try:
        mail_city = re.findall(r"^[^,]+",mail_address1)
        mail_state = re.findall(r"\s\w\w\s",mail_address1)
        mail_zip = re.findall(r"\d.*",mail_address1)
    except:
        mail_city = None
        mail_state = None
        mail_zip = None

    land_area = resp.xpath("//dt[contains(text(),'Total Land Area')]/following-sibling::dd[1]/text()[1]").extract_first()
    living_area = resp.xpath("normalize-space(//dt[contains(text(),'Total Improvement Main Area')]/following-sibling::dd[1]/text()[1])").extract_first()
    built_year = resp.xpath("normalize-space((//td[contains(text(),'Year Built')]/ancestor::thead)[1]/following-sibling::tbody/tr[1]/td[3]/text())").extract_first()
    bldg_value = resp.xpath("//dt[contains(text(),'Total Improvement Market Value')]/following-sibling::dd[1]//text()[1]").extract_first()
    land_value = resp.xpath("//dt[contains(text(),'Total Land Market Value')]/following-sibling::dd[1]//text()[1]").extract_first()
    total_market_value = resp.xpath("//dt[contains(text(),'Total Assessed Value')]/following-sibling::dd[1]//text()[1]").extract_first()
    sale_date = resp.xpath("//table[@id='collapsed_deeds']/tbody/tr[1]/td[1]/text()").extract_first()
    property_type =  resp.xpath("//dt[contains(text(),'Property Type')]/following-sibling::dd[1]/text()").extract_first()

    
    print()
    print(f"Scraping ====>{a1} {a2}")
    print("parcel:",parcel)
    print("property_Id:",property_Id)
    print("DBA_NAME:",DBA_NAME)
    print("Owners:",Owners)
    print("site_address:",site_address)
    print("site_city:",site_address1)
    print("site_state:",sa)
    print("mail_zip:",si)
    print("mail_address:",mail_address)
    print("mail_city:",mail_city)
    print("mail_state:",mail_state)
    print("mail_zip:",mail_zip)
    print("property_type:",property_type)
    print("sale_date:",sale_date)
    print("land_value:",land_value)
    print("bldg_value:",bldg_value)
    print("total_market_value:",total_market_value)
    print("living_area:",living_area)
    print("land_area:",land_area)
    print("built_year:",built_year)
    print()
    
    with open('dataset_for_mckinney TX 01-01-2020 - 04-20-2021.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,parcel,property_Id,DBA_NAME,Owners,site_address,site_address1,sa,si,mail_address,mail_city,mail_state,mail_zip,property_type,sale_date,land_value,bldg_value,total_market_value,land_area,living_area,built_year])
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


with open("./mckinney TX 01-01-2020 - 04-20-2021.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company1 = str(i[1])
        company1 = company1.strip()
        search = driver.find_element_by_xpath("//input[@id='situs_num']")
        search.send_keys(Keys.CONTROL + "a")
        search.send_keys(Keys.DELETE)
        time.sleep(1)
        search.send_keys(company1)
        time.sleep(1)

        company2 = str(i[2])
        company2 = company2.strip()
        search1 = driver.find_element_by_xpath("//input[@id='situs_street']")
        search1.send_keys(Keys.CONTROL + "a")
        search1.send_keys(Keys.DELETE)
        time.sleep(1)
        search1.send_keys(company2)
        time.sleep(1)
        search.send_keys(Keys.ENTER)
        time.sleep(10)

        html = driver.page_source
        resp = Selector(text=html)
        results = resp.xpath("//table[@id='propertysearchresults']/tbody/tr/td/a[contains(@href,'/property')]/@href").getall()
        if results !=[]:
            for ri in results:
                relative_url = f"https://www.collincad.org/{ri}"
                driver.get(relative_url)
                time.sleep(5)
                count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9])
        else:
            count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9])



        driver.get(ul)
        time.sleep(3)


