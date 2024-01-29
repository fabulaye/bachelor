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
    gaming_company_names=games_förderung_df["name"]+games_förderung_df["rechtsform"]
    gaming_company_names=tuple(gaming_company_names.dropna())
    print(gaming_company_names)
    return gaming_company_names

gaming_company_names=get_gaming_company_names()
#gaming_company_names_tuple=tuple(map(lambda x: x.upper(),gaming_company_names))



def delete_haftungsbeschränkt():
    list=[]
    haftungsbeschränkt_regex=re.compile("(haftungsbeschränkt)")
    for name in gaming_company_names:
        search=haftungsbeschränkt_regex.findall(name)
        if len(haftungsbeschränkt_regex.findall(name))>=1:
            list.append(name[:-21])
        else:
            list.append(name)
    return list

gaming_company_names_without_haftung=delete_haftungsbeschränkt()
print(gaming_company_names_without_haftung)  