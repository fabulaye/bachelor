import pandas as pd
from datahandling.change_directory import chdir_data
from lukasdata.cleaning.return_rechtsform import strip_rechtsform_list,return_rechtsform,filter_companies_with_rechtsform

def split_game_ev_members():
    chdir_data()
    game_ev_members=pd.read_csv("game_ev_members.csv",index_col=False)["name"].to_list()

    game_ev_members_rechtsform,game_ev_members_no_rechtsform=filter_companies_with_rechtsform(game_ev_members)

    game_ev_members_rechtsform=pd.Series(game_ev_members_rechtsform,name="name")
    game_ev_members_rechtsform.to_csv("game_ev_members_rechtsform.csv",index=False)

    game_ev_members_no_rechtsform=pd.Series(game_ev_members_no_rechtsform,name="name")
    game_ev_members_no_rechtsform.to_csv("game_ev_members_no_rechtsform.csv",index=False)



split_game_ev_members()