import wrds
import regex as re
import pandas as pd
import os
from orbis_request import amadeus_request,orbis_request
from file_manager.json_to_dict import json_to_dict

connection=wrds.Connection(wrds_username="lukasmeyer")

os.chdir("C:/Users/Lukas/Desktop/bachelor/data")

def rstrip_list(iterable):
    list=[]
    for string in iterable:
        string=str(string)
        list.append(string.rstrip())
    return list

def create_names_csv():
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
    games_förderung_df=pd.read_excel("Games_Förderung_df.xlsx")
    names=rstrip_list(games_förderung_df["name"])
    names=pd.DataFrame(names)
    rechtsformen=rstrip_list(games_förderung_df["rechtsform"])
    rechtsformen=delete_haftungsbeschränkt(rechtsformen)
    rechtsformen=pd.DataFrame(rechtsformen)
    df=pd.DataFrame()
    df["name"]=names
    df["rechtsform"]=rechtsformen
    df.to_csv("gaming_company_names.csv")
    return df

def get_gaming_company_names():
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
    
    names=pd.read_csv("gaming_company_names.csv")["name"]
    rechtsformen=pd.read_csv("gaming_company_names.csv")["rechtsform"]
    names=list(map(lambda x: x+" ",names))
    names=pd.Series(names)
    print(names)
    print(rechtsformen)
    gaming_company_names=names+rechtsformen
    print(gaming_company_names)
    return gaming_company_names




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


os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
gaming_company_names=get_gaming_company_names()
names_tuple=tuple(gaming_company_names)
cap_names_tuple=tuple(capitalize_names(gaming_company_names))


gaming_companies_df=amadeus_request(connection,cap_names_tuple)
gaming_companies_df.to_csv("subsidized_amadeus.csv")

orbis_request_df=orbis_request(connection,cap_names_tuple)
orbis_request_df.to_csv("subsidized_orbis.csv")


def find_missing_amadeus():
    missing_list=[]
    for name in gaming_company_names_tuple:
        if name not in bvd["name_nat"]:
            missing_list.append(name)
    df=pd.DataFrame(missing_list)
    df.to_excel("missing_companies_bvd.xlsx")
    return missing_list

def find_missing_orbis():
    missing_list=[]
    for name in gaming_company_names_tuple:
        if name not in orbis["name_native"]:
            missing_list.append(name)
    df=pd.DataFrame(missing_list)
    df.to_excel("missing_companies_orbis.xlsx")        
    return missing_list



# economic data
#mergen so das alle übernommen werden
# komplettes df erstellen

#connection.close()




#checken welche fehlen
#bvd index raussuchen   
#aus beiden quellen die indexes bündeln
#data tabelle aufstellen



