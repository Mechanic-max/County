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
from pandas import DataFrame
import re

count = 0
ul = "http://www2.co.davidson.nc.us/taxnet/RealEstate.aspx"
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
with open('davidson_sample.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name","Site Address", "Mail Address", "Mail city","Mail State","Zip Code","BLDG Value","land value","Assessed Value","Sale Year","Sale Month","Sale Price","Year Built","Beds","Bath(ADD Full and Hald)"])
with open("input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        search = driver.find_element_by_xpath("//input[@id='ctl00_contentplaceholderRealEstateSearch_usercontrolRealEstateSearch_textboxAccount']")
        search.send_keys(company)
        search.send_keys(Keys.ENTER)
        time.sleep(2)
        try:
            btn = driver.find_element_by_xpath("//td[@class='HyperLinkField']/a")
            btn.click()
            time.sleep(1)
            nxt_btn = driver.find_element_by_xpath("(//span[@class='ajax__tab_tab'])[5]")
            nxt_btn.click()
            time.sleep(1)
            link = driver.find_element_by_xpath("//td[@class='HyperLinkField']/a[contains(@href,'AppraisalCard')]").get_attribute("href")
            driver.get(link)
            time.sleep(2)
            html = driver.page_source
            resp = Selector(text=html)

            name = resp.xpath("//span[@id='ctl04_labelAccountNameAValue']/text()").extract_first()
            site_address = resp.xpath("//span[@id='ctl04_labelAddressValue']/text()").extract_first()
            year_built = resp.xpath("//span[@id='ctl04_labelActualYearBuiltValue']/text()").extract_first()
            
            bld = []
            bld1 = resp.xpath("//span[@id='ctl04_labelDepreciationBuildingValueValue']/text()").get()
            bld2 = resp.xpath("//span[@id='ctl04_labelDepreciationOBXFValueValue']/text()").get()
            try:
                bld.append(bld1)
            except:
                try:
                    bld.append(bld2)
                except:
                    bld = []
            land_value = resp.xpath("//span[@id='ctl04_labelTotalLandValueValue']/text()").get()
            total_assessed_value = resp.xpath("//span[@id='ctl04_labelTotalLandValueValue']/text()").get()
            sale_month = resp.xpath("//span[@id='ctl04_repeaterSales_ctl00_labelSaleMonth']/text()").get()
            sale_year = resp.xpath("//span[@id='ctl04_repeaterSales_ctl00_labelSaleYear']/text()").get()
            sale_price = resp.xpath("//span[@id='ctl04_repeaterSales_ctl00_labelSale_SalePrice']/text()").get()
            beds_bath = resp.xpath("//span[@id='ctl04_repeaterBedBathHalf_ctl00_labelBedBathHalf_BreakdownValue']/text()").extract_first()
            try:
                beds = re.findall(r"^([0-9]+)",beds_bath)
            except:
                beds = None
            baths = str(beds_bath)
            baths = baths.replace('000', '')
            driver.back()
            owner_btn = driver.find_element_by_xpath("//span[@id='__tab_ctl00_contentplaceholderRealEstateWorkplace_tabcontainerWorkSpace_tabpanelOwners']")
            owner_btn.click()
            time.sleep(2)
            html = driver.page_source
            resp = Selector(text=html)
            mail_address = resp.xpath("(//table[@id='ctl00_contentplaceholderRealEstateWorkplace_tabcontainerWorkSpace_tabpanelOwners_usercontrolRealEstateParcelOwnersData_gridviewParcelOwnersData']//td)[3]/text()").extract_first()
            mail_city = resp.xpath("(//table[@id='ctl00_contentplaceholderRealEstateWorkplace_tabcontainerWorkSpace_tabpanelOwners_usercontrolRealEstateParcelOwnersData_gridviewParcelOwnersData']//td)[4]/text()").extract_first()
            mail_state = resp.xpath("(//table[@id='ctl00_contentplaceholderRealEstateWorkplace_tabcontainerWorkSpace_tabpanelOwners_usercontrolRealEstateParcelOwnersData_gridviewParcelOwnersData']//td)[5]/text()").extract_first()
            zip_code = resp.xpath("(//table[@id='ctl00_contentplaceholderRealEstateWorkplace_tabcontainerWorkSpace_tabpanelOwners_usercontrolRealEstateParcelOwnersData_gridviewParcelOwnersData']//td)[6]/text()").extract_first()
            if zip_code:
                zil = ""
                
                zil = str(zip_code)
                zil = zil.replace("-0000","")

            with open('davidson_sample.csv', 'a',newline='') as file:
                writer = csv.writer(file)
                writer.writerow([name, site_address,mail_address, mail_city,mail_state,zil,bld,land_value,total_assessed_value,sale_year,sale_month,sale_price,year_built,beds,baths])
                count = count + 1
                print("Data Saved in CSV :",count)
        
        except:
            print("Search Result is empty")
            
        driver.get(ul)
        time.sleep(2)
        search = driver.find_element_by_xpath("//input[@id='ctl00_contentplaceholderRealEstateSearch_usercontrolRealEstateSearch_textboxAccount']")
        search.clear()