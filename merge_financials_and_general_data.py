

import pandas as pd
import os

os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
financials_df=pd.read_csv("sql_amadeus_financial.csv")
general_df=pd.read_csv("sql_amadeus.csv")

def merge_general_and_financial():
    new_df=pd.merge(financials_df,general_df,on="idnr")
    new_df.set_index(["closdate_year","idnr"],inplace=True)
    #new_df.to_csv("full_amadeus.csv")









