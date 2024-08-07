import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.metrics import mean_absolute_error
from datahandling.change_directory import chdir_sql_requests
from cleaning.drop_column_with_na import drop_nan_columns
from sklearn.preprocessing import StandardScaler
from machine_learning.

def return_bad_imputations(metric_df):
    metric_df_agg=metric_df.agg("mean").sort_values()
    bad_imputations=metric_df_agg[metric_df_agg>=0.5]
    return bad_imputations

chdir_sql_requests()
financials=pd.read_csv("financialsbvd_ama.csv",index_col=False)
years=financials["closdate_year"]

imputer=KNNImputer(n_neighbors=5)

mae_df_mean_multiple=optimize_n_neighnors([2,10])



#mae_df_mean_selected_variables=mae_df_mean_multiple[["shfd","cuas","empl","toas","tshf","shlq"]]

#plot_n_neighbor_optimization(mae_df_mean_multiple)
#other metrics?
#What ways are there to numerically optimize k neighbors?   

#3 neighbors sind gut so eyeball mäßig


#financials_numeric=financials.select_dtypes(include=[int,float])