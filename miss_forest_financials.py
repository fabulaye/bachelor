import pandas as pd
from datahandling.change_directory import chdir_data
#from machine_learning.missing_forest import MissForestImputer
from manipulation.filter_numeric_columns import filter_numeric_columns

chdir_data()


from machine_learning.missing_forest import MissForestImputer

chdir_data()

ama_financials=pd.read_csv("sql_data/financialsbvd_ama.csv",index_col=0)
miss_forest=MissForestImputer()
imputed=miss_forest.run_miss_forest(ama_financials)
imputed.to_csv("financialsbvd_ama_imputed.csv",index=False)


