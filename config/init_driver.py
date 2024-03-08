#初始化
from selenium import webdriver

def init_webdriver():
    driver=webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    return driver
