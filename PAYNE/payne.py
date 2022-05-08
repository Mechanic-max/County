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
ul = "https://property.spatialest.com/ok/payne#/"
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
time.sleep(4)

with open('test.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["ACCT No","Site Address","Owner","Mail Address","Mail City","Mail Zip","Property Type","Land value","Bldg Value","Total Accessed Value","Sale Date","Sale Amount","Living Area","Year Built","Bedrooms","Full Bath","Half Bath"])

try:
    driver.find_element_by_xpath("//button[contains(text(),'I Understand')]").click()
    time.sleep(2)
except:
    print("Pop up did'nt appear")

with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='primary_search']")))
        try:
            driver.find_element_by_id('primary_search').send_keys(Keys.CONTROL + "a")
            driver.find_element_by_id('primary_search').send_keys(Keys.DELETE)
        except:
            break
        element.send_keys(company)
        
        element.send_keys(Keys.ENTER)
        time.sleep(2)
        try:
            links = driver.find_elements_by_xpath("//div[@class='tile']/a")
            for i in range(0,len(links)):
                driver.find_elements_by_xpath("//div[@class='tile']/a")[i].click()
                time.sleep(3)
                try:
                    html = driver.page_source
                    resp = Selector(text=html)
                    
                    ACCT_No = resp.xpath("//div[@class='owner']/span/text()").extract_first()
                    site_address = resp.xpath("//div[@class='location text-highlight']/span/text()").extract_first()
                    owner = resp.xpath("(//div[@class='mailing']/div/text())[1]").extract_first()
                    mail_address = resp.xpath("(//div[@class='mailing']/div/text())[2]").extract_first()
                    mail_city_zip = resp.xpath("(//div[@class='mailing']/div/text())[3]").extract_first()
                    try:
                        mail_city_zip = str(mail_city_zip)
                        mail_city = re.findall(r"^\S*",mail_city_zip)
                        mail_state = re.findall(r"\s\w\w\s",mail_city_zip)
                        mail_zip = re.findall(r"\d.*$",mail_city_zip)
                    except:
                        mail_city = None
                        mail_state = None
                        mail_zip = None
                    
                    property_type = resp.xpath("//span[contains(text(),'Class')]/following-sibling::span/text()").extract_first()
                    land_value = resp.xpath("//span[contains(text(),'Land Value')]/following-sibling::span/text()").extract_first()
                    bldg_value = resp.xpath("//span[contains(text(),'Building Value')]/following-sibling::span/text()").extract_first()
                    total_accessed_value = resp.xpath("//span[contains(text(),'Total Market Value')]/following-sibling::span/text()").extract_first()
                    sale_date = resp.xpath("((//table[@class='table table-striped table-nolines '])[1]//td)[1]/text()").extract_first()
                    sale_amount = resp.xpath("((//table[@class='table table-striped table-nolines '])[1]//td)[2]/text()").extract_first()
                    living_area = resp.xpath("//span[contains(text(),'Finished Living Area')]/following-sibling::span/text()").extract_first()
                    year_built = resp.xpath("//span[contains(text(),'Year Built')]/following-sibling::span/text()").extract_first()
                    Bedrooms = resp.xpath("//span[contains(text(),'Bedrooms')]/following-sibling::span/text()").extract_first()
                    full_bath = resp.xpath("//span[contains(text(),'Full Bath')]/following-sibling::span/text()").extract_first()
                    half_bath = resp.xpath("//span[contains(text(),'Half Bath')]/following-sibling::span/text()").extract_first()
                    
                except:
                    ACCT_No = None
                    site_address = None
                    owner = None
                    mail_address = None
                    mail_city = None
                    mail_state = None
                    mail_zip = None
                    property_type = None
                    land_value = None
                    bldg_value = None
                    total_accessed_value = None
                    sale_date = None
                    sale_amount = None
                    living_area = None
                    year_built = None
                    Bedrooms = None
                    full_bath = None
                    half_bath = None
        
                with open('test.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([ACCT_No,site_address,owner,mail_address,mail_city,mail_zip,property_type,land_value,bldg_value,total_accessed_value,sale_date,sale_amount,living_area,year_built,Bedrooms,full_bath,half_bath])
                    count = count + 1
                    print("Data Saved in CSV",count)
                driver.back()
                time.sleep(2)
            driver.get(ul)
            time.sleep(3)
                        
        except:
            print("Search Result is empty")
            driver.get(ul)
            time.sleep(2)
        
driver.close()