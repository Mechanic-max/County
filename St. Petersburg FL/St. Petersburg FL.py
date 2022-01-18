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

ul = "https://www.pcpao.org/searchbyAddress.php"


def scrap(count,a0,a1,a2,a3,a4,a5):
    try:
        iframe = driver.find_element_by_xpath("//frame[@name='bodyFrame']")
        driver.switch_to.frame(iframe)
    except:
        None
    html = driver.page_source
    resp = Selector(text=html)
    
    Parcel = resp.xpath("normalize-space(//font[contains(text(),'-') and @size='+2']/text())").extract_first()
    owner_name = resp.xpath("normalize-space(//th[contains(text(),'Ownership/Mailing Address')]/parent::tr/following-sibling::tr[1]/td[1]/text()[1])").extract_first()
    mail_address = resp.xpath("normalize-space(//th[contains(text(),'Ownership/Mailing Address')]/parent::tr/following-sibling::tr[1]/td[1]/text()[last()-1])").extract_first()
    mail_city_state_zip = resp.xpath("normalize-space(//th[contains(text(),'Ownership/Mailing Address')]/parent::tr/following-sibling::tr[1]/td[1]/text()[last()])").extract_first()
    mail_zip = ''
    mail_state = ''
    mail_city_state_zip = str(mail_city_state_zip)
    try:
        ma_zip = re.findall(r"\d.*",mail_city_state_zip)
        ma_state = re.findall(r"\s\w\w\s",mail_city_state_zip)
    except:
        ma_zip = ''
        ma_state = ''


    for mail_zip in ma_zip:
        mail_city_state_zip = mail_city_state_zip.replace(mail_zip,'')
        mail_city_state_zip = mail_city_state_zip.strip()

    for mail_state in ma_state:
        mail_state = str(mail_state)
        mail_state = mail_state.strip()
        mail_city_state_zip = mail_city_state_zip.replace(mail_state,'')
        mail_city_state_zip = mail_city_state_zip.strip()

    site_address = resp.xpath("normalize-space(//th[contains(text(),'Ownership/Mailing Address')]/parent::tr/following-sibling::tr[1]/td[2]/text()[1])").extract_first()
    site_city = resp.xpath("normalize-space(//th[contains(text(),'Ownership/Mailing Address')]/parent::tr/following-sibling::tr[1]/td[2]/text()[2])").extract_first()

    property_use = resp.xpath("normalize-space(//a[contains(text(),'Property Use')]/parent::td/text())").extract_first()
    living_area = resp.xpath("normalize-space(//td[contains(text(),'Total Living:')]/text())").extract_first()
    living_area = str(living_area)
    living_area = living_area.replace("Total Living:","")
    living_area = living_area.strip()
    Legal_Description = resp.xpath("normalize-space(//div[@id='legal']/text())").extract_first()
    Census_Tract = resp.xpath("normalize-space(//th[contains(text(),'Most Recent Recording')]/parent::tr/following-sibling::tr[1]/td[3]/div/text())").extract_first()

    total_market_value = resp.xpath("normalize-space((//a[contains(text(),'Assessed ')]/parent::td/parent::tr[1]/following-sibling::tr)[1]/td[3]/b/text())").extract_first()
    assessed_value = resp.xpath("normalize-space((//a[contains(text(),'Assessed ')]/parent::td/parent::tr[1]/following-sibling::tr)[1]/td[4]/b/text())").extract_first()


    sale_date = resp.xpath("normalize-space((//th[contains(text(),'Sale Date')]/parent::tr/following-sibling::tr)[1]/td[1]/text())").extract_first()
    sale_price = resp.xpath("normalize-space((//th[contains(text(),'Sale Date')]/parent::tr/following-sibling::tr)[1]/td[3]/text())").extract_first()

    property_type = resp.xpath("//td[contains(text(),'Building Type: ')]/b/text()").extract_first()
    built_year = resp.xpath("normalize-space(//td[contains(text(),'Year Built: ')]/b/text())").extract_first()


    print()
    print(f"Scraping ====>{a2}")
    print("Parcel:",Parcel)
    print("owner_name:",owner_name)
    print("site_address:",site_address)
    print("site_city:",site_city)
    print("mail_address:",mail_address)
    print("mail_city:",mail_city_state_zip)
    print("mail_state:",mail_state)
    print("mail_zip:",mail_zip)
    print("property_use:",property_use)
    print("Legal_Description:",Legal_Description)
    print("Census_Tract:",Census_Tract)
    print("living_area:",living_area)    
    print("property_type:",property_type)    
    print("built_year:",built_year)
    print("assessed_value:",assessed_value)
    print("total_market_value:",total_market_value)
    print("sale_date:",sale_date)
    print("sale_price:",sale_price)
    print()
    
    with open('dataset_for_St. Petersburg FL (01-01-2020 - 04-13-2021) CODE VIOLATIONS.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,Parcel,owner_name,site_address,site_city,mail_address,mail_city_state_zip,mail_state,mail_zip,property_use,Legal_Description,Census_Tract,living_area,property_type,built_year,assessed_value,total_market_value,sale_date,sale_price])
        count = count + 1
        print("Data saved in CSV: ",count)
    
    driver.switch_to.default_content()
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
time.sleep(7)
try:
    driver.find_element_by_xpath("//font[contains(text(),'I accept, continue')]").click()
    time.sleep(3)
except:
    None
with open("./St. Petersburg FL (01-01-2020 - 04-13-2021) CODE VIOLATIONS.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:

        company = str(i[2])
        company = company.strip()
        search = driver.find_element_by_xpath("//input[@id='Addr2']")
        search.send_keys(Keys.CONTROL + "a")
        search.send_keys(Keys.DELETE)
        time.sleep(1)
        search.send_keys(company)
        time.sleep(1)
        search.send_keys(Keys.ENTER)
        time.sleep(4)
        try:
            driver.find_element_by_xpath("//a[contains(text(),'-')]").click()
            time.sleep(3)
        except:None
        count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5])
        driver.get(ul)
        time.sleep(7)
