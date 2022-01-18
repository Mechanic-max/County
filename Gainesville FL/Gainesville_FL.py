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

ul = "https://qpublic.schneidercorp.com/Application.aspx?AppID=1081&LayerID=26490&PageTypeID=2&PageID=10768"




def scrap(count,a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11):
    html = driver.page_source
    resp = Selector(text=html)
    
    parcel_id = resp.xpath("normalize-space(//span[@id='ctlBodyPane_ctl00_ctl01_lblParcelID']/text())").extract_first()
    parcel_id = str(parcel_id)

    Owners = resp.xpath("normalize-space(//span[@id='ctlBodyPane_ctl01_ctl01_lstOwner_ctl00_lnkOwnerName1_lblSearch']/text())").extract_first()
    if Owners:
        pass
    else:
        Owners = resp.xpath("normalize-space(//a[@id='ctlBodyPane_ctl01_ctl01_lstOwner_ctl00_lnkOwnerName1_lnkSearch']/text())").extract_first()
    site_address = resp.xpath("//span[@id='ctlBodyPane_ctl00_ctl01_lblLocationAddress']/text()").extract_first()
    site_address1 = resp.xpath("//span[@id='ctlBodyPane_ctl00_ctl01_lblCityStZip']/text()").extract_first()
    site_address1 = str(site_address1)
    try:
        site_state = re.findall(r"\s\w\w\s",site_address1)
        site_zip = re.findall(r"\d.*",site_address1)
    except:
        site_state = None
        site_zip = None

    sa =  ''
    for sa in site_state:
        sa = str(sa)
        site_address1 = site_address1.replace(sa,'')
    si = ''
    for si in site_zip:
        si = str(si)
        site_address1 = site_address1.replace(si,'')
        site_address1 = site_address1.strip()

    property_use_code = resp.xpath("//span[@id='ctlBodyPane_ctl00_ctl01_lblPropertyUse']/text()").extract_first()

    
    mail_address = resp.xpath("//span[@id='ctlBodyPane_ctl01_ctl01_lstOwner_ctl00_lblOwnerAddress']/text()[1]").extract_first()
    mail_address1 = resp.xpath("//span[@id='ctlBodyPane_ctl01_ctl01_lstOwner_ctl00_lblOwnerAddress']/text()[2]").extract_first()
    mail_address1 = str(mail_address1)
    try:
        mail_state = re.findall(r"\s\w\w\s",mail_address1)
        mail_zip = re.findall(r"\d.*",mail_address1)
    except:
        mail_state = None
        mail_zip = None

    mo = ''
    for mo in mail_zip:
        mo = str(mo)
        mail_address1 = mail_address1.replace(mo,'')

    ma = ''
    for ma in mail_state:
        ma =str(ma)
        mail_address1 = mail_address1.replace(ma,'')
        mail_address1 = mail_address1.strip()

    bldg_value = resp.xpath("//th[contains(text(),'Improvement Value')]/following-sibling::td[1]/text()").extract_first()
    land_value = resp.xpath("//th[contains(text(),'Land Value')]/following-sibling::td[1]/text()").extract_first()
    total_market_value = resp.xpath("//th[contains(text(),'Just (Market) Value')]/following-sibling::td[1]/text()").extract_first()
    sale_date = resp.xpath("normalize-space(//th[contains(text(),'Sale Price')]/ancestor::thead/following-sibling::tbody/tr[1]/td[1]/text())").extract_first()
    sale_price = resp.xpath("normalize-space(//th[contains(text(),'Sale Price')]/ancestor::thead/following-sibling::tbody/tr[1]/td[2]/text())").extract_first()
    acres =  resp.xpath("normalize-space(//th[contains(text(),'Acres')]/ancestor::thead/following-sibling::tbody/tr[1]/td[3]/text())").extract_first()
    land_sqare_area = resp.xpath("normalize-space(//th[contains(text(),'Acres')]/ancestor::thead/following-sibling::tbody/tr[1]/td[4]/text())").extract_first()
    living_area = resp.xpath("normalize-space(//th/strong[contains(text(),'Total Area')]/parent::th/following-sibling::td/span/text()[1])").extract_first()
    baths = resp.xpath("normalize-space(//th/strong[contains(text(),'Bathrooms')]/parent::th/following-sibling::td/span/text()[1])").extract_first()
    bedrooms = resp.xpath("normalize-space(//th/strong[contains(text(),'Bedrooms')]/parent::th/following-sibling::td/span/text()[1])").extract_first()
    built_year = resp.xpath("normalize-space(//th/strong[contains(text(),'Actual Year Built')]/parent::th/following-sibling::td/span/text()[1])").extract_first()
    property_type = resp.xpath("normalize-space((//th/strong[contains(text(),'Type')])[1]/parent::th/following-sibling::td/span/text()[1])").extract_first()



    print()
    print(f"Scraping ====>{a8}")
    print("parcel_id:",parcel_id)
    print("Owners:",Owners)
    print("site_address:",site_address)
    print("site_city:",site_address1)
    print("site_state:",sa)
    print("mail_zip:",si)
    print("mail_address:",mail_address)
    print("mail_city:",mail_address1)
    print("mail_state:",ma)
    print("mail_zip:",mo)
    print("bldg_value:",bldg_value)
    print("land_value:",land_value)
    print("total_market_value:",total_market_value)
    print("bedrooms:",bedrooms)
    print("baths:",baths)
    print("sale_date:",sale_date)
    print("sale_price:",sale_price)
    print("property_use_code:",property_use_code)    
    print("living_area:",living_area)    
    print("acres:",acres)
    print("land_sqare_area:",land_sqare_area)
    print("property_type:",property_type)
    print("built_year:",built_year)
    print()
    
    with open('dataset_for_Gainesville FL  (01-2020 to 04-2021) Code Enforcement.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,parcel_id,Owners,site_address,site_address1,sa,si,mail_address,mail_address1,ma,mo,bldg_value,land_value,total_market_value,sale_date,sale_price,property_use_code,acres,land_sqare_area,property_type,living_area,bedrooms,baths,built_year])
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

try:
    driver.find_element_by_xpath("//a[contains(text(),'Agree')]").click()
    time.sleep(3)
except:
    print("pop up didn't appear")

with open("./Gainesville FL  (01-2020 to 04-2021) Code Enforcement.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company1 = str(i[8])
        company1 = company1.strip()
        search = driver.find_element_by_xpath("//input[@id='ctlBodyPane_ctl01_ctl01_txtAddressExact']")
        search.send_keys(Keys.CONTROL + "a")
        search.send_keys(Keys.DELETE)
        time.sleep(1)
        search.send_keys(company1)
        time.sleep(1)
        search.send_keys(Keys.ENTER)
        time.sleep(3)

        count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11])
        driver.get(ul)
        time.sleep(3)


