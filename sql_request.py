import wrds
import regex as re
import pandas as pd
import os
from orbis_amadeus_request import amadeus_request,orbis_request,excact_name_amadeus_request
from datahandling.json_to_dict import json_to_dict


connection=wrds.Connection(wrds_username="lukasmeyer")

os.chdir("C:/Users/Lukas/Desktop/bachelor/data")


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

from replace_umlaut import replace_umlaut
os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
gaming_company_names=pd.read_csv("bmwi_request.csv")["Zuwendungsempfänger"].to_list()
gaming_company_names=replace_umlaut(gaming_company_names)
names_tuple=tuple(gaming_company_names)

cap_names_tuple=tuple(capitalize_names(gaming_company_names))
print(cap_names_tuple)

gaming_companies_df=amadeus_request(connection,cap_names_tuple)
gaming_companies_df.to_csv("subsidized_amadeus.csv")

print("amadeus done")

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



