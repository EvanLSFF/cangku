import requests
import time
import os,sys
from utils.page_DataParser import ExcelUtil
from utils.page_DataParser import yaml_data_with_file
from utils.page_DataParser import readMysql
from utils.page_DataParser import readTxtOrCsv

#函数功能:post上传文件,支持上传单个，多个文件
'''
场景:
post http://abc.com/user/UploadZaopian?method=reg
    请求参数form:
        username="xx"
        pwd="1234"
    上传文件
        wj1=C:/A/1.png
        wj2=C:/A/2.png
'''
#形参filePaths:要上传的多个文件的路径列表。例如:"C:/A/1.PNG,C:/A/2.PNG"
#形参formData:表单数据！支持：json字典、json字符串、列表
def uploadFileorFiles(url,filePaths,formData=None):
    # file={"zhaopian1":open('D:/A/2.png','rb'),
    #       "zhaopian2":open('D:/A/3.png','rb'),
    #       "zhaopian":open('D:/A/4.png','rb'),
    #       "……"}
    files={}
    a=filePaths.split(",")
    for x in a:
        b=x.split(":")
        files[b[0]]=open(b[1],"rb")
        response=requests.post(url=url,data=formData,files=filePaths)


