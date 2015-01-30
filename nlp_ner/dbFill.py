# -*- coding: utf-8 -*-
import sqlite3
import os
import re
import requests
import codecs
import datetime
import csv
from pythonds.basic.stack import Stack

os.chdir("E:\\EIO")

def trimRefAndComments(inputString):
    ### Used for trimming comments and reference 
    ### Input:  string to be trimmed 
    ### Output: string after trimming.
    outputString=re.sub("<comment>(.+?)</comment>","",inputString,flags=re.S)
    outputString=re.sub("<ref(.+?)</ref>","",outputString,flags=re.S)
    outputString=re.sub("\&lt;(.*?)\&gt;","",outputString,flags=re.S)
    return outputString

def get_infobox_from_text(article_text):
    ### Used for finding infobox in plain text
    ### Input:  plain text
    ### Output: infobox string
    
    #Build a regexp to get the source artery from the artery infobox
    box_title = None
    exp = r'\{\{'                  # the opening brackets for the infobox 
    exp = exp + r'\s*'           # any amount of whitespace
    exp = exp + r'[Ii]nfobox +'  # the word "infobox", capitalized or not followed by at least one space
    if box_title:
        exp = exp + box_title     # the infobox title, capitalized or not
        exp = exp + r'\s*\|'         # any number of spaces or returns followed by a pipe character
    exp = exp + r'.*'           # a bunch of other stuff in the infobox  
    exp3 = exp                  # save the regexp so far so that I can use it later
    exp3 = exp3 + r'.*\}\}'          # any amount of anything, followed by the end of the infobox
    exp3_obj = re.compile(exp3, re.DOTALL)
    
    search_result = exp3_obj.search(article_text)
    if search_result:
        result_text = search_result.group(0) # returns the entire matching sequence
    else:
        return None
    
    # the regex isn't perfect, so look for the closing brackets of the infobox
    count = 0
    last_ind = None
    for ind, c in enumerate(result_text):
        if c == '}':
            count = count -1
        elif c == '{':
            count = count +1
        if count == 0 and not ind == 0:
            last_ind = ind
            break
    try:
        return result_text[0:last_ind+1][2:-2]
    except TypeError:
        return result_text[2:-2]
    
def infoboxTrimBigBrackets(inputString):
    s=Stack()
    jobList=[]
    len_string=len(inputString)
    start=0
    end=0
    for i in range(len_string):
        symbol=inputString[i]
        if symbol=="{":
            if s.isEmpty():
                start=i
            s.push(symbol)
        if symbol=="}":
            s.pop()
            if s.isEmpty():
                end=i
                newJob=(start,end+1)
                jobList.append(newJob)

    if len(jobList)>0:
        outputString=inputString[0:jobList[0][0]]
        for i in range(len(jobList)):
            jobStart=jobList[i][0]
            jobEnd=jobList[i][1]
            replacement=re.sub("\|","7_5_5_9",inputString[jobStart:jobEnd],re.S)
            if(i+1<len(jobList)):
                outputString=outputString+replacement+inputString[jobEnd:(jobList[i+1][0])]
            else:
                outputString=outputString+replacement+inputString[jobEnd:]
                
    else:
        outputString=inputString
            
    return outputString

def infoboxTrimMidBrackets(inputString):
    s=Stack()
    jobList=[]
    len_string=len(inputString)
    start=0
    end=0
    for i in range(len_string):
        symbol=inputString[i]
        if symbol=="[":
            if s.isEmpty():
                start=i
            s.push(symbol)
        if symbol=="]":
            s.pop()
            if s.isEmpty():
                end=i
                newJob=(start,end+1)
                jobList.append(newJob)


    if len(jobList)>0:
        outputString=inputString[0:jobList[0][0]]
        for i in range(len(jobList)):
            jobStart=jobList[i][0]
            jobEnd=jobList[i][1]
            replacement=re.sub("\|","7_5_5_9",inputString[jobStart:jobEnd],re.S)
            if(i+1<len(jobList)):
                outputString=outputString+replacement+inputString[jobEnd:(jobList[i+1][0])]
            else:
                outputString=outputString+replacement+inputString[jobEnd:]
                
    else:
        outputString=inputString
            
    return outputString

def getKeyAndValue(inputString):
    var_keyAndValue=re.split("\|",inputString,flags=re.S)
    
    for i in range(len(var_keyAndValue)):
        var_keyAndValue[i]=re.sub("7_5_5_9","|",var_keyAndValue[i],flags=re.S) #restore '_*_' to '|'
    
    #split key and value
    for i in range(len(var_keyAndValue)):
        var_keyAndValue[i]=var_keyAndValue[i].split("=")

    #Strip whitespace
    for i in range(len(var_keyAndValue)):
        for j in range(len(var_keyAndValue[i])):
            var_keyAndValue[i][j]=var_keyAndValue[i][j].strip()
    
    #delete null items        
    var_keyAndValue=[i for i in var_keyAndValue if i[0] !='']

  
    return var_keyAndValue

def createTriple(inputList,inputTitle):
    var_buffer=inputList

    #creating triple tuple:(title,key,value)
    var_outputString=""
    for i in range(1,len(var_buffer),1):
        var_outputTriple="["+inputTitle+"]"+" <"+var_buffer[i][0]+"> "+"["+var_buffer[i][1]+"]"+"\r\n"
        var_outputString+=var_outputTriple
    
    return var_outputString

def main():
    ### Fill sqlite db
    
    #connect to DB and set coding=utf8
    cx=sqlite3.connect("E:\\IOE.db")
    cu=cx.cursor()
    cu.execute("create table kb_knowledgebase (id integer primary key, entityName varchar(256) NOT NULL, entityType varchar(256) NOT NULL, fact text NOT NULL, mention text NOT NULL, confidence real NOT NULL, timestamp datetime NOT NULL, image_url varchar(200) NOT NULL)")
    cx.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
    
    #get fileName list
    fileNameList=os.listdir(os.getcwd())
#     writer=csv.writer(file("E:\\test.csv",'wb'))
#     writer.writerow(['ID','ENTITY NAME','TYPE','FACT','MENTION','CONFIDENCE','TIMESTAMP','IMAGE_URL'])
    
    #get infobox and write
    id=1
    for files in fileNameList:
#         with codecs.open(files, 'r', encoding='ISO8859-1') as fd:
        fd=codecs.open(files,'r',encoding='utf-8')
        try:
            plainText=fd.read()
            if re.search("missing=",plainText) !=None:
                continue
#             print plainText
        
            outputString=trimRefAndComments(plainText)
            #get id
            db_id=id
            
            #get title
            title=files.decode('gb2312')[:-4]
            print title
 
            #get facts
            infobox=get_infobox_from_text(outputString)
            if infobox==None: 
                with codecs.open("C:\\Users\\S1LV3R@DELL\\Desktop\\Newlist.txt",'r',encoding="utf-8",errors="ignore",buffering=1) as fd_in:
                    data=fd_in.read()
                data_list=data.split("\n")
                for lines in data_list:
                    lines_split=lines.split("||")
                    if lines_split[0]==title:
                        item_type=lines_split[1]
                        print "Type:",item_type
                        break

                facts="==Empty==\r\n"
             
            else:
                temp_list=re.split(r'\|',infobox,flags=re.S)
                ans=temp_list[0]
                #get type
                ans=re.sub(r'[Ii]nfobox',"",ans,flags=re.S)
                item_type=ans.strip()
                infobox=infoboxTrimBigBrackets(infobox)
                infobox=infoboxTrimMidBrackets(infobox)
                infobox=getKeyAndValue(infobox)
                facts=createTriple(infobox, title) 
             
            print facts
              
              
    		#get mention
            mention="http://zh.wikipedia.org/wiki/"+title
         		
    		#set confidence
            confidence=1.0
         		
    		#set timestamp
            timestamp=datetime.datetime.now()
         		
    		#set image_url
    		###TO DO
            url_base="http://image.baidu.com/i?tn=baiduimagejson&fm=result&fr=&sf=1&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2"
            keyword="&word="+title
            url=url_base+keyword+"&pn=1"+"&rn=1"
            r=requests.get(url,timeout=2.0)
  
            try:
                if (r.status_code==200):
                    image_url=(r.json())['data'][0]['objURL']
                    image_url=str(image_url)
                    print image_url
                    print id
                else:
                    image_url="http://ww4.sinaimg.cn/large/005yyi5Jjw1em5uhtpb0yj302s046glm.jpg"
            except requests.exceptions.RequestException:
                image_url="http://ww4.sinaimg.cn/large/005yyi5Jjw1em5uhtpb0yj302s046glm.jpg"        
            id=id+1
#                 print id
    	#write to sql
            t=(db_id,title,item_type,facts,mention,confidence,timestamp,image_url)
#                 print t
            cx.execute("insert into kb_knowledgebase values (?,?,?,?,?,?,?,?)",t)
            
            cx.commit()

        except IndexError:
            continue
        
        except TypeError:
            continue
        
        except Exception as e:
            print e
            continue

main()
