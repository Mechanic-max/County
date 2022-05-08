from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from shutil import which
import time
from scrapy.selector import Selector
from selenium.webdriver.common.action_chains import ActionChains
import csv
import pandas as pd
import re
import undetected_chromedriver as uc

count = 0

ul = "https://arcgisserver.lincolncounty.org/taxparcelviewer/assets/Lincoln/PropertyReport.htm?59619"
path = which("chromedriver")
options = Options()
options.add_experimental_option("detach", True)
#options.add_argument("--headless")
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
driver = uc.Chrome(executable_path=path,options=options)
driver.get(ul)
time.sleep(8)