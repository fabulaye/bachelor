import wrds
import regex as re
import pandas as pd
import os
from orbis_amadeus_request import amadeus_request,orbis_request,orbis_exact_request,orbis_combination_request,amadeus_exact_request
from datahandling.json_to_dict import json_to_dict
from manipulation.my_list import upper_list
from load_config import orbis_backup,amadeus_backup,orbis_subsidized,amadeus_subsidized,amadeus_not_subsidized,orbis_not_subsidized


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


def delete_names(lst,to_be_deleted):
    for item in to_be_deleted:
        try:
             lst.remove(item)
        except:
            None
    return lst

def continue_with_list(company_names,backup):
    last_entry=backup[-1]
    company_names_index=company_names.index(last_entry)
    new_list=company_names[company_names_index:]
    return new_list
    

from cleaning.replace_umlaut import replace_umlaut

os.chdir("C:/Users/Lukas/Desktop/bachelor/data")


from return_rechtsform import strip_rechtsform_list,return_rechtsform,filter_companies_with_rechtsform
#game_ev_members=pd.read_csv("game_ev_members.csv",index_col=False)["name"].to_list()

#game_ev_members_rechtsform,game_ev_members_no_rechtsform=filter_companies_with_rechtsform(game_ev_members)
#print(game_ev_members_rechtsform)
#game_ev_members=strip_rechtsform_list(game_ev_members)

def start_orbis_request(gaming_company_names,backup_name,output_file_name,request_type="exact",continue_from_backup=False,*args):
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
    if continue_from_backup:
        orbis_save=pd.read_csv(backup_name)["name_native"].to_list()
        orbis_save=upper_list(orbis_save)
        gaming_company_names=upper_list(gaming_company_names)
        gaming_company_names=continue_with_list(gaming_company_names,orbis_save)
    cap_names_tuple=tuple(capitalize_names(gaming_company_names))
    if request_type=="exact":
        orbis_request_df=orbis_exact_request(connection,cap_names_tuple,output_file_name,backup_name)
        return orbis_request_df
    if request_type=="combination":
        orbis_request_df=orbis_combination_request(connection,cap_names_tuple,backup_name,output_file_name,backup_name)
        return orbis_request_df

def start_amadeus_request(gaming_company_names,backup_name,output_file_name,request_type="exact",continue_from_backup=False,*args):
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
    if continue_from_backup:
        amadeus_save=pd.read_csv(backup_name)["name_native"].to_list()
        amadeus_save=upper_list(amadeus_save)
        gaming_company_names=upper_list(gaming_company_names)
        gaming_company_names=continue_with_list(gaming_company_names,amadeus_save)
    cap_names_tuple=tuple(capitalize_names(gaming_company_names))
    if request_type=="exact":
        amadeus_request_df=amadeus_exact_request(connection,cap_names_tuple,output_file_name,backup_name)
        return amadeus_request_df
    #if request_type=="combination":
        #amadeus_request_df=amadeus_combination_request(connection,cap_names_tuple,backup_name,output_file_name)
        #amadeus_request_df.to_csv("amadeus_combination_backup.csv")


#orbis_missing=pd.read_csv("orbis_missing.csv")["name"]

def delete_haftungsbeschränkt(lst):
    haftungsbeschränkt_list=[]
    for item in lst:
        if item.endswith("UG (HAFTUNGSBESCHRÄNKT)"):
            item=item[:-len(" (HAFTUNGSBESCHRÄNKT)")]
            print(item)
            haftungsbeschränkt_list.append(item)
    return haftungsbeschränkt_list

#haftungsbeschränkt_orbis=delete_haftungsbeschränkt(orbis_missing)

#start_orbis_request(haftungsbeschränkt_orbis,"haftungsbeschränkt_orbis_backup.csv","exact")



