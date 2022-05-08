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
#     writer.writerow(["Source Owner Name","Source Owner Name 2","Source Price","parcel_id","property_address","Acc_no","owner_name","Mailing_address","mail_city","mail_state","mail_zip","SaleDate","SalePrice","land_value","bldg_value","total_market_value"])

ul = "https://gis.jacksonnc.org/rpv/"


def scrap(count,a,a1,a2):
    html = driver.page_source
    resp = Selector(text=html)
    
    parcel_id = resp.xpath("normalize-space(//i[contains(text(),'PIN')]/parent::font/parent::td/following-sibling::td/font/text()[1])").extract_first()
    property_address = resp.xpath("normalize-space(//i[contains(text(),'PIN')]/parent::font/parent::td/following-sibling::td/font/text()[2])").extract_first()
    Acc_no = resp.xpath("normalize-space(//i[contains(text(),'PIN')]/parent::font/parent::td/following-sibling::td/font/text()[3])").extract_first()
    owner_name = resp.xpath("normalize-space(//i[contains(text(),'CurrentOwner1:')]/parent::font/parent::td/following-sibling::td/font/text()[1])").extract_first()
    Mailing_address = resp.xpath("normalize-space(//i[contains(text(),'MailingAddress1:')]/parent::font/parent::td/following-sibling::td/font/text()[1])").extract_first()
    mail_city_state_zip = resp.xpath("normalize-space(//i[contains(text(),'MailingCityState:')]/parent::font/parent::td/following-sibling::td/font/text()[1])").extract_first()
    try:
        mail_city_state_zip = str(mail_city_state_zip)
        mail_city = re.findall(r"^[^,]+",mail_city_state_zip)
        mail_state = re.findall(r",\s\w\w",mail_city_state_zip)
    except:
        mail_city = None
        mail_state = None
    mail_zip = resp.xpath("normalize-space(//i[contains(text(),'MailingZip:')]/parent::font/parent::td/following-sibling::td/font/text()[1])").extract_first()
    SaleDate = resp.xpath("normalize-space(//i[contains(text(),'SaleDate:')]/parent::font/parent::td/following-sibling::td//span/text())").extract_first()
    SalePrice = resp.xpath("normalize-space(//i[contains(text(),'SalePrice:')]/parent::font/parent::td/following-sibling::td//span/text())").extract_first()
    land_value = resp.xpath("normalize-space(//i[contains(text(),'TotBldgValue:')]/parent::font/parent::td/following-sibling::td//span/text())").extract_first()
    bldg_value = resp.xpath("normalize-space(//i[contains(text(),'TotBldgValue:')]/parent::font/parent::td/following-sibling::td//span/text())").extract_first()
    total_market_value = resp.xpath("normalize-space(//i[contains(text(),'TotBldgValue:')]/parent::font/parent::td/following-sibling::td//span/text())").extract_first()


    print()
    print("Scraping=======>",a)
    print("Source Onwer Name 2:",a1)
    print("Source price:",a2)
    print("parcel_id", parcel_id)
    print("property_address", property_address)
    print("Acc_no", Acc_no)
    print("Owner_Name", owner_name)
    print("Mailing_address", Mailing_address)
    print("mail_city", mail_city)
    print("mail_state", mail_state)
    print("mail_zip", mail_zip)
    print("SaleDate", SaleDate)
    print("SalePrice", SalePrice)
    print("land_value", land_value)
    print("bldg_value", bldg_value)
    print("total_market_value", total_market_value)
    print()
    with open('test.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a,a1,a2,parcel_id,property_address,Acc_no,owner_name,Mailing_address,mail_city,mail_state,mail_zip,SaleDate,SalePrice,land_value,bldg_value,total_market_value])
        count = count + 1
        print("Data Saved in CSV:",count)

    return count



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
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(executable_path=path,options=options)
driver.get(ul)
time.sleep(70)

try:
    aloo = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='checkbox jimu-float-leading jimu-icon jimu-icon-checkbox']"))
    )
    aloo.click()
    moli = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//button[@class='jimu-btn jimu-float-trailing lastFocusNode enable-btn']"))
    )
    moli.click()
except:
    print("Pop up didn't appear")
with open("input.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:

        # search = WebDriverWait(driver, 30).until(
        #     EC.presence_of_element_located((By.ID, "esri_dijit_Search_0_input"))
        # )
        time.sleep(4)
        search = driver.find_element_by_xpath("//input[@id='esri_dijit_Search_0_input']")
        time.sleep(2)
        search.clear()
        time.sleep(1)
        search.send_keys(i[0])
        search.send_keys(Keys.ENTER)
        time.sleep(20)
        html = driver.page_source
        resp = Selector(text=html)
        parcel_id = resp.xpath("normalize-space(//i[contains(text(),'PIN')]/parent::font/parent::td/following-sibling::td/font/text())").extract_first()
        if parcel_id:
            count = scrap(count,i[0],i[1],i[2])

        else:
            try:
                search = driver.find_element_by_xpath("//input[@id='esri_dijit_Search_0_input']")
                time.sleep(2)
                search.clear()
                time.sleep(1)
                search.send_keys(i[1])
                search.send_keys(Keys.ENTER)
                time.sleep(6)
                count = scrap(count,i[0],i[1],i[2])
            except:
                print("Search Result is empty")




            
            


        # driver.get(ul)
        # time.sleep(10)
            
    
driver.close()
