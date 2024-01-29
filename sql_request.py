import wrds
import regex as re

import pandas as pd
import os


connection=wrds.Connection(wrds_username="lukasmeyer")
connection.create_pgpass_file()


#libraries=test.list_libraries()
#amadeus_tables=test.list_tables("bvd_ama_small")

#print(amadeus_tables)

#print(variablen)

#values=test.get_table("bvd_ama_small","amadeus_s",obs=100)
#print(values)

#help(test.get_table)



def get_gaming_company_names():
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
    games_förderung_df=pd.read_excel("Games_Förderung_df.xlsx")
    gaming_company_names=games_förderung_df["name"]+games_förderung_df["rechtsform"]
    gaming_company_names=tuple(gaming_company_names.dropna())
    print(gaming_company_names)
    return gaming_company_names

gaming_company_names=get_gaming_company_names()
#gaming_company_names_tuple=tuple(map(lambda x: x.upper(),gaming_company_names))



def delete_haftungsbeschränkt(list_of_companies):
    list=[]
    haftungsbeschränkt_regex=re.compile("(haftungsbeschränkt)")
    for name in list_of_companies:
        search=haftungsbeschränkt_regex.findall(name)
        if len(haftungsbeschränkt_regex.findall(name))>=1:
            list.append(name[:-21])
        else:
            list.append(name)
    return list

gaming_company_names_without_haftung=delete_haftungsbeschränkt(gaming_company_names) 


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


gaming_company_names_cap_tuple=capitalize_names(gaming_company_names_without_haftung)
gaming_company_names_tuple=tuple(gaming_company_names_without_haftung)




#amadeus_medium=connection.list_tables("bvd_ama_medium")
#amadeus_large=connection.list_tables("bvd_ama_large")


#variables_small=connection.describe_table(library="bvd_ama_small",table="amadeus_s")
#variables_medium=


def bvd_request(tuple,bvd_size):
    if bvd_size=="small":
        library_and_table="bvd_ama_small.amadeus_s"
    if bvd_size=="medium":
        library_and_table="bvd_ama_medium.amadeus_m"
    if bvd_size=="large":
        library_and_table="bvd_ama_large.amadeus_l"    
    #verylarge fehlt
        


    sql=connection.raw_sql(f"SELECT * FROM {library_and_table} WHERE cntrycde='DE' AND name IN {tuple}")
    sql.to_excel("sql_request.xlsx")

    whole_df=pd.concat([sql_small,sql_medium,sql_large]) #WIP
    whole_df.to_excel("complete_sql.xlsx")

    return sql


tables=connection.list_tables("bvd_orbis_large")
#print(tables)




def orbis_request():
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
    #large
    "bvd_orbis_medium."
    #small
    sql_orbis_large=connection.raw_sql(f"SELECT * FROM bvd_orbis_large.ob_w_company_id_table_l WHERE ctryiso='DE' AND name_native in {gaming_company_names_tuple}")
    sql_orbis_small=connection.raw_sql(f"SELECT * FROM bvd_orbis_small.ob_w_company_id_table_s WHERE ctryiso='DE' AND name_native in {gaming_company_names_tuple}")
    sql_orbis_medium=connection.raw_sql(f"SELECT * FROM bvd_orbis_medium.ob_w_company_id_table_m WHERE ctryiso='DE' AND name_native in {gaming_company_names_tuple}")
    full_df=pd.concat([sql_orbis_large,sql_orbis_small,sql_orbis_medium])
    
    full_df.to_excel("sql_orbis.xlsx")
    print(full_df)
    return full_df

print(gaming_company_names_tuple)
orbis=orbis_request()

def find_missing_amadeus():
    missing_list=[]
    for name in gaming_company_names_tuple_cap:
        if name not in whole_df["name_nat"]:
            missing_list.append(name)
    return missing_list

def find_missing_orbis():
    missing_list=[]
    for name in gaming_company_names_tuple:
        if name not in orbis["name_native"]:
            missing_list.append(name)
    return missing_list



missing_entries=find_missing_orbis()
#print("missing_entries:",missing_entries)


connection.close()

def create_bvd_id_df():
    amadeus=pd.read_excel("full_sql.xslx")
    orbis=pd.read_excel("sql_orbis.xlsx")
    df=pd.concat([amadeus.loc["name_nat","idnr"]])
    #mergen


#checken welche fehlen
#bvd index raussuchen 
#data tabelle aufstellen


