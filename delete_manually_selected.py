import pandas as pd

def delete_game_ev_members():
    new_list=[]
    game_ev_members=pd.read_csv("game_ev_members.csv")
    to_be_deleted=pd.read_csv("manual_deleted.csv").to_list()
    for member in game_ev_members["name"]:
        if member not in to_be_deleted:
            new_list.append(member)
    new_series=pd.Series(new_list,name="name")
    new_series.to_csv("manual_deleted.csv")


delete_game_ev_members()
