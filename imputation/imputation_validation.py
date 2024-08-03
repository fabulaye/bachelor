#cross validation split:
#for train,test in kfold

#introducing missing values
#save to new_missing_mask
#fit knn
#brauchen wir überhaupt ein holdout set?
#apply mask
# calculate metric
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.metrics import mean_absolute_error
from datahandling.change_directory import chdir_sql_requests


chdir_sql_requests()
financials=pd.read_csv("financialsbvd_ama.csv",index_col=False)
#financials_numeric=financials.select_dtypes(include=[int,float])

def missing_column_debug(df, array_column):
    for column in df.columns:
        if np.array_equal(df[column].values, array_column):
            df.drop(column, axis=1, inplace=True)
    return df

# Function to randomly delete values in the dataframe
def delete_values(df, fraction):
    df_missing = df.copy()
    mask = df_missing.apply(lambda col: np.random.rand(len(col)) < fraction)
    df_missing[mask] = np.nan
    return df_missing, mask

# Function to validate KNN imputation
def validate_knn_imputation(df, fraction_missing=0.1, n_neighbors=5):
    # Select only numeric columns
    numeric_df = df.select_dtypes(include=[np.number])
    
    # Create a copy of the original numeric dataframe with missing values and the mask
    df_missing, mask = delete_values(numeric_df, fraction_missing)
    
    # Fit the KNN imputer on the numeric dataframe with missing values
    imputer = KNNImputer(n_neighbors=n_neighbors)
    imputed_array = imputer.fit_transform(df_missing)
    lost_columns=missing_column_debug(numeric_df,imputed_array)
    print(lost_columns.columns)
    # Convert the imputed array back to a DataFrame with original column names
    imputed_df = pd.DataFrame(imputed_array, columns=numeric_df.columns)
    
    # Calculate the Mean Absolute Error only for the previously deleted values
    mae = mean_absolute_error(numeric_df[mask], imputed_df[mask])
    return mae, df_missing, imputed_df, numeric_df.columns


mae=validate_knn_imputation(financials)
print(mae)

def missing_column_debug():
    #check if all values from a np array column match that of any df column
    #delete column if true/mask
    #return name of column thats left over
    None
   
# Function to check and delete matching columns


