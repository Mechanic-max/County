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
import requests

count = 0
# with open('test.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(["pin","owner_name","Site_address","Mail address","Mail city","Mail state","Mail zip","Land_Use_Code","Built_Year","Living_area","Bedrooms","Full_Bath","Half_Bath","Sale_dates","Sale_price","Land_Values","Market_Values"])


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
        company = str(company)
        if len(company) == 3:
            company = f"00000{company}"
        elif len(company) == 4:
            company = f"0000{company}"
        elif len(company) == 5:
            company = f"000{company}"
        elif len(company) == 6:
            company = f"00{company}"
        elif len(company) == 7:
            company = f"0{company}"
        else:
            company = company
        ul = f"https://air.norfolk.gov/#/property/{company}"
        try:
            driver.get(ul)
            time.sleep(10)

            html = driver.page_source
            resp = Selector(text=html)

            pin = resp.xpath("//span[contains(text(),'Account Number')]/following-sibling::span/text()").extract_first()
            owner_name = resp.xpath("//span[contains(text(),'Owner Name')]/following-sibling::span/text()").extract_first()
            Land_Use_Code = resp.xpath("//span[contains(text(),'Property Use')]/following-sibling::span/text()").extract_first()
            Site_address = resp.xpath("//span[contains(text(),'Property Address')]/following-sibling::span/text()").extract_first()
            Mailing_address = resp.xpath("//span[contains(text(),'Mailing Address')]/following-sibling::span/text()").extract_first()
            Built_Year = resp.xpath("//span[contains(text(),'Year Built')]/following-sibling::span/text()").extract_first()
            Living_area = resp.xpath("//span[contains(text(),'Finished Living Area')]/following-sibling::span/text()").extract_first()
            Bedrooms = resp.xpath("//span[contains(text(),'Bedrooms')]/following-sibling::span/text()").extract_first()
            Full_Bath = resp.xpath("//span[contains(text(),'Full Baths')]/following-sibling::span/text()").extract_first()
            Half_Bath = resp.xpath("//span[contains(text(),'Half Baths')]/following-sibling::span/text()").extract_first()
            Sale_dates = resp.xpath("//th[contains(@title,'Transfer Date')]/parent::tr/parent::thead/following-sibling::tbody/tr[1]/td[2]/text()").get()
            Sale_price = resp.xpath("//th[contains(@title,'Transfer Date')]/parent::tr/parent::thead/following-sibling::tbody/tr[1]/td[3]/text()").get()
            Land_Values = resp.xpath("//th[contains(@title,'Land Value')]/parent::tr/parent::thead/following-sibling::tbody/tr[1]/td[2]/text()").get()
            Market_Values = resp.xpath("//th[contains(@title,'Land Value')]/parent::tr/parent::thead/following-sibling::tbody/tr[1]/td[last()]/text()").get()

            Mailing_address = str(Mailing_address)
            zip_code = re.findall(r"\s\d\d\d\d\d",Mailing_address)
            city = ''
            state = ''
            if zip_code:
                for zip in zip_code:
                    zip = str(zip)
                    zip = zip.strip()
                    request_url = f"http://api.zippopotam.us/us/{zip}"
                    print(request_url)
                    zone = requests.get(request_url)
                    if zone.status_code == 200:
                        data = zone.json()
                        if data:
                            city = data['places'][0]['place name']
                            state = data['places'][0]['state abbreviation']
            else:
                zip = ''
                city = ''
                state = ''

            address = Mailing_address.replace(city, '').replace(state, '').replace(zip,'')
            
            print("pin: ",pin)
            print("owner_name: ",owner_name)
            print("Site_address: ",Site_address)
            print("address: ",address)
            print("state: ",state)
            print("city: ",city)
            print("zip: ",zip)
            print("Land_Use_Code: ",Land_Use_Code)
            print("Built_Year: ",Built_Year)
            print("Living_area: ",Living_area)
            print("Bedrooms: ",Bedrooms)
            print("Full_Bath: ",Full_Bath)
            print("Half_Bath: ",Half_Bath)
            print("Sale_dates: ",Sale_dates)
            print("Sale_price: ",Sale_price)
            print("Land_Values: ",Land_Values)
            print("Market_Values: ",Market_Values)
            print()
            #print(pin,owner_name,Site_address,address,city,state,zip,Land_Use_Code,Built_Year,Living_area,Bedrooms,Full_Bath,Half_Bath,Sale_dates,Sale_price,Land_Values,Market_Values)
            

            with open('test.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([pin,owner_name,Site_address,address,city,state,zip,Land_Use_Code,Built_Year,Living_area,Bedrooms,Full_Bath,Half_Bath,Sale_dates,Sale_price,Land_Values,Market_Values])
                count = count + 1
                print("Data Saved in CSV:",count)
        except:
            print("Search results is empty")