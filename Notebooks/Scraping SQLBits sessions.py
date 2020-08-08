#!/usr/bin/env python
# coding: utf-8

# Scraping from SQLBits

# In[279]:


from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import json
import pyodbc
import unicodedata


# Connect to a SQLServer Database

# In[280]:


server = 'sqlgla.database.windows.net'
database = 'sqlgla'
username = 'sqlgla'
password = 'Password1234!'
driver= '{SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
cursor2 = cnxn.cursor()


# Connect to the SQLBits website. 

# In[281]:


my_url = 'https://sqlbits.com/information/publicsessions' 
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()


# In[282]:


page_soup = soup(page_html, 'html.parser')


# In[283]:


bitsSessions = page_soup.findAll("div", attrs={"class":"panel"})


# Find the speakers name:

# In[284]:


speaker = bitsSessions[0].findAll("div", attrs={"class":"col-sm-3"})[0].a['href'].replace("../speakers/","").replace("_"," ").strip()
speakerLink = bitsSessions[0].findAll("div", attrs={"class":"col-sm-3"})[0].a['href'].replace("..","https://sqlbits.com").strip()
print(speakerLink)


# Find the session topic and level

# In[285]:


topic = bitsSessions[0].findAll("div", attrs={"class":"col-sm-3"})[1].text.strip()
print(topic)


# Find the session abstract:

# In[286]:


abstract = bitsSessions[0].findAll("div", attrs={"class":"panel-body"})[0].text.strip()
print(abstract)


# Find the title of the session:

# In[287]:


title = bitsSessions[0].findAll("div", attrs={"class":"col-sm-6"})[0].text.strip()
print(title)


# In[288]:


link = bitsSessions[0].findAll("div", attrs={"class":"col-sm-6"})[0].a['href'].replace("..","https://sqlbits.com").strip()
print(link)


# In[289]:


uClient = uReq(link)
page_html = uClient.read()
uClient.close()
abstractHTML = soup(page_html, 'html.parser')


# In[290]:


abstractText = abstractHTML.findAll("div", attrs={"class":"row"})


# In[291]:


abstractTagList = abstractHTML.findAll("div", attrs={"id":"TagList"})


# In[292]:


abstractTags = abstractTagList[0].findAll("a")


# In[293]:


abstractTags


# In[294]:


link


# In[295]:


import string 
def cleanString(strr):
    strr = unicodedata.normalize("NFKD", strr)
    strr = strr.replace('\r\n',' ')
    strr = strr.replace('\n',' ')
    strr = strr.replace('\r',' ')
    strr = strr.replace('\t',' ')
    strr = strr.replace('             ',' ')
    strr = strr.replace('  ','')
    strr = strr.replace('’','')
    strr = strr.replace('Well be voting to see where we go at each step and see what happens',' ')
           
    strr = strr.replace('                              ',' ')
    ''
    strr = strr.translate(str.maketrans('', '', string.punctuation))
    return strr


# In[296]:


abstractFull = abstractText[0].findAll("div", attrs={"class":"row"})[0].text.strip()
cleanString(abstractFull)


# In[297]:


for tag in abstractTags:
    tagg = tag.text.strip() 
    print(cleanString(tagg))


# In[298]:


abstractTags[0]


# Well that does sound interesting William!
# 
# But lets go a bit deeper. Lets look at all the sessions which went in to SQLBits in 2018.
# 
# In python we can use len to find the length of a list. 

# In[299]:


y = len(bitsSessions)


# In[300]:


speakerLink = 'https://sqlbits.com/speakers/Simon_Whiteley'
uClient = uReq(speakerLink)
page_html = uClient.read()
uClient.close()
speakerHTML = soup(page_html, 'html.parser')


# In[301]:


sessionList = speakerHTML.findAll("div", attrs={"class":"row"})[2].findAll("div", attrs={"class":"col-sm-12"})
output = []
for sl in sessionList:
    if sl.text.strip() not in output:
        output.append(sl.text.strip())
len(output)


# In[302]:


a[4]


# In[303]:


len()


# In[304]:


len(speakerHTML.findAll("div", attrs={"class":"row"})[3].findAll("div", attrs={"class":"item"}))


# In[305]:


for x in range(0, y):
    title = bitsSessions[x].findAll("div", attrs={"class":"col-sm-6"})[0].text.strip()
    abstract = bitsSessions[x].findAll("div", attrs={"class":"panel-body"})[0].text.strip()
    speaker = bitsSessions[x].findAll("div", attrs={"class":"col-sm-3"})[0].a['href'].replace("../speakers/","").replace("_"," ").strip()
    speakerLink = bitsSessions[x].findAll("div", attrs={"class":"col-sm-3"})[0].a['href'].replace("..","https://sqlbits.com").strip()
    topic = bitsSessions[x].findAll("div", attrs={"class":"col-sm-3"})[1].text.strip()
    link = bitsSessions[x].findAll("div", attrs={"class":"col-sm-6"})[0].a['href'].replace("..","https://sqlbits.com").strip()
    uClient = uReq(link)
    page_html = uClient.read()
    uClient.close()
    abstractHTML = soup(page_html, 'html.parser')
    abstractText = abstractHTML.findAll("div", attrs={"class":"row"})
    abstractTagList = abstractHTML.findAll("div", attrs={"id":"TagList"})
    abstractTags = abstractTagList[0].findAll("a")
    abstractFull = abstractText[0].findAll("div", attrs={"class":"row"})[0].text.strip()
    uClient = uReq(speakerLink)
    page_html = uClient.read()
    uClient.close()
    speakerHTML = soup(page_html, 'html.parser')
    sessionList = speakerHTML.findAll("div", attrs={"class":"row"})[2].findAll("div", attrs={"class":"col-sm-12"})
    output = []
    for sl in sessionList:
        if sl.text.strip() not in output:
            output.append(sl.text.strip())
    sub = len(output)
    sel = len(speakerHTML.findAll("div", attrs={"class":"row"})[3].findAll("div", attrs={"class":"item"}))
    print(y - x)
    
    cursor = cnxn.cursor()
    cursor.execute('INSERT INTO dbo.sqlbitssessions2 (SessionId, Title, Speaker, Topic, Abstract, AbstractFull,NumberOfSessionsSubmitted, NumberOfSessionsSelected) VALUES (?,?,?,?,?,?,?,?)',(x,title,speaker,topic,abstract, abstractFull, sub, sel))
    cnxn.commit()
    for tag in abstractTags:
        tagg = cleanString(tag.text.strip())
        #print(tagg)
        cursor = cnxn.cursor()
        cursor.execute('INSERT INTO dbo.sqlbitssessionstags (SessionId, Tag) VALUES (?,?)',(x,tagg))
        cnxn.commit()


    


# In[ ]:





# In[ ]:




