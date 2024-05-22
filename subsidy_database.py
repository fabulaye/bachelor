import pandas as pd
import os
from return_rechtsform import return_rechtsform
from my_strip import my_rstrip
os.chdir("C:/Users/lukas/Desktop/bachelor/data")
query=pd.read_csv("C:/Users/lukas/Desktop/bachelor/data/Suchliste_utf8.csv",delimiter=";",encoding="utf-8")


def delete_equal(query):
    column_names=query.columns
    def lstrip_equal(string):
        if isinstance(string,str):
            string=string.lstrip("=")
            string=string.rstrip(".1\"")
            string=string.strip("\"")
            return string
        else:
            return string
    for column_name in column_names:
        query[column_name]=query[column_name].map(lstrip_equal)
        stripped_column_name=lstrip_equal(column_name)
        query.rename(columns={column_name:stripped_column_name},inplace=True)
    return query

delete_equal(query)

my_df=query.loc[:,["Zuwendungsempfänger","Gemeindekennziffer","Stadt/Gemeinde","Ort","Bundesland","Laufzeit von","Laufzeit bis","Fördersumme in EUR"]]

def split_name_and_rechtsform(query):
    rechtsform_list=[]
    name_list=[]
    for name_and_rechtsform in query["Zuwendungsempfänger"]:
        rechtsform=return_rechtsform(name_and_rechtsform)
        name=my_rstrip(name_and_rechtsform,rechtsform).strip()
        rechtsform_list.append(rechtsform)
        name_list.append(name)
    query["Name"]=name_list
    query["Rechtsform"]=rechtsform_list
    return query

my_df=split_name_and_rechtsform(my_df)
print(my_df)
my_df.to_csv("bmwi_request.csv")




