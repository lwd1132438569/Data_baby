# -*- coding: utf-8 -*-
import requests
import time
import random
import sys
# from imp import reload
#
# reload(sys)
# sys.setdefaultencoding('utf-8')

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept':'*/*',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Referer':'https://item.jd.com/3219817.html'
}

cookie = {
    'unpl':'V2_ZzNtbRBeQhciCxUAKE5YBmIARQ0SAkMccVgUVisQWQYzUBtdclRCFXMUR1FnGFoUZwIZXkRcQhdFCHZXchBYAWcCGllyBBNNIEwHDCRSBUE3XHxcFVUWF3RaTwEoSVoAYwtBDkZUFBYhW0IAKElVVTUFR21yVEMldQl2VH0RVQZvABRdQ2dzEkU4dlJ4Gl4MYzMTbUNnAUEpC0RRexxcSGcFGlRBX0ATdQl2VUsa',
    '__jdv':'122270672|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_c803f2bebf5242faad185ac3a842eb81|1491532024032',
    'ipLoc-djd':'1-72-2799-0',
    'ipLocation':'%u5317%u4EAC',
    'user-key':'e0dd75a9-a9a1-4b83-a107-cafa54043b74',
    'cn':'0',
    '__jda':'122270672.1798292710.1491532023.1491532023.1491532024.1',
    '__jdb':'122270672.14.1798292710|1.1491532024',
    '__jdc':'122270672',
    '__jdu':'1798292710'
}

url1 = "https://i.meituan.com/poi/42051528/feedbacks/page_"

ran_num = random.sample(range(82), 82)  #82

for i in ran_num:
    a = ran_num[0]
    if i == a:
        i = str(i)
        url = (url1 + i)
        r = requests.get(url = url,headers = headers,cookies=cookie)
        # r = requests.get(url=url, headers=headers, cookies=cookie)
        html = r.content
    else:
        i = str(i)
        url = (url1 + i)
        r = requests.get(url=url, headers=headers,cookies=cookie)
        html2 = r.content
        html = html + html2
        time.sleep(5)
        print("当前抓取页面" + url + "状态" + str(r))

html = str(html,encoding='utf-8')

file = open("D:\\dxjadg.txt", "w", encoding='utf-8')
file.write(html)

file.close()