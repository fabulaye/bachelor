
import pandas as pd


from processing.format_dates import calculate_months_between,get_months,get_year

import pandas as pd
from processing.my_df import mydf
from processing.format_numbers import german_to_us_numbers
from datahandling.change_directory import chdir_root_search


class treatment_data_treatment_group(mydf):
    def __init__(self,bmwi_request_subset):
        super().__init__(bmwi_request_subset)
    def calculate_years(self):
        self["start_year"]=self["Laufzeit von"].apply(lambda x: get_year(x))
        self["end_year"]=self["Laufzeit bis"].apply(lambda x: get_year(x))
        self["treatment_years"]=self.apply(lambda x: range(x["start_year"],x["end_year"]+1),axis=1)
        self["treatment_years"]=self["treatment_years"].apply(lambda x: tuple(x))
        return self
    def calculate_annual_subsidy(self):
        rows_list=[]
        for index,row in self.iterrows():
            start_year=row["start_year"]
            end_year=row["end_year"]
            subsidized_months=calculate_months_between(row["Laufzeit von"],row["Laufzeit bis"])
            subsidy_per_month=german_to_us_numbers(row["Fördersumme in EUR"])/subsidized_months

            for year in row["treatment_years"]:
                new_row=row.copy()
                new_row["year"]=year
                if year !=start_year and year !=end_year:
                    new_row["treatment_weight"]=1
                    new_row["annual_subsidy"]=subsidy_per_month*12
                #int(row["Laufzeit von"][3:5])
                if year==start_year: 
                    new_row["treatment_weight"]=get_months(new_row["Laufzeit von"])/12
                    new_row["annual_subsidy"]=subsidy_per_month*get_months(new_row["Laufzeit von"])
                if year==end_year: 
                    new_row["treatment_weight"]=get_months(new_row["Laufzeit von"])/12
                    new_row["annual_subsidy"]=subsidy_per_month*get_months(new_row["Laufzeit bis"])
                row["treatment"]=1
                row_series=pd.Series(new_row)
                rows_list.append(row_series)
                del new_row
        df=pd.concat(rows_list,axis=1).T
        self.__init__(df)
        return self
    def drop_and_export(self):
        self.drop(columns=["year","months","name","Zuwendungsempfänger","project_id","start_year","end_year","treatment_years"],inplace=True)
        self.to_excel("treatment_group.xlsx")
                
class treatment_data_control_group(mydf):
    def __init__(self,df) -> None:
        super().__init__(df)
    def add_treatment_cols(self):
        self["treatment"]=0
        self["treatment"]=0
        self["annual_subsidy"]=0
        self["summed_annual_subsidy"]=0
        self["treatment_weight"]=0
        return self




#es fehlen 11 entries mit treatment years etc. also da wo wir aus Treatment nichts in id fanden: weird,318 die fehlen sind expected
#wir mergen nur subsidized --> ist wahrscheinlich ok



class treatment_df(mydf):
    def __init__(self,financial_df) -> None:
        super().__init__(financial_df)
    def merge_financials_and_concurrent_treatment(self,treatment_df):
        financial=self.astype(float,errors="ignore")
        treatment_data=treatment_df.astype(float,errors="ignore")
        treatment_data=treatment_data[["bvdid","year","annual_subsidy","start_year","end_year","treatment","treatment_weight"]]
        new_df=pd.merge(financial,treatment_data,left_on=["bvdid","closdate_year"],right_on=["bvdid","year"],how="left")
        self.__init__(new_df)
        return self
    
    def handle_parallel_projects(self):
        merged_df = self.groupby(['bvdid', 'year'], as_index=False).agg({
        'annual_subsidy': 'sum'
})      
        merged_df.rename(columns={'annual_subsidy': 'summed_annual_subsidy'}, inplace=True)
        result_df = self.merge(merged_df, on=['bvdid', 'year'], how='left')
        final_df = result_df.drop_duplicates(subset=['bvdid', 'year'])
        self.__init__(final_df)
        return self
        #return final_df
    
    def fill_not_subsidized_years(self):
        #treatment_weights=self["treatment_weigths"]
        filled=self[["summed_annual_subsidy","treatment","treatment_weight"]].fillna(0)
        self[["summed_annual_subsidy","treatment","treatment_weight"]]=filled
        return self




def treatment_group_treatment_workflow():
    chdir_root_search("data")
    bmwi_request=pd.read_csv("bmwi_request_with_ids.csv")
    chdir_root_search("treatment")
    treatment_financials=pd.read_excel("financials_merge.xlsx")
    treatment_group_treatment=treatment_data_treatment_group(bmwi_request).calculate_years().calculate_annual_subsidy()
    df=treatment_df(treatment_financials).merge_financials_and_concurrent_treatment(treatment_group_treatment).handle_parallel_projects()
    df.fill_not_subsidized_years()
    df.to_excel("financials_with_treatment.xlsx")
    return df



