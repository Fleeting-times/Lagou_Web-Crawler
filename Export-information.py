# -*- coding: utf-8 -*-
"""
Created on Fri May 22 00:21:26 2020

@author: RaingEye
"""

import pandas as pd
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient['拉勾网']
data1= db['拉勾网数据采集（2）']
data2 = list(data1.find())

data = pd.DataFrame(data2)
data.to_csv('C:/Users/RaingEye/Desktop/Lagou_website-information.csv', index =False, encoding = 'gb18030')