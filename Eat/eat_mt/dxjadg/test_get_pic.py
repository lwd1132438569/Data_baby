# -*- coding: utf-8 -*-

import re
import pandas as pd
import urllib
from bs4 import BeautifulSoup

def do_res(res):
    res_final = []
    for it in res:
        it = str(it)
        soup = BeautifulSoup(it)
        res_mid = soup.find("p").get_text().strip()
        res_final.append(res_mid)

    return res_final

def do_res_user(res):
    res_final = []
    for it in res:
        it = str(it)
        soup = BeautifulSoup(it)
        res_mid = soup.find("weak").get_text().strip()
        res_final.append(res_mid)

    return res_final

def do_res_pics(res):
    res_final = []
    for it in res:
        it = str(it)
        soup = BeautifulSoup(it)
        res_mid = soup.find("span")['data-src']
        res_final.append(res_mid)

    return res_final

html = open('D:\\dxjadg.txt','r',encoding='utf-8').read()

# comment = re.findall(r'<div class="comment"><p>.*?</p></div>',html)
soup = BeautifulSoup(html,'lxml')
res_com = soup.find_all("div",{"class":'comment'})
res_usr = soup.find_all("weak", {"class": 'username'})
res_pic = soup.find_all("span", {"class": 'pic-container imgbox'})

username = do_res_user(res_usr)
comment = do_res(res_com)
pics = do_res_pics(res_pic)

# r1 = str(pics[0])
# r2 = 'http://' + r1[2:]
# urllib.request.urlretrieve(r2,'D://1.jpg')
i = 0
for p in pics:
    p1 = str(p)
    p2 = 'http://' + p1[2:]
    urllib.request.urlretrieve(p2, 'D://dxjadg_pics//%s.jpg'%i)
    i = i+1


# res_table = pd.DataFrame({'用户':username,'评论':comment})
# res_table.to_csv("D:\\dxjadg_res.csv",encoding="utf_8_sig")