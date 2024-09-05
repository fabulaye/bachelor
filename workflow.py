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
from bachelor.sql_requests.wrds_connection import start_connection
from bachelor.archived.split_game_ev_members import split_game_ev_members
from bachelor.requests.game_ev_request import game_ev_request
from bachelor.imputation.knn_imputation import impute_amadeus
from bachelor.after_request.treatment import treatment_workflow
from manipulation.my_list import list_difference
from complete_search import complete_search
from bachelor.objects_and_builders.request_builder import id_request



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
    complete_search()
    control_variables_workflow(continue_from_backup=continue_from_backup)
    chdir_data()
    all_ids_df=pd.read_csv("id/all_ids.csv")
    id_request(connection,"orbis",all_ids_df) #ist df spezifik
    id_request(connection,"amadeus",all_ids_df)
    #filtern und company objects
    #bachelor_db create tables for sql
    impute_amadeus()
    impute 
    treatment_workflow()
    estimate_earnings
    merge_mobygames_and_steam_data
    merge_game_data_and_treatment
    filter_companies_by_num_reports

    #append_treatment_to_sql_data()

#complete_workflow(continue_from_backup=True)

#like request für kontrollvariablen? Hier wissen wir ja die Rechtsform nicht, wieder für alle wiederholen?



