from datahandling.change_directory import chdir_data
import pandas as pd
import datetime


chdir_data()
def strip_moby(id_string):
    id=id_string.lstrip("Moby ID: ")
    try:
        id=int(id)
    except: 
        None
    return id
games_data_steam=pd.read_csv("games_data_steam.csv",index_col=False)
games_data_steam["moby_id"]=games_data_steam["moby_id"].apply(lambda x: strip_moby(x))
games_data_mobygames=pd.read_csv("games_data.csv")
games_data_mobygames["moby_id"]=games_data_mobygames["moby_id"].apply(lambda x: strip_moby(x))

merged_df=games_data_mobygames.merge(games_data_steam,how="left",on="moby_id")

def get_year(date,date_formats=("%d.%m.%Y")):
    for format in date_formats:
        try:
            date=str(date)
            date=datetime.datetime.strptime(date,format)
            year=date.year
            year=int(year)
            return year
        except:
            continue

merged_df["year"]=merged_df["release_date"].apply(lambda x: get_year(x,("%B %d, %Y","%Y")))

merged_df.to_csv("games_data_mobygames_steam_merged.csv",index=False)



