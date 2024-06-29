#from machine_learning.missing_forest import MissForestImputer
import pandas as pd
from datahandling.change_directory import chdir_sql_requests

import pandas as pd
from datahandling.change_directory import chdir_data
chdir_data()

from exploration.count_nans import count_nan
from cleaning.drop_column_with_na import drop_nan_columns
from machine_learning.mean_impute import mean_impute
from manipulation.filter_numeric_columns import filter_numeric_columns
from sklearn.metrics import mean_squared_error

def reorder_columns_by_na(df):
    missing_values_dict=count_nan(df)
    sorted_by_value=dict(sorted(missing_values_dict.items(),key=lambda x: x[1]))
    sorted_list_of_column_names=[]
    for number,entry in enumerate(sorted_by_value):
        sorted_list_of_column_names.append(entry)
    new_df=df[sorted_list_of_column_names]
    return new_df

import numpy as np
from sklearn.ensemble import RandomForestRegressor


chdir_sql_requests()
financials=pd.read_csv("financialsbvd_ama.csv")

imputer=MissForestImputer()
imputer.run_miss_forest(financials)

imputer.imputed.to_csv("financialsbvd_ama_imputed.csv")