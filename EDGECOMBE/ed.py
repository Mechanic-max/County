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
ul = "https://taxpa.edgecombecountync.gov/paas/index.asp?DEST=pSearch"
path = which("chromedriver")
options = Options()
options.add_experimental_option("detach", True)
#options.add_argument("--headless")
ua = UserAgent()
userAgent = ua.random
options.add_argument(f'user-agent={userAgent}')
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(executable_path=path,options=options)
driver.get(ul)
time.sleep(2)

with open('test.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Parcel Id","Site Address","Owner","Mail Address","Mail City","Mail State","Mail Zip Code","Sale Date","Sale Amount","Land Value","BLDG value","Total Accessed Value","Property Type"])

with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        search = driver.find_element_by_xpath("//input[@id='OWNER']")
        time.sleep(1)
        search.clear()
        search.send_keys(company)
        search.send_keys(Keys.ENTER)
        time.sleep(3)
        try:
            links = driver.find_elements_by_xpath("//td[@id='wText']/a")
            for i in range(0,len(links)):
                driver.find_elements_by_xpath("//td[@id='wText']/a")[i].click()
                time.sleep(3)
                try:
                    html = driver.page_source
                    resp = Selector(text=html)
                    parcel_id = resp.xpath("//td[contains(text(),'Parcel:')]/text()").extract_first()
                    if parcel_id:
                        parcel_id = str(parcel_id)
                        parcel_id = parcel_id.replace("Parcel:",'')
                        parcel_id = parcel_id.lstrip()
                    site_address = resp.xpath("normalize-space((//td[@id='wText'])[1]/text())").extract_first()
                    owners = resp.xpath("normalize-space((//td[@id='wText'])[14]/text())").extract_first()
                    mail_address = resp.xpath("((//td[@id='wText'])[15]/text())[1]").extract_first()
                    mail_city_zip = resp.xpath("((//td[@id='wText'])[15]/text())[2]").extract_first()
                    try:
                        mail_city_zip = str(mail_city_zip)
                        mail_city = re.findall(r"^[^,]+",mail_city_zip)
                        mail_state = re.findall(r"\s\w\w\s",mail_city_zip)
                        mail_zip = re.findall(r"\d.*",mail_city_zip)
                    except:
                        mail_city = None
                        mail_state = None
                        mail_zip = None
                    
                    sale_date = resp.xpath("(//td[@id='wText'])[17]/text()").extract_first()
                    sale_amt = resp.xpath("normalize-space((//td[@id='wText'])[18]/text())").extract_first()
                    land_value = resp.xpath("(//td[@id='wText'])[20]/text()").extract_first()
                    total_bldg_value = resp.xpath("(//td[@id='wText'])[21]/text()").extract_first()
                    total_accessed_value = resp.xpath("(//td[@id='wText'])[24]/text()").extract_first()
                    
                    try:
                        
                        driver.find_element_by_xpath("//input[contains(@value,'Buildings')]").click()
                        time.sleep(2)
                        try:
                            property_type = driver.find_element_by_xpath("(//td[@id='wText'])[2]").text
                        except:
                            property_type = None
                        
                        driver.execute_script("window.history.go(-1)")
                        time.sleep(2)
                    except:
                        property_type = None
                        driver.execute_script("window.history.go(-1)")
                        time.sleep(2)
                    with open('test.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([parcel_id,site_address,owners,mail_address,mail_city,mail_state,mail_zip,sale_date,sale_amt,land_value,total_bldg_value,total_accessed_value,property_type])
                        count = count + 1
                        print("Data Saved in CSV:",count)
                    driver.execute_script("window.history.go(-1)")
                    time.sleep(2)
                    
                except:
                    print("There is nothing to scrape")
                    driver.execute_script("window.history.go(-1)")
                    time.sleep(2)
        except:
            print("There is no searched records")
            driver.get(ul)
            time.sleep(2)


# try:

# driver.find_element_by_xpath("//input[contains(@value,'Prop Card')]").click()
# time.sleep(2)

# try:
#     driver.find_element_by_xpath("(//h1/input[@type='button'])[1]").click()
#     time.sleep(2)
#     try:
#         year_built = driver.find_element_by_xpath("(//td[@id='pText'])[30]").text
#     except:
#         year_built = None
#     try:
#         bedrooms = driver.find_element_by_xpath("(//td[contains(text(),'Bedrooms')]/following-sibling::td)[1]").text
#     except:
#         bedrooms = None
    
#     try:
#         full_baths = driver.find_element_by_xpath("(//td[contains(text(),'Bath')]/following-sibling::td)[1]").text
#     except:
#         full_baths = None
#     try:
#         half_baths = driver.find_element_by_xpath("(//td[contains(text(),'Hf Baths')]/following-sibling::td)[1]").text
#     except:
#         half_baths = None

# except:
#     year_built = None
#     bedrooms = None
#     full_baths = None
#     half_baths = None

#     print("Mushkil ha")
# driver.execute_script("window.history.go(-1)")
# time.sleep(2)
# except:
# property_type = None
# driver.execute_script("window.history.go(-1)")
# time.sleep(2)