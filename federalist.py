
# coding: utf-8

# # Import Packages for the script

# In[6]:


def load_federalist_dataset():
    import json
    import requests
    import os
    import urllib.request
    import pandas as pd
    import numpy as np
    pd.options.mode.chained_assignment = None  # default='warn'

    url="http://ptrckprry.com/course/ssd/data/federalist.json"
    with urllib.request.urlopen(url) as response:
        k = response.read()

    k=str(k)
    a=k.lower()

    k=k.replace("\\\\n"," ").replace("\\\'","'").replace("b\'","")

    l=[]
    dictlist=[]

    z=k.split("\\n")

    del z[-1]

    for i in range(0,len(z)):
        try:
            dictlist.append(json.loads(z[i]))
        except:
            try:
                d=z[i]
                #d=d.replace('\\\\*','"').replace('*','"')
                ftext=d[d.find('"text": "')+9:d.find('", "date":')]#.replace('"','*')
                fauthor=d[d.find('"author": ')+11:d.find('", "text":')]
                fdate=d[d.find('"date": ')+8:d.find('", "title": ')]
                ftitle=d[d.find('"title": ')+10:d.find('", "paper_id": ')]
                fpaperid=d[d.find('"paper_id": ')+12:d.find(', "venue": ')]
                fvenue=d[d.find('"venue": ')+10:d.find('"}')]
                emptydict={}
                emptydict['author']=fauthor
                emptydict['text']=ftext
                emptydict['date']=fdate
                emptydict['title']=ftitle
                emptydict['paper_id']=fpaperid
                emptydict['venue']=fvenue
                #emptydict=str(emptydict)
                dictlist.append(emptydict)
                #l.append(i)
            except:
                l.append(i)

    #dictlist[1]
    from collections import Counter

    df=pd.DataFrame(columns=['paper_id','text','date','title','author','venue','wordcount'])

    df['total_words']=0

    #df['text']=df['text'].replace('\\\\"','"')

    for i in range(0,len(dictlist)):
        text=dictlist[i]['text'].lower().replace("'"," ").replace("!"," ").replace("?"," ").replace(","," ").replace(":"," ").replace(";"," ").replace("   "," ").replace("  "," ").replace('\\\\"','"')
        words =text.split()
        wordcount = Counter(words)
        df = df.append({"paper_id":dictlist[i]['paper_id'],
        "text": text,
        "date":dictlist[i]['date'],"title":dictlist[i]['title'],"author":dictlist[i]['author'],"venue":dictlist[i]['venue'],"wordcount":wordcount}, ignore_index=True)

    for i in range(0,len(df)):
        #df['text'].iloc[i]=df['text'].iloc[i].replace('\\\\"','"')
        #df['text'].iloc[i]=df['text'].iloc[i].replace("'"," ").replace("!"," ").replace("?"," ").replace(","," ").replace(":"," ").replace(";"," ").replace("   "," ").replace("  "," ")
        #df['text'].iloc[i]=df['text'].iloc[i].lower()
        df['total_words'].iloc[i]=len(df['text'].iloc[i].split(" "))
        try:
            if df['date'].iloc[i].find("null") != -1:
                df['date'].iloc[i]="null"
            else:
                continue
        except:
            df['date'].iloc[i]="null"
    return(df)

