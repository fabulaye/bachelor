import pandas as pd
import os
from cleaning.return_rechtsform import return_rechtsform
import sys
#sys.path.append(r'E:\virtual_environments\gaming_venv\Lib\site-packages\wrds')

from cleaning.my_strip import my_rstrip
#from lukasdata.cleaning.my_strip import my_rstrip
from cleaning.my_strip import my_rstrip
import regex as re
from datahandling.change_directory import chdir_data

def delete_equal(query):
    column_names=query.columns
    def lstrip_equal(string):
        if isinstance(string,str):
            string=string.lstrip("=")
            string=my_rstrip(string,".1\"")
            #string=string.rstrip(".1\"")
            string=string.strip("\"")
            return string
        else:
            return string
    for column_name in column_names:
        query[column_name]=query[column_name].map(lstrip_equal)
        stripped_column_name=lstrip_equal(column_name)
        query.rename(columns={column_name:stripped_column_name},inplace=True)
    return query



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


def clean_bmwi_request(path=None):
    chdir_data()
    if path!=None:
        os.chdir(path)
    query=pd.read_csv("Suchliste_utf8.csv",delimiter=";",encoding="utf-8")
    delete_equal(query)
    column_indeces=[5,6,7,8,9,17,20,21,22]
    my_df=query.iloc[:,column_indeces]
    my_df=split_name_and_rechtsform(my_df)
    my_df["project_id"]=range(len(my_df))
    print(my_df)
    my_df=my_df[my_df["Zuwendungsempfänger"]!="Keine Anzeige aufgrund datenschutzrechtlicher Regelungen."]
    my_df.to_csv("bmwi_request.csv",index=False)








