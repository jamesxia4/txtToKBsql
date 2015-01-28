#coding:utf-8
import requests
import re
import os
import codecs
import json

API_KEY='Q1O138475iJxLlgaMzBjMkcrlCZw0sdZwtPv0a7o'

def do_nlp_nre(inputString):
    """
    Handles input string and do NLP Named Recognized Entity Task via HTTP POST method, using LTP-Cloud
    
    Arguments:
        inputString: Target string to be analyzed by NLP front-end
    
    Returns:
        entityList: a list of Named Recognized Entities
        
    Raises:
        #TO DO#
    """
    entityList=[]
    payload={'api_key':API_KEY,'text':inputString,'pattern':'ner','format':'json','xml_input':'false','has_key':'true'}
    response=requests.get("http://api.ltp-cloud.com/analysis/?",params=payload)
    if response.status_code==200:
        NRE_Data=response.json()
        for i in range(len(NRE_Data)):
            for j in range(len(NRE_Data[i])):
                for k in range(len(NRE_Data[i][j])):
                    flag=0
                    for l in range(len(entityList)):
                        if (NRE_Data[i][j][k]['cont']==entityList[l][0]):
                            flag=flag+1
                    if flag==0:
                        if NRE_Data[i][j][k]['pos']=='ni':
                            entityList.append((NRE_Data[i][j][k]['cont'],"Organization"))
                        elif (NRE_Data[i][j][k]['pos']=='nl') or (NRE_Data[i][j][k]['pos']=='ns'):
                            entityList.append((NRE_Data[i][j][k]['cont'],"Location/Geographical name"))
                        elif (NRE_Data[i][j][k]['pos']=='nz'):
                            entityList.append((NRE_Data[i][j][k]['cont'],"Proper noun"))
                        elif (NRE_Data[i][j][k]['pos']=='nh'):
                            entityList.append((NRE_Data[i][j][k]['cont'],"Person name"))
                        else:
                            continue
                        
        for i in range(len(entityList)):
            print entityList[i][0],' ',entityList[i][1],"\n"
        return entityList
    
    else:
        retry=5
        while (retry>0) and (response.status_code!=200):
            response=requests.get("http://api.ltp-cloud.com/analysis/?",params=payload)
            retry=retry-1
        
        if response.status_code==200:
            NRE_Data=response.json()
            for i in range(len(NRE_Data)):
                for j in range(len(NRE_Data[i])):
                    for k in range(len(NRE_Data[i][j])):
                        flag=0
                        for l in range(len(entityList)):
                            if (NRE_Data[i][j][k]['cont']==entityList[l][0]):
                                flag=flag+1
                        if flag==0:
                            if NRE_Data[i][j][k]['pos']=='ni':
                                entityList.append((NRE_Data[i][j][k]['cont'],"Organization"))
                            elif (NRE_Data[i][j][k]['pos']=='nl') or (NRE_Data[i][j][k]['pos']=='ns'):
                                entityList.append((NRE_Data[i][j][k]['cont'],"Location/Geographical name"))
                            elif (NRE_Data[i][j][k]['pos']=='nz'):
                                entityList.append((NRE_Data[i][j][k]['cont'],"Proper noun"))
                            elif (NRE_Data[i][j][k]['pos']=='nh'):
                                entityList.append((NRE_Data[i][j][k]['cont'],"Person name"))
                            else:
                                continue
                            
            for i in range(len(entityList)):
                print entityList[i][0],' ',entityList[i][1],"\n"
            return entityList
        else:
            return entityList
        
        
        
        

def do_nlp_nre_document(fileName):
    docEntityList=[]
    docText=(codecs.open(fileName,mode='r',errors='ignore',buffering=1)).read()
    iter_time=len(docText)/1000
    
    for i in range(iter_time):
        paraEntityList=do_nlp_nre(docText[i*1000,(i+1)*1000])
        
        #Check for redundant entities
        for j in range(len(paraEntityList)):
            flag=0
            for k in range(len(docEntityList)):
                if (paraEntityList[j][0]==docEntityList[k][0]) and (paraEntityList[j][1]==docEntityList[k][1]):
                    flag=flag+1
            
            #Append new items:
            if flag==0:
                docEntityList.append(paraEntityList[j])
                
    #deal with residue
    paraEntityList=do_nlp_nre(docText[iter_time*1000,len(docText)])
    #Check for redundant entities
    for j in range(len(paraEntityList)):
        flag=0
        for k in range(len(docEntityList)):
            if (paraEntityList[j][0]==docEntityList[k][0]) and (paraEntityList[j][1]==docEntityList[k][1]):
                    flag=flag+1
            
        #Append new items:
        if flag==0:
            docEntityList.append(paraEntityList[j])
            
    return docEntityList
    
        
