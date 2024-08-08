from datahandling.change_directory import chdir_data,chdir_sql_requests
import pandas as pd

from datetime import datetime
from cleaning.format_dates import calculate_months_between,get_months,get_year
from exploration.count_nans import count_nan
import pandas as pd
from datahandling.change_directory import chdir_sql_requests

from datetime import datetime

def calculate_months_between(d1, d2):
    date_format = "%d.%m.%Y"
    start_date = datetime.strptime(d1, date_format)
    end_date = datetime.strptime(d2, date_format)

    # Calculate the number of months between the two dates
    months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
    return months

def get_months(date):
    date_format = "%d.%m.%Y"
    date=datetime.strptime(date,date_format)
    months=date.month
    return months

def get_year(date,date_format="%d.%m.%Y"):
    date=str(date)
    date=datetime.strptime(date,date_format)
    year=date.year
    year=int(year)
    
    return year

def analyze_dataframes(*dfs):
    for i,df in enumerate(dfs):
        print(f"shape of Dataframe {i}: {df.shape}")
    for df in dfs:
        df_nans=count_nan(df)
        print(df_nans)


def german_to_us_numbers(german_number):
    us_number=german_number.replace(".","").replace(",",".")
    us_number=float(us_number)
    return us_number

def calculate_annual_subsidy(df):
        df_columns=list(df.columns)
        df_columns=df_columns+["year","treatment_weight","annual_subsidy"]
        new_df=pd.DataFrame(columns=df_columns)
        for index,row in df.iterrows():
            start_year=int(row["Laufzeit von"][-4:])
            end_year=int(row["Laufzeit bis"][-4:])
            subsidized_months=calculate_months_between(row["Laufzeit von"],row["Laufzeit bis"])
            subsidy_per_month=german_to_us_numbers(row["Fördersumme in EUR"])/subsidized_months
            for year in row["treatment_years"]:
                row["year"]=year
                if year !=start_year and year !=end_year:
                    row["treatment_weight"]=1
                    row["annual_subsidy"]=subsidy_per_month*12
                #int(row["Laufzeit von"][3:5])
                if year==start_year: 
                    row["treatment_weight"]=get_months(row["Laufzeit von"])/12
                    row["annual_subsidy"]=subsidy_per_month*get_months(row["Laufzeit von"])
                if year==end_year: 
                    row["treatment_weight"]=get_months(row["Laufzeit von"])/12
                    row["annual_subsidy"]=subsidy_per_month*get_months(row["Laufzeit bis"])
                new_df.loc[len(new_df)]=row
                #new_df=pd.concat([new_df,row])
        new_df.drop(columns=["Laufzeit von", "Laufzeit bis"],inplace=True)
        return new_df


def calculate_years(df):
        df["start_year"]=df["Laufzeit von"].apply(lambda x: get_year(x))
        df["end_year"]=df["Laufzeit bis"].apply(lambda x: get_year(x))
        df["treatment_years"]=df.apply(lambda x: range(x["start_year"],x["end_year"]+1),axis=1)
        df["treatment_years"]=df["treatment_years"].apply(lambda x: tuple(x))
        return df


def append_treatment_to_data(file_name,database):
    chdir_sql_requests()
    df=pd.read_csv(file_name)
    chdir_data()
    all_ids=pd.read_csv("id/all_ids.csv")
    treatment_df=pd.read_csv("treatment.csv")
    if database=="orbis":
        id="bvdid"
    if database=="amadeus":
        id="idnr"
        closedate="closdate_year"
    #if "treatment" in df.columns:
    #    df.drop(columns="treatment",inplace=True)
    if "treatment" not in df.columns:
        new_df=pd.merge(df,treatment_df,left_on=[id,closedate],right_on=["bvdid","year"],how="outer")
        chdir_sql_requests()
        new_df.to_csv("treatment"+file_name)
    else:
        print("treatment already appended")


#es fehlen 11 entries mit treatment years etc. also da wo wir aus Treatment nichts in id fanden: weird,318 die fehlen sind expected
#wir mergen nur subsidized --> ist wahrscheinlich ok

def merge_financials_and_concurrent_treatment(financials,all_subsidized_ids,concurrent_treatment):
    new_df=pd.merge(financials,all_subsidized_ids[["treatment","bvdid"]],on="bvdid")
    new_df=pd.merge(financials,concurrent_treatment,left_on=["bvdid","closdate_year"],right_on=["bvdid","year"],how="left")
    return new_df

def handle_parallel_projects(df):
    merged_df = df.groupby(['bvdid', 'year'], as_index=False).agg({
    'annual_subsidy': 'sum'
})
    merged_df.rename(columns={'annual_subsidy': 'summed_annual_subsidy'}, inplace=True)

    # Merge the summed subsidies back to the original DataFrame
    result_df = pd.merge(df, merged_df, on=['bvdid', 'year'], how='left')
    #
    final_df = result_df.drop_duplicates(subset=['bvdid', 'year'])
    #result_df = merged_df
    # Drop the original 'annual_subsidy' column if necessary
    result_df.drop(columns=['annual_subsidy'], inplace=True)
    return final_df
        
def fill_not_treated_data(df):
    df["treatment"].fillna(0,inplace=True)
    df["annual_subsidy"].fillna(0,inplace=True)
    df.fillna({"summed_annual_subsidy":0},inplace=True)
    df.fillna({"Fördersumme in EUR":0},inplace=True)
    #df["annual_subsidy_combined"].fillna(0,inplace=True)
    df["treatment_weight"].fillna(0,inplace=True)
    return df

def drop_unnamed_columns(df):
    to_drop=[]
    for column_name in df.columns:
        if column_name.startswith("Unnamed"):
            to_drop.append(column_name)
    df.drop(columns=to_drop,inplace=True)
    return df

def clean_final_df(df):
    df.fillna({"closdate_year":df["year"]},inplace=True)
    df.drop(columns=["year","months","name","Zuwendungsempfänger","project_id","start_year","end_year","treatment_years"],inplace=True)
    df=drop_unnamed_columns(df)
    return df

def treatment_workflow(sql_df):
    chdir_sql_requests()
    df=pd.read_csv("treatmentfinancialsbvd_ama.csv")
    chdir_data()
    all_subsidized_ids=pd.read_csv("id/all_subsidized_ids.csv",index_col=False)
    bmwi_request=pd.read_csv("bmwi_request.csv")
    bmwi_request=bmwi_request[["Zuwendungsempfänger","Fördersumme in EUR","Laufzeit von","Laufzeit bis","project_id",]]
    bmwi_request_with_ids=pd.merge(bmwi_request,all_subsidized_ids,left_on="Zuwendungsempfänger",right_on="name",how="left") #wir verlieren hier 11 datenpunkte
    #financials=pd.read_csv("financialsbvd_ama.csv")
    bmwi_request_with_ids.to_excel("bmwi_request_debug.xlsx")
    print(sum(bmwi_request_with_ids["Zuwendungsempfänger"].isna()))
    bmwi_request_with_ids=calculate_years(bmwi_request_with_ids)    
    bmwi_request_with_ids=calculate_annual_subsidy(bmwi_request_with_ids)
    chdir_sql_requests()
    #sql_df=pd.read_csv("financialsbvd_ama_imputed.csv",index_col=False) 
    #new_test=merge_financials_and_concurrent_treatment(financials,all_subsidized_ids,treatment_with_id)#hier verlieren wir die namen
    new_test=pd.merge(sql_df,bmwi_request_with_ids,left_on=["bvdid","closdate_year"],right_on=["bvdid","year"],how="left")
    #new_test.to_csv("treatmentfinancialsbvd_ama.csv",index=False)
    df=handle_parallel_projects(new_test)
    df=fill_not_treated_data(df)
    df=clean_final_df(df)
    df.to_csv("treatmentfinancialsbvd_ama.csv",index=False)
    df.to_excel("treatmentfinancialsbvd_ama.xlsx",index=False)


chdir_sql_requests()
ama_financials_knn_imputation=pd.read_excel("knn_imputation_ama_financials.xlsx")
ama_financials_knn_imputation.rename(columns={"idnr":"bvdid"},inplace=True)
treatment_workflow(ama_financials_knn_imputation)
