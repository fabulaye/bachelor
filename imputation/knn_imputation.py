import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from manipulation.filter_numeric_columns import filter_numeric_columns
from datahandling.change_directory import chdir_sql_requests
from cleaning.drop_column_with_na import drop_nan_columns
import pandas as pd

def impute_amadeus():
    chdir_sql_requests()
    financials=pd.read_csv("financialsbvd_ama.csv")
    #financials_numerical,dropped_columns=filter_numeric_columns(financials)
    financials_numerical=financials.select_dtypes(include=[float,int])
    financials_non_numerical=financials.select_dtypes(exclude=[float,int])
    
    imputer = KNNImputer(n_neighbors=3)
    
    # Perform the imputation
    
    financials_numerical_dropped=drop_nan_columns(financials_numerical,0.5)
    
    df_imputed = imputer.fit_transform(financials_numerical_dropped)
    #df_imputed=pd.DataFrame(df_imputed,columns=financial_columns)
    df_imputed = pd.DataFrame(df_imputed, columns=financials_numerical_dropped.columns)
    df_imputed=pd.concat([financials_non_numerical,df_imputed],axis=1)
    df_imputed.to_excel("knn_imputation_ama_financials.xlsx")


impute_amadeus()