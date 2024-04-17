import pandas as pd
from file_manager.change_directory import chdir_data

def add_subsidized_column():
    chdir_data()
    subsidized_financial_amadeus=pd.read_csv("subsidized_financial_amadeus.csv")
    not_subsidized_financial_amadeus=pd.read_csv("not_subsidized_financial_amadeus.csv")
    subsidized_financial_amadeus["subsidized"]=[1 for i in range(len(subsidized_financial_amadeus))]
    not_subsidized_financial_amadeus["subsidized"]=[0 for i in range(len(not_subsidized_financial_amadeus))]
    subsidized_financial_amadeus.to_csv("subsidized_financial_amadeus.csv")
    not_subsidized_financial_amadeus.to_csv("not_subsidized_financial_amadeus.csv")

add_subsidized_column()