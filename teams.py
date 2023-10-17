from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

from datetime import datetime
import time
import os

load_dotenv()

#chromedriverのパスを下で指定してください
#ex) "/Users/xxx/xxxx/chromedriver.exe"
CHROMEDRIVER = "chromedriver.exe"
SIGNINURL = os.environ["UNIPA_URL"]

#Setting up the selenium browser
chrome_service = service.Service(executable_path=CHROMEDRIVER)

#Options for the Chrome Browser
options = Options()
options.add_argument(f'service={chrome_service}')
options.page_load_strategy = 'eager'                     
options.add_argument('--disable-gpu')                      
options.add_argument('--disable-extensions')               
options.add_argument('--proxy-server="direct://"')         
options.add_argument('--proxy-bypass-list=*')              
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument('--lang=ja')                          
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--log-level=3")
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.page_load_strategy = 'eager'
options.add_argument('--disable-extensions')
options.add_argument("--start-maximized")
#options.add_argument("--headless")


class Teams_Login():

    def __init__(self,ID,PWD):
        self.id = ID
        self.pwd = PWD
        #Opening the Chrome browser
        self.driver = webdriver.Chrome(service=chrome_service)
        self.wait = WebDriverWait(self.driver,timeout=30)
        self.driver.get(url="https://teams.microsoft.com/")

    def login(self):
        #Login to account
        self.wait.until(EC.presence_of_element_located((By.ID,"i0116")))
        #time.sleep(10)
        username_input = self.driver.find_element(By.ID,"i0116")
        username_input.send_keys(self.id)
        next_btn = self.driver.find_element(By.ID,"idSIButton9")
        next_btn.click()     
        self.wait.until(EC.presence_of_element_located((By.ID,"i0118")))
        pwd_input = self.driver.find_element(By.ID,"i0118")
        pwd_input.send_keys(self.pwd)
        time.sleep(5)
        pwd_input.send_keys(Keys.ENTER)
        #login_btn = self.driver.find_element(By.ID,"idSIButton9")
        #login_btn.click()
        #self.wait.until(EC.element_to_be_clickable((By.ID,"idSIButton9")))
        time.sleep(100)
        #login_btn = self.driver.find_element(By.ID,"idSIButton9")
        #self.wait.until(EC.staleness_of(login_btn))
