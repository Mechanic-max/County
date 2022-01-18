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

ul = "https://revenue.stlouisco.com/IAS/"




def scrap(count,a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,a20,a21,a22,a23,a24,a25,a26,a27,a28,a29,a30,a31,a32,a33,a34,a35,a36,a37,a38,a39,a40,a41,a42,a43,a44,a45,a46,a47,a48,a49,a50,a51,a52,a53,a54,a55,a56,a57,a58,a59,a60,a61,a62,a63,a64,a65,a66,a67,a68):
    html = driver.page_source
    resp = Selector(text=html)


    parcel_id = resp.xpath("//span[@id='ctl00_MainContent_OwnLeg_labLocatorNum']/text()").extract_first()
    jv = resp.xpath("//th[contains(text(),'Appraised Values')]/parent::tr/following-sibling::tr[2]/td[last()-4]/text()").extract_first()
    try:
        driver.find_element_by_xpath("//a[contains(text(),'Property Information')]").click()
        time.sleep(3)
        html = driver.page_source
        resp = Selector(text=html)
        
        sale_date = resp.xpath("//td[contains(text(),'Sale Price')]/parent::tr/following-sibling::tr[1]/td[1]/text()").extract_first()
        sale_price = resp.xpath("//td[contains(text(),'Sale Price')]/parent::tr/following-sibling::tr[1]/td[2]/text()").extract_first()
    except:
        sale_date = None
        sale_price = None
    print()
    print(f"Scraping ====>{a3}{a4}")
    print("parcel_id:",parcel_id)
    print("jv:",jv)
    print("sale_date:",sale_date)
    print("sale_price:",sale_price)
    print()
    
    with open('dataset_for_Bryan to Scrape StLouis and Milwaukee 08-12-2021 - Nabeel.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,a20,a21,a22,a23,a24,a25,a26,a27,a28,a29,a30,a31,a32,a33,a34,a35,a36,a37,a38,a39,a40,a41,a42,a43,a44,a45,a46,a47,a48,a49,a50,a51,a52,a53,a54,a55,a56,a57,a58,a59,a60,a61,a62,a63,a64,a65,a66,a67,a68,parcel_id,jv,sale_date,sale_price])
        count = count + 1
        print("Data saved in CSV: ",count)

    driver.switch_to.default_content()
    return count





# # try:

# # except:
# #     print("Pop up didn't appear")
with open("./Bryan to Scrape StLouis and Milwaukee 08-12-2021 - Nabeel.csv", 'r') as input_file:
    reader = csv.reader(input_file,delimiter=",")
    for i in reader:
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
        time.sleep(7)
        driver.switch_to.frame(1)
        try:
            driver.find_element_by_xpath("//label[contains(text(),'Property Address')]/preceding-sibling::input").click()
            time.sleep(3)
            company1 = str(i[2])
            company1 = company1.strip()
            search = driver.find_element_by_xpath("//input[@id='tboxAddrNum']")
            search.clear()
            search.send_keys(company1)
            time.sleep(1)
            
            company2 = str(i[3])
            company2 = company2.strip()
            search1 = driver.find_element_by_xpath("//input[@id='tboxStreet']")
            search1.clear()
            search1.send_keys(company2)
            time.sleep(1)
            search1.send_keys(Keys.ENTER)
            time.sleep(5)

            driver.switch_to.default_content()
            driver.switch_to.frame(2)
            try:

                driver.find_elements_by_xpath("//img[contains(@src,'../Images/spacer')]/parent::td")[0].click()
                time.sleep(3)
            except:
                None
            driver.switch_to.default_content()
            driver.switch_to.frame(0)
            count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16],i[17],i[18],i[19],i[20],i[21],i[22],i[23],i[24],i[25],i[26],i[27],i[28],i[29],i[30],i[31],i[32],i[33],i[34],i[35],i[36],i[37],i[38],i[39],i[40],i[41],i[42],i[43],i[44],i[45],i[46],i[47],i[48],i[49],i[50],i[51],i[52],i[53],i[54],i[55],i[56],i[57],i[58],i[59],i[60],i[61],i[62],i[63],i[64],i[65],i[66],i[67],i[68])

        except:
            driver.get(ul)
            time.sleep(7)
            driver.switch_to.frame(1)
            driver.find_element_by_xpath("//label[contains(text(),'Property Address')]/preceding-sibling::input").click()
            time.sleep(3)
            company1 = str(i[2])
            company1 = company1.strip()
            search = driver.find_element_by_xpath("//input[@id='tboxAddrNum']")
            search.clear()
            search.send_keys(company1)
            time.sleep(1)
            
            company2 = str(i[3])
            company2 = company2.strip()
            search1 = driver.find_element_by_xpath("//input[@id='tboxStreet']")
            search1.clear()
            search1.send_keys(company2)
            time.sleep(1)
            search1.send_keys(Keys.ENTER)
            time.sleep(5)

            driver.switch_to.default_content()
            driver.switch_to.frame(2)
            try:

                driver.find_elements_by_xpath("//img[contains(@src,'../Images/spacer')]/parent::td")[0].click()
                time.sleep(3)
            except:
                None
            driver.switch_to.default_content()
            driver.switch_to.frame(0)
            count = scrap(count,i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16],i[17],i[18],i[19],i[20],i[21],i[22],i[23],i[24],i[25],i[26],i[27],i[28],i[29],i[30],i[31],i[32],i[33],i[34],i[35],i[36],i[37],i[38],i[39],i[40],i[41],i[42],i[43],i[44],i[45],i[46],i[47],i[48],i[49],i[50],i[51],i[52],i[53],i[54],i[55],i[56],i[57],i[58],i[59],i[60],i[61],i[62],i[63],i[64],i[65],i[66],i[67],i[68])

            
        driver.close()
        
