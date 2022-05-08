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
ul = "http://www.ottertailcounty.us/ez/publicsearch.php"
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
    writer.writerow(["Owner","Mail Address","Mail State","Mail City","Mail Zip Code","Site Address","Site Zip Code","Property Type","Living Area ","Land Value","Year Built","BLDG value","Total Accessed Value","Sale Date","Sale Amount"])

with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        company = str(company)
        company = company.replace("R","")
        company = company.lstrip()
        search = driver.find_element_by_xpath("//input[@id='OTCPIN']")
        time.sleep(1)
        search.clear()
        search.send_keys(company)
        search.send_keys(Keys.ENTER)
        time.sleep(3)
        a = f"//a[contains(text(),'{company}')]"
        try:
            driver.find_element_by_xpath(a).click()
            time.sleep(3)
            try:
                beta = driver.find_element_by_xpath("(//a[@class='type1'])[3]").get_attribute("href")
                try:
                    driver.get(beta)
                    time.sleep(2)
                    try:
                        
                        html = driver.page_source
                        resp = Selector(text=html)
                        owner = resp.xpath("((//td[@class='style13'])[11]/text())[1]").extract_first()
                        owner_Address = resp.xpath("normalize-space(((//td[@class='style13'])[11]/text())[3])").extract_first()
                        owner_city_state_zip = resp.xpath("normalize-space(((//td[@class='style13'])[11]/text())[6])").extract_first()
                        try:
                            owner_city_state_zip = str(owner_city_state_zip)
                            owner_city = re.findall(r"\w.*,",owner_city_state_zip)
                            owner_state = re.findall(r",.*[A-Z]",owner_city_state_zip)
                            owner_zip = re.findall(r"\s\s\d.*",owner_city_state_zip)
                        except:
                            owner_city = None
                            owner_state = None
                            owner_zip = None
                        
                        
                        site_address = resp.xpath("((//td[@class='style13'])[9]/p/text())[1]").extract_first()
                        try:
                            site_address = str(site_address)
                            site_add = re.findall(r".*\s",site_address) 
                            site_zip = re.findall(r"\s\s\d.*",site_address)
                        except:
                            site_add = None
                            site_zip = None
                        land_value = resp.xpath("((//span[contains(text(),'Total')])[1]//parent::div//parent::td/following-sibling::td//span/text())[1]").extract_first()
                        total_bldg_value = resp.xpath("((//span[contains(text(),'Total')])[2]//parent::div//parent::td/following-sibling::td/div)[1]/text()").extract_first()
                        total_accessed_value = resp.xpath("((//span[contains(text(),'Total')])[last()]//parent::div//parent::td/following-sibling::td/div/text())[1]").extract_first()

                        proper_type = resp.xpath("(//span[contains(text(),'Building Type: ')]//parent::td/following-sibling::td)[1]/span/text()").extract_first()
                        living_area = resp.xpath("((//span[contains(text(),'Age')]/parent::div/parent::td/parent::tr/following-sibling::tr)[1]/td)[3]/div/text()").extract_first()
                    except:
                        site_add = None
                        site_zip = None
                        owner_city = None
                        owner_state = None
                        owner_zip = None
                        owner_Address = None
                        owner = None
                        land_value = None
                        total_bldg_value = None
                        total_accessed_value = None
                        proper_type = None
                        living_area = None
                
                    try:
                        sales_btn = driver.find_element_by_xpath("//td[@class='style13']/a[contains(text(),'Data')]").get_attribute("href")
                        driver.get(sales_btn)
                        time.sleep(3)
                        html = driver.page_source
                        resp = Selector(text=html)
                        
                        year_built = resp.xpath("//span[contains(text(),'Year')]//parent::td/following-sibling::td/span/text()").extract_first()
                        sale_date = resp.xpath("(//span[contains(text(),'Date:')]//parent::td/following-sibling::td/span/text())[1]").extract_first()
                        sale_amt = resp.xpath("(//span[contains(text(),'Price:')]//parent::td/following-sibling::td/span/text())[1]").extract_first()
                    except:
                        year_built = None
                        sale_date = None
                        sale_amt = None

                    with open('test.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([owner,owner_Address,owner_state,owner_city,owner_zip,site_add,site_zip,proper_type,living_area,land_value,year_built,total_bldg_value,total_accessed_value,sale_date,sale_amt])
                        count = count + 1
                        print("Data Saved in CSV:",count)

                    driver.get(ul)
                    time.sleep(3) 
                except:
                    print("Cannot access First Page")
                    driver.get(ul)
                    time.sleep(3) 

            except:
                print("There is nothing here to scrape")
                driver.get(ul)
                time.sleep(3) 
                        
        except:
            print("Search Result is empty")
            driver.get(ul)
            time.sleep(3) 
        