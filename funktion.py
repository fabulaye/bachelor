import pandas as pd
import os

os.chdir("C:/Users/Lukas/Desktop/bachelor/data")

def get_gaming_company_names():
    games_förderung_df=pd.read_excel("Games_Förderung_df.xlsx")
    gaming_company_names=tuple(games_förderung_df["name"]+games_förderung_df["rechtsform"])
    print(gaming_company_names)
    return gaming_company_names

get_gaming_company_names()