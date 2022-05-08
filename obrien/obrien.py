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
ul = "https://obrien.iowaassessors.com/search.php"
path = which("chromedriver")
options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--headless")
ua = UserAgent()
userAgent = ua.random
options.add_argument(f'user-agent={userAgent}')
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(executable_path=path,options=options)
driver.get(ul)
time.sleep(2)
with open('ober.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Parcel ID","Owner","Site Address","Site City","Site State","Site Zip","Mail address","Mail City","Mail State","Mail Zip","Land Value", "BLDG value", "Total Value","Sale Date","Sale Price","Prppery_type","Year Built","Living Area(SQFT)","Beds","Baths"])

try:
    driver.find_element_by_xpath("//input[contains(@value,'Yes, I Agree')]").click()
    time.sleep(3)
except:
    print("Pop up didn't appear")


with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        if len(company) == 4:
            company = str(company)
            company = f"000000{company}"
        elif len(company) == 5:
            company = str(company)
            company = f"00000{company}"
        elif len(company) == 6:
            company = str(company)
            company = f"0000{company}"
        elif len(company) == 7:
            company = str(company)
            company = f"000{company}"
        elif len(company) == 8:
            company = str(company)
            company = f"00{company}"
        else:
            company = company
        search = driver.find_element_by_xpath("//input[@id='iparcelNumber']")
        time.sleep(3)
        search.clear()
        search.send_keys(company)
        search.send_keys(Keys.ENTER)
        time.sleep(5)
        try:

            html = driver.page_source
            resp = Selector(text=html)

            Parcel_id = resp.xpath("//td[contains(text(),'Parcel Number')]/following-sibling::td/text()").extract_first()
            owner_name = resp.xpath("normalize-space(//td[contains(text(),'Deed Holder:')]/following-sibling::td/text())").extract_first()
            site_address = resp.xpath("normalize-space((//td[contains(text(),'Property Address:')]/following-sibling::td/text())[1])").extract_first()
            site_city = resp.xpath("(//td[contains(text(),'Property Address:')]/following-sibling::td/text())[2]").extract_first()
            if site_city:
                site_city = str(site_city)
                site_citi = re.findall(r"^[^,]+",site_city)
                site_state = re.findall(r",\s\w*",site_city)
                site_zip = re.findall(r"\d\d\d\d\d",site_city)
            else:
                site_citi = None
                site_state = None
                site_zip = None
            
            mail_address = resp.xpath("(//td[contains(text(),'Mailing Address:')]/following-sibling::td)[1]/text()").extract_first()
            st_mail_add = resp.xpath("(//td[contains(text(),'Mailing Address:')]/following-sibling::td/text())[2]").extract_first()
            if st_mail_add:
                st_mail_add = str(st_mail_add)
                mail_state = re.findall(r",\s\w*", st_mail_add)
                mail_city = re.findall(r"^[^,]+", st_mail_add)
                mail_zip = re.findall(r"\d\d\d\d\d", st_mail_add)
            else:
                mail_state = None
                mail_zip = None  
                mail_city = None

            sale_date = resp.xpath("//div[@id='sale0']/div[@class='saleColumn']/text()").extract_first()
            sale_price = resp.xpath("//div[@id='sale0']/div[@class='saleColumn2']/text()").extract_first()

            land_value = resp.xpath("(//th[contains(text(),'Land')]/parent::tr/following-sibling::tr/td)[1]/text()").extract_first()
            bld = []
            bldg_value = resp.xpath("(//th[contains(text(),'Land')]/parent::tr/following-sibling::tr/td)[2]/text()").extract_first()
            bldg_value1 = resp.xpath("(//th[contains(text(),'Land')]/parent::tr/following-sibling::tr/td)[3]/text()").extract_first()
            bld.append(bldg_value)
            bld.append(bldg_value1)
            total_accessed_value = resp.xpath("(//th[contains(text(),'Land')]/parent::tr/following-sibling::tr/td)[4]/text()").extract_first()
            
            
            try:
                driver.find_element_by_xpath("//div[@id='res0']").click()
                time.sleep(1)
                html = driver.page_source
                resp = Selector(text=html)
                bed = []
                living_area = resp.xpath("(//div[contains(text(),'TLA')]/following-sibling::div)[1]/text()").extract_first()
                built_year = resp.xpath("(//div[contains(text(),'Year Built:')]/following-sibling::div)[1]/text()").extract_first()
                property_type = resp.xpath("normalize-space((//div[contains(text(),'Occupancy:')]/following-sibling::div)[1]/text())").extract_first()
                baths = resp.xpath("(//div[contains(text(),'Full Bath')]/following-sibling::div)[1]/text()").extract_first()
                bed1 = resp.xpath("(//div[contains(text(),'Bedrooms Above:')]/following-sibling::div)[1]/text()").extract_first()
                bed2 = resp.xpath("(//div[contains(text(),'Bedrooms Below:')]/following-sibling::div)[1]/text()").extract_first()
                bed.append(bed1)
                bed.append(bed2)
            except:
                living_area = None
                built_year = None
                property_type = None
                baths = None
                bed = None      

            with open('ober.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([Parcel_id,owner_name,site_address,site_citi,site_state,site_zip,mail_address,mail_city,mail_state,mail_zip,land_value,bld,total_accessed_value,sale_date,sale_price,property_type,built_year,living_area,bed,baths])
                count = count + 1 
                print("Data Saved in CSV:",count)
            driver.get(ul)
            time.sleep(3) 
        except:
            print("Search Result is empty")
            driver.get(ul)
            time.sleep(3) 
        

driver.close()