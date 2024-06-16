from clean_bmwi_request import clean_bmwi_request
from sql_request import start_orbis_request,start_amadeus_request
import pandas as pd
from filter_wrong_companies import create_amadeus_filtered,create_orbis_filtered,filter_game_ev_members
from build_ids import create_amadeus_id_csv,create_orbis_id_csv,create_all_id_csv
from id_sql_requests import fetch_all
from append_treatment_to_data import append_treatment_to_sql_data
from split_test_and_control_sets import create_amadeus_control_csv,create_orbis_control_csv
from load_config import orbis_backup,amadeus_backup,orbis_subsidized,amadeus_subsidized,amadeus_not_subsidized,orbis_not_subsidized,orbis_subsidized_filtered,amadeus_subsidized_filtered,orbis_game_ev_filtered,orbis_not_subsidized_ids,amadeus_not_subsidized_ids,orbis_subsidized_ids,amadeus_subsidized_ids
from datahandling.change_directory import chdir_data



def bmwi_workflow():
    bmwi_request=clean_bmwi_request()


def test_variables_workflow(create_id_csv=True,get_data=True):
    if create_id_csv:
        gaming_company_names_subsidized=pd.read_csv("bmwi_request.csv")["Zuwendungsempfänger"].to_list()[:5]
        #gaming_company_names_subsidized=replace_umlaut(gaming_company_names_subsidized)
        # start_orbis_request(gaming_company_names_subsidized,orbis_backup,orbis_subsidized)
        #start_amadeus_request(gaming_company_names_subsidized,amadeus_backup,amadeus_subsidized)
        create_orbis_filtered()
        create_amadeus_filtered()
        create_orbis_id_csv(orbis_subsidized_filtered,orbis_subsidized_ids)
        create_amadeus_id_csv(amadeus_subsidized_filtered,amadeus_subsidized_ids)
    
 
#data_merge?
#control_variables:

def control_variables_workflow(reset=False):
    chdir_data()
    game_ev_members=pd.read_csv("game_ev_members.csv")["name"]
    if reset==True:
        None
        #game_ev_request
    else: 
        #start_orbis_request(game_ev_members[:5],orbis_backup,orbis_not_subsidized)
        #start_amadeus_request(game_ev_members[:5],amadeus_backup,amadeus_not_subsidized)
        filter_game_ev_members()
    
    create_orbis_id_csv(orbis_not_subsidized,orbis_not_subsidized_ids)
    create_amadeus_id_csv(amadeus_not_subsidized,amadeus_not_subsidized_ids)

def complete_workflow():
    test_variables_workflow()
    control_variables_workflow()
    create_all_id_csv()
    #create_orbis_control_csv
    #crete_amadeus_control_csv import_config noch eintragen
    fetch_all(database="amadeus") #mit all_ids und treatment columns
    fetch_all(database="orbis")
    append_treatment_to_sql_data()

complete_workflow()

#like request für kontrollvariablen? Hier wissen wir ja die Rechtsform nicht, wieder für alle wiederholen?



