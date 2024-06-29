from datahandling.change_directory import chdir_data,chdir_sql_requests
import pandas as pd

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

def german_to_us_numbers(german_number):
    us_number=german_number.replace(".","").replace(",",".")
    us_number=float(us_number)
    return us_number
def concurrent_treatment():
    chdir_data()
    
    df=pd.read_csv("bmwi_request.csv",index_col=False)    
    df=df[["Zuwendungsempfänger","Fördersumme in EUR","Laufzeit von","Laufzeit bis","project_id",]]
    new_df_columns=["Zuwendungsempfänger","Laufzeit von","Fördersumme in EUR","Laufzeit bis","project_id","year","treatment_weight","annual_subsidy"]
    new_df=pd.DataFrame(columns=new_df_columns)
    df["start_year"]=df["Laufzeit von"].apply(lambda x: int(x[-4:]))
    df["end_year"]=df["Laufzeit bis"].apply(lambda x: int(x[-4:]))
    df["treatment_years"]=df.apply(lambda x: range(x["start_year"],x["end_year"]+1),axis=1)
    df["treatment_years"]=df["treatment_years"].apply(lambda x: list(x))

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
    new_df.to_csv("concurrent_testbla.csv")
    return new_df


#concurrent=concurrent_treatment()
#print(concurrent)


#all_subsidized_ids=pd.read_csv("id/all_subsidized_ids.csv",index_col=False)


def merge_id_and_concurrent_treatment(concurrent_treatment_df,id_df):
    #concurrent_treatment_df=concurrent_treatment_df[["Zuwendungsempfänger","treatment_years","project_id"]]
    new_df=pd.merge(id_df,concurrent_treatment_df,left_on="name",right_on="Zuwendungsempfänger",how="outer",)
    #new_df.drop(columns="Zuwendungsempfänger",inplace=True)
    print(new_df)
    new_df.to_csv("concurrent_test.csv")
    return new_df

#test=merge_id_and_concurrent_treatment(concurrent,all_subsidized_ids)

#chdir_sql_requests()
#financials=pd.read_csv("financialsbvd_ama.csv")


def merge_financials_and_concurrent_treatment(financials,concurrent_treatment):
    new_df=pd.merge(financials,concurrent_treatment,left_on=["bvdid","closdate_year"],right_on=["bvdid","year"]) #überschreiben wir jetzt wieder?
    print(new_df)
    return new_df

#new_test=merge_financials_and_concurrent_treatment(financials,test)
#new_test.to_csv("concurrent_test.csv")

chdir_data()
concurrent=pd.read_csv("concurrent_test.csv")

def handle_parallel_projects(df):
    df_grouped=df.groupby("bvdid")
    new_df_list=[]
    for group_name,group in df_grouped:
        years=group["year"]
        mask=years.duplicated()
        if any(mask)==True:
            duplicate_values=group[mask]
            duplicate_years=duplicate_values["year"].to_list()
            for year in duplicate_years:
                duplicate_data=group[group["year"]==year]
                combined_subsidy=duplicate_data["annual_subsidy"].sum()
            group["annual_subsidy_combined"]=combined_subsidy
        else:
            group["annual_subsidy_combined"]=group["annual_subsidy"]
        
        new_df_list.append(group)

    new_df=pd.concat(new_df_list)
    print(new_df)

                #alles egal außer annual_subsidy die müssen wir combinen

            #print(duplicate_years)
        


handle_parallel_projects(concurrent)