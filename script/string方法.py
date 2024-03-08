#count方法,统计字符串的次数
#int obj.count(String s)
a="aaasDFSAghaa"
print(a.count("a"))
#startwith方法,判断以某字符开头,布尔
#boolean
print(a.startswith("a"))
print(a.endswith("a"))
#find方法,获取字符首次出现的正向下标
#int obj.find(String s,[int start,int end])
print(a.find("sD",0,-1),a.rfind("aa"))
#split,以某字符分割字符串返回列表(不可空)
print(a.split("F"))
#strip,掐头去尾两边的指定字符
print(a.strip("a"))
#lower,upper,swapcase,小写，大写，互换
print(a.lower(),a.upper(),a.swapcase())
#join,以某字符(空,非空都行)连接把多个字符串连接为1个(对str,list都行)
print("".join(["a","b","c","d"]))
b=["1","2","3"]
c=["1","2"]
print(b.extend(["asd","asds"]))



#
#判断一个字符串是不是ip地址
a="192.168.0.1"
b=[]
for i in a:
    if i==".":
        b.append(i)
        if b==[".",".","."]:
            print("a是ip地址")
            print(b)
    else:
        pass

