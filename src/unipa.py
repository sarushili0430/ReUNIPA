from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_tools import check_exists_by_xpath
from dotenv import load_dotenv

from datetime import datetime
import time
import os

load_dotenv()

#chromedriverのパスを下で指定してください
#ex) "/Users/xxx/xxxx/chromedriver.exe"
CHROMEDRIVER = "chromedriver.exe"
SIGNINURL = os.environ["UNIPA_URL"]
USERID = os.environ["UNIPA_ID"]
USERPWD = os.environ["UNIPA_PWD"]
EMPTY = "EMPTY"

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
options.add_argument("--headless")



class UNIPA_Login():

    def __init__(self,ID,PWD):
        self.id = ID
        self.pwd = PWD
        self.assignment_list = []
        #Opening the Chrome browser
        self.driver = webdriver.Chrome(service=chrome_service,options=options)
        self.wait = WebDriverWait(self.driver,timeout=30)
        self.driver.get(SIGNINURL)
        self.login()

    def __enter__(self):
        return self
    
    def __exit__(self,exception_type, exception_value, traceback):
        self.driver.close()

    def login(self):
        #Login to account
        self.wait.until(EC.presence_of_all_elements_located)
        username_input = self.driver.find_element(By.ID,"loginForm:userId")
        pwd_input = self.driver.find_element(By.ID,"loginForm:password")
        login_btn = self.driver.find_element(By.ID,"loginForm:loginButton")
        username_input.send_keys(self.id)
        pwd_input.send_keys(self.pwd)
        login_btn.click()

    def get_assignment(self):
        """
            Args:
                assignment_list: List of the assignment names and deadlines
        """
        #Getting the assignment information
        self.wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[4]/div[5]/div[2]/form/div[2]/div[1]/div[1]/ul/li[2]")))
        juyo_button = self.driver.find_element(By.XPATH,"/html/body/div[4]/div[5]/div[2]/form/div[2]/div[1]/div[1]/ul/li[2]")
        juyo_button.click()

        #If「もっと表示」button, click
        self.wait.until(EC.presence_of_all_elements_located)
        motto_button = check_exists_by_xpath(driver=self.driver,xpath="/html/body/div[4]/div[5]/div[2]/form/div[2]/div[1]/div[1]/div/div[2]/div/div[2]/a")
        if motto_button:
            motto_button.click()
        
        #Taking out the time.sleep() in the future
        self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"ui-datalist-item")))
        time.sleep(3)

        if self.driver.find_elements(By.CLASS_NAME,"ui-datalist-empty-message"):
            return EMPTY
        
        notify = self.driver.find_element(By.ID,"funcForm:j_idt162:j_idt211_list").find_elements(By.CLASS_NAME,"ui-datalist-item")
        cnt = 0
        for _ in notify:
            try:
                assignment_id = "funcForm:j_idt162:j_idt211:"+str(cnt)+":j_idt232"
                assignment_name = _.find_element(By.ID,"funcForm:j_idt162:j_idt211:"+str(cnt)+":j_idt232").get_attribute("textContent")
                assignment_deadline = _.find_elements(By.CSS_SELECTOR,"span.textDate")[1].get_attribute("textContent")
                self.assignment_list.append([assignment_id,assignment_name,assignment_deadline])
            except:
                pass
            cnt += 1
        
        for _ in range(len(self.assignment_list)):
            content = self.get_assignment_detail(self.assignment_list[_][0])
            print(_)
            print(content)
            self.assignment_list[_].append(content)
            
        return self.assignment_list
    
    def get_assignment_detail(self,id):
        #Clicking the assignment, atriving content
        try:
            self.wait.until(EC.presence_of_element_located((By.ID,id)))
            assignment_btn = self.driver.find_element(By.ID,id)
            assignment_btn.click()
            self.wait.until(EC.presence_of_all_elements_located)
            content = self.driver.find_element(By.CSS_SELECTOR,"div.fr-box.fr-view").get_attribute("textContent")
            self.wait.until(EC.presence_of_element_located((By.ID,"headerForm:j_idt54")))
            home_btn = self.driver.find_element(By.ID,"headerForm:j_idt54")
            home_btn.click()

            #Getting the assignment information
            self.wait.until(EC.presence_of_all_elements_located)
            juyo_button = self.driver.find_element(By.XPATH,"/html/body/div[4]/div[5]/div[2]/form/div[2]/div[1]/div[1]/ul/li[2]")
            juyo_button.click()

            #If「もっと表示」button, click
            self.wait.until(EC.presence_of_all_elements_located)
            motto_button = check_exists_by_xpath(driver=self.driver,xpath="/html/body/div[4]/div[5]/div[2]/form/div[2]/div[1]/div[1]/div/div[2]/div/div[2]/a")
            if motto_button:
                motto_button.click()
        except Exception as e:
            raise e
    
        return content
        

class UNIPA_Submit(UNIPA_Login):

    def __init__(self, ID, PWD):
        super().__init__(ID, PWD)
        #Opening the Chrome browser
        #self.driver = webdriver.Chrome(service=chrome_service,options=options)
        #self.wait = WebDriverWait(self.driver,timeout=30)

    def __enter__(self):
        return self.driver
    
    def __exit__(self):
        self.driver.close()
    
    def submit_assignment(self,id,file_path):
        #Getting the assignment information
        self.wait.until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/div[4]/div[5]/div[2]/form/div[2]/div[1]/div[1]/ul/li[2]")))
        juyo_button = self.driver.find_element(By.XPATH,"/html/body/div[4]/div[5]/div[2]/form/div[2]/div[1]/div[1]/ul/li[2]")
        juyo_button.click()

        #If「もっと表示」button, click
        self.wait.until(EC.presence_of_all_elements_located)
        motto_button = check_exists_by_xpath(driver=self.driver,xpath="/html/body/div[4]/div[5]/div[2]/form/div[2]/div[1]/div[1]/div/div[2]/div/div[2]/a")
        if motto_button:
            motto_button.click()
        
        #Click the assignment to submit        
        #Taking out the time.sleep() in the future
        self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"ui-datalist-item")))
        time.sleep(3)
        assignment_btn = self.driver.find_element(By.ID,id)
        assignment_btn.click()
        #time.sleep(100)

        #Submitting the assignment
        submission_box = self.driver.find_element(By.ID,"funcForm:kdiTstAccordion:j_idt430:fileUpload1_input")
        submit_btn = self.driver.find_element(By.ID,"funcForm:j_idt500")
        confirm_yes_btn = self.driver.find_element(By.ID,"yes")

        submission_box.send_keys(file_path)
        time.sleep(3)
        submit_btn.click()
        time.sleep(1)
        confirm_yes_btn.click()
        time.sleep(1)
        
        #Check whether the assignment is submitted or not
        if self.driver.find_elements(By.CSS_SELECTOR,"div.ui-growl-item-container.ui-state-highlight.ui-corner-all.ui-helper-hidden.ui-shadow"):
            return True
        else:
            return False
        
def check_id(id,pwd,url):
        #Login to account
        driver = webdriver.Chrome(service=chrome_service,options=options)
        driver.get(url=url)
        username_input = driver.find_element(By.ID,"loginForm:userId")
        pwd_input = driver.find_element(By.ID,"loginForm:password")
        login_btn = driver.find_element(By.ID,"loginForm:loginButton")
        username_input.send_keys(id)
        pwd_input.send_keys(pwd)
        login_btn.click()
        if driver.find_elements(By.CLASS_NAME,"ui-messages-error"):
            driver.close()
            return "ERROR"
        else:
            driver.close()
            return "SUCCESS"


#Test
if __name__ == "__main__":
    with UNIPA_Login(USERID,USERPWD) as client:
        print(client.get_assignment())
    








