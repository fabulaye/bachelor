import pandas as pd
from datahandling.change_directory import chdir_data
from datetime import datetime
from exploration.count_nans import count_nan

date_formats=["%B %d, %Y","%Y"]

def format_european_date(date):
    for format in date_formats:
        try:
            date_obj = datetime.strptime(date, format)
            year=date_obj.year
            return year
        except ValueError:
            continue

chdir_data()
games_data=pd.read_csv("games_data.csv")

def format_moby_id(df):
    df["moby_id"]=df["moby_id"].apply(lambda x: x.lstrip("Moby ID: "))
    return df

def format_date(df):
    df["release_date"]=df["release_date"].apply(lambda x: format_european_date(x))
    return df

games_data=format_moby_id(games_data)
games_data=format_date(games_data)
games_data.to_csv("games_data.csv")


#nans=count_nan(games_data)
#print(nans)

