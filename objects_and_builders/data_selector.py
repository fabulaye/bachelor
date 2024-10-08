import pandas as pd
from datahandling.change_directory import chdir_root_search
from processing.format_string import format_df





def df_format_wrapper(df):
    df=format_df(df,rename_df={"idnr":"bvdid"})
    return df

class data_selector():
    def __init__(self,id_dfs:list) -> None:
        concat_id_df=pd.concat(id_dfs)
        concat_id_df.drop_duplicates(subset="bvdid",inplace=True)
        concat_id_df=format_df(concat_id_df)
        self._df=None
        self._id_df=concat_id_df
    def add_data(self,list_of_dfs:list,variables:list,merge_on="bvdid"):
        map_object=map(df_format_wrapper,list_of_dfs)
        #df_list_new=list(map_object)
        #wir müssen idnr renamen
        chdir_root_search("data")
        combined_df=pd.concat(map_object,ignore_index=True)
        combined_df=df_format_wrapper(combined_df,)#problem ensteht durchs renamen
        list_of_vars=variables+[merge_on]
        #for var in list_of_vars:
        #        if var not in combined_df.columns:
        #            list_of_vars.remove(var)
        combined_df=combined_df[list_of_vars]
        chdir_root_search("data")
        #combined_df=format_df(combined_df)
        combined_df=combined_df[combined_df.isna().sum(axis=1)<len(variables)]
        combined_df.drop_duplicates(subset=list_of_vars,inplace=True)
        agg_df=dict(zip(list_of_vars,["custom_agg" for entry in range(len(list_of_vars))]))
        test_df = combined_df.groupby("bvdid").agg({col: custom_agg for col in combined_df.columns}).reset_index(drop=True)
        #drop wo all variables ==na sind
         #was passiert hier wenn ich vars selecte die nicht drin sind?
        
        self._df=pd.merge(self._id_df,test_df,on=merge_on,how="left")
        self._df.to_excel("data_selector_debug.xlsx")
        return self

def custom_agg(series:pd.Series):
    series.dropna(inplace=True)
    unique_values=series.unique()
    if len(unique_values)==1:
        return pd.Series(unique_values[0])
    if len(unique_values)==0:
        return pd.Series(["na"])
    if len(unique_values)>1:
        return pd.Series(["agg error"])



def bvdid_exploration():
    chdir_root_search("id")
    all_ids=pd.read_csv("treatment_and_control_ids.csv")
    chdir_root_search("treatment")
    orbis_financials=pd.read_csv("ob_ind_g_fins_eurbvd_orbis.csv")
    orbis_financials=pre_financial_merge_workflow(orbis_financials)
    orbis_legal=pd.read_csv("ob_legal_infobvd_orbis.csv")
    orbis_contact=pd.read_csv("ob_contact_infobvd_orbis.csv")
    #erstmal nur orbis
    selector=data_selector([all_ids]).add_data([orbis_financials,orbis_legal,orbis_contact],["conscode","closdate_year","addr_native","name_native"])
    #selector._df=pd.merge(selector._df,all_ids[["bvdid","name"]],how="left",on="bvdid")
    bvdid_count=selector._df.groupby("name_native")["bvdid"].unique()
    indices=[True if len(val)>1 else False for val in bvdid_count]
    double_names=bvdid_count.index[indices]
    doubles=selector._df[selector._df["name_native"].isin(double_names)]
    double_financials=orbis_financials[orbis_financials["bvdid"].isin(doubles["bvdid"])]
    double_financials=double_financials.merge(doubles[["bvdid","name_native"]],on="bvdid",how="left")
    double_financials_grouped=double_financials.groupby("name_native")
    for name,group in double_financials_grouped:
        print(group)
    print(bvdid_count)



        

