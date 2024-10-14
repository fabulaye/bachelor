
import pandas as pd


from processing.format_dates import calculate_months_between,get_months,get_year

import pandas as pd
from processing.my_df import mydf
from processing.format_numbers import german_to_us_numbers
from datahandling.change_directory import chdir_root_search
from datetime import datetime

def calculate_days_between(date_1,date_2,date_format="%d.%m.%Y"):
    date_1=datetime.strptime(date_1,date_format)
    date_2=datetime.strptime(date_2,date_format)
    delta=date_2-date_1
    return delta.days


treatment_vars=["annual_subsidy","treatment","treatment_weight","subsidy","subsidy_duration_day","one_year_lag_total_annual_subsidy"]
to_merge_vars=["bvdid","year","project_id","subsidy_start","subsidy_end"]+treatment_vars


class treatment_data_treatment_group(mydf):
    def __init__(self,bmwi_request_subset):
        super().__init__(bmwi_request_subset)
    def calculate_years(self):
        self["start_year"]=self["subsidy_start"].apply(lambda x: get_year(x))
        self["end_year"]=self["subsidy_end"].apply(lambda x: get_year(x))
        self["treatment_years"]=self.apply(lambda x: range(x["start_year"],x["end_year"]+1),axis=1)
        self["treatment_years"]=self["treatment_years"].apply(lambda x: tuple(x))
        self["subsidy"]=self["subsidy"].apply(german_to_us_numbers)
        
        return self
    def calculate_annual_subsidy(self):
        rows_list=[]
        for index,row in self.iterrows():
            start_year=row["start_year"]
            end_year=row["end_year"]

            subsidized_days=calculate_days_between(row["subsidy_start"],row["subsidy_end"])
        
            subsidy_per_day=row["subsidy"]/subsidized_days
            row["subsidy_duration_day"]=subsidized_days

            for year in row["treatment_years"]:
                new_row=row.copy()
                new_row["year"]=year
                if year !=start_year and year !=end_year:
                    new_row["treatment_weight"]=1
                    new_row["annual_subsidy"]=subsidy_per_day*365
                #int(row["Laufzeit von"][3:5])
                if year==start_year: 
                    year_string=f"31.12.{year}"
                    days=calculate_days_between(row["subsidy_start"],year_string)
                    #days*daily subsidy. 
                    new_row["treatment_weight"]=get_months(new_row["subsidy_start"])/12
                    new_row["annual_subsidy"]=subsidy_per_day*days
                if year==end_year: 
                    year_string=f"01.01.{year}"
                    days=calculate_days_between(year_string,row["subsidy_end"])
                    new_row["treatment_weight"]=get_months(new_row["subsidy_start"])/12
                    new_row["annual_subsidy"]=subsidy_per_day*days
                row["treatment"]=1
                row_series=pd.Series(new_row)
                rows_list.append(row_series)
                del new_row
        
        df=pd.concat(rows_list,axis=1).T
        self.__init__(df)
        return self
    
    def lagged_subsidy(self):
        grouped=self.groupby("bvdid")
        #erste var muss 0 sein 
        #insert 0 in first position cutoff last one
        new_df=[]
        for name,group in grouped:
            zero_series=pd.Series([0])
            annual_subsidy=group["annual_subsidy"]
            annual_subsidy_sliced=annual_subsidy.iloc[:-1]
            values=pd.concat([zero_series,annual_subsidy_sliced]).reset_index(drop=True)
            group["one_year_lag_total_annual_subsidy"]=values.to_list()
            new_df.append(group)
        new_df=pd.concat(new_df)
        self.__init__(new_df)
        return self

    
                
class treatment_data_control_group(mydf):
    def __init__(self,df) -> None:
        super().__init__(df)
    def add_treatment_cols(self):
        for col in treatment_vars:
            self[col]=0
        return self




#es fehlen 11 entries mit treatment years etc. also da wo wir aus Treatment nichts in id fanden: weird,318 die fehlen sind expected
#wir mergen nur subsidized --> ist wahrscheinlich ok
def integrated_dummy(row):
    nans=row.notna()
    if nans["annual_subsidy"]==True:
        if row["annual_subsidy"]!=row["total_annual_subsidy"]:
            return 1
        else:
            return 0
    else:
        return 0


import numpy as np
class treatment_df(mydf):
    def __init__(self,financial_df) -> None:
        super().__init__(financial_df)
    def merge_financials_and_concurrent_treatment(self,treatment_df):
        financial=self.astype(float,errors="ignore")
        #treatment_data=treatment_df.astype(float,errors="ignore")
        treatment_data=treatment_df[to_merge_vars]
        new_df=pd.merge(financial,treatment_data,left_on=["bvdid","closdate_year"],right_on=["bvdid","year"],how="left")
        print(len(financial)+len(treatment_data))
        print(len(new_df))
        self.__init__(new_df)
        return self
    
    def handle_parallel_projects(self):
        grouped_df = self.groupby(['bvdid', 'year'], as_index=False)
        annual_subsidy_sum=grouped_df.agg({'annual_subsidy': 'sum'})     
        annual_subsidy_sum.rename(columns={'annual_subsidy': 'total_annual_subsidy'}, inplace=True) 
        treatment_vars.append("total_annual_subsidy")
        to_merge_vars.append("total_annual_subsidy")

        subsidy_sum=grouped_df.agg({'subsidy': 'sum'}) 
        subsidy_sum.rename(columns={'subsidy': 'total_subsidy'}, inplace=True) 
        treatment_vars.append("total_subsidy")
        to_merge_vars.append("total_subsidy")

        project_ids=grouped_df.agg({'project_id':np.unique}) 
        project_ids.rename(columns={'project_id': 'project_ids'}, inplace=True)


        df=self.merge(annual_subsidy_sum, on=['bvdid', 'year'], how='left')
        df=df.merge(project_ids, on=['bvdid', 'year'], how='left')
        df=df.merge(subsidy_sum, on=['bvdid', 'year'], how='left')
        df["integrated_dummy"]=df.apply(lambda x: integrated_dummy(x),axis=1)
        treatment_vars.append("integrated_dummy")
        to_merge_vars.append("integrated_dummy")
        #df.to_excel("parallel_projects_debug.xlsx")
        df.drop_duplicates(subset=['bvdid', 'year'],inplace=True)
        self.__init__(df) #can I use __new__ here?
        return self
    
    def fill_not_subsidized_years(self):
        #treatment_weights=self["treatment_weigths"]
        self["treatment"].fillna(1,inplace=True)
        filled=self[treatment_vars].fillna(0)
        self[treatment_vars]=filled
        return self




def treatment_group_treatment_workflow():
    chdir_root_search("data")
    bmwi_request=pd.read_csv("bmwi_request_with_ids.csv",index_col=False)
    chdir_root_search("treatment")
    treatment_financials=pd.read_excel("financials_merge.xlsx",index_col=False)
    treatment_group_treatment=treatment_data_treatment_group(bmwi_request).calculate_years().calculate_annual_subsidy().lagged_subsidy()
    df=treatment_df(treatment_financials).merge_financials_and_concurrent_treatment(treatment_group_treatment).handle_parallel_projects()
    df.fill_not_subsidized_years()
    df.drop(columns=["year","project_id","annual_subsidy"],inplace=True)
    df.to_excel("financials_with_treatment.xlsx")
    return df



