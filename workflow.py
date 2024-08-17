from bachelor.requests.clean_bmwi_request import clean_bmwi_request
from bachelor.requests.sql_request import start_orbis_request,start_amadeus_request
import pandas as pd
from bachelor.requests.filter_wrong_companies import create_amadeus_filtered,create_orbis_filtered,filter_game_ev_members
from bachelor.requests.build_ids import create_amadeus_id_csv,create_orbis_id_csv,create_all_id_csv,combine_ids_unique
from bachelor.requests.id_sql_requests import fetch_all
from append_treatment_to_data import append_treatment_to_sql_data
from split_test_and_control_sets import create_amadeus_control_csv,create_orbis_control_csv
from load_config import orbis_backup,amadeus_backup,orbis_subsidized,amadeus_subsidized,amadeus_not_subsidized,orbis_not_subsidized,orbis_subsidized_filtered,amadeus_subsidized_filtered,orbis_game_ev_filtered,amadeus_game_ev_filtered,orbis_not_subsidized_ids,amadeus_not_subsidized_ids,orbis_subsidized_ids,amadeus_subsidized_ids
from datahandling.change_directory import chdir_data
from wrds_connection import start_connection
from split_game_ev_members import split_game_ev_members
from bachelor.requests.game_ev_request import game_ev_request
from bachelor.imputation.knn_imputation import impute_amadeus
from bachelor.after_request.treatment import treatment_workflow
from manipulation.my_list import list_difference



connection=start_connection()

def bmwi_workflow():
    clean_bmwi_request()

def game_ev_workflow(html_request=False,continue_from_backup=False,exact_search=True,like_search=True):
    if html_request==True:
        game_ev_request()
    split_game_ev_members()
    game_ev_members_rechtsform=pd.read_csv("game_ev_members_rechtsform.csv")["name"]
    if exact_search==True:
        start_orbis_request(game_ev_members_rechtsform,"game_ev_members_rechtsform_orbis_backup.csv","game_ev_members_orbis.csv",connection,continue_from_backup=continue_from_backup) 
        start_amadeus_request(game_ev_members_rechtsform,"game_ev_members_rechtsform_amadeus_backup.csv","game_ev_members_amadeus.csv",connection,continue_from_backup=continue_from_backup,skip_df_name="game_ev_members_rechtsform_orbis_backup.csv")
    game_ev_members_no_rechtsform=pd.read_csv("game_ev_members_no_rechtsform.csv")["name"]
    if like_search==True:
        start_orbis_request(game_ev_members_no_rechtsform,"game_ev_members_no_rechtsform_orbis_backup.csv","game_ev_members_orbis_no_rechtsform.csv",connection,"like",continue_from_backup=continue_from_backup) 
        start_amadeus_request(game_ev_members_no_rechtsform,"game_ev_members_no_rechtsform_amadeus_backup.csv","game_ev_members_amadeus.csv_no_rechtsform",connection,"like",continue_from_backup=continue_from_backup,skip_df_name="game_ev_members_no_rechtsform_amadeus_backup.csv")
    #haftungsbeschränkt fehlt

class search_list(list):
    def __init__(self,*kwargs):
        super().__init__(args)
        for key,value in kwargs.items():
            if key=="filename":
                self.filename=value
    def to_csv(self):
        list_series=pd.Series(self).to_csv(self.filename)
    def append_from_csv(self,filename):
        df=pd.read_csv(filename)
        try:
            names=list(df["name_native"])
        except:
            names=list(df["name_nat"])
        self.append(names)

def test_variables_workflow(create_id_csv=True,get_data=True,exact_search=True,like_search=True,complete_search=False):
    #catch_all_names: 1. exact_search,2. create_diff_list,3. like_search_with_diff_list
    if create_id_csv:
        gaming_company_names_subsidized=pd.read_csv("bmwi_request.csv")["Zuwendungsempfänger"].to_list()
        #gaming_company_names_subsidized=replace_umlaut(gaming_company_names_subsidized)
        os.chdir("C:/Users/lukas/Desktop/bachelor/data/complete_search")
        if complete_search:
            found=search_list()
            not_found=search_list(gaming_company_names_subsidized)
            
            start_orbis_request(gaming_company_names_subsidized,orbis_backup,"orbis_exact_search_incomplete",connection)
            found.append_from_csv("orbis_exact_search_incomplete.csv")
            not_found=list_difference(not_found,found)

            start_amadeus_request(not_found,amadeus_backup,"amadeus_exact_search_incomplete",connection,continue_from_backup=False)
            found.append_from_csv("amadeus_exact_search_incomplete.csv")
            not_found=list_difference(not_found,found)

            start_orbis_request(not_found,orbis_backup,"like_request_orbis_subsidized",connection,request_type="like",skip_df_name=orbis_subsidized)
            found.append_from_csv("like_request_orbis_subsidized.csv")
            not_found=list_difference(not_found,found)

            start_amadeus_request(not_found,amadeus_backup,"like_request_amadeus_subsidized",connection,request_type="like",skip_df_name=orbis_subsidized)
            found.append_from_csv("like_request_amadeus_subsidized.csv")
            not_found=list_difference(not_found,found)

        elif exact_search==True:
            start_orbis_request(gaming_company_names_subsidized,orbis_backup,orbis_subsidized,connection)
            start_amadeus_request(gaming_company_names_subsidized,amadeus_backup,amadeus_subsidized,connection,continue_from_backup=True)
        elif like_search==True:
            start_orbis_request(gaming_company_names_subsidized,orbis_backup,"like_request_orbis_subsidized",connection,request_type="like",skip_df_name=orbis_subsidized)
            start_amadeus_request(gaming_company_names_subsidized,amadeus_backup,"like_request_orbis_subsidized",connection,request_type="like",skip_df_name=orbis_subsidized)
            #checken welche nicht drin sind und dann like request machen
        
        create_orbis_filtered()
        create_amadeus_filtered()
        create_orbis_id_csv(orbis_subsidized_filtered,orbis_subsidized_ids)
        create_amadeus_id_csv(amadeus_subsidized_filtered,amadeus_subsidized_ids)
        

 
#data_merge?
#control_variables:
import os

def control_variables_workflow(continue_from_backup=False,reset=False,):
    chdir_data()
    game_ev_members=pd.read_csv("game_ev_members.csv")["name"]
    if reset==True:
        None
        #game_ev_request
    else: 
        game_ev_workflow(exact_search=False,like_search=False,continue_from_backup=continue_from_backup)
        create_orbis_control_csv()
        create_amadeus_control_csv()
        filter_game_ev_members()
        create_amadeus_control_csv()
        create_orbis_control_csv()
        create_amadeus_id_csv("control_variables_amadeus.csv","amadeus_control_ids.csv")
        create_orbis_id_csv("control_variables_orbis.csv","orbis_control_ids.csv")
        control_ids=combine_ids_unique("amadeus_control_ids.csv","orbis_control_ids.csv")
        control_ids.to_csv("all_not_subsidized_ids.csv")
       
    
    create_orbis_id_csv(orbis_not_subsidized,orbis_not_subsidized_ids)
    create_amadeus_id_csv(amadeus_not_subsidized,amadeus_not_subsidized_ids)

def complete_workflow(continue_from_backup=True):
    bmwi_workflow()
    test_variables_workflow(exact_search=False,like_search=False)
    complete_search
    control_variables_workflow(continue_from_backup=continue_from_backup)
    create_all_id_csv()
    chdir_data()
    all_ids_df=pd.read_csv("id/all_ids.csv")
    fetch_all(connection,database="amadeus",id_df=all_ids_df) #mit all_ids und treatment columns
    fetch_all(connection,database="orbis",id_df=all_ids_df)
    impute_amadeus()
    treatment_workflow()
    estimate_earnings
    merge_mobygames_and_steam_data
    merge_game_data_and_treatment
    filter_companies_by_num_reports

    #append_treatment_to_sql_data()

#complete_workflow(continue_from_backup=True)

#like request für kontrollvariablen? Hier wissen wir ja die Rechtsform nicht, wieder für alle wiederholen?



