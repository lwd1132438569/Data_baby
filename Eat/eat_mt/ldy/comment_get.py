# -*- coding: utf-8 -*-
# 功能为对抓取的网页进行分析，提取出用户（昵称）和评论

import re
import sys
import pandas as pd
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

reload(sys)
sys.setdefaultencoding('utf-8')

html = open('D:\\ldy.txt','r').read()

# comment = re.findall(r'<div class="comment"><p>.*?</p></div>',html)
soup = BeautifulSoup(html,'lxml')
res_com = soup.find_all("div",{"class":'comment'})
res_usr = soup.find_all("weak", {"class": 'username'})

username = do_res_user(res_usr)
comment = do_res(res_com)

res_table = pd.DataFrame({'用户':username,'评论':comment})
res_table.to_csv("D:\\ldy_res.csv",encoding="utf_8_sig")