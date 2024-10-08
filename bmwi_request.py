import pandas as pd
import os
#from cleaning.return_rechtsform import return_rechtsform
import sys
#sys.path.append(r'E:\virtual_environments\gaming_venv\Lib\site-packages\wrds')
from processing.format_string import my_rstrip
import regex as re
from datahandling.change_directory import chdir_data,chdir_id
from processing.rechtsform import return_rechtsform

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
    my_df=rename_bmwki(my_df)
    my_df.to_csv("bmwi_request.csv",index=False)


def rename_bmwki(df):
    bmwki_colname_map={"Zuwendungsempfänger":"name","Laufzeit von":"subsidy_start","Laufzeit bis":"subsidy_end","Fördersumme in EUR":"subsidy"}
    df.rename(columns=bmwki_colname_map,inplace=True)
    return df


def add_id_to_bmwi_data(id_filename):
    chdir_data()
    bmwi_data=pd.read_csv("bmwi_request.csv")
    chdir_id()
    ids_and_names=pd.read_csv(id_filename)
    #up both?
    #bmwi_data["Zuwendungsempfänger"]=bmwi_data["Zuwendungsempfänger"].map(lambda x:x.upper())
    bmwi_data_with_ids=pd.merge(bmwi_data,ids_and_names,left_on="name",right_on="names",how="inner")
    bmwi_data_with_ids.drop(columns="names",inplace=True)
    chdir_data() 
    bmwi_data_with_ids.to_csv("bmwi_request_with_ids.csv",index=False)










