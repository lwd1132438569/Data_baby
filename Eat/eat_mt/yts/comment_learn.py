# -*- coding: utf-8 -*-
import jieba
import jieba.analyse
import pandas as pd

comments = pd.read_csv("D:\\yts_res.csv")

# print type(comments['评论'])
comments_list = comments['评论'].tolist()

res_list = []

for line in comments_list:
    line_cut = jieba.cut(line,cut_all=False)
    # line_cut = jieba.analyse.extract_tags(line, topK=3)
    # print "Full Mode: " + ",".join(line_cut)
    # res_list.append(jieba.cut(l,cut_all=True))

# for l in comments['评论'].tolist():
#     for topic in jieba.analyse.extract_tags(l, topK=3):


# print topic_list
