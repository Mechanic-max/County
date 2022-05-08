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
with open('test.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["ID","owner_name","owner_address","city","state","zip","site_address","site_city","site_state","site_zip","tex_year","property_class","land_value","bldg_value","total_market_value","property_type","living_area","year_built","bed1","bed2"])



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
        ul = f"http://www2.co.black-hawk.ia.us/website/bhmap/bhRepDet.asp?apn={company}"
        try:
            driver.get(ul)
            time.sleep(1)

            html = driver.page_source
            resp = Selector(text=html)
            
            owner_name = resp.xpath("(//table)[2]/tbody/tr[2]/td[2]/font/text()").extract_first()
            owner_address = resp.xpath("(//table)[2]/tbody/tr[2]/td[3]/font/text()[last()-1]").extract_first()
            city_state_zip = resp.xpath("(//table)[2]/tbody/tr[2]/td[3]/font/text()[last()]").extract_first()
            try:
                city_state_zip = str(city_state_zip)
                city = re.findall(r"^[^,]+",city_state_zip)
                state = re.findall(r"\s\w\w\s",city_state_zip)
                zip = re.findall(r"\d\d\d\d\d$",city_state_zip)
            except:
                city = None
                state = None
                zip = None
            site_address = resp.xpath("(//table)[3]/tbody/tr[2]/td[1]/font/text()[last()-1]").extract_first()
            site_city_state_zip = resp.xpath("(//table)[3]/tbody/tr[2]/td[1]/font/text()[last()]").extract_first()
            try:
                city_state_zip = str(site_city_state_zip)
                site_city = re.findall(r"^[^,]+",site_city_state_zip)
                site_state = re.findall(r"\s\w\w\s",site_city_state_zip)
                site_zip = re.findall(r"\d\d\d\d\d$",site_city_state_zip)
            except:
                site_city = None
                siite_state = None
                site_zip = None
            tex_year = resp.xpath("(//b[contains(text(),'Year')][1]/parent::font/parent::td[@class='nogray'])[2]/parent::tr/following-sibling::tr/td[1]/font/b/text()").extract_first()
            property_class = resp.xpath("(//b[contains(text(),'Year')][1]/parent::font/parent::td[@class='nogray'])[2]/parent::tr/following-sibling::tr/td[2]/font/b/text()").extract_first()
            land_value = resp.xpath("(//b[contains(text(),'Land')])[3]/parent::font/ancestor::td[1]/parent::tr/following-sibling::tr[1]/td[1]/font/text()").extract_first()
            bldg_value = resp.xpath("(//b[contains(text(),'Land')])[3]/parent::font/ancestor::td[1]/parent::tr/following-sibling::tr[1]/td[2]/font/text()").extract_first()
            total_market_value = resp.xpath("(//b[contains(text(),'Land')])[3]/parent::font/ancestor::td[1]/parent::tr/following-sibling::tr[1]/td[4]/font/text()").extract_first()
            property_type = resp.xpath("(//b[contains(text(),'Type')])[3]/ancestor::tr/following-sibling::tr/td[1]/font/text()").extract_first()
            living_area = resp.xpath("(//b[contains(text(),'Type')])[3]/ancestor::tr/following-sibling::tr/td[3]/font/text()").extract_first()
            year_built = resp.xpath("(//b[contains(text(),'Year Built')])[1]/ancestor::tr/following-sibling::tr/td[1]/font/text()").extract_first()
            bed1 = resp.xpath("(//b[contains(text(),'Bedrooms Above')])[1]/ancestor::tr/following-sibling::tr/td[3]/font/text()").extract_first()
            bed2 = resp.xpath("(//b[contains(text(),'Bedrooms Above')])[1]/ancestor::tr/following-sibling::tr/td[4]/font/text()").extract_first()
            # # if bed1 and bed2:
            # #     bed1 = str(bed1)
            # #     bed2 = str(bed2)
            # #     be = int(bed1)
            # #     be2 = int(bed2)
            # #     final_bed = be+be2
            # else:
            #     final_bed = 0

            with open('test.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([company,owner_name,owner_address,city,state,zip,site_address,site_city,site_state,site_zip,tex_year,property_class,land_value,bldg_value,total_market_value,property_type,living_area,year_built,bed1,bed2])
                count = count + 1
                print("Data Saved in CSV: ",count)
        except:
            print("Search results is empty")