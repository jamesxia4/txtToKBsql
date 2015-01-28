#coding:utf-8
import requests
import re
import os
import codecs
import json
from bosonnlp import BosonNLP

TXT_PATH="E:\\wordDir\\text"
API_TOKEN='5jxUoCKu.2677.G-NqmaiA83Q1'


def boson_nre_batch():
    os.chdir("E:\\wordDir")
    fd_out=codecs.open("EntityList.txt",'a',encoding="utf-8",errors='ignore',buffering=1)
    nlp=BosonNLP(API_TOKEN)
    entityCollection=[]
    os.chdir(TXT_PATH)
    for files in os.listdir(os.getcwd()):
        fd=codecs.open(files,"r",encoding="utf-8")
        docText=fd.read()
        result=nlp.ner(docText)[0]
        words=result['word']
    #     tags=result['tag']
        entities=result['entity']
        docEntityList=[]
        for i in range(len(entities)):
            mergedToken=u""
            for j in range(entities[i][0],entities[i][1],1):
                mergedToken=mergedToken+words[j]
            token_candidate=(mergedToken,str(entities[i][2]),files.decode('gb2312'))
            
            #check for redundant token, only add new token into the entity_list
            flag=0
            for k in range(len(docEntityList)):
                if (token_candidate[0]==docEntityList[k][0]) and \
                (token_candidate[1]==docEntityList[k][1]):
                    flag=flag+1        
            if flag==0:
                docEntityList.append(token_candidate)
        print files.decode('gb2312')," ",len(docEntityList)
        entityCollection.append(docEntityList)
                

    for i in range(len(entityCollection)):
        for j in range(len(entityCollection[i])):
            outputStr=entityCollection[i][j][0]+"||"+entityCollection[i][j][1]+"||"+entityCollection[i][j][2]+"\n"
            fd_out.write(outputStr)
    fd_out.close()
    
    
    #     return docEntityList
#         print "=============="        
#         print len(docEntityList)
#         for i in range(len(docEntityList)):
#             print docEntityList[i][0],"    ","type:",docEntityList[i][1]
        
        
def boson_nre_testCase():
    nlp=BosonNLP(API_TOKEN)
    os.chdir(TXT_PATH)
    fd=codecs.open("1.txt",'r',encoding='utf-8',errors="ignore",buffering=1)
    docText=fd.read()
    result=nlp.ner(docText)[0]
    words=result['word']
#     tags=result['tag']
    entities=result['entity']
#     print len(words)," ",len(tags)," ",len(entities)
#     print words
#     print "\n"
#     print tags
#     print "\n"
#     print len(entities)
#     print entities
#     print "\n"
    
    docEntityList=[]
    for i in range(len(entities)):
        mergedToken=u""
        for j in range(entities[i][0],entities[i][1],1):
            mergedToken=mergedToken+words[j]
        token_candidate=(mergedToken,str(entities[i][2]))
        
        #check for redundant token, only add new token into the entity_list
        flag=0
        for k in range(len(docEntityList)):
            if (token_candidate[0]==docEntityList[k][0]) and \
            (token_candidate[1]==docEntityList[k][1]):
                flag=flag+1        
        if flag==0:
            docEntityList.append(token_candidate)
            
#     return docEntityList
    print "=============="        
    print len(docEntityList)
    for i in range(len(docEntityList)):
        print docEntityList[i][0],"    ","type:",docEntityList[i][1]


def main():
    boson_nre_batch()
    #boson_nre_testCase()
    
main()        
    
    