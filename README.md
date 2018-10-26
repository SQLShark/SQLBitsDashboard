# SQLBits Dashboard

Here is all the files and the Python to build a web scraper and to store the data in to a SQL Database. 

There is a Jupyter notebook with all the code for web scraping but I will list it out here too. 

In Python we first need to import a few packages: 

```
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import json
import pyodbc
```

We need BeautifulSoup (bs4) for webscraping, urllib to obtain out HTML and pyodbc for saving the data in to SQL Server. 

Then we need to create a connection to SQL Server. I am using a database in Azure. 

```
server = '<servername>.database.windows.net'
database = '<databasename>'
username = '<username>'
password = '<password>'
driver= '{ODBC Driver 13 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
```

Next we will connect to the SQLBits website, pull the details and then convert the response in to a HTML object. 

```
my_url = 'https://sqlbits.com/information/publicsessions' 
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
```

Change the HTML to a bs4 object
```
page_soup = soup(page_html, 'html.parser')
```

There is more detail in the Notebook but here is the last part which will loop over the sessions and write in to SQLServer DB. 

What we are doing is looking for sections of the HTML and then lifting the text to write out to a database. An example may be:

```
title = bitsSessions[x].findAll("div", attrs={"class":"col-sm-6"})[0].text.strip()
```

We are assigning a var called title with the contents of the elements which has the class of col-sm-6 which happens to be the title of the session. You can find this by inspecting the code via chrome or another browser. 

```
for x in range(0, y):
    title = bitsSessions[x].findAll("div", attrs={"class":"col-sm-6"})[0].text.strip()
    abstract = bitsSessions[x].findAll("div", attrs={"class":"panel-body"})[0].text.strip()
    speaker = bitsSessions[x].findAll("div", attrs={"class":"col-sm-3"})[0].a['href'].replace("../Speakers/","").replace("_"," ").strip()
    topic = bitsSessions[x].findAll("div", attrs={"class":"col-sm-3"})[1].text.strip()
    print(title)
    cursor.execute('INSERT INTO dbo.sqlbitssessions (Title, Speaker, Topic, Abstract) VALUES (?,?,?,?)',(title,speaker,topic,abstract))
cnxn.commit()
```

Then we can use the PowerBI dashboard to point at it. 

Thanks for reading. 