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

ul = "https://www.leepa.org/Search/PropertySearch.aspx"




def scrap(count,a0,a1,a2,a3,a4):
    html = driver.page_source
    resp = Selector(text=html)
    
    parcel_id = resp.xpath("normalize-space(//span[@id='parcelLabel']/text())").extract_first()
    parcel_id = str(parcel_id)
    strap = ''
    folio = ''

    if parcel_id:
        parcel_id = parcel_id.replace("STRAP:",'')
        parcel_id = parcel_id.strip()
        strap = re.findall(r"^[\w\-]+\S\d+",parcel_id)
        folio = re.findall(r"\b(\w+)$",parcel_id)

    Owners = resp.xpath("normalize-space(//div[@class='textPanel']/div/text()[1])").extract_first()
    site_address = resp.xpath("//div[contains(text(),'Site Address')]/following-sibling::div/text()[last()-1]").extract_first()
    site_address1 = resp.xpath("//div[contains(text(),'Site Address')]/following-sibling::div/text()[last()]").extract_first()
    site_address1 = str(site_address1)
    try:
        site_state = re.findall(r"\s\w\w\s",site_address1)
        site_zip = re.findall(r"\d.*",site_address1)
    except:
        site_state = None
        site_zip = None

    for sa in site_state:
        site_address1 = site_address1.replace(sa,'')

    for si in site_zip:
        site_address1 = site_address1.replace(si,'')
        site_address1 = site_address1.strip()



    
    mail_address = resp.xpath("//div[@class='textPanel']/div/text()[last()-1]").extract_first()
    mail_address1 = resp.xpath("//div[@class='textPanel']/div/text()[last()]").extract_first()
    mail_address1 = str(mail_address1)
    try:
        mail_state = re.findall(r"\s\w\w\s",mail_address1)
        mail_zip = re.findall(r"\d.*",mail_address1)
    except:
        mail_state = None
        mail_zip = None

    for mo in mail_zip:
        mail_address1 = mail_address1.replace(mo,'')

    for ma in mail_state:
        mail_address1 = mail_address1.replace(ma,'')
        mail_address1 = mail_address1.strip()


    sale_date = resp.xpath("normalize-space(//th[contains(text(),'Sale Price')]/parent::tr/following-sibling::tr/td[1]/text())").extract_first()
    sale_price = resp.xpath("normalize-space(//th[contains(text(),'Sale Price')]/parent::tr/following-sibling::tr/td[2]/text())").extract_first()
    accessed_value = resp.xpath("normalize-space(//th[contains(text(),'Assessed')]/following-sibling::td/text())").extract_first()
    just = resp.xpath("normalize-space(//th[contains(text(),'Just')]/following-sibling::td/text())").extract_first()
    living_area = resp.xpath("normalize-space(//th[contains(text(),'Total Living Area')]/following-sibling::td/text())").extract_first()
    baths = resp.xpath("normalize-space(//th[contains(text(),'Total Bedrooms / Bathrooms')]/following-sibling::td/text())").extract_first()
    built_year = resp.xpath("normalize-space(//th[contains(text(),'st Year Building')]/following-sibling::td/text())").extract_first()
    bedroomms = ''
    baths = str(baths)
    if baths:
        bedroomms = re.findall(r"^[^,]",baths)
        for bi in bedroomms:
            baths = baths.replace(bi,'')
            baths = baths.replace('/','')
            baths = baths.strip()





    
    print()
    print(f"Scraping ====>{a4}")
    print("strap:",strap)
    print("folio:",folio)
    print("Owners:",Owners)
    print("site_address:",site_address)
    print("site_city:",site_address1)
    print("site_state:",site_state)
    print("mail_zip:",site_zip)
    print("just:",just)
    print("accessed_value:",accessed_value)
    print("mail_address:",mail_address)
    print("mail_city:",mail_address1)
    print("mail_state:",mail_state)
    print("mail_zip:",mail_zip)
    print("bedrooms:",bedroomms)
    print("baths:",baths)
    print("sale_date:",sale_date)
    print("sale_price:",sale_price)
    print("living_area:",living_area)    
    print("built_year:",built_year)
    print()
    
    with open('dataset_for_canton.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,strap,folio,Owners,site_address,site_address1,site_state,site_zip,mail_address,mail_address1,mail_state,mail_zip,just,accessed_value,sale_date,sale_price,living_area,bedroomms,baths,built_year])
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
        company1 = str(i[4])
        company1 = company1.strip()
        search = driver.find_element_by_xpath("//input[@id='ctl00_BodyContentPlaceHolder_AddressTextBox']")
        search.send_keys(Keys.CONTROL + "a")
        search.send_keys(Keys.DELETE)
        time.sleep(1)
        search.send_keys(company1)
        time.sleep(1)
        search.send_keys(Keys.ENTER)
        time.sleep(10)


        html = driver.page_source
        resp = Selector(text=html)
        res = resp.xpath("//a[contains(text(),'Parcel Details')]/@href").getall()
        if res != []:

            for ri in res:
                ule = f"https://www.leepa.org/{ri}&SalesDetails=True&TaxRollDetails=True#PermitDetails"
                driver.get(ule)
                time.sleep(10)
                count = scrap(count,i[0],i[1],i[2],i[3],i[4])
        else:
            count = scrap(count,i[0],i[1],i[2],i[3],i[4])



        driver.get(ul)
        time.sleep(3)


