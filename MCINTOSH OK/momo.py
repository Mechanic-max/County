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
# with open('test.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(["Source_Parcel","parcel_id","owner_name1","owner_name2","site_address","site_city","site_state","site_zip","owner_address","owner_city","owner_state","owner_zip","property_class","Atucal_year_built","living_area","sale_date","sale_price","land_value","BLDG Value","total_market_value","Bedrooms","Full_Baths","Half_Baths"])

ul = "https://www.actdatascout.com/RealProperty/Oklahoma/McIntosh"


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
time.sleep(30)



with open("./input.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company = i[0]
        ifram = driver.find_element_by_xpath('//iframe')
        ifram.click()
        driver.switch_to.frame(ifram)
        #WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe")))
        # driver.switch_to.frame(driver.find_element_by_xpath("(//iframe)[last()]"))
        time.sleep(5)
        # driver.find_element_by_xpath("//li[@class='text-right']/a").click()
        # time.sleep(3)
        search = driver.find_element_by_xpath("//input[@id='FirstName']")
        # search.clear()
        time.sleep(1)
        search.send_keys(company)
        time.sleep(1)
        search.send_keys(Keys.ENTER)
        time.sleep(10)
 
        # try:
        #     html = driver.page_source
        #     resp = Selector(text=html)
            
        #     parcel_id = resp.xpath("//td[contains(text(),'Parcel ID:')]/text()").extract_first()
        #     owner_name1 = resp.xpath("//td[contains(text(),'Owner1')]/following-sibling::td/text()").extract_first()
        #     owner_name2 = resp.xpath("//td[contains(text(),'Owner2')]/following-sibling::td/text()").extract_first()
        #     owner_address = resp.xpath("//td[contains(text(),'Mailing Address')]/following-sibling::td[1]/text()").extract_first()
        #     owner_city_state_zip = resp.xpath("//td[contains(text(),'City,  State,  Zip')]/following-sibling::td[1]/text()").extract_first()
        #     try:
        #         owner_city_state_zip = str(owner_city_state_zip)
        #         owner_city = re.findall(r"^[^\s]+",owner_city_state_zip)
        #         owner_state = re.findall(r"\s\w\w\s",owner_city_state_zip)
        #         owner_zip = re.findall(r"\d.*",owner_city_state_zip)
        #     except:
        #         owner_city = None
        #         owner_state = None
        #         owner_zip = None
            

        #     site_address = resp.xpath("//td[contains(text(),'Property Address')]/following-sibling::td[1]/text()").extract_first()
        #     site_state_zip = resp.xpath("//td[contains(text(),'City, State, Zip')]/following-sibling::td/text()").extract_first()
        #     try:
        #         site_state_zip = str(site_state_zip)
        #         site_city = re.findall(r"^[^\s]+",site_state_zip)
        #         site_state = re.findall(r"\s\w\w\s",site_state_zip)
        #         site_zip = re.findall(r"\d.*",site_state_zip)
        #     except:
        #         site_city = None
        #         site_state = None
        #         site_zip = None
            
        #     property_class = resp.xpath("//td[contains(text(),'Class Code/Description')]/following-sibling::td/text()").extract_first()
        #     living_area = resp.xpath("//td[contains(text(),'Deeded Acres')]/following-sibling::td/text()").extract_first()
        #     try:
        #         driver.find_element_by_xpath("//span[contains(text(),'Sales')]/parent::a").click()
        #         time.sleep(3)
        #         html = driver.page_source
        #         resp = Selector(text=html)
        #         sale_date = resp.xpath("(//td[contains(text(),'Sale Date')])[1]/parent::tr/following-sibling::tr[1]/td[1]/text()").extract_first()
                
        #         sale_price = resp.xpath("(//td[contains(text(),'Sale Date')])[1]/parent::tr/following-sibling::tr[1]/td[2]/text()").extract_first()
            

        #     except:
        #         sale_date = None
        #         sale_price = None
            
        #     try:
        #         driver.find_element_by_xpath("//span[contains(text(),'Residential')]/parent::a").click()
        #         time.sleep(3)
        #         html = driver.page_source
        #         resp = Selector(text=html)
                
        #         Atucal_year_built = resp.xpath("//td[contains(text(),'Year Built')]/following-sibling::td/text()").extract_first()
                
        #         Bedrooms = resp.xpath("//td[contains(text(),'Bedrooms')]/following-sibling::td/text()").extract_first()
        #         Full_Baths = resp.xpath("//td[contains(text(),'Full Baths')]/following-sibling::td/text()").extract_first()
        #         Half_Baths = resp.xpath("//td[contains(text(),'Half Baths')]/following-sibling::td/text()").extract_first()
            

        #     except:
        #         Atucal_year_built = None
        #         Bedrooms = None
        #         Full_Baths = None
        #         Half_Baths = None
            
        #     try:
        #         driver.find_element_by_xpath("//span[contains(text(),'Assessed Values')]/parent::a").click()
        #         time.sleep(3)
        #         html = driver.page_source
        #         resp = Selector(text=html)
        #         land_value = resp.xpath("//td[contains(text(),'Assessed Land')]/following-sibling::td/text()").extract_first()
                
        #         bldg_value = resp.xpath("//td[contains(text(),'Assessed Buildings')]/following-sibling::td/text()").extract_first()
        #         total_market_value = resp.xpath("//td[contains(text(),'Total Assessed Value')]/following-sibling::td/text()").extract_first()
            

        #     except:
        #         land_value = None
        #         total_market_value = None
        #         bldg_value = None

    
            
        #     with open('test.csv', 'a', newline='') as file:
        #         writer = csv.writer(file)
        #         writer.writerow([i[0],parcel_id,owner_name1,owner_name2,site_address,site_city,site_state,site_zip,owner_address,owner_city,owner_state,owner_zip,property_class,Atucal_year_built,living_area,sale_date,sale_price,land_value,bldg_value,total_market_value,Bedrooms,Full_Baths,Half_Baths])
        #         count = count + 1
        #         print("Data Saved in CSV",count)
                  
        # except:
        #     print("Search result is empty")

        driver.get(ul)
        time.sleep(7)

driver.close()