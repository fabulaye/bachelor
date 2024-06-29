from manipulation.create_mask import create_in_mask
import pandas as pd
from datahandling.change_directory import chdir_data
from manipulation.my_list import upper_list,unique_list,list_difference
import numpy as np
from load_config import amadeus_subsidized_filtered,orbis_subsidized_filtered
from manipulation.create_mask import create_in_mask
chdir_data()


def create_orbis_control_csv():
    game_ev_members_orbis=pd.read_csv("game_ev_members_orbis.csv")

    #game_ev_members_orbis=upper_list(game_ev_members_orbis["name_native"])
    filtered_subsidized_orbis=upper_list(pd.read_csv(orbis_subsidized_filtered)["name_native"].to_list())
    game_ev_members_orbis["name_native"]=game_ev_members_orbis["name_native"].apply(lambda x: x.upper())

    game_ev_members_orbis_control=list_difference(game_ev_members_orbis["name_native"],filtered_subsidized_orbis)
    game_ev_members_orbis_control=unique_list(game_ev_members_orbis_control)

    mask=create_in_mask(game_ev_members_orbis["name_native"],game_ev_members_orbis_control)
    control_variables=game_ev_members_orbis[mask]
    control_variables.to_csv("control_variables_orbis.csv")


def create_amadeus_control_csv():
    game_ev_members_amadeus=pd.read_csv("game_ev_members_amadeus.csv")

    #game_ev_members_amadeus=upper_list(game_ev_members_amadeus["name_nat"].to_list())
    filtered_subsidized_orbis=upper_list(pd.read_csv(amadeus_subsidized_filtered)["name_nat"].to_list())
    game_ev_members_amadeus["name_nat"]=game_ev_members_amadeus["name_nat"].apply(lambda x: x.upper())
    
    game_ev_members_amadeus_control=list_difference(game_ev_members_amadeus["name_nat"],filtered_subsidized_orbis)
    game_ev_members_amadeus_control=unique_list(game_ev_members_amadeus_control)

    mask=create_in_mask(game_ev_members_amadeus["name_nat"],game_ev_members_amadeus_control)
    control_variables=game_ev_members_amadeus[mask]
    control_variables.to_csv("control_variables_amadeus.csv") 