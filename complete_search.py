#from sql_requests.clean_bmwi_request import clean_bmwi_request
from sql_requests.sql_request import start_orbis_request
import pandas as pd
from sql_requests.filter_wrong_companies import create_amadeus_filtered,create_orbis_filtered,filter_game_ev_members
from sql_requests.build_ids import create_id_csv,create_all_id_csv,combine_ids_unique
from sql_requests.id_sql_requests import fetch_all
#from append_treatment_to_data import append_treatment_to_sql_data
from split_test_and_control_sets import create_amadeus_control_csv,create_orbis_control_csv
from load_config import orbis_backup,amadeus_backup,orbis_subsidized,amadeus_subsidized,amadeus_not_subsidized,orbis_not_subsidized,orbis_subsidized_filtered,amadeus_subsidized_filtered,orbis_game_ev_filtered,amadeus_game_ev_filtered,orbis_not_subsidized_ids,amadeus_not_subsidized_ids,orbis_subsidized_ids,amadeus_subsidized_ids
from datahandling.change_directory import chdir_data
from wrds_connection import start_connection
#from split_game_ev_members import split_game_ev_members
from sql_requests.game_ev_request import game_ev_request
from imputation.knn_imputation import impute_amadeus
#from after_request.treatment import treatment_workflow
from manipulation.my_list import list_difference
import os
from sql_requests.orbis_amadeus_request import general_request

connection=start_connection()

class search_list(list):
    def __init__(self,*args):
        super().__init__(*args)
    def to_csv(self,filename):
        pd.Series(self,name="name_nat").to_csv(filename,index=False)
    def append_from_csv(self,filename):
        df=pd.read_csv(filename)
        if len(df)>=1:
            try:
                names=list(df["name_native"])
            except:
                names=list(df["name_nat"])
            self.extend(names)

def remove_haftungsbeschränkt(names):
    new_names=[]
    names=list(names)
    for name in names:
        name=name.strip()
        name=name.rstrip(" (haftungsbeschränkt)")
        new_names.append(name)
    return new_names

os.chdir("C:/Users/lukas/Desktop/bachelor/data/complete_search")
gaming_company_names_subsidized=pd.read_csv("bmwi_request.csv")["Zuwendungsempfänger"].to_list()[:10]

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

def complete_search(names:list):
    cap_names_tuple=tuple(capitalize_names(names))
    
    def return_not_found(csv_name,found,not_found):
        found.append_from_csv(csv_name)
        difference=list_difference(not_found,found)
        not_found=search_list(difference) #does the order matter?
        found.to_csv("found.csv")
        not_found.to_csv("not_found.csv")
        return not_found
    #catch_all_names: 1. exact_search,2. create_diff_list,3. like_search_with_diff_list
    
    os.chdir("C:/Users/lukas/Desktop/bachelor/data/complete_search")

    found=search_list()
    not_found=search_list(cap_names_tuple)

    general_request(connection,"amadeus",not_found,"amadeus_exact_search_incomplete.csv",{"how":"exact","country":"de"})
    not_found=return_not_found("amadeus_exact_search_de.csv",found,not_found)
    
    general_request(connection,"orbis",not_found,"orbis_exact_search_incomplete.csv",{"how":"exact","country":"de"})
    not_found=return_not_found("orbis_exact_search_de.csv",found,not_found)
    
    general_request(connection,"amadeus",not_found,"amadeus_exact_search.csv",{"how":"exact"})
    not_found=return_not_found("amadeus_exact_search.csv",found,not_found)
    
    general_request(connection,"orbis",not_found,"orbis_exact_search.csv",{"how":"exact"})
    not_found=return_not_found("orbis_exact_search.csv",found,not_found)

    not_found=remove_haftungsbeschränkt(not_found)

    general_request(connection,"amadeus",not_found,"amadeus_like_search.csv",{"how":"like"})
    not_found=return_not_found("amadeus_exact_search.csv",found,not_found)
    
    general_request(connection,"orbis",not_found,"orbis_like_search.csv",{"how":"like"})
    not_found=return_not_found("orbis_exact_search.csv",found,not_found)

    #combine ids
    orbis_id=create_id_csv("orbis_exact_search_incomplete.csv","orbis_exact_search_incomplete_ids.csv")
    amadeus_id=create_id_csv("amadeus_exact_search_incomplete.csv","amadeus_exact_search_incomplete_ids.csv")
    #id for like amadeus
    #id for like orbis
    all_ids=pd.concat([orbis_id,amadeus_id]) #concat rest
    all_ids.to_csv("all_ids_complete_search.csv")
        
complete_search(gaming_company_names_subsidized)