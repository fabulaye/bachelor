#from objects_and_builders.data_selector import data_selector
from datahandling.change_directory import chdir_root_search
import pandas as pd
from processing.format_string import format_df
from processing.my_df import mydf

def add_name_to_df(financial_df):
    ids=pd.read_csv(r"C:\Users\lukas\Desktop\bachelor\data\id\treatment_and_control_ids.csv")
    financial_df=financial_df.merge(ids,on="bvdid",how="left")
    return financial_df



def add_my_id_to_financial(df):
    new_grouped=df.groupby("name")
    df['my_id'] = new_grouped.ngroup()
    return df

def fill_series(series:pd.Series):
    series=series.bfill().ffill().fillna("nan_placeholder")
    if series.duplicated(keep=False).sum()==len(series):
        return series.iloc[0]
    else:
        return pd.Series(["fill error"])

def filter_12_months(df):
    twelve_months_df=df[df["months"]==12]
    six_months_df=df[df["months"]==6]
    return twelve_months_df

def drop_companies_with_few_entries(df):
    year_range=range(2017,2025)
    new_df_data=[]
    grouped=df.groupby("bvdid")
    dropped_companies=[]
    for index,group in grouped:
        year_values=group["closdate_year"]
        if sum(year_values.isin(year_range))>=3:
            #recent_data=group[group["closdate_year"]>=2017]
            new_df_data.append(group) 
            #ich belohne companies die doppelte entries haben weil es so aussieht 
        else:
            dropped_companies.extend(group["name"].unique())
    new_df=pd.concat(new_df_data)
    print(dropped_companies)
    return new_df

def drop_observations_by_na(df,threshold):
    grouped=df.groupby("bvdid")
    new_df_data=[]
    n_columns=len(df.columns)
    empty_rows=0
    for index,group in grouped:
        new_group=[]
        for index,row in group.iterrows():
            if sum(row.isna())/n_columns>threshold:
                empty_rows+=1
            else:
                new_group.append(row)
        new_group=pd.DataFrame(new_group)
        new_df_data.append(new_group)
    new_df=pd.concat(new_df_data)
    print(f"dropped {empty_rows} rows")
    return new_df


def clean_workflow(df):
    df=format_df(df)
    df=filter_12_months(df)
    if "name" not in df.columns:
        df=add_name_to_df(df)
    #df=resolve_duplicate_ids(df) löschen? ist jetzt method von merge financail
    new_df=drop_companies_with_few_entries(df)
    new_df=mydf(new_df)
    bachelor_exemptions=["cf","cuas","culi","ebit","ebitda","empl","enva","fias","ifas","ltdb","ncas","ncli","ocas","ocli","ofas","oncl","shfd","tfas","toas","tshf"]
    #new_df_dropped,dropped_cols=new_df.drop_nan_columns(0.8,return_dropped_colname=True,exemptions=bachelor_exemptions)
    #new_df=drop_observations_by_na(new_df_dropped,0.7)
    return new_df
