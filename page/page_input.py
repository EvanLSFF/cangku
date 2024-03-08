#页面类
import time
import allure
from selenium.webdriver.common.by import By
from utils.page_webBase import webPageBase
class Pageform(webPageBase):
    pngNum = 1
    def __init__(self,webBase_driver,url=None):
        webPageBase.__init__(self,webBase_driver)

    def getUrl(self,url):
        self.webBase_driver.get(url)

    def input_username(self,userid):
        loc_username=By.CSS_SELECTOR,'input'
        self.input(loc=loc_username,data=userid)


    def input_pwd(self,pwd):
        loc_pwd=By.CSS_SELECTOR,'input ~ input'
        self.input(loc=loc_pwd,data=pwd)

    def click_sex(self,sex):
        sexname='sex'
        sexvalue=sex
        self.click_Oneradio(sexname,sexvalue)

    def click_guoji(self,guoji):
        loc_guojiName='guoji'
        loc_guojiValue =guoji
        self.click_Oneradio(loc_guojiName,loc_guojiValue)
    def clicks_like(self,like):
        self.click_radios('aihao',like)

    def select_click(self,loc):
        loc_sel=By.CSS_SELECTOR,'select#degree'
        self.click_SelectValue(loc_sel,'text',loc)

    def big_sendkeys(self,data):
        loc_bigsend=By.CSS_SELECTOR,'textarea#jiesao'
        self.input(loc_bigsend,data)

    # def upfile(self,loc):
    #     loc_arr=By.CSS_SELECTOR,'input#zaopian'
    #     self.upload_windowsFile(loc_arr,r'D:\A\updatePush.exe',loc)

    def upfiles(self,loc):
        loc_arr=By.CSS_SELECTOR,'input#zaopian'
        self.uploadS_windowsFile(loc_arr,r'D:\A\updateFiles.exe',loc)

    def click_zhuceorqingkong(self,loc):
        loc_zhuce=By.CSS_SELECTOR,'input[value="{}"]'.format(loc)
        self.click(loc_zhuce)

    def assert_001(self,loc,key):
        if loc=="注册":
            alert=self.getJsText()
            assert True if alert=="注册成功" else False
            self.getJsAccept()
        elif loc=="清空":
            self.AllureSavePng_push(key)
            assert True
        else:
            print("没找到对应元素")
    pngNum += 1
