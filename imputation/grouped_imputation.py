from lukasdata.get_number_columns import filter_numeric_columns
from lukasdata.concat_dfs import concat_dfs
from lukasdata.change_directory import chdir_data
import pandas as pd

chdir_data()
subsidized_financial_amadeus=pd.read_csv("subsidized_financial_amadeus.csv")
not_subsidized_financial_amadeus=pd.read_csv("not_subsidized_financial_amadeus.csv")
complete_financial=pd.concat([subsidized_financial_amadeus.reset_index(drop=True),not_subsidized_financial_amadeus.reset_index(drop=True)],ignore_index=True)

complete_financial_numerical=filter_numeric_columns(complete_financial)

complete_financial_numerical_compcat=complete_financial_numerical
complete_financial_numerical_compcat["compcat"]=complete_financial["compcat"]


def get_miss_values_hierachie(df):
    missing_values_dict=count_nan(df)
    sorted_by_value=dict(sorted(missing_values_dict.items(),key=lambda x: x[1]))
    sorted_list_of_column_names=[]
    for number,entry in enumerate(sorted_by_value):
        sorted_list_of_column_names.append(entry)
    return sorted_list_of_column_names

def grouped_imputation(df,groupby_label):
    missing_values_column_vector=get_miss_values_hierachie(df)
    df_grouped=df.groupby(groupby_label)
    new_df=pd.DataFrame()
    mean_values = df_grouped.mean()
    print(mean_values)
    print(type(mean_values))
    for group_name,group_df in df_grouped:
        group_df.drop(columns=groupby_label,inplace=True)
        fillna_dict=mean_values.loc[group_name].to_dict()
        group_df=group_df.fillna(fillna_dict)
        #group_df=group_df.iloc[:,1:]
        new_df=concat_dfs([new_df,group_df])
    #new_df=new_df.fillna(new_df.mean)
    #new_df=new_df.dropna(axis=1)

    new_df=new_df.reset_index()
    column_mean=mean_values.mean()
    new_df=new_df.fillna(column_mean)
    new_df=new_df.dropna(axis=1)
    return new_df

test_df=grouped_imputation(complete_financial_numerical_compcat,"compcat")
test_df.to_csv("imputation_test.csv",index=False)
print("converted to csv")