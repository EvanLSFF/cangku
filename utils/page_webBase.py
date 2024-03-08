#web自动化测试的页面基类,使用page的页面类继承这个页面基类即可
import os
import sys
import time

import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains

class webPageBase(object):
    #初始化webdriver
    def __init__(self,webBase_driver):
        self.webBase_driver=webBase_driver

    '''
    函数功能：拼接XPATH字符串中间部分（不过，后面会多个"and"）。例如：XPATH字符串"//*[contains(@text,'设')]"的中间部分是"contains(@text,'设')"!
    即：
    如果loc 给 "text,设置"或"text,设置,0",函数返回"contains(@text,'设置')and"，情况1！
    如果loc = "text,设置,1",函数返回"@text='设置'and"，情况2！
    '''
    #这个不调用
    def make_xpath_with_unit_feature(self, loc):
        args = loc.split(",")
        feature = ""  # 返回值

        if len(args) == 2:
            feature = "contains(@" + args[0] + ",'" + args[1] + "')" + "and "
        elif len(args) == 3:
            if args[2] == "1":
                feature = "@" + args[0] + "='" + args[1] + "'" + "and "
            elif args[2] == "0":
                feature = "contains(@" + args[0] + ",'" + args[1] + "')" + "and "
        return feature

    '''
    函数功能：给简化的xpath，函数返回标准的xpath字符串。
    即:
    如果loc = "text,设置"或"text,设置,0"，函数返回"//*[contains(@text,'设置')]"，情况1。
    如果loc = "text,设置,1"，函数返回"//*[@text='设置']"，情况2。
    如果loc = ["text,设置"] ，函数返回"//*[contains(@text,'设置')]"，情况1。
    如果loc = ["text,设置", "index,20,1", "index1,50"]，函数返回"//*[contains(@text,'设置')and@index='20'andcontains(@index1,'50')]"，情况3。
    如果loc = "//*[contains(@text,'设')]" ，即故意传个正常的xpath字符串，函数返回"//*[contains(@text,'设')]"，情况4。
    '''
    #当xpath使用contains和text时，这个才能生效
    #调用时只需要调用这个即可
    def make_xpath_with_feature(self, loc):
        feature_start = "//*["
        feature_end = "]"
        feature = ""

        # 如果传的是字符串，即情况1和情况2
        if isinstance(loc, str):
            # 如果是正常的xpath，即情况4
            if loc.startswith("//"):
                return loc
            feature = self.make_xpath_with_unit_feature(loc)
        else:  # 如果传的是列表，即情况3
            for i in loc:
                feature += self.make_xpath_with_unit_feature(i)

        feature = feature.rstrip("and ")  # 删除最右侧的"and "
        ret_loc = feature_start + feature + feature_end
        return ret_loc

    #函数功能：根据元素定位特征定位某元素。
    #形参loc:编写格式[BY.CSS_SELECTOR,"input input"],如:BY.CLASS_NAME,"sex"
    def find_element(self,loc):
        by=loc[0]
        value=loc[1]
        if by==By.XPATH: #如果定位是xpath定位，可以简化
            value=self.make_xpath_with_feature(value)
        return self.webBase_driver.find_element(by,value)

    # 函数功能：根据元素定位特征定位多个元素。
    # 形参loc:编写格式[BY.CSS_SELECTOR,"input input"],如:BY.CLASS_NAME,"sex"
    def find_elements(self,loc):
        by = loc[0]
        value = loc[1]
        if by == By.XPATH:  # 如果定位是xpath定位，可以简化
            value = self.make_xpath_with_feature(value)
        return self.webBase_driver.find_elements(by, value)

    #通用操作:输入数据(send_keys)
    #函数功能:定位元素loc,并输入数据data
    # loc元素是定位元素,如:By.CSS_SELECTOR,"input#pwd"
    #适合文本框输入以及大文本框的输入
    def input(self,loc,data):
        self.find_element(loc).send_keys(data)

    #函数功能:定位元素loc,并清空文本
    # loc元素是定位元素,如:By.CSS_SELECTOR,"input#pwd"
    def clear(self,loc):
        self.find_element(loc).clear()

    #函数功能：定位元素loc,并点击
    # loc元素是定位元素,如:By.CSS_SELECTOR,"input#pwd"
    def click(self,loc):
        self.find_element(loc).click()


    #函数功能:上传单个文件，适合调用windows系统的窗口，使用autoIT技术
    #形参loc_file:需要上传文件的元素定位,一般是input标签的定位特征！
    #形参uploadExePath:AutoIT编译后的脚本在windows中存放的文件路径：例如"C:/A/uploadFile.exe"
    #形参filePath:windows需要上传的图片的位置,例如:C:\A\1.png
    def upload_windowsFile(self,loc_attr,uploadExePath,filePath):
        #让需要上传文件的windows窗口出现
        ele_file = self.find_element(loc_attr)
        self.mouse_click(loc=ele_file,mouse_class="单击")
        time.sleep(2)
        #利用autoIT技术实现文件上传,操作OS的windows窗口
        os.system(uploadExePath+" "+filePath)


    #函数功能,上传多个文件,适合调用windows系统
    #形参loc_attr:上传文件的那个input标签的定位特征
    #形参uploadExepath:auto IT脚本编译后的上传文件的路径，例如"C:/A/uploadFiles.exe"
    #形参filePaths:想要上传的文件的路径。注意路径中的斜杠。例如:"D:\\A\\2.png,C:\\A\\3.png"或"C:\A\1,PNG"或""
    def uploadS_windowsFile(self,loc_attr,uploadExepath,filePaths):
        if filePaths=="":
            pass
        else:
            #让文件上传窗口出现
            ele_openwin=self.find_element(loc_attr)
            self.mouse_click(ele_openwin,"单击")
            time.sleep(1)
            #利用autoIT技术实现
            c=r''
            a = filePaths.split(",")#a=["C:\A\1.png","C:\A\2.png"]
            for x in a:
                c+='"'+x+'" '#c='"C:\A\1.png" "C:\A\2.png" '
            os.system(uploadExepath+"  "+c)
            time.sleep(2)

    # 函数功能:send_keys上传单个文件。只适合(send_keys上传)
    # 形参loc元素是定位元素,如:By.CSS_SELECTOR,"input#pwd"
    # 形参filePath:要上传的文件路径，如D:/A/1.png
    def upload_oneFile(self, loc, filePath, timeout=10):
        self.find_element(loc).send_keys(filePath)
        time.sleep(timeout)

    #函数功能:send_keys上传文件或多个文件
    #形参loc_attr:上传文件的那个input标签的定位特征
    # 形参filePaths:想要上传的文件的路径。注意路径中的斜杠。例如:"D:\\A\\2.png,C:\\A\\3.png"或"C:\\A\\1,PNG"或""
    def uploadS_sendkeysFile(self,loc_attr,filePaths):
        if filePaths=="":
            pass
        else:
            filePaths=filePaths.replace("\\","\\\\")
            a=filePaths.split(",")
            b="\n".join(a)
            print(b) # D:\A\2.png  "\n"(换行)  C:\\A\\3.png ele_openwin=
            self.find_element(loc_attr).send_keys(b)
            time.sleep(2)
            # self.mouse_click(ele_openwin,"单击")
            # time.sleep(1)


    #函数功能:获取JS弹窗的文本
    def getJsText(self):
        return self.webBase_driver.switch_to.alert.text


    #函数功能:获取JS弹窗并点击确定按钮
    def getJsAccept(self):
        return self.webBase_driver.switch_to.alert.accept()

    #函数功能:获取JS弹窗并点击取消按钮
    def getJsDismiss(self):
        return self.webBase_driver.switch_to.alert.dismiss()

    #函数功能:获取JS的prompt弹窗并输入文本
    def getJsInput(self,data):
        return self.webBase_driver.switch_to.alert.send_keys(data)

    #函数功能:封装单选按钮
    #适合网页中的单选按钮,单选按钮必备name和value属性
    #形参radio_valuename:单选按钮的name属性的值
    #形参radio_value:单选按钮的value属性的值
    def click_Oneradio(self,radio_valuename,radio_value):
        loc=By.CSS_SELECTOR,"input[name='{}'][value='{}']".format(radio_valuename,radio_value)
        ele_Oneradio=self.find_element(loc)
        ele_Oneradio.click()

    #函数功能:获取元素loc的形参attr_name属性的值
    def getAttribute(self,loc,attr_name):
        return self.find_element(loc).get_attribute(attr_name)

    #函数功能:获取元素的文本内容,title标签除外
    def getText(self,loc_ele):
        return self.find_element(loc_ele).text

    #函数功能:封装复选框
    #适合网页中的复选按钮，复选按钮必备name和value属性
    #形参redio_name:复选框选项的name属性的值
    #形参radio_values:你想要选中的这些复选框选项的value属性的值的列表,例如"dalanqiu,tizuqiu,wanyouxi"
    def click_radios(self,radio_namebq_value,radio_valuebq_values):
        loc=By.NAME,radio_namebq_value
        eles=self.find_elements(loc) #获取页面对应标签所有的选项
        for ele in eles: #for遍历这所有的选项
            value=ele.get_attribute('value')
            checked=ele.get_attribute('checked') #返回 "true"或None
            # 获取每个选项的value属性，判断该属性是否在你文件参数中要点击的选项中
            if value in radio_valuebq_values:
                if checked=="true":
                    pass
                else:
                    ele.click()
            elif value not in radio_valuebq_values:
                if checked=="true":
                    ele.click()
                else:
                    pass

    #函数功能:使用Select选择下拉框元素
    #形参loc_select:填入select标签的值,例子:By.CLASS_NAME,"select"
    #形参click_select_textorindexorvalue:填入选择下拉框的方式,text,index,value
    #形参loc:填入选中哪个下拉框,选text就填下拉框的文本内容,选index就填下
    #       拉框的下标,选value,就填下拉框的value属性的值。
    def click_SelectValue(self,loc_select,click_select_textorindexorvalue,loc):
        selectbq=self.find_element(loc_select)
        sel=Select(selectbq)
        if click_select_textorindexorvalue=='text':
            sel.select_by_visible_text(loc)
        elif click_select_textorindexorvalue=='index':
            sel.select_by_value(loc)
        elif click_select_textorindexorvalue=='value':
            sel.select_by_value(loc)
        else:
            print("没匹配到相应的select操作函数")

    #函数功能:切换iframe框架
    #形参loc_iframe:传入iframe框架的元素特征,如:By.NAME,'frame'
    def switch_iframe(self,loc_iframe):
        frame=self.find_element(loc_iframe)
        self.webBase_driver.switch_to.frame(frame)

    #函数功能:从iframe框架切换到主框架
    def switch_default_iframe(self):
        return self.webBase_driver.switch_to.deafult.content()

    #函数功能:切换浏览器窗口
    #形参window_n:要切换到哪个装口，0:第一个,1:第二个,-1:最新的一个
    def switch_window(self,n):
        windows=self.webBase_driver.window_handles[n]
        return self.webBase_driver.switch_to.window(windows)

    #函数功能:鼠标相关处理,单击双击
    #形参loc:传入鼠标需要点击的元素
    #形参mouse_class:鼠标需要操作的类型,(单击,双击,悬停,右键)
    def mouse_click(self,loc,mouse_class):
        if mouse_class=="单击":
            return ActionChains(self.webBase_driver).click(loc).perform()
        elif mouse_class=="双击":
            return ActionChains(self.webBase_driver).double_click(loc).perform()
        elif mouse_class=="悬停":
            return ActionChains(self.webBase_driver).move_to_element(loc).perform()
        elif mouse_class=="右键":
            return ActionChains(self.webBase_driver).context_click(loc).perform()

    #函数功能：浏览器滚动
    #形参start:开始位置
    #形参end:结束位置
    def pageMove_scrollTo(self,start,end):
        movejs='window.scrollTo({},{})'.format(start,end)
        return self.webBase_driver.execute_script(movejs)

    #函数功能:页面截图
    #形参filePath:截图想保存到哪就到哪
    def savePng_zidingyi(self,filePath):
        return self.webBase_driver.get_screenshot_as_file(filePath)

    # 函数功能:页面截图
    # 形参fileName:截图名称，只给截图名称即可
    def savePng_ScreenFile(self,fileName):
        return self.webBase_driver.get_screenshot_as_file("./screen/{}.png".format(fileName))

    #函数功能:页面截图
    #形参Key:给用例编号,如test_K001
    def savePng_AutoScreenFile(self,key=None):
        newTime=time.strftime('%Y%m%d_%H%M%S')
        self.webBase_driver.get_screenshot_as_file('./screen/{}_{}.png'.format(key,newTime))
        return newTime #执行这个函数则会返回时间

    #函数功能:截图并上传至allure测试报告中
    #形参key:要上传文件的测试用例名称，如yaml中的K001,K002,K003…
    def AllureSavePng_push(self,key):
        filename=self.savePng_AutoScreenFile(key) #将截图名称返回的时间传入
        #以二进制打开并读取图片,然后可以直接写入截图名称(变量为name),然后使用上传截图的参数即可
        allure.attach(open("./screen/{}_{}.png".format(key,filename),'rb').read(),"步骤:本次截图",allure.attachment_type.PNG)