#from machine_learning.missing_forest import MissForestImputer
import pandas as pd
from datahandling.change_directory import chdir_sql_requests
from machine_learning.missing_forest import MissForestImputer
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

class MissForestImputer:
    def __init__(self, max_iter=10, n_estimators=100):
        self.max_iter = max_iter
        self.n_estimators = n_estimators
        self.imputed=None
    
    def fit_transform(self, X):
        self.X = X.copy()
        self.X=reorder_columns_by_na(self.X)
        na_bool_df=self.X.isna()
        self.X=mean_impute(self.X)
        mse_list=[]
        for i in range(self.max_iter):
            print(i)
            for feature_idx in range(self.X.shape[1]): #hier eigentlich sortieren nachdem was wir am häufigsten haben
                missing_mask = na_bool_df.iloc[:,feature_idx]
                X_train = self.X[~missing_mask]
                y_train_column = self.X.iloc[:, feature_idx]
                y_train=y_train_column[~missing_mask]
                X_test = self.X[missing_mask].copy()
                X_test.iloc[:, feature_idx] = np.nan 
                rf = RandomForestRegressor(n_estimators=self.n_estimators)
                rf.fit(X_train, y_train)
                predicted_values = rf.predict(self.X.iloc[:,:])
                self.X.iloc[missing_mask, feature_idx] = predicted_values[missing_mask]
        return self.X
    def run_miss_forest(self,df,insert_id=True,missing_percent=0.5):
        df_index=df.index
        df_dropped=drop_nan_columns(df,missing_percent)
        df_dropped_numerical=filter_numeric_columns(df_dropped)
        self.imputed=self.fit_transform(df_dropped_numerical)
        if insert_id==True:
            try:
                self.imputed.insert(0,"bvdid",df_dropped["idnr"])
                self.imputed.set_index("bvdid")
            except KeyError:
                self.imputed.insert(0,"bvdid",df_dropped["bvdid"])
                self.imputed.set_index("bvdid")
        return self.imputed

chdir_sql_requests()
financials=pd.read_csv("financialsbvd_ama.csv")

imputer=MissForestImputer()
imputer.run_miss_forest(financials,missing_percent=0.4)

imputer.imputed.to_csv("financialsbvd_ama_imputed.csv")

