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
import wget

count = 0
with open('test.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Parce lID","owner_name","site_address","site_city","site_state","site_zip","mailing_address","mailing_city","mailing_state","mailing_zip_code","land_use_code","Tex_year","land_value","bldg_value","total_accessed_value","sale_date","sale_price","property_type","living_area","Atucal_year_built"])


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



with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        ul = f"https://engage.xsoftinc.com/vanderburgh/Map/GetParcelDetail?parcelId={company}"
        try:
            driver.get(ul)
            time.sleep(2)

            html = driver.page_source
            resp = Selector(text=html)

            site_address = resp.xpath("normalize-space(//th[contains(text(),'Property Address')]/following-sibling::td/text()[1])").get()
            site_city = resp.xpath("normalize-space(//th[contains(text(),'Property Address: ')]/following-sibling::td/text()[2])").extract_first()
            site_state = resp.xpath("normalize-space(//th[contains(text(),'Property Address: ')]/following-sibling::td/text()[3])").extract_first()
            site_zip = resp.xpath("normalize-space(//th[contains(text(),'Property Address: ')]/following-sibling::td/text()[4])").extract_first()
            
            land_use_code = resp.xpath("(//th[contains(text(),'Property Class:')]/following-sibling::td/text())[1]").extract_first()
            owner_name = resp.xpath("(//th[contains(text(),'CURRENT OWNER')]/parent::tr/following-sibling::tr/td)[1]/text()").extract_first()
            mailing_address = resp.xpath("(//th[contains(text(),'CURRENT OWNER')]/parent::tr/following-sibling::tr/td)[2]/text()").extract_first()
            mailing_city = resp.xpath("(//th[contains(text(),'CURRENT OWNER')]/parent::tr/following-sibling::tr/td)[3]/text()").extract_first()
            mailing_state = resp.xpath("(//th[contains(text(),'CURRENT OWNER')]/parent::tr/following-sibling::tr/td)[4]/text()").extract_first()
            mailing_zip_code = resp.xpath("(//th[contains(text(),'CURRENT OWNER')]/parent::tr/following-sibling::tr/td)[5]/text()").extract_first()
            
            Tex_year = resp.xpath("(//th[contains(text(),'Assessment Year')]/parent::tr/following-sibling::tr[1]/td)[1]/text()").extract_first()
            land_value = resp.xpath("(//th[contains(text(),'Assessment Year')]/parent::tr/following-sibling::tr[1]/td)[3]/text()").extract_first()
            bldg_value = resp.xpath("(//th[contains(text(),'Assessment Year')]/parent::tr/following-sibling::tr[1]/td)[9]/text()").extract_first()
            total_accessed_value = resp.xpath("(//th[contains(text(),'Assessment Year')]/parent::tr/following-sibling::tr[1]/td)[last()]/text()").extract_first()
            
            property_type = resp.xpath("(//th[contains(text(),'Grade')]/parent::tr/following-sibling::tr[1]/td)[1]/text()").extract_first()
            Atucal_year_built = resp.xpath("(//th[contains(text(),'Grade')]/parent::tr/following-sibling::tr[1]/td)[3]/text()").extract_first()
            living_area = resp.xpath("(//th[contains(text(),'Grade')]/parent::tr/following-sibling::tr[1]/td)[last()]/text()").extract_first()
            
            sale_price = resp.xpath("(//th[contains(text(),'Sale Price')]/parent::tr/following-sibling::tr[1]/td)[last()]/text()").extract_first()
            sale_date = resp.xpath("(//th[contains(text(),'Sale Price')]/parent::tr/following-sibling::tr[1]/td)[last()-1]/text()").get()

            with open('test.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([company,owner_name,site_address,site_city,site_state,site_zip,mailing_address,mailing_city,mailing_state,mailing_zip_code,land_use_code,Tex_year,land_value,bldg_value,total_accessed_value,sale_date,sale_price,property_type,living_area,Atucal_year_built])
                count = count + 1
                print("Data Saved in CSV:",count)
        except:
            print("Search results is empty")
            break