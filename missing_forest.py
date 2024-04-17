import pandas as pd

subsidized_financial_amadeus=pd.read_csv("subsidized_financial_amadeus.csv")
not_subsidized_financial_amadeus=pd.read_csv("not_subsidized_financial_amadeus.csv")

complete_financial=pd.concat([subsidized_financial_amadeus,not_subsidized_financial_amadeus])