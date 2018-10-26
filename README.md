# SQLBits Dashboard

![PowerBIImage](https://github.com/SQLShark/SQLBitsDashboard/blob/master/Images/PowerBI.png)

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

There is a table and some a view required for the dashboard: 

```
CREATE TABLE dbo.sqlbitssessions
(
	Id INT NOT NULL IDENTITY, 
	Title VARCHAR(1000),
	Speaker VARCHAR(1000),
	Topic VARCHAR(1000),
	Abstract VARCHAR(8000)
)

DROP VIEW IF EXISTS dbo.sqlbits;
GO

CREATE VIEW dbo.sqlbits as
SELECT
    Id
  , Title
  , Speaker
  , UPPER(RTRIM(LEFT(Topic,3))) AS Topic
  , CONVERT(INT, RIGHT(Topic, 3)) AS Level
  , Abstract
  , LEN(Abstract) [Abstract Length]
  , LEN(Abstract) - LEN(REPLACE(Abstract, ' ', '')) +1 Words
  , CASE WHEN PATINDEX('%Kubernetes%', Abstract) > 0 THEN 1 ELSE 0 END AS [Kubernetes]
  , CASE WHEN PATINDEX('%2019%', Abstract) > 0 THEN 1 ELSE 0 END AS [2019]
  , CASE WHEN PATINDEX('%Machine Learning%', Abstract) > 0 THEN 1 ELSE 0 END AS [Machine Learning]
  , CASE WHEN PATINDEX('%Python%', Abstract) > 0 THEN 1 ELSE 0 END AS [Python]
  , CASE WHEN PATINDEX('%Databricks%', Abstract) > 0 THEN 1 ELSE 0 END AS [Databricks]
  , CASE WHEN PATINDEX('%Cosmosdb%', Abstract) > 0 THEN 1 ELSE 0 END AS [Cosmosdb]
  , CASE WHEN PATINDEX('%Graph%', Abstract) > 0 THEN 1 ELSE 0 END AS [Graph]
  , CASE WHEN PATINDEX('%Stream Analytics%', Abstract) > 0 THEN 1 ELSE 0 END AS [Stream Analytics]
  , CASE WHEN PATINDEX('%Power bi%', Abstract) > 0 THEN 1 ELSE 0 END AS [Power bi]
  , CASE WHEN PATINDEX('%Docker%', Abstract) > 0 THEN 1 ELSE 0 END AS [Docker]
  , CASE WHEN PATINDEX('%Data Lake%', Abstract) > 0 THEN 1 ELSE 0 END AS [Data Lake]
  , CASE WHEN PATINDEX('%HDInsight%', Abstract) > 0 THEN 1 ELSE 0 END AS [HDInsight]
  , CASE WHEN PATINDEX('%Spark%', Abstract) > 0 THEN 1 ELSE 0 END AS [Spark]
  , CASE WHEN PATINDEX('%Apache%', Abstract) > 0 THEN 1 ELSE 0 END AS [Apache]
  , CASE WHEN PATINDEX('%SSIS%', Abstract) > 0 THEN 1 ELSE 0 END AS [SSIS]
  , CASE WHEN PATINDEX('%SSRS%', Abstract) > 0 THEN 1 ELSE 0 END AS [SSRS]
  , CASE WHEN PATINDEX('%Master Data%', Abstract) > 0 THEN 1 ELSE 0 END AS [Master Data]
  , CASE WHEN PATINDEX('%2008%', Abstract) > 0 THEN 1 ELSE 0 END AS [2008]
  , CASE WHEN PATINDEX('%dba%', Abstract) > 0 THEN 1 ELSE 0 END AS [DBA]
  , CASE WHEN PATINDEX('%dbatools%', Abstract) > 0 THEN 1 ELSE 0 END AS [dbatools]
  , CASE WHEN PATINDEX('%powershell%', Abstract) > 0 THEN 1 ELSE 0 END AS [powershell]
FROM
    dbo.sqlbitssessions
WHERE 
	Abstract LIKE '%%'
ORDER BY 
	Speaker
;


```

Then we can use the PowerBI dashboard to point at it. 

Thanks for reading. 