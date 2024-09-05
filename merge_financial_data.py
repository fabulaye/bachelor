import pandas as pd
from datahandling.change_directory import chdir_sql_requests
from processing.my_list import list_intersection
import os
from datahandling.json_to_dict import json_to_dict
from datahandling.change_directory import chdir_data
from processing.my_list import unique_list

chdir_data()
wrds_map=pd.read_csv("map.csv")
wrds_map=dict(zip(wrds_map["name"],wrds_map["description"]))
chdir_sql_requests()
os.chdir("financials")
amadeus_financials=pd.read_csv("financialsbvd_ama.csv")

orbis_financials=pd.read_csv("ob_ind_g_fins_eurbvd_orbis.csv")

def replace_wrds_data(df):
    df.replace("Unconsolidated data","nan_placeholder",inplace=True)
    df.replace("No recent & Limited Fin.","nan_placeholder",inplace=True) #vorher mit u1 replaced
    df.replace("Limited Fin. Data","nan_placeholder",inplace=True)
    df.replace("SMALL COMPANY","SMALL",inplace=True)
    df.replace("MEDIUM SIZED COMPANY","MEDIUM",inplace=True)
    df.replace("MEDIUM SIZED","MEDIUM",inplace=True)
    df.replace("LARGE COMPANY","LARGE",inplace=True)
    df.replace("VERY LARGE COMPANY","VERY LARGE",inplace=True)
    #uniques anzeigen
    return df

amadeus_financials=replace_wrds_data(amadeus_financials).rename(columns=wrds_map)
orbis_financials=replace_wrds_data(orbis_financials).rename(columns=wrds_map)

import regex as re


def find_duplicate_columns(df):
    duplicate_regex=re.compile(r"^(.*?)(?=_\d)")
    matches_list=[]
    not_matched_list=[]
    for column in df.columns:
        matches=duplicate_regex.findall(column)
        if len(matches)>=1:
            if len(matches)==1:
                matches_list.append(matches[0])
        else:
            not_matched_list.append(column)
    return matches_list,not_matched_list


#vorher columns gleich renamen und dann einfacch resolve_conflicts nutzen
def merge_all_financials():
    chdir_sql_requests()
    os.chdir("financials")
    #idnr immer renamen, 
    for index,table_path in enumerate(os.listdir()):
        if index==0:
            df=pd.read_csv(table_path).rename(columns=wrds_map)
            df=replace_wrds_data(df)
        else:
            df_2=pd.read_csv(table_path,encoding="utf-8").rename(columns=wrds_map)
            df_2=replace_wrds_data(df)
            df=pd.merge(df,df_2,on=["bvdid","closdate_year","consolidation code"]) #wir machen das doppelt hier
    return df


def resolve_conflicts(df,column_intersection):
    conflict_indices=[]
    try:
        column_intersection.remove('exchange rate from local currency to usd')
    except ValueError:
        None
    unique_columns_values=[]
    for column in column_intersection:
        values=df[[column+"_1",column+"_2"]]
        values=values.bfill(axis=1).ffill(axis=1).fillna("nan_placeholder")
        
        if values.iloc[:,0].equals(values.iloc[:,1]):
            value=values.iloc[:,0].rename(column)
            value_series=pd.Series(value,name=column)
            unique_columns_values.append(value_series)
            
        else: 
            comparison = values.iloc[:,0] != values.iloc[:,1]
            rows_with_diff = values[comparison]  
            number_diff=comparison.sum()

            if number_diff>=20:
                print(column)
            conflict_indices.extend(list(rows_with_diff.index))
    conflict_indices=unique_list(conflict_indices)
    df=pd.concat(unique_columns_values,axis=1)
    return df,conflict_indices


#financials_merged=merge_all_financials()
financials_merged=pd.merge(amadeus_financials,orbis_financials,on=["bvdid","closdate_year","consolidation code"],suffixes=["_1","_2"],how="outer") 
chdir_data()

duplicate_columns,not_duplicate_columns=find_duplicate_columns(financials_merged)
duplicate_columns=unique_list(duplicate_columns)
duplicate_df,indices=resolve_conflicts(financials_merged,duplicate_columns)
problem_df=financials_merged.loc[indices]

#financials_merged.drop(columns=duplicate_columns,inplace=True)

not_duplicate_df=financials_merged[not_duplicate_columns]
complete=not_duplicate_df.join(duplicate_df)
complete.replace("nan_placeholder",None,inplace=True)

complete.to_excel("financials_merge_test.xlsx",index=False)
problem_df.to_excel("problem_df.xlsx",index=False)
duplicate_df.to_excel("duplicate_columns.xlsx",index=False)

#Wie handle ich consolidation codes--> vielleicht die Partens einfach droppen
#duplicates für closdate_year,bvdid columns selecten. consolidation codes vergleichen 
#units:thousands millions etc.
#imputation mit groups







