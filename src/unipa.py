from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tools import check_exists_by_xpath
from tools import format_datetime
from dotenv import load_dotenv

from datetime import datetime
import time
import os
import dotenv

load_dotenv()

# chromedriverのパスを下で指定してください
# ex) "/Users/xxx/xxxx/chromedriver.exe"
CHROMEDRIVER = "chromedriver.exe"
SIGNINURL = os.environ["UNIPA_URL"]
USERID = os.environ["UNIPA_ID"]
USERPWD = os.environ["UNIPA_PWD"]
EMPTY = "EMPTY"

# Setting up the selenium browser
chrome_service = service.Service(executable_path=CHROMEDRIVER)

# Options for the Chrome Browser
options = Options()
options.add_argument(f"service={chrome_service}")
options.page_load_strategy = "eager"
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument('--proxy-server="direct://"')
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--lang=ja")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--log-level=3")
options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
options.add_argument("--headless=new")


class UNIPA_Login:
    """Login and gets data from UNIPA

    Attributes:
      id (str):
      PWD (str):
    """

    def __init__(self, ID, PWD):
        self.id = ID
        self.pwd = PWD
        self.assignment_list = []
        # Opening the Chrome browser
        self.driver = webdriver.Chrome(service=chrome_service, options=options)
        self.wait = WebDriverWait(self.driver, timeout=30)
        login(self.driver, id=ID, pwd=PWD, url=SIGNINURL, wait=self.wait)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.driver.close()

    def get_assignment(self):
        """Gets the assignment information from UNIPA

        Return:
            list: List of the assignment names and deadlines
        """
        try:
            # Clicks the 「期限あり」button
            kigenari_button_click(driver=self.driver, wait=self.wait)

            # If「もっと表示」button, click
            motto_button_click(driver=self.driver, wait=self.wait)

            # Taking out the time.sleep() in the future
            self.wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "ui-datalist-item"))
            )
            time.sleep(3)

            notify = self.driver.find_element(
                By.ID, "funcForm:j_idt162:j_idt211_list"
            ).find_elements(By.CLASS_NAME, "ui-datalist-item")
            cnt = 0
            for _ in notify:
                try:
                    assignment_id = (
                        "funcForm:j_idt162:j_idt211:" + str(cnt) + ":j_idt232"
                    )
                    assignment_name = _.find_element(
                        By.ID, "funcForm:j_idt162:j_idt211:" + str(cnt) + ":j_idt232"
                    ).get_attribute("textContent")
                    self.assignment_list.append([assignment_id, assignment_name])
                except:
                    pass
                cnt += 1
            print(self.assignment_list)

            for _ in range(len(self.assignment_list)):
                print(self.assignment_list[_][0])
                content = self.get_assignment_detail(self.assignment_list[_][0])
                print(_)
                print(content)
                self.assignment_list[_].extend(content)
                # Too much http requests at a time => Implicit wait (Time lag occured by browser rendering)
                time.sleep(1)

        except Exception as e:
            print(e)
            self.assignment_list = None

        return self.assignment_list

    def get_assignment_detail(self, id: str):
        """Gets the assignment detail under id

        Args:
          id (str): id-tag of the assignment

        Return:
          list: Detail and deadline of the assignment [Datetime,Detail]

        """
        try:
            # Clicks the assignment, and moves to the assignment detail page
            assignment_btn = self.driver.find_element(By.ID, id)
            assignment_btn.click()
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.fr-box.fr-view"))
            )
            content = self.driver.find_element(
                By.CSS_SELECTOR, "div.fr-box.fr-view"
            ).get_attribute("textContent")
            deadline = self.driver.find_element(
                By.XPATH,
                "/html/body/div[4]/div[5]/div[2]/form/div[2]/div[2]/div[1]/table/tbody/tr[4]/td[2]/div/span[3]",
            ).get_attribute("textContent")
            # Formatting deadline to datetime understandable string
            deadline = format_datetime(deadline)
            submit_method = True

            # Returns to initial screen
            home_button_click(driver=self.driver, wait=self.wait)

            # Clicks the 「期限あり」button
            kigenari_button_click(driver=self.driver, wait=self.wait)

            # If「もっと表示」button, click
            motto_button_click(driver=self.driver, wait=self.wait)

        except Exception as e:
            raise e

        return [content, deadline]

    def get_attached_file(self):
        """Gets the attached file when available

        Return:
          str: "NO_FILE" when attached file doesn't exist.
               ""
        """
        try:
            self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[4]/div[5]/div[2]/form/div[2]/div[2]/div[1]/table/tbody/tr[2]/td[2]",
                    )
                )
            )
            look_file_btn = self.driver.find_element(
                By.ID, "funcForm:kdiTstAccordion:j_idt382"
            )
            look_file_btn.click()
        except:
            return "NO_FILE"

        try:
            cnt = 0
            assignment_file_name = []
            self.wait.until(
                EC.presence_of_element_located(
                    (By.ID, "pkx02201:ch:appendList:0:j_idt588")
                )
            )

            # Check all file names
            for _ in self.driver.find_elements(
                By.CSS_SELECTOR, "div.fileListCell.downLoadCellFilNm"
            ):
                assignment_file_name.append(_.get_attribute("textContent"))

            # Download all files available
            while True:
                download_btn = self.driver.find_element(
                    By.ID, "pkx02201:ch:appendList:" + str(cnt) + ":j_idt588"
                )
                download_btn.click()
                cnt += 1
        except:
            pass


class UNIPA_Submit(UNIPA_Login):
    """Submits file to UNIPA

    Attributes:
      ID (str): ID to login to UNIPA
      PWD (str): PWD to login to UNIPA

    """

    def __init__(self, ID, PWD):
        super().__init__(ID, PWD)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.driver.close()

    def submit_assignment(self, id: str, file_path: str):
        """Submitting the Assignment

        Args:
          id (str): ID for signing in UNIPA
          file_path (str): File path of the chosen file

        Return:
          bool: True when succeeded submission
        """
        try:
            # Getting the assignment information
            kigenari_button_click(driver=self.driver, wait=self.wait)

            # If「もっと表示」button, click
            motto_button_click(driver=self.driver, wait=self.wait)

            # Click the assignment to submit
            # Taking out the time.sleep() in the future
            self.wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "ui-datalist-item"))
            )
            time.sleep(3)
            assignment_btn = self.driver.find_element(By.ID, id)
            assignment_btn.click()

            # Submitting the assignment
            submission_box = self.driver.find_element(
                By.ID, "funcForm:kdiTstAccordion:j_idt430:fileUpload1_input"
            )
            submit_btn = self.driver.find_element(By.ID, "funcForm:j_idt500")
            confirm_yes_btn = self.driver.find_element(By.ID, "yes")
            time.sleep(5)
            submission_box.send_keys(file_path)
            self.wait.until(
                EC.presence_of_element_located(
                    (By.ID, "funcForm:kdiTstAccordion:j_idt433:j_idt434:0:j_idt437")
                )
            )
            submit_btn.click()
            time.sleep(3)
            confirm_yes_btn.click()
            # Error occurs, so wait implicitly
            self.wait.until(
                EC.presence_of_element_located((By.ID, "funcForm:j_idt496"))
            )
            print("completed")

            return True
        except Exception as e:
            print(e)
            return False


def check_id(id: str, pwd: str, url: str):
    """Checks the validility of the ID

    Args:
        id (str): ID for signing to UNIPA
        pwd (str): PWD for signing to UNIPA
        url (str): URL to specify the UNIPA website to login

    Return:
        bool: True when succeeds login
    """
    try:
        # Login to account
        driver = webdriver.Chrome(service=chrome_service, options=options)
        driver.get(url=url)
        if driver.find_elements(By.CLASS_NAME, "ui-messages-error"):
            driver.close()
            return False
        else:
            driver.close()
            dotenv_file = dotenv.find_dotenv()
            dotenv.set_key(
                dotenv_path=dotenv_file, key_to_set="UNIPA_URL", value_to_set=url
            )
            dotenv.set_key(
                dotenv_path=dotenv_file, key_to_set="UNIPA_ID", value_to_set=id
            )
            dotenv.set_key(
                dotenv_path=dotenv_file, key_to_set="UNIPA_PWD", value_to_set=pwd
            )
            os.environ["UNIPA_URL"] = url
            os.environ["UNIPA_ID"] = id
            os.environ["UNIPA_PWD"] = pwd
            return True
    except Exception as e:
        print(e)
        return False


def home_button_click(driver: webdriver.Chrome, wait: WebDriverWait):
    """Clicks UNIPAロゴ and goes to home

    Args:
      driver (webdriver.Chrome): The target webdriver
      wait (webDriverWair): The target webdriver's wait instance

    Return:
      bool: True when succeed clicking button
    """
    try:
        wait.until(EC.presence_of_element_located((By.ID, "headerForm:j_idt54")))
        home_btn = driver.find_element(By.ID, "headerForm:j_idt54")
        home_btn.click()
    except Exception as e:
        print(e)


def kigenari_button_click(driver: webdriver.Chrome, wait: WebDriverWait):
    """Clicks 「期限あり」button

    Args:
      driver (webdriver.Chrome): The target webdriver
      wait (WebDriverWait): The target webdriver's wait instance

    Return:
      bool: True when succeed clicking button
    """
    try:
        wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[4]/div[5]/div[2]/form/div[2]/div[1]/div[1]/ul/li[2]",
                )
            )
        )
        kigenari_button = driver.find_element(
            By.XPATH,
            "/html/body/div[4]/div[5]/div[2]/form/div[2]/div[1]/div[1]/ul/li[2]",
        )
        kigenari_button.click()
        return True
    except Exception as e:
        print(e)


def motto_button_click(driver: webdriver.Chrome, wait: WebDriverWait):
    """Clicks 「もっと表示」button if available

    Args:
      driver (webdriver.Chrome): The target webdriver
      wait (WebDriverWait): The target webdriver's Wait object

    Return:
      bool: True when succeed clicking button
    """
    try:
        wait.until(EC.presence_of_all_elements_located)
        motto_button = check_exists_by_xpath(
            driver=driver,
            xpath="/html/body/div[4]/div[5]/div[2]/form/div[2]/div[1]/div[1]/div/div[2]/div/div[2]/a",
        )
        if motto_button:
            motto_button.click()
        return True
    except Exception as e:
        print(e)


def login(driver: webdriver.Chrome, wait: WebDriverWait, id: str, pwd: str, url: str):
    """Logins to UNIPA

    Args:
      driver (webdriver.Chrome): The target webdriver
      wait (WebDriverWait): The target webdriver's Wait object

    Return:
      bool: True when succeeded UNIPA login
    """
    try:
        driver.get(url=url)
        wait.until(EC.presence_of_all_elements_located)
        username_input = driver.find_element(By.ID, "loginForm:userId")
        pwd_input = driver.find_element(By.ID, "loginForm:password")
        login_btn = driver.find_element(By.ID, "loginForm:loginButton")
        username_input.send_keys(id)
        pwd_input.send_keys(pwd)
        login_btn.click()
        return True
    except Exception as e:
        print(e)
        return False


# Test
if __name__ == "__main__":
    with UNIPA_Login(USERID, USERPWD) as client:
        print(client.get_assignment())
