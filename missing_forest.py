import pandas as pd
from lukasdata.change_directory import chdir_data
chdir_data()

from lukasdata.count_nans import count_nan
from lukasdata.drop_column_with_na import drop_column_with_na
from lukasdata.mean_impute import mean_impute
from lukasdata.get_number_columns import filter_numeric_columns
from sklearn.metrics import mean_squared_error

def reorder_columns_by_na(df):
    missing_values_dict=count_nan(df)
    sorted_by_value=dict(sorted(missing_values_dict.items(),key=lambda x: x[1]))
    sorted_list_of_column_names=[]
    for number,entry in enumerate(sorted_by_value):
        sorted_list_of_column_names.append(entry)
    new_df=df[sorted_list_of_column_names]
    return new_df


complete_financial=pd.read_csv("complete_financial.csv")


complete_financial_numerical=filter_numeric_columns(complete_financial)

import numpy as np
from sklearn.ensemble import RandomForestRegressor

class MissForestImputer:
    def __init__(self, max_iter=10, n_estimators=100):
        self.max_iter = max_iter
        self.n_estimators = n_estimators
    
    def fit_transform(self, X):
        self.X = X.copy()
        self.X=drop_column_with_na(self.X,10)
        #drop column if all values are na
        self.X=reorder_columns_by_na(self.X)
        na_bool_df=self.X.isna()
        self.X=mean_impute(self.X)
        mse_list=[]
        for _ in range(self.max_iter):
            for feature_idx in range(self.X.shape[1]): #hier eigentlich sortieren nachdem was wir am häufigsten haben
                to_impute=self.X.iloc[:, feature_idx]
                #print(to_impute)
                missing_mask = na_bool_df.iloc[:,feature_idx]
                #print(missing_mask)
                #er trainiert hier nur mit den werten die er hat oder???
                X_train = self.X[~missing_mask] #müssten wir unsere abhängige nicht rauspoppen? Kann ich auch die mean imputed values nutzen?
                #xtrain ist nach dem Paper nur die observed variables, bekommen wir einen performance boost wenn wir auch die imputed variables nutzen?
                #print(X_train)
                #print(f"id:{feature_idx}")
                #print(f"X train is {X_train.shape} long")
                y_train_column = self.X.iloc[:, feature_idx]
                y_train=y_train_column[~missing_mask]
                #print(f"Y train is {y_train.shape} long")
                X_test = self.X[missing_mask].copy()
                #print(f"X test is {X_test.shape} long")
                X_test.iloc[:, feature_idx] = np.nan # was machen wir hier? muss man beim testen alles auf nan setzen? Muss das nicht eigentlich auch imputed sein?
                rf = RandomForestRegressor(n_estimators=self.n_estimators)
                rf.fit(X_train, y_train)
                #predicted_values = rf.predict(X_test) # hier wieder auf basis aller werte predicten und dann mit der mask selecten?
                predicted_values = rf.predict(self.X.iloc[:,:])
                #hier nicht ganz predicted values nutzen, warum benutze ich nicht train_test_split? Kann ich gegen alles testen
                #muss ich hier column feature_idxs rausnehmen?
                #print(f"predicted values ist {len(predicted_values)} lang")
                #print(f"missing_mask  ist {len(missing_mask)} lang")
                self.X.iloc[missing_mask, feature_idx] = predicted_values[missing_mask]
        print(self.X)
        mse_df=pd.DataFrame(mse_list)
        return self.X
    


imputer = MissForestImputer()
X_imputed = imputer.fit_transform(complete_financial_numerical)
X_imputed.insert(loc=1,value=complete_financial["idnr"],column="idnr")
X_imputed.set_index("idnr")
X_imputed.to_csv("rf_imputed.csv")