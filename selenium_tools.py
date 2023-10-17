from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def check_exists_by_xpath(driver,xpath):
    try:
        element = driver.find_element(By.XPATH,xpath)
    except NoSuchElementException:
        return False
    return element
    