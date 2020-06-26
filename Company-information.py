# -*- coding: utf-8 -*-
"""
Created on Thu May 21 22:41:14 2020

@author: RaingEye
"""
import time
import re
import pymongo
import random
from selenium import webdriver
import warnings
warnings.filterwarnings('ignore')


def login(url, usernamei, passwordi):
    '''
    【登陆】函数
    url：起始网址
    usernamei：用户名
    passwordi：密码
    '''
    brower.get(url)
    #访问网页
    
    brower.find_element_by_xpath('//*[@id="lg_tbar"]/div/div[2]/ul/li[3]/a').click()
    #点击登录账号
    
    username = brower.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div[2]/div[3]/div[1]/div/div[1]/form/div[1]/div/input')
    password = brower.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div[2]/div[3]/div[1]/div/div[1]/form/div[2]/div/input')
    #定位账号输入框和密码输入框
    
    username.clear()
    password.clear()
    #清空输入框内的数据
    
    username.send_keys(usernamei)
    password.send_keys(passwordi)
    #输入账号和密码
    
    brower.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div[2]/div[3]/div[2]/div[2]/div[2]').click()
    #点击登录
    
    print('登陆成功，当前网址为：', brower.current_url)
    
    return brower.current_url
    
    
    

def get_data(url, table, page_n):
    '''
    【访问页面 + 采集岗位信息】函数
    url：数据页面网址
    table：mongo集合对象
    page_n：翻页次数
    ''' 
    brower.get(url)
    n = 0
    for p in range(page_n):
        #访问网页
        
        ul = brower.find_element_by_xpath('//*[@id="company_list"]/ul')
        lis = ul.find_elements_by_tag_name('li')
        #获取所有的li标签
        
        for i in range(len(lis)):
            dic = {}
            dic['企业名称'] = lis[i].find_element_by_xpath('//*[@id="company_list"]/ul/li[%i]/div[1]/h3/a'%(i + 1)).text
            info1 = lis[i].find_element_by_xpath('//*[@id="company_list"]/ul/li[%i]/div[1]/h4[1]'%(i+1)).text
            dic['行业'] = info1.split('/')[0]
            dic['融资情况'] = info1.split('/')[1]
            dic['企业规模'] = info1.split('/')[2]
            dic['企业简介'] = lis[i].find_element_by_xpath('//*[@id="company_list"]/ul/li[%i]/div[1]/h4[2]'%(i+1)).text
            info2 = lis[i].find_element_by_xpath('//*[@id="company_list"]/ul/li[%i]/div[2]'%(i+1)).text
            info2 = re.split(r'\n', info2)
            dic['面试评价'] = info2[0]
            dic['在招职位'] = info2[2]
            dic['监理处理率'] = info2[4].split('%')[0]
            table.insert_one(dic)
            #存储数据库
            n+=1
        brower.find_element_by_xpath('//*[@id="company_list"]/div/div/span[6]').click()
        #点击下一页
        
        sleeptime = random.randint(1, 5)
        print('成功采集%i条数据，等待sleep....' % n,sleeptime)
        time.sleep(sleeptime)


if __name__ == '__main__':
    brower = webdriver.Chrome()
    #启动测试器
    
    url = login('https://www.lagou.com/gongsi/', '130****1405', '*********')
    #登陆网址
    
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = myclient['拉勾网']
    datatable = db['拉勾网数据采集（2）']
    #设置数据库集合
    
    get_data(url, datatable, 20)
    # 采集数据，翻20页
    
