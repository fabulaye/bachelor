import pandas as pd
import wrds
from orbis_amadeus_request import orbis_request,amadeus_request
import os

games_dataset=pd.read_csv("C:/Users/lukas/Desktop/bachelor/data/games.csv")
developers=games_dataset["Developers"]

def replace_quotes(iterable):
    list=[]
    for string in iterable:
        string=str(string)
        list.append(string.replace("\'",""))
    tuples=tuple(list)
    return tuples


developers=developers.drop_duplicates().to_list()
developers=replace_quotes(developers)
developers_tuple=tuple(developers)

publishers=games_dataset["Publishers"]
publishers=publishers.drop_duplicates()

def capitalize_names(company_names):
    names=[]
    for name in company_names:
        try:
            name=name.upper()
            names.append(name)
        except:
            print(name)
    names=tuple(names)
    return names

def batched_request(connection,developers,pg_descriptions_tuple,batch_len):
    developers_capitalized=capitalize_names(developers)
    length=len(developers)
    number_of_batches=int(length/batch_len)+1
    for batch in range(0,number_of_batches):
        print(batch)
        if batch==0:
            subset=developers[:batch_len]
            subset_capitalized=developers_capitalized[:batch_len]
            amadeus_request_df=amadeus_request(connection,developers_capitalized,pg_descriptions_tuple)
            orbis_request_df=orbis_request(connection,subset)
            orbis_request_df.to_excel("sql_orbis.xlsx")
            amadeus_request_df.to_excel("sql_amadeus.xlsx")
        if batch==number_of_batches:
            subset=developers[batch_len*(batch):len(developers)]
            subset_capitalized=developers_capitalized[batch_len*batch:len(developers_capitalized)]
            sql_amadeus=pd.read_excel("sql_amadeus.xlsx")
            sql_orbis=pd.read_excel("sql_orbis.xlsx")
            amadeus_request_df=amadeus_request(connection,subset_capitalized,pg_descriptions_tuple)
            orbis_request_df=orbis_request(connection,subset)
            sql_amadeus=pd.concat([sql_amadeus,amadeus_request_df])
            sql_orbis=pd.concat([sql_orbis,orbis_request_df])
            sql_orbis.to_excel("sql_orbis.xlsx")
            sql_amadeus.to_excel("sql_amadeus.xlsx")     
        else:
            subset=developers[batch_len*(batch):batch_len*(batch+1)]
            subset_capitalized=developers_capitalized[batch_len*(batch):batch_len*(batch+1)]
            sql_amadeus=pd.read_excel("sql_amadeus.xlsx")
            sql_orbis=pd.read_excel("sql_orbis.xlsx")
            amadeus_request_df=amadeus_request(connection,subset_capitalized,pg_descriptions_tuple)
            orbis_request_df=orbis_request(connection,subset)
            sql_amadeus=pd.concat([sql_amadeus,amadeus_request_df])
            sql_orbis=pd.concat([sql_orbis,orbis_request_df])
            sql_orbis.to_excel("sql_orbis.xlsx")
            sql_amadeus.to_excel("sql_amadeus.xlsx")



def batched_amadeus_request(connection,developers,pg_descriptions_tuple,batch_len):
    developers_capitalized=capitalize_names(developers)
    length=len(developers)
    number_of_batches=int(length/batch_len)+1
    for batch in range(0,number_of_batches):
        print(f"{batch}/{number_of_batches}")
        if batch==0:
            subset_capitalized=developers_capitalized[:batch_len]
            amadeus_request_df=amadeus_request(connection,developers_capitalized,pg_descriptions_tuple)
            amadeus_request_df.to_csv("sql_amadeus.csv")
        if batch==number_of_batches:
            subset_capitalized=developers_capitalized[batch_len*batch:len(developers_capitalized)]
            sql_amadeus=pd.read_csv("sql_amadeus.csv")
            amadeus_request_df=amadeus_request(connection,subset_capitalized,pg_descriptions_tuple)
            sql_amadeus=pd.concat([sql_amadeus,amadeus_request_df],ignore_index=True)
            sql_amadeus.to_csv("sql_amadeus.csv")     
        else:
            subset_capitalized=developers_capitalized[batch_len*(batch):batch_len*(batch+1)]
            sql_amadeus=pd.read_csv("sql_amadeus.csv").iloc[:,1:]
            amadeus_request_df=amadeus_request(connection,subset_capitalized,pg_descriptions_tuple)
            sql_amadeus=pd.concat([sql_amadeus,amadeus_request_df],ignore_index=True)
            sql_amadeus.to_csv("sql_amadeus.csv")   
            
types_of_companies=("Manufacture of games and toys","Physical well-being activities","Business and other management consultancy activities","Specialised design activities","Computer programming activities","Activities of holding companies","Other software publishing","Other professional, scientific and technical activities nec","Motion picture, video and television programme production activities","Other amusement and recreation activities","Other amusement and recreation activities","Other research and experimental development on natural sciences and engineering","Publishing of computer games","Computer consultancy activities","Engineering activities and related technical consultancy","Computer programming, consultancy and related activities")

def create_pgdesc(pg_descriptions):
    complete_descriptions=[]
    company_sizes=["(Large Companies)","(Medium Companies)","(Small Companies)","(Very Large Companies)"]
    for string in pg_descriptions:
        for company_size in company_sizes: 
            complete_string=string+" "+company_size
            complete_descriptions.append(complete_string)
    complete_descriptions.append("")
    complete_descriptions=tuple(complete_descriptions)
    return complete_descriptions
        

pg_descriptions_tuple=tuple(create_pgdesc(types_of_companies))






