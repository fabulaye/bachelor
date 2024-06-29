import wrds
import regex as re
import pandas as pd
import os
from orbis_amadeus_request import amadeus_request,orbis_request,orbis_exact_request,orbis_combination_request,amadeus_exact_request
from datahandling.json_to_dict import json_to_dict
from manipulation.my_list import upper_list
from datahandling.change_directory import chdir_data
from load_config import orbis_backup,amadeus_backup,orbis_subsidized,amadeus_subsidized,amadeus_not_subsidized,orbis_not_subsidized
from manipulation.create_mask import create_in_mask
import numpy as np


chdir_data()


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
    
from build_ids import combine_ids_unique
#
def create_in_mask(iterable1, iterable2, case_sensitive=True):

    if not case_sensitive:
        if isinstance(iterable1, pd.Series):
            iterable1 = iterable1.str.lower()
        else:
            iterable1 = [str(i).lower() for i in iterable1]
        
        if isinstance(iterable2, pd.Series):
            iterable2 = iterable2.str.lower()
        else:
            iterable2 = [str(i).lower() for i in iterable2]
    else:
        if not isinstance(iterable1, pd.Series):
            iterable1 = [str(i) for i in iterable1]
        
        if not isinstance(iterable2, pd.Series):
            iterable2 = [str(i) for i in iterable2]
    mask = [element in iterable2 for element in iterable1]
    return mask

import csv

def start_orbis_request(gaming_company_names,backup_name,output_file_name,connection,request_type="exact",continue_from_backup=False,skip_df_name=None,*args):
    chdir_data()
    if continue_from_backup:
        try:
            orbis_save=pd.read_csv(backup_name)["name_native"].to_list()
            orbis_save=upper_list(orbis_save)
            gaming_company_names=gaming_company_names.to_list()
            gaming_company_names=upper_list(gaming_company_names)
            print(gaming_company_names)
            gaming_company_names=continue_with_list(gaming_company_names,orbis_save)
        except FileNotFoundError:
            #with open(backup_name,mode="w") as file:
                #writer = csv.DictWriter(file, fieldnames=["name_native"])
                #writer.writeheader()
            #orbis_save=pd.read_csv(backup_name)["name_native"].to_list()
            pass
    if skip_df_name!=None:
        skip_df=pd.read_csv(skip_df_name)
        mask=create_in_mask(gaming_company_names,skip_df["name_nat"],case_sensitive=False) #wir nehmen die namen vom anderen dataset 
        reverse_mask=[not x for x in mask]
        gaming_company_names=gaming_company_names[reverse_mask]
    cap_names_tuple=tuple(capitalize_names(gaming_company_names))
    if request_type=="exact":
        orbis_request_df=orbis_exact_request(connection,cap_names_tuple,output_file_name,backup_name,continue_from_backup=continue_from_backup)
        return orbis_request_df
    if request_type=="combination":
        orbis_request_df=orbis_combination_request(connection,cap_names_tuple,backup_name,output_file_name,backup_name,continue_from_backup=continue_from_backup)
        return orbis_request_df
    if request_type=="like":
        orbis_request_df=orbis_request(connection,cap_names_tuple,backup_name,output_file_name,continue_from_backup=continue_from_backup)
        return orbis_request_df
    

def start_amadeus_request(gaming_company_names,backup_name,output_file_name,connection,request_type="exact",continue_from_backup=False,skip_df_name=None,*args):
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
    if continue_from_backup:
        amadeus_save=pd.read_csv(backup_name)["name_nat"].to_list()
        amadeus_save=upper_list(amadeus_save)
        gaming_company_names=upper_list(gaming_company_names)
        gaming_company_names=continue_with_list(gaming_company_names,amadeus_save)
    cap_names_tuple=tuple(capitalize_names(gaming_company_names))
    if skip_df_name!=None:
        skip_df=pd.read_csv(skip_df_name)
        mask=create_in_mask(gaming_company_names,skip_df["name_native"],case_sensitive=False)
        reverse_mask=[not x for x in mask]
        gaming_company_names_numpy=np.array(gaming_company_names)
        gaming_company_names=gaming_company_names_numpy[reverse_mask]
        #gaming_company_names=gaming_company_names[reverse_mask]
    if request_type=="exact":
        amadeus_request_df=amadeus_exact_request(connection,cap_names_tuple,output_file_name,backup_name,continue_from_backup=continue_from_backup)
        return amadeus_request_df
    #if request_type=="combination":
        #amadeus_request_df=amadeus_combination_request(connection,cap_names_tuple,backup_name,output_file_name)
        #amadeus_request_df.to_csv("amadeus_combination_backup.csv")
    if request_type=="like":
        amadeus_request_df=amadeus_request(connection,cap_names_tuple,output_file_name,backup_name,continue_from_backup=continue_from_backup)
        return amadeus_request_df


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



