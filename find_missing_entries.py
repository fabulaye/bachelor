import pandas as pd
from datahandling.change_directory import chdir_data
from upper_list import upper_list

def find_missing_amadeus(subset,amadeus_df):
    missing_list=[]
    for name in amadeus_df["name_nat"]:
        if name not in subset["name_nat"]:
            missing_list.append(name)
    return missing_list

def find_missing_orbis(subset,names_list):
    names_list=upper_list(names_list)
    missing_list=[]
    subset_list=upper_list(subset["name_native"].to_list())
    for name in names_list:
        if name not in subset_list:
            missing_list.append(name)        
    return missing_list

chdir_data()
game_ev_members_orbis=pd.read_csv("game_ev_members_orbis.csv")
game_ev_members=pd.read_csv("game_ev_members.csv")["name"]

game_ev_missing_orbis=find_missing_orbis(game_ev_members_orbis,game_ev_members)
print(game_ev_missing_orbis)


filtered_subsidized_orbis=pd.read_csv("filtered_subsidized_orbis.csv")
subsidized_names=pd.read_csv("bmwi_request.csv")["Zuwendungsempfänger"].to_list()

orbis_missing=find_missing_orbis(filtered_subsidized_orbis,subsidized_names)
orbis_missing.to_csv("orbis_missing.csv")


#viele nicht gaming unternehmen im set



