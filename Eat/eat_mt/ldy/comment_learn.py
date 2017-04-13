# -*- coding: utf-8 -*-
import jieba
import jieba.analyse
import pandas as pd

comments = pd.read_csv("D:\\ldy_res.csv")

# print type(comments['评论'])
topic_list = []

# for l in comments['评论'].tolist():
#     for topic in jieba.analyse.extract_tags(l, topK=3):


# print topic_list