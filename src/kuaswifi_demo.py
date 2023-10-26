from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from pywifi import const
import pywifi
import time
import os

load_dotenv()

#wifi settings
wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]
Name = iface.name()

#profie
profile = pywifi.Profile()
profile.ssid = "kuas-wifi"
profile.auth = const.AUTH_ALG_OPEN
profile.akm.append(const.AKM_TYPE_NONE)
profile.cipher = const.CIPHER_TYPE_NONE
profile.key = "Kyotosentan2019"

profile = iface.add_network_profile(profile)
iface.connect(profile)

#chromedriverのパスを下で指定してください
#ex) "/Users/xxx/xxxx/chromedriver.exe"
CHROMEDRIVER = "chromedriver.exe"
SIGNINURL = os.environ["WIFI_URL"]

#Setting up the selenium browser
chrome_service = service.Service(executable_path=CHROMEDRIVER)

#Options
options = Options()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-proxy-certificate-handler")
options.add_argument("--ignore-ssl-errors")
options.add_argument("--disable-content-security-policy")

driver = webdriver.Chrome(service=chrome_service,options=options)

print(os.environ["UNIPA_ID"])
print(os.environ["UNIPA_PWD"])



driver.get(os.environ["WIFI_URL"])
wait = WebDriverWait(driver=driver,timeout=30)
wait.until(EC.presence_of_element_located((By.NAME,"user")))
username = driver.find_element(By.NAME,"user")
pwd = driver.find_element(By.NAME,"password")
#wait.until(EC.presence_of_element_located((By.NAME,"submit")))
driver.implicitly_wait(6)
submit_btn = driver.find_elements(By.TAG_NAME,"input")[2]
username.send_keys(os.environ["UNIPA_ID"])
pwd.send_keys(os.environ["UNIPA_PWD"])
submit_btn.click()


