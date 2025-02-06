import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

log_name  = 'etl_project_log.txt'
with open(log_name, "w") as archivo:
    archivo.write("Initiated Log:\n")

url = r'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'

db_name = 'World_Economies.db'
table_name = 'Countries_by_GDP'
json_path = 'Countries_by_GDP.json'

with open(log_name, "a") as archivo:
    archivo.write("Constants Loaded:\n")

df = pd.DataFrame(columns=["Country","GDP_USD_billion."])
count = 0

html_page = requests.get(url).text


data = BeautifulSoup(html_page, 'html.parser')
with open(log_name, "a") as archivo:
    archivo.write("Request and get html data ok:\n")
tables = data.find_all('tbody')

rows = tables[2].find_all('tr')

with open(log_name, "a") as archivo:
    archivo.write("Get all Rows element as rows:\n")
#print(rows)
for row in rows:

    col = row.find_all('td')
    coltmp = row.find('a')

    print(coltmp)
    if len(col)!=0:

        countryname  = str(col[0].get_text())
        imfstr = str(col[2].contents[0])
        print(imfstr)
        print(type(imfstr))
        imfflt = imfstr.replace(",","")
        if imfflt.isdigit():
            imfflt = float(imfflt)
        else:
            imfflt = float(0)
        
        imfflt = round(imfflt/1000000,2)


        data_dict = {"Country": countryname,
                        "GDP_USD_billion.": imfflt}
        df1 = pd.DataFrame(data_dict, index=[0])
        df = pd.concat([df,df1], ignore_index=True)
        count+=1

with open(log_name, "a") as archivo:
    archivo.write("Iterate ok for all row in Rows and record required data in a dataframe:\n")


df.to_json(json_path)
with open(log_name, "a") as archivo:
    archivo.write("Export data from dataframe to a json file:\n")
conn = sqlite3.connect(db_name)
df.to_sql(table_name, conn, if_exists='replace', index=False)
conn.close()
with open(log_name, "a") as archivo:
    archivo.write("load data into a database:\n")

conn = sqlite3.connect(db_name)
sqlquery = r"SELECT * FROM " + table_name
dfout = pd.read_sql_query(sqlquery, conn)
conn.close()
print(dfout)
with open(log_name, "a") as archivo:
    archivo.write("checked data ok in db:\n")
