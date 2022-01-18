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

ul = "https://www.mcassessor.maricopa.gov/"




def scrap(count,a0,a1,a2,a3,a4,a5,a6,owner):
    html = driver.page_source
    resp = Selector(text=html)
    
    parcel_id = resp.xpath("normalize-space((//h3[@class='h5 mt-2'])[1]/text())").extract_first()


    Owners = resp.xpath("normalize-space((//a[contains(@href,'/mcs/?q')])[last()]/text())").extract_first()
    site_address = resp.xpath("//div[@class='col-md-11 pt-3 banner-text']/a[contains(@href,'http://maps.')]/text()").extract_first()




    
    mail_address = resp.xpath("//div[contains(text(),'Mailing Address')]/following-sibling::div[1]/text()").extract_first()
    mail_address = str(mail_address)
    try:
        mail_street = re.findall(r"^[^,]+,",mail_address)
    except:
        mail_street = None

    ma_address = ''
    
    for ma_address in mail_street:
        mail_address = mail_address.replace(ma_address,'')
        mail_address = mail_address.strip()

    try:
        mail_state = re.findall(r"\s\w\w\s",mail_address)
        mail_zip = re.findall(r"\d.*",mail_address)
    except:
        mail_state = None
        mail_zip = None
    mo = ''
    for mo in mail_zip:
        mail_address = mail_address.replace(mo,'')
    ma = ''
    for ma in mail_state:
        mail_address = mail_address.replace(ma,'')
        mail_address = mail_address.strip()


    property_use = resp.xpath("normalize-space(//div[contains(text(),'PU Description')]/following-sibling::div[2]/text())").extract_first()
    
    

    full_cash_value = resp.xpath("//div[contains(text(),'Full Cash Value')]/following-sibling::div[2]/text()").extract_first()
    limited_value = resp.xpath("//div[contains(text(),'Limited Value')]/following-sibling::div[2]/text()").extract_first()



    living_area = resp.xpath("normalize-space((//div[contains(text(),'Living Area')]/following-sibling::div)[1]/text())").extract_first()
    baths = resp.xpath("normalize-space((//div[contains(text(),'Bath Fixtures')]/following-sibling::div)[1]/text())").extract_first()
    built_year = resp.xpath("normalize-space((//div[contains(text(),'Construction Year')]/following-sibling::div)[1]/text())").extract_first()
    land_area = resp.xpath("normalize-space(//div[contains(text(),'Lot Size')]/following-sibling::div[1]/text())").extract_first()



    sale_date = resp.xpath("normalize-space(//div[contains(text(),'Sale Date')]/following-sibling::div[1]/text())").extract_first()
    sale_price = resp.xpath("normalize-space(//div[contains(text(),'Sale Price')]/following-sibling::div[1]/text())").extract_first()

        

    
    print()
    print(f"Scraping ====>{a4}")
    print("parcel_id:",parcel_id)
    print("Owners:",Owners)
    print("site_address:",site_address)
    print("mail_address:",ma_address)
    print("mail_city:",mail_address)
    print("mail_state:",ma)
    print("mail_zip:",mo)
    print("baths:",baths)
    print("land_area:",land_area)
    print("property_use:",property_use)
    print("sale_date:",sale_date)
    print("sale_price:",sale_price)
    print("land_value:",full_cash_value)
    print("bldg_value:",limited_value)
    print("living_area:",living_area)    
    print("built_year:",built_year)
    print("owner:",owner)
    print()
    
    with open('dataset_for_Tempe AZ- Code Violations.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,a6,parcel_id,Owners,owner,site_address,ma_address,mail_address,ma,mo,baths,land_area,property_use,sale_date,sale_price,full_cash_value,limited_value,living_area,built_year])
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


with open("./Tempe AZ- Code Violations.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:

        company1 = str(i[4])
        company1 = company1.strip()
        search = driver.find_element_by_xpath("//input[@id='search-param']")
        search.send_keys(Keys.CONTROL + "a")
        search.send_keys(Keys.DELETE)
        time.sleep(1)
        search.send_keys(company1)
        time.sleep(1)
        search.send_keys(Keys.ENTER)
        time.sleep(10)
        clickkable = f"//a[contains(text(),'{i[4]}')]/parent::td/preceding-sibling::td[2]//@href"
        own_name = f"//a[contains(text(),'{i[4]}')]/parent::td/preceding-sibling::td[1]//text()"
        html = driver.page_source
        resp = Selector(text=html)
        result = resp.xpath(clickkable).extract_first()
        owner_name = resp.xpath(own_name).extract_first()
        if result:
            if "https://preview" in result:
                None
            else:
                result = f"https://preview.mcassessor.maricopa.gov{result}"
            print(result)
            driver.get(result)
            time.sleep(20)
            try:
                driver.find_element_by_xpath("//div[@id='jimu_dijit_CheckBox_0']/div[@class='checkbox jimu-float-leading']").click()
                time.sleep(2)
                
                driver.find_element_by_xpath("//div[contains(text(),'OK')]").click()
                time.sleep(2)
                
                html = driver.page_source
                resp = Selector(text=html)
                res = resp.xpath("//img[contains(@alt,'Property Information')]/parent::a/@href").get()
                driver.get(res)
                time.sleep(7)
            except:
                None


        count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],owner_name)



        driver.get(ul)
        time.sleep(3)


