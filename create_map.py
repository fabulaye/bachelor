import pandas as pd
from bs4 import BeautifulSoup
import os
from datahandling.change_directory import chdir_data

map_df=pd.DataFrame()

#variable name mit description tabelle für die sets und dann chatgpt fragen oder selber script schreiben 
from processing.my_list import list_to_string


def txt_to_str(path):
  with open(path,"r",encoding="utf-8") as f:
      text=f.readlines()
  text=list_to_string(text)
  return text


amadeus_dir=r"C:\Users\lukas\Desktop\bachelor\data\wrds_htmls\amadeus"
orbis_dir=r"C:\Users\lukas\Desktop\bachelor\data\wrds_htmls\orbis\financials"

def extract_table_data(directory):
    data_list=[]
    os.chdir(directory)
    for file in os.listdir(directory):
        html=txt_to_str(file)
        soup=BeautifulSoup(html)

        tables=soup.find_all("table")
        data_table=tables[1]

        rows = data_table.find_all('tr')

        for row in rows:
            columns = row.find_all('td')
            data = [column.text.strip() for column in columns]
            data_list.append(data)

    df=pd.DataFrame(data_list,columns=["name","type","length","description"])    
    return df

amadeus_df=extract_table_data(amadeus_dir).iloc[1:,].apply(lambda x: x.str.lower()) #.drop_duplicates(subset=["name"],inplace=True)
orbis_df=extract_table_data(orbis_dir).apply(lambda x: x.str.lower())#.drop_duplicates(subset=["name"],inplace=True)

complete_df=pd.concat([amadeus_df,orbis_df])[["name","description"]].drop_duplicates(subset=["name"])
chdir_data()
complete_df.to_csv("map.csv")






