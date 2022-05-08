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

ul = "https://propaccess.trueautomation.com/clientdb/?cid=19"




def scrap(count,a0,a1):
    html = driver.page_source
    resp = Selector(text=html)
    
    parcel_id = resp.xpath("normalize-space(//td[contains(text(),'Property ID:')]/following-sibling::td/text())").extract_first()
    Owners = resp.xpath("//td[contains(text(),'Name:')]/following-sibling::td[1]/text()").extract_first()
    Owner_id = resp.xpath("//td[contains(text(),'Owner ID:')]/following-sibling::td[1]/text()").extract_first()
    Property_use_code = resp.xpath("normalize-space(//td[contains(text(),'Property Use Code:')]/following-sibling::td[1]/text())").extract_first()
    site_address = resp.xpath("(//td[contains(text(),'Address:')])[1]/following-sibling::td[1]/text()[1]").extract_first()
    site_state_zip = resp.xpath("(//td[contains(text(),'Address:')])[1]/following-sibling::td[1]/text()[2]").extract_first()
    site_state_zip = str(site_state_zip)
    try:
        site_zip = re.findall(r"\d.*",site_state_zip)
        site_state = re.findall(r"\s\w\w\s",site_state_zip)
    except:
        site_state = None
        site_zip = None
    mail_address = resp.xpath("normalize-space((//td[contains(text(),'Mailing Address:')])[1]/following-sibling::td[1]/text()[last()-1])").extract_first()
    mail_address1 = resp.xpath("normalize-space((//td[contains(text(),'Mailing Address:')])[1]/following-sibling::td[1]/text()[last()])").extract_first()
    mail_address1 = str(mail_address1)
    try:
        mail_city = re.findall(r"^[^,]+",mail_address1)
        mail_state = re.findall(r"\s\w\w\s",mail_address1)
        mail_zip = re.findall(r"\d.*",mail_address1)
    except:
        mail_city = None
        mail_state = None
        mail_zip = None

    try:
        driver.find_element_by_xpath("//div[@id='values']").click()
        time.sleep(3)
        html = driver.page_source
        resp = Selector(text=html)

        land_value = resp.xpath("//td[contains(text(),'(+) Land Homesite Value:')]/following-sibling::td[contains(@class,'c')]/text()").extract_first()
        bldg_value = resp.xpath("//td[contains(text(),'Improvement Homesite Value')]/following-sibling::td[contains(@class,'c')]/text()").extract_first()
        total_market_value = resp.xpath("//td[contains(text(),'(=) Market Value:')]/following-sibling::td[contains(@class,'c')]/text()").extract_first()

    except:
        land_value = None
        bldg_value = None
        total_market_value = None
    

    try:
        driver.find_element_by_xpath("//div[@id='improvementBuilding']").click()
        time.sleep(3)
        html = driver.page_source
        resp = Selector(text=html)

        Property_TYPE = resp.xpath("//th[contains(text(),'Improvement #1:')]/following-sibling::td/text()").extract_first()
        living_area = resp.xpath("//th[contains(text(),'Improvement #1:')]/following-sibling::th[contains(text(),'Living Area:')]/following-sibling::td[1]/text()").extract_first()
        built_year = resp.xpath("(//table[@class='improvementDetails'])[1]/tbody/tr[2]/td[last()-1]/text()").extract_first()

    except:
        Property_TYPE = None
        living_area = None
        built_year = None


    
    
    print()
    print(f"Scraping ====>{a1}")
    print("parcel_id:",parcel_id)
    print("Owner_id:",Owner_id)
    print("Owners:",Owners)
    print("Property_use_code:",Property_use_code)
    print("site_address:",site_address)
    print("site_state:",site_state)
    print("site_zip:",site_zip)
    print("mail_address:",mail_address)
    print("mail_city:",mail_city)
    print("mail_state:",mail_state)
    print("mail_zip:",mail_zip)
    print("land_value:",land_value)
    print("bldg_value:",bldg_value)
    print("total_market_value:",total_market_value)
    print("Property_TYPE:",Property_TYPE)
    print("living_area:",living_area)    
    print("built_year:",built_year)
    print()
    
    with open('dataset_for_carrolton.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,parcel_id,Owner_id,Owners,site_address,site_state,site_zip,mail_address,mail_city,mail_state,mail_zip,Property_use_code,land_value,bldg_value,total_market_value,Property_TYPE,living_area,built_year])
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
        company1 = str(i[1])
        company1 = company1.strip()
        search = driver.find_element_by_xpath("//input[@id='propertySearchOptions_searchText']")
        search.clear()
        search.send_keys(company1)
        time.sleep(1)
        search.send_keys(Keys.ENTER)
        time.sleep(5)
        # try:
        results = driver.find_elements_by_xpath("//a[contains(@href,'Property.aspx')]")
        if len(results) != 0:
            for ri in range(0,len(results)):
                driver.find_elements_by_xpath("//a[contains(@href,'Property.aspx')]")[ri].click()
                time.sleep(3)
                count = scrap(count,i[0],i[1])
                driver.back()
                time.sleep(3)

        else:
            count = scrap(count,i[0],i[1])


        # except:
        #     print("Search result is empty")
        
        driver.get(ul)
        time.sleep(5)