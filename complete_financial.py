from lukasdata.change_directory import chdir_data
from lukasdata.concat_dfs import concat_dfs
import pandas as pd

chdir_data()
subsidized_financial_amadeus=pd.read_csv("subsidized_financial_amadeus.csv",index_col=False)
print(subsidized_financial_amadeus)
not_subsidized_financial_amadeus=pd.read_csv("not_subsidized_financial_amadeus.csv",index_col=False)
#complete_financial=pd.concat([subsidized_financial_amadeus.reset_index(drop=True),not_subsidized_financial_amadeus.reset_index(drop=True)],ignore_index=True)

complete_financial=concat_dfs([subsidized_financial_amadeus,not_subsidized_financial_amadeus])
#complete_financial.set_index("idnr",inplace=True)
complete_financial.to_csv("complete_financial.csv",index=False)