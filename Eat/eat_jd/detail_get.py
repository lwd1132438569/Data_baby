# -*- coding: utf-8 -*-
import re
import sys
import pandas as pd

reload(sys)
sys.setdefaultencoding('utf-8')

html = open("D:\\jd_7p.txt",'r').read()

#客户端
userClient = re.findall(r'.*?,"userClientShow":(.*?),',html)
#用户名
nickname = re.findall(r'.*?,"nickname":(.*?),',html)
#评论内容
content = re.findall(r'"guid".*?,"content":(.*?),',html)
content_pure = []
for i in content:
    if not "img" in i:
        content_pure.append(i)
#是否来自手机
isMobile = re.findall(r'.*?"isMobile":(.*?),',html)
#对isMobile字段数据进行清洗
mobile = []
for m in isMobile:
    n = m.replace('}','')
    mobile.append(n)

#将评论数据写入到文件
# print str(content)
# file = open('D:\\jd_7p_content.txt','w')
# # for line in content:
# #     file.w
# file.writelines(content_pure)
# file.close()

res_table = pd.DataFrame({'用户':nickname,'评论':content_pure})

res_table.to_csv("D:\\res.csv")