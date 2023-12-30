import wrds
import regex as re

import pandas as pd
import os


#libraries=test.list_libraries()
#amadeus_tables=test.list_tables("bvd_ama_small")

#print(amadeus_tables)

#print(variablen)

#values=test.get_table("bvd_ama_small","amadeus_s",obs=100)
#print(values)

#help(test.get_table)

os.chdir("C:/Users/Lukas/Desktop/bachelor/data")

def get_gaming_company_names():
    games_förderung_df=pd.read_excel("Games_Förderung_df.xlsx")
    gaming_company_names=tuple(games_förderung_df["name"]+games_förderung_df["rechtsform"])
    print(gaming_company_names)
    return gaming_company_names

gaming_company_names=get_gaming_company_names()
#gaming_company_names_tuple=tuple(map(lambda x: x.upper(),gaming_company_names))

def delete_haftungsbeschränkt():
    re.

def capitalize_names():
    names=[]
    for name in gaming_company_names:
        try:
            name=name.upper()
            names.append(name)
        except:
            print(name)
    names=tuple(names)
    return names


gaming_company_names_tuple=capitalize_names()



connection=wrds.Connection(wrds_username="lukasmeyer")
connection.create_pgpass_file()


amadeus_medium=connection.list_tables("bvd_ama_medium")
amadeus_large=connection.list_tables("bvd_ama_large")

print(amadeus_medium)

print(amadeus_large)

#variables_small=connection.describe_table(library="bvd_ama_small",table="amadeus_s")
#variables_medium=


def bvd_request(tuple,bvd_size):
    if bvd_size=="small":
        library_and_table="bvd_ama_small.amadeus_s"
    if bvd_size=="medium":
        library_and_table="bvd_ama_medium.amadeus_m"
    if bvd_size=="large":
        library_and_table="bvd_ama_large.amadeus_l"    
        


    sql=connection.raw_sql(f"SELECT * FROM {library_and_table} WHERE cntrycde='DE' AND name IN {tuple}")
    sql.to_excel("sql_request.xlsx")
    return sql

sql_small=bvd_request(gaming_company_names_tuple,"small")
sql_medium=bvd_request(gaming_company_names_tuple,"medium")
print(sql_medium)
sql_large=bvd_request(gaming_company_names_tuple,"large")
print(sql_large)



def find_missing():
    missing_list=[]
    for name in gaming_company_names_tuple:
        if name not in whole_df["name_nat"]:
            missing_list.append(name)
    return missing_list



whole_df=pd.concat([sql_small,sql_medium,sql_large])
whole_df.to_excel("complete_sql.xlsx")

missing_entries=find_missing()
print(missing_entries)

connection.close()

#bvd switchen
#ich muss alle bvds durchgehen: bvd_large,medium,small,very_large
#namen liste verbessern --> 
#https://wrds-www.wharton.upenn.edu/pages/about/data-vendors/bureau-van-dijk-bvd/

