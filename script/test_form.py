#操作类
import os,sys

import allure

sys.path.append(os.getcwd())
import time
import pytest
from utils.page_DataParser import yaml_data_with_file
from config.init_driver import init_webdriver
from page.page_input import Pageform
class Test01(object):
    url = "http://oss.52studyit.net/webzdh/form.html"
    def setup(self):
        self.config_driver=init_webdriver()
        #把config引入的driver传到page中
        self.webBase_driver=Pageform(self.config_driver)


    def teardown(self):
        time.sleep(3)
        self.config_driver.quit()
    @allure.step(title="覆盖用例,k001,K002,K003")
    @pytest.mark.parametrize("data",yaml_data_with_file('data/data.yaml','test_zhuce_001'))
    def test_001(self,data):
        username = data["username"]
        pwd = data["pwd"]
        sex = data["sex"]
        guoji = data["guoji"]
        like = data["like"]
        xueli = data["xueli"]
        ziwojies = data["ziwojies"]
        zp = data["zp"] #D:\A\2.png,C:\A\3.png
        zc = data["zc"]
        allure.attach("","步骤:输入账号:"+data["username"])

        allure.attach("操作步骤：1.输入{},2.输入{},3.输入{}".format(username,pwd,sex))

        self.webBase_driver.getUrl(self.url)

        self.webBase_driver.input_username(username)
        time.sleep(1)

        self.webBase_driver.input_pwd(pwd)

        self.webBase_driver.click_sex(sex)

        self.webBase_driver.click_guoji(guoji)

        self.webBase_driver.clicks_like(like)

        self.webBase_driver.select_click(xueli)

        self.webBase_driver.big_sendkeys(ziwojies)

        self.webBase_driver.upfiles(zp)
        time.sleep(2)
        self.webBase_driver.click_zhuceorqingkong(zc)
        time.sleep(1)

        self.webBase_driver.assert_001(zc,data["key"])
        time.sleep(2)