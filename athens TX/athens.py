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


def scrao(count):
    html = driver.page_source
    resp = Selector(text=html)
    
    property_id = resp.xpath("//th[contains(text(),'Property ID:')]/following-sibling::td/text()").extract_first()
    property_type = resp.xpath("//th[contains(text(),'Type:')]/following-sibling::td/text()").extract_first()
    site_address = resp.xpath("(//th[contains(text(),'Address:')])[1]/following-sibling::td/text()").extract_first()
    owner_id = resp.xpath("(//th[contains(text(),'Owner ID:')])[1]/following-sibling::td/text()").extract_first()
    owner_name = resp.xpath("(//th[contains(text(),'Name:')])[1]/following-sibling::td/text()").extract_first()
    mail_address1 = resp.xpath("(//th[contains(text(),'Mailing Address:')])[1]/following-sibling::td/text()[1]").extract_first()
    mail_address2 = resp.xpath("(//th[contains(text(),'Mailing Address:')])[1]/following-sibling::td/text()[2]").extract_first()
    living_area = resp.xpath("//table[@class='table table-striped table-bordered table-condensed']//td[contains(text(),'LA')]/following-sibling::td[last()]/text()").extract_first()
    year_built = resp.xpath("//table[@class='table table-striped table-bordered table-condensed']//td[contains(text(),'LA')]/following-sibling::td[last()-1]/text()").extract_first()
    bldg_value = resp.xpath("(//th[contains(text(),'Improvement Homesite Value:')])[1]/following-sibling::td/text()").extract_first()
    land_value = resp.xpath("(//th[contains(text(),'Land Homesite Value:')])[1]/following-sibling::td/text()").extract_first()
    total_market_value = resp.xpath("(//th[contains(text(),'Market Value:')])[1]/following-sibling::td/text()").extract_first()
    deed_date = resp.xpath("(//table[@class='table table-striped table-bordered table-condensed']/tbody/tr/th[contains(text(),'Deed Date')]/parent::tr/following-sibling::tr)[1]/td[1]/text()").extract_first()
    deed_type = resp.xpath("(//table[@class='table table-striped table-bordered table-condensed']/tbody/tr/th[contains(text(),'Deed Date')]/parent::tr/following-sibling::tr)[1]/td[2]/text()").extract_first()
    mail_address2 = str(mail_address2)
    try:
        city = re.findall(r"^[^,]+",mail_address2)
        state = re.findall(r"\s\w\w\s",mail_address2)
        zip_code = re.findall(r"\d.*",mail_address2)
    except:
        city = None
        state = None
        zip_code = None
    print()
    print(f"scraping ====>{i[4]} {i[5]}")
    print("property_id",property_id)
    print("property_type",property_type)
    print("site_address",site_address)
    print("owner_id",owner_id)
    print("owner_name",owner_name)
    print("mail_address1",mail_address1)
    print("city",city)
    print("state",state)
    print("zip_code",zip_code)
    print("living_area",living_area)
    print("year_built",year_built)
    print("bldg_value",bldg_value)
    print("land_value",land_value)
    print("total_market_value",total_market_value)
    print("deed_date",deed_date)
    print("deed_type",deed_type)
    print()
    with open('Sharp.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([i[0],i[1],i[2],i[3],i[4],i[5],property_id,property_type,site_address,owner_id,owner_name,mail_address1,city,state,zip_code,land_value,bldg_value,total_market_value,living_area,year_built,deed_date,deed_type])
        count = count + 1
        print("Data Saved in CSV: ",count)

    return count




ul = "https://esearch.henderson-cad.org/"

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
        driver.find_element_by_xpath("//a[contains(text(),' By Address')]").click()
        time.sleep(5)

        search = driver.find_element_by_xpath("//input[@id='StreetNumber']")
        search.clear()
        search.send_keys(i[4])
        search1 = driver.find_element_by_xpath("//input[@id='StreetName']")
        search1.clear()
        search1.send_keys(i[5])
        search1.send_keys(Keys.ENTER)
        time.sleep(15)
        try:
            results = driver.find_elements_by_xpath("//div[@class='k-grid-content k-auto-scrollable']/table/tbody/tr")
            for result in range(0,len(results)):
                driver.find_elements_by_xpath("//div[@class='k-grid-content k-auto-scrollable']/table/tbody/tr")[result].click()
                time.sleep(5)
                count = scrao(count)
                driver.back()
                time.sleep(5)
        except:
            print("Search result is empty")
            count = scrao(count)
        driver.get(ul)
        time.sleep(3) 

