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
import requests
count = 0



path = which("chromedriver")
options = Options()
options.add_experimental_option("detach", True)
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


with open("input.csv","r") as f:
    data = csv.reader(f)
    for row in data:
        company = row[0]
        ul = f"https://www.bttaxpayerportal.com/itspublical//AppraisalCard.aspx?id={company}"
        driver.get(ul)
        time.sleep(3)
        response = requests.get(ul)
        name = f"{company}.pdf"
        with open(name, 'wb') as f:
            f.write(response.content)
            count = count + 1
            print("Data Saved in pdf: ",count)

    
