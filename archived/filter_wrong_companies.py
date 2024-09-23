import pandas as pd
import os
import numpy as np
from manipulation.create_mask import create_in_mask
from bachelor.archived.load_config import amadeus_not_subsidized,amadeus_subsidized_filtered,orbis_subsidized,amadeus_subsidized,orbis_subsidized_filtered,amadeus_game_ev_filtered,orbis_game_ev_filtered,orbis_not_subsidized,amadeus_not_subsidized_ids,orbis_not_subsidized_ids
from datahandling.change_directory import chdir_data


def filter_correct_companies_amadeus(amadeus_request,bmwi_request):
    chdir_data()
    names=[]
    for index_amadeus,company in enumerate(amadeus_request["name_nat"]):
        for index_bmwi,company_name_bmwi in enumerate(bmwi_request["Zuwendungsempfänger"]):
            if company_name_bmwi.upper()==company:
                try:
                    bmwi_ort=bmwi_request["Ort"].loc[index_bmwi].upper()
                    #amadeus_ort_small=amadeus_request["city_nat"].loc[index_amadeus]
                    amadeus_ort=amadeus_request["city_nat"].loc[index_amadeus].upper()
                    if bmwi_ort==amadeus_ort:
                        names.append(company)
                except AttributeError:
                    print("Nan")
    names=list(np.unique(np.array(names)))
    return names

def filter_correct_companies_orbis(orbis_request,bmwi_request):
    chdir_data()
    names=[]
    for index_orbis,company in enumerate(orbis_request["name_native"]):
        for index_bmwi,company_name_bmwi in enumerate(bmwi_request["Zuwendungsempfänger"]):
            if company_name_bmwi.upper()==company.upper():
                try:
                    bmwi_ort=bmwi_request["Ort"].loc[index_bmwi].upper()
                    #amadeus_ort_small=amadeus_request["city_nat"].loc[index_amadeus]
                    orbis_ort=orbis_request["city_native"].loc[index_orbis].upper()
                    if bmwi_ort==orbis_ort:
                        names.append(company)
                except AttributeError:
                    print("Nan")
    names=list(np.unique(np.array(names)))
    return names

def build_german_mask(df): #returned nicht ne mask sondern ein df
    column_names=df.columns
    if "bvdid" in column_names:
        id="bvdid"
    if "idnr" in column_names:
        id="idnr"
    mask=[]
    id_series=df[id]
    for id_nr in id_series:
        if id_nr.startswith("DE"):
            mask.append(True)
        else:
            mask.append(False)
    return mask

def filter_game_ev_members():
    orbis_df=pd.read_csv(orbis_not_subsidized)
    amadeus_df=pd.read_csv(amadeus_not_subsidized) #eigentlich können wir not subsidized noch nicht importieren wir müssen subsidized importieren
    german_mask_orbis=build_german_mask(orbis_df)
    german_mask_amadeus=build_german_mask(amadeus_df)
    print(german_mask_orbis)
    print(german_mask_amadeus)
    filtered_df_orbis=orbis_df[german_mask_orbis]
    filtered_df_amadeus=amadeus_df[german_mask_amadeus]
    filtered_df_orbis.to_csv(orbis_game_ev_filtered)
    filtered_df_amadeus.to_csv(amadeus_game_ev_filtered)
    return filtered_df_orbis,filtered_df_amadeus

def create_orbis_filtered():
    orbis_request=pd.read_csv(orbis_subsidized)
    bmwi_request=pd.read_csv("bmwi_request.csv")
    names=filter_correct_companies_orbis(orbis_request,bmwi_request)
    filtered_orbis=orbis_request[create_in_mask(orbis_request["name_native"],names)]
    filtered_orbis.to_csv(orbis_subsidized_filtered)

def create_amadeus_filtered():
    amadeus_request=pd.read_csv(amadeus_subsidized)
    bmwi_request=pd.read_csv("bmwi_request.csv")
    names=filter_correct_companies_amadeus(amadeus_request,bmwi_request)
    amadeus_orbis=amadeus_request[create_in_mask(amadeus_request["name_nat"],names)]
    amadeus_orbis.to_csv(amadeus_subsidized_filtered)
