import pandas as pd
import os

os.chdir(r"C:\Users\lukas\Desktop\bachelor\data\scraped")
orbis_financials=pd.read_csv("games_data_mobygames_steam_merged.csv")
orbis_financials.to_excel("games_data_mobygames_steam_merged.xlsx")
