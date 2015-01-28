#coding:utf-8
'''
    Multi-threaded Wikipedia Spider
    Author: Yuanfang Xia
    Mailto: johnnyrxia4@126.com
    Github: https://www.github.com/jamesxia4
    Last Update: 2015/01/28
'''

'''
    External dependent Libraries: requests
'''
import re
import requests
import os
import codecs
import json
import urllib

'''
    Environmental Variables:
'''
ENTITY_PATH="C:\\Users\\S1LV3R@DELL\\Desktop"
ENTITY_FILENAME="Newlist.txt"

headers1={'content-type':'application/json'}
URL_BASE_EN="http://en.wikipedia.org/w/api.php?"
URL_BASE_CH="http://zh.wikipedia.org/w/api.php?"
URL_S="format=xml&action=query&titles="
URL_E="&redirects&prop=revisions&rvprop=content&rawcontinue"

'''
    Code:
'''
def parse_and_return_joblist():
    '''
        Parse input "||" separated lines of entities
        Arguments: none
        Returns: a list, entity_list
    '''
    os.chdir(ENTITY_PATH)
    fd_in=codecs.open(ENTITY_FILENAME,'r',encoding="utf-8",errors="ignore",buffering=1)
    wholeList=fd_in.read()
    entity_list=wholeList.split("\r\n")
    entity_list=[i for i in entity_list if i !=u''] #Exclude Null items in entity_list
#     print entity_list
    return entity_list
    
def spider_master(jobList):
    jobs=[]
    for items in jobList:
        items_split=items.split("||")
        items_tuple=(items_split[0],items_split[1],items_split[2])
        jobs.append(items_tuple)
    
    
def testCase():
    parse_and_return_joblist()
    
testCase()