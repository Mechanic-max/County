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
# with open('test.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(["Source_Parcel","Source_Name","Source_LegalDescription","Source_CurrentTax","Source_CurrentPenalty","Source_PastYearTax","Source_PastYearPenalty","Source_OlderYearsTax","Source_OlderYearsPenalty","Source_TotalDelCharges","Source_TotalPenalty","Source_TotalTax","Source_TaxSale","Source_vcAddress1","Source_vcAddress2","Source_bBankruptcy","Source_vcCity","Source_vcState","Source_vcZip","parcel_id","owner_name","site_address","site_city","owner_address","owner_city","owner_state","owner_zip","property_class","Atucal_year_built","text_year","living_area","sale_date","sale_price","land_value","Bedrooms","Full_Baths","Half_Baths","total_market_value"])

ul = "https://beacon.schneidercorp.com/Application.aspx?AppID=200&LayerID=2653&PageTypeID=2&PageID=1504"
def scrap():
    html = driver.page_source
    resp = Selector(text=html)
    
    parcel_id = resp.xpath("//th[contains(text(),'Parcel Number')]/following-sibling::td/text()").extract_first()
    site_address = resp.xpath("//span[@id='ctlBodyPane_ctl00_ctl01_detSummary_lblPropAddr1']/text()").extract_first()
    site_city = resp.xpath("ctlBodyPane_ctl00_ctl01_detSummary_lblPropCity").extract_first()
    owner_name = resp.xpath("//a[@id='ctlBodyPane_ctl01_ctl01_frmOwner_lblName1']/text()").extract_first()
    owner_address = resp.xpath("//a[@id='ctlBodyPane_ctl01_ctl01_frmOwner_lblAddr1']/text()").extract_first()
    owner_city = resp.xpath("//a[@id='ctlBodyPane_ctl01_ctl01_frmOwner_lblCity']/text()").extract_first()
    owner_state = resp.xpath("//a[@id='ctlBodyPane_ctl01_ctl01_frmOwner_lblState']/text()").extract_first()
    owner_zip = resp.xpath("//a[@id='ctlBodyPane_ctl01_ctl01_frmOwner_lblZip']/text()").extract_first()
    text_year = resp.xpath("//table[@id='ctlBodyPane_ctl10_ctl01_gvwData']/tbody/tr[1]/th/text()").extract_first()
    total_market_value = resp.xpath("//table[@id='ctlBodyPane_ctl10_ctl01_gvwData']/tbody/tr[1]/td[last()]/text()").extract_first()
    land_value = resp.xpath("//table[@id='ctlBodyPane_ctl10_ctl01_gvwData']/tbody/tr[1]/td[last()-2]/text()").extract_first()
    Bedrooms = resp.xpath("//span[@id='ctlBodyPane_ctl06_ctl01_lstResDetail_ctl00_BedroomsLabel']/text()").extract_first()
    Full_Baths = resp.xpath("//span[@id='ctlBodyPane_ctl06_ctl01_lstResDetail_ctl00_FullBathsLabel']/text()").extract_first()
    Half_Baths = resp.xpath("//span[@id='ctlBodyPane_ctl06_ctl01_lstResDetail_ctl00_HalfBathsLabel']/text()").extract_first()
    property_class = resp.xpath("//span[@id='ctlBodyPane_ctl07_ctl01_gvwImprovements_ctl02_lblBldgs']/text()").extract_first()
    Atucal_year_built = resp.xpath("//span[@id='ctlBodyPane_ctl07_ctl01_gvwImprovements_ctl02_lblYrConst']/text()[1]").extract_first()
    living_area = resp.xpath("//span[@id='ctlBodyPane_ctl07_ctl01_gvwImprovements_ctl02_lblSize']/text()[1]").extract_first()
    sale_date = resp.xpath("//table[@id='ctlBodyPane_ctl09_ctl01_gvwSales']/tbody/tr[1]/th[1]/text()").extract_first()
    sale_price = resp.xpath("//table[@id='ctlBodyPane_ctl09_ctl01_gvwSales']/tbody/tr[1]/td[1]/text()").extract_first()
    
    with open('test.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16],i[17],i[18],parcel_id,owner_name,site_address,site_city,owner_address,owner_city,owner_state,owner_zip,property_class,Atucal_year_built,text_year,living_area,sale_date,sale_price,land_value,Bedrooms,Full_Baths,Half_Baths,total_market_value])
        print(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16],i[17],i[18],parcel_id,owner_name,site_address,site_city,owner_address,owner_city,owner_state,owner_zip,property_class,Atucal_year_built,text_year,living_area,sale_date,sale_price,land_value,Bedrooms,Full_Baths,Half_Baths,total_market_value)
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
time.sleep(2)
try:
    driver.find_element_by_xpath("//a[contains(text(),'Agree')]").click()
    time.sleep(2)
except:
    print("Button not Found")

with open("./Montgomery County IN Delinquent Taxpayers 6-16-2021.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
        company = i[1]
        search = driver.find_element_by_xpath("//input[@id='ctlBodyPane_ctl00_ctl01_txtName']")
        search.clear()
        time.sleep(2)
        search.send_keys(company)
        time.sleep(3)
        search.send_keys(Keys.ENTER)
        time.sleep(5)
        count = count + 1
        print("Data Saved In CSV",count)
        try:
            btns = driver.find_elements_by_xpath("//a[@class='normal-font-label']")
            if btns == []:
                scrap()
            else:
                for j in range(0,len(btns)):
                    btn = driver.find_elements_by_xpath("//a[@class='normal-font-label']")[j].click()
                    time.sleep(10)
                    scrap()
                    driver.back()
                    time.sleep(10)
        except:
            print("Search result is empty")

        driver.get(ul)
        time.sleep(30)