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

ul = "https://kaneil.devnetwedge.com/"




def scrap(count,a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12):
    html = driver.page_source
    resp = Selector(text=html)

    parcel_id = resp.xpath("//div[contains(text(),'Parcel Number')]/following-sibling::div/text()").extract_first()
    site_address = resp.xpath("normalize-space(//div[contains(text(),'Site Address')]/following-sibling::div/text()[1])").extract_first()
    site_address1 = resp.xpath("normalize-space(//div[contains(text(),'Site Address')]/following-sibling::div/text()[last()])").extract_first()
    site_address1 = str(site_address1)
    try:
        site_state = re.findall(r"\s\w\w\s",site_address1)
        site_city = re.findall(r"^[^,]+",site_address1)
        site_zip_code = re.findall(r"\d.*",site_address1)
    except:
        site_city = None
        site_state =None
        site_zip_code = None
    
    Property_Class = resp.xpath("//div[contains(text(),'Property Class')]/following-sibling::div/text()").extract_first()
    Owners = resp.xpath("//div[contains(text(),'Owner Name & Address')]/following-sibling::div/text()").extract_first()
    owner_name =''
    if Owners:
        Owners = str(Owners)
        owner_mailing_address = re.findall(r"^[^,]+.*",Owners)
        for owner_name in owner_mailing_address:
            owner_name = str(owner_name)
            Owners = Owners.replace(owner_name,'')



    mail_address = Owners
    mail_address = str(mail_address)
    m_city = ''
    try:
        
        mail_city = re.findall(r"^[^,]+",mail_address)
        for  m_city in mail_city:
            m_city = str(m_city)
            mail_address = mail_address.replace(m_city,'')

    except:
        mail_city = None

    m_city = m_city.replace("\n",' ')
    mio = ''
    try:
        m_city1 = re.findall(r"\b(\w+)$",m_city)
        for mio in m_city1:
            mio = str(mio)
            m_city = m_city.replace(mio,'')
    except:
        m_city1 = None

    try:
        mail_state = re.findall(r"\s\w\w,",mail_address)
        mail_zip = re.findall(r"\d.*",mail_address)
    except:
        mail_state = None
        mail_zip =None

    sale_date = resp.xpath("//th[contains(text(),'Sale Date')]/ancestor::thead/following-sibling::tbody/tr[1]/td[4]//text()").extract_first()
    sale_price = resp.xpath("//th[contains(text(),'Sale Date')]/ancestor::thead/following-sibling::tbody/tr[1]/td[last()]//text()").extract_first()
    land_value = resp.xpath("//th[contains(text(),'Dwelling')]/ancestor::thead/following-sibling::tbody/tr[1]/td[2]//text()").extract_first()
    bldg_value = resp.xpath("//th[contains(text(),'Dwelling')]/ancestor::thead/following-sibling::tbody/tr[1]/td[3]//text()").extract_first()
    total_market_value = resp.xpath("//th[contains(text(),'Dwelling')]/ancestor::thead/following-sibling::tbody/tr[1]/td[last()]//text()").extract_first()
    tex_year = resp.xpath("(//div[contains(text(),'Tax Year')]/following-sibling::div/div/text())[1]").extract_first()


    
    
    print()
    print(f"Scraping ====>{a8} {a9} {a10} {a11}")
    print("parcel_id:",parcel_id)
    print("site_address:",site_address)
    print("site_city:",site_city)
    print("site_state:",site_state)
    print("site_zip_code:",site_zip_code)
    print("Property_Class:",Property_Class)
    print("Owners:",owner_name)
    print("mail_address:",m_city)
    print("mail_city:",mio)
    print("mail_state:",mail_state)
    print("mail_zip:",mail_zip)
    print("sale_date:",sale_date)
    print("sale_price:",sale_price)
    print("tex_year:",tex_year)
    print("land_value:",land_value)
    print("bldg_value:",bldg_value)
    print("total_market_value:",total_market_value)
    print()
    
    with open('dataset_for_elgin_il.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,parcel_id,owner_name,site_address,site_state,site_city,site_zip_code,Property_Class,m_city,m_city1,mail_state,mail_zip,sale_date,sale_price,tex_year,land_value,bldg_value,total_market_value])
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

with open("./input.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company1 = str(i[8])
        company1 = company1.strip()
        
        company2 = str(i[9])
        company2 = company2.strip()
        
        company3 = str(i[10])
        company3 = company3.strip()
        
        company4 = str(i[11])
        company4 = company4.strip()
        
        search = driver.find_element_by_xpath("//input[@id='house-number']")
        search.clear()
        search.send_keys(company1)
        time.sleep(1)
        search1 = driver.find_element_by_xpath("//input[@id='street-name']")
        search1.clear()
        search1.send_keys(company2)
        time.sleep(1)
        search2 = driver.find_element_by_xpath("//input[@id='street-suffix']")
        search2.clear()
        search2.send_keys(company3)
        time.sleep(1)
        search3 = driver.find_element_by_xpath("//input[@id='city-name']")
        search3.clear()
        search3.send_keys(company4)
        time.sleep(1)
        search.send_keys(Keys.ENTER)
        time.sleep(5)
        try:
            results = driver.find_elements_by_xpath("//table[@id='search-results']/tbody/tr")
            if len(results) != 0:
                for ri in range(0,len(results)):
                    driver.find_elements_by_xpath("//table[@id='search-results']/tbody/tr")[ri].click()
                    time.sleep(3)
                    count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12])
                    driver.back()
                    time.sleep(3)

            else:
                count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12])


        except:
            print("Search result is empty")
        
        driver.get(ul)
        time.sleep(2)
        
