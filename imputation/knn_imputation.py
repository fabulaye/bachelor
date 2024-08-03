import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from manipulation.filter_numeric_columns import filter_numeric_columns
from datahandling.change_directory import chdir_sql_requests

import pandas as pd
def filter_numeric_columns(df):
    columns=df.columns
    new_df=pd.DataFrame()
    dropped_columns=[]
    for column_name in columns:
        column=df[column_name]
        try:
            pd.to_numeric(column)
            new_df[column_name]=column
            print(column_name)
        except ValueError:
            dropped_columns.append(column_name)
            print(f"{column_name} can't be converted to numeric")
    return new_df,dropped_columns

chdir_sql_requests()
financials=pd.read_csv("financialsbvd_ama.csv")
#financials_numerical,dropped_columns=filter_numeric_columns(financials)
financials_numerical=financials.select_dtypes(include=[float,int])
financials_non_numerical=financials.select_dtypes(exclude=[float,int])


imputer = KNNImputer(n_neighbors=3)

# Perform the imputation
financials_numerical_array=financials_numerical.to_numpy()

financial_columns=financials_numerical.columns.drop("pl")
#financial_columns=financial_columns.remove("pl")
df_imputed = imputer.fit_transform(financials_numerical_array)
#df_imputed=pd.DataFrame(df_imputed,columns=financial_columns)
df_imputed = pd.DataFrame(df_imputed, columns=financial_columns)
df_imputed=pd.concat([financials_non_numerical,df_imputed],axis=1)
df_imputed.to_excel("knn_imputation_test.xlsx")


#permutation?
#accuracy metrics?
#dropping under 50%
#