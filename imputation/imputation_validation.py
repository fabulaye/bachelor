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
from cleaning.drop_column_with_na import drop_nan_columns

chdir_sql_requests()
financials=pd.read_csv("financialsbvd_ama.csv",index_col=False)
years=financials["closdate_year"]

#financials_numeric=financials.select_dtypes(include=[int,float])


def find_missing_column(df,array):
    transposed_array = array.T
    for row in transposed_array:
        df=check_array_column(df,row)
    #for column in np.nditer(array):
        #df=check_array_column(df,column)
    return df

def check_array_column(df, array_column):
    for column in df.columns:
        df_values=df[column].values
        equal=np.array_equal(df_values, array_column)
        minus=df_values-array_column
        minus_cumsum=minus.cumsum()
        if equal :
            df.drop(column, axis=1, inplace=True)
            continue
    return df

# Function to randomly delete values in the dataframe
def delete_values(df, fraction):
    #mask with nas
    #use np function for random selection: müssen die selecten die false sind bei isna
    #
    df_missing = df.copy()
    mask = df_missing.apply(lambda col: np.random.rand(len(col)) < fraction)
    df_missing[mask] = np.nan
    #mask hat alle nans nicht nur die neuen
    return df_missing, mask

# Function to validate KNN imputation
def validate_knn_imputation(df, fraction_missing=0.1, n_neighbors=5):
    # Select only numeric columns
    numeric_df = df.select_dtypes(include=[np.number,int,float])
    numeric_df=drop_nan_columns(numeric_df,0.3)
    # Create a copy of the original numeric dataframe with missing values and the mask
    df_missing, mask = delete_values(numeric_df, fraction_missing)
    #missing_sum=df_missing.isnull().sum()
    #missing_sum=missing_sum[missing_sum>=1700]

    #df_missing.drop(columns=["enva","exre","extr","rd"],inplace=True)
    imputer = KNNImputer(n_neighbors=n_neighbors)
    imputed_array = imputer.fit_transform(df_missing)
    print(df_missing.shape)
    imputed_df = pd.DataFrame(imputed_array, columns=df_missing.columns)
    
    numeric_df_na=numeric_df[mask].isna().sum()
    imputed_df_na=imputed_df[mask].isna().sum()
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


