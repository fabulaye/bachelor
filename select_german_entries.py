import os
import pandas as pd
def select_german_entries(dataframe):
    mask=[]
    id_series=dataframe.iloc[:,1]
    for id in id_series:
        if id.startswith("DE"):
            mask.append(True)
        else:
            mask.append(False)
    df=dataframe[mask]
    return df


os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
amadeus_publishers=pd.read_csv("publishers_amadeus.csv")
video_game_companies_steam=pd.read_csv("sql_amadeus.csv")


german_publishers=select_german_entries(amadeus_publishers)
german_publishers.to_csv("publishers_amadeus_de.csv")
german_video_game_companies_steam=select_german_entries(video_game_companies_steam)
german_video_game_companies_steam.to_csv("sql_amadeus_de.csv")

german_companies=pd.concat([german_publishers,german_video_game_companies_steam])

duplicate_mask = german_companies.duplicated(subset=["idnr"], keep=False)

german_companies=german_companies[~duplicate_mask]

german_companies.to_csv("german_companies_amadeus.csv")




