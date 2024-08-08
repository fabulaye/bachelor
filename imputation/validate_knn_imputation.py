import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.metrics import mean_absolute_error
from datahandling.change_directory import chdir_sql_requests
from cleaning.drop_column_with_na import drop_nan_columns
from sklearn.preprocessing import StandardScaler
from machine_learning.imputation_validation import repeat_validation


chdir_sql_requests()
financials=pd.read_csv("financialsbvd_ama.csv",index_col=False)
years=financials["closdate_year"]

imputer=KNNImputer(n_neighbors=3)
mae_df,df=repeat_validation(financials,imputer,5,)
bad_imputations=return_bad_imputations(mae_df,0.3)
print(bad_imputations)
bad_columns=bad_imputations.index
print(bad_columns)
#mae_df_mean_multiple=optimize_n_neighnors([2,10])



#mae_df_mean_selected_variables=mae_df_mean_multiple[["shfd","cuas","empl","toas","tshf","shlq"]]

#plot_n_neighbor_optimization(mae_df_mean_multiple)
#other metrics?
#What ways are there to numerically optimize k neighbors?   

#3 neighbors sind gut so eyeball mäßig


#financials_numeric=financials.select_dtypes(include=[int,float])