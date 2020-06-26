# -*- coding: utf-8 -*-
"""
Created on Thu May 21 13:29:22 2020

@author: RaingEye
"""
import time
import re
import random
import pymongo
from selenium import webdriver
import warnings
warnings.filterwarnings('ignore')
#不发出警告
 
'''
函数1：login(url,username,password) → 【登陆】
u：起始网址
username：用户名
password：密码
'''
def login(url, usernamei, passwordi):
    brower.get(url)
    #访问目标网址
    
    brower.find_element_by_xpath('//*[@id="changeCityBox"]/p[1]/a').click()
    #登录
    
    brower.find_element_by_xpath('//*[@id="lg_tbar"]/div/div[2]/ul/li[3]/a').click()
    #选择站点
    
    username = brower.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div[2]/div[3]/div[1]/div/div[1]/form/div[1]/div/input')
    password = brower.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div[2]/div[3]/div[1]/div/div[1]/form/div[2]/div/input')
    #找到input标签
    
    username.clear()
    password.clear()
    username.send_keys(usernamei)
    password.send_keys(passwordi)
    #清空登录框，输入登录信息
    
    brower.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div[2]/div[3]/div[2]/div[2]/div[2]').click()
    #点击登录按钮
    print('登陆成功，返回目前网址：',brower.current_url)



'''
【分页网页url采集】函数
    n：页数参数
    结果：得到一个分页网页的list
'''    
def get_url(n):
    lst = []
    for i in range(1, n+1):
        lst.append('https://www.lagou.com/shanghai-zhaopin/shujuwajue/%i/?filterOption=%i'%(i, i))
    return lst
   

'''
【访问页面 + 采集岗位信息】函数
url：数据页面网址
table：mongo集合对象
'''   
def get_data(url, table):
    brower.get(url)
    #访问网页
    
    ul = brower.find_element_by_xpath('//*[@id="s_position_list"]/ul')
    lis= ul.find_elements_by_tag_name('li')
    #获取所有li标签
    
    n = 0
    
    for li in lis:
        dic = {}
        #存储岗位信息
        
        dic['岗位名称'] = li.find_element_by_xpath('//*[@id="s_position_list"]/ul/li[1]/div[1]/div[1]/div[1]/a/h3').text
        dic['发布时间'] = li.find_element_by_xpath('//*[@id="s_position_list"]/ul/li[1]/div[1]/div[1]/div[1]/span').text
        
        info1 = li.find_element_by_class_name('li_b_l').text
        info1 = re.split(r'[ /]', info1)
        
        dic['薪资'] = info1[0]
        dic['经验要求'] = info1[1]
        dic['学历要求'] = info1[-1]
        dic['企业'] = li.find_element_by_class_name('company_name').text
        info2 = li.find_element_by_class_name('industry').text.split(' / ')
        dic['行业'] = info2[0]
        dic['融资情况'] = info2[1]
        dic['规模'] = info2[2]
        table.insert_one(dic)   #存入数据库
        n+=1
    return n

    
if __name__ == '__main__':
    brower = webdriver.Chrome()
    #启动模拟器
     
    url = 'https://www.lagou.com/'
    #目标网站的网址
    
    login(url, '130****1405', '***********')
    #登录网址(填写自己的手机号和密码)
        
    url_list = get_url(30)
    #获取每一页的URL
    
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = myclient['拉勾网']
    datatable = db['拉勾网数据采集（1）'] 
    #链接MongoDB数据库
    
    errorlst = []
    #访问失败的URL列表
    
    datacount = 0
    
    for url in url_list:
        try:
            datacount += get_data(url, datatable)
            print('成功采集%i条数据' % datacount)
            sleeptime = random.randint(1, 5)
            print('sleep......', sleeptime)
            time.sleep(sleeptime)
        except:
            errorlst.append(url)
            print('数据采集失败，数据网址为：',url)
    
