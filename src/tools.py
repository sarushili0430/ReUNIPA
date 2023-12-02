from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import os
import shutil

DOWNLOAD_DIR = "C:/Users/kouyu/Downloads"


def check_exists_by_xpath(driver, xpath):
    try:
        element = driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return element


def format_datetime(date):
    new_date = date[0:9]
    new_time = date[14:]
    return str(new_date + " " + new_time).replace("/", "-")


def list_to_dict(ls: list):
    assign_dict = {}
    for _ in ls:
        assign_dict[_[1]] = [_[0], _[4]]
    return assign_dict


class file_downloaded(object):
    def __init__(self, dirname):
        self.filename = dirname
        pass

    def __call__(self):
        return os.path.exists(DOWNLOAD_DIR + self.dirname)


def move_assignment_file(filename, dirname, parent_path):
    old_path = DOWNLOAD_DIR + "/" + filename
    new_path = parent_path + "/" + dirname
    if os.path.exists(path=new_path) == False:
        os.mkdir(path=new_path)
    shutil.move(src=old_path, dst=new_path)
