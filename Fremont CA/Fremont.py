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
# with open('Sharp.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(["Parcel ID","owner_name","site_address","city","state","zip","mail_address","m_city","m_state","m_zip","sale_date","sale_price","land_value","bldg_value","total_accessed_value","living_area","property_type","built_year","baths"])

ul = "https://www.acassessor.org/homeowners/assessment-resources/parcel-viewer/"




def scrap(count,a0,a1,a2,a3,a4):
    html = driver.page_source
    resp = Selector(text=html)
    
    parcel_id = resp.xpath("normalize-space(//div[@class='attribute-details']/span[contains(text(),'-')]/text())").extract_first()

    site_address = resp.xpath("normalize-space(//span[contains(text(),'Situs Address')]//following-sibling::div/span[1]/text())").extract_first()
    site_address = str(site_address)
    se = ''
    site_zip = re.findall(r"\b(\w+)$",site_address)
    for se in site_zip:
        se = str(se)
        site_address = site_address.replace(se,'')
        site_address = site_address.strip()
    
    sc = ''
    site_city = re.findall(r"\b(\w+)$",site_address)
    for sc in site_city:
        sc = str(sc)
        site_address = site_address.replace(sc,'')
        site_address = site_address.strip()



    mail_address = resp.xpath("//span[contains(text(),'Mailing Address')]//following-sibling::div/span[1]/text()").extract_first()
    mail_address = str(mail_address)
    mail_address.strip()
    mail_city = ''
    mail_state = ''
    mail_zip = ''
    mz = re.findall(r"\b(\w+)$",mail_address)
    for mail_zip in mz:
        mail_zip = str(mail_zip)
        mail_address = mail_address.replace(mail_zip,'')
        mail_address = mail_address.strip()
    ms = re.findall(r"\b(\w+)$",mail_address)
    for mail_state in ms:
        mail_state = str(mail_state)
        mail_address =mail_address.replace(mail_state,'')
        mail_address = mail_address.strip()
    mc = re.findall(r"\b(\w+)$",mail_address)
    for mail_city in mc:
        mail_city = str(mail_city)
        mail_address = mail_address.replace(mail_city,'')
        mail_address = mail_address.strip()


    land_value = resp.xpath("//span[contains(text(),'Land Value')][1]//following-sibling::div/span[1]/text()").extract_first()
    bldg_value = resp.xpath("//span[contains(text(),'Improvement Value')][1]//following-sibling::div/span[1]/text()").extract_first()
    total_market_value = resp.xpath("//span[contains(text(),'Total Net Value')][1]//following-sibling::div/span[1]/text()").extract_first()


    print()
    print(f"Scraping ====>{a4}")
    print("parcel_id:",parcel_id)
    print("site_address:",site_address)
    print("site_city:",sc)
    print("mail_zip:",se)
    print("mail_address:",mail_address)
    print("mail_city:",mail_city)
    print("mail_state:",mail_state)
    print("mail_zip:",mail_zip)
    print("land_value:",land_value)
    print("bldg_value:",bldg_value)
    print("total_market_value:",total_market_value)
    print()
    
    with open('dataset_for_fort_worth.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,parcel_id,site_address,sc,se,mail_address,mail_city,mail_state,mail_zip,land_value,bldg_value,total_market_value])
        count = count + 1
        print("Data saved in CSV: ",count)

    return count


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
time.sleep(10)


with open("./input.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company1 = str(i[4])
        ele = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='et_pb_button et_pb_button_0 et_pb_bg_layout_light']")))
        ele.click()
        elo = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(),'Situs Address')]/parent::td/following-sibling::td/input")))
        elo.click()
        time.sleep(3)
        company1 = company1.strip()
        search = driver.find_element_by_xpath("//input[contains(@title,'Search')]")
        search.send_keys(Keys.CONTROL + "a")
        search.send_keys(Keys.DELETE)
        time.sleep(1)
        search.send_keys(company1)
        time.sleep(1)
        search.send_keys(Keys.ENTER)
        time.sleep(3)
        try:
            ely = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='results-list']/div[@class='list-menu active has-icon bound-visible']")))
            ely.click()
            time.sleep(5)
            count = scrap(count,i[0],i[1],i[2],i[3],i[4])
        except:
            count = scrap(count,i[0],i[1],i[2],i[3],i[4])
        driver.get(ul)
        time.sleep(5)

driver.close()


