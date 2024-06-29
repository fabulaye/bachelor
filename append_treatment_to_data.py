import pandas as pd
from datahandling.change_directory import chdir_data,chdir_sql_requests
import os
def append_treatment_to_data(file_name,database):
    chdir_sql_requests()
    df=pd.read_csv(file_name)
    chdir_data()
    all_ids=pd.read_csv("id/all_ids.csv")
    if database=="orbis":
        id="bvdid"
    if database=="amadeus":
        id="idnr"
    if "treatment" not in df.columns:
        new_df=pd.merge(df,all_ids,left_on=id,right_on="bvdid")
        #try:
        #    new_df.drop("Unnamed: 0",axis=1)
        #except KeyError:
        #    None
        #merged_df = merged_df.drop(columns=['bvdid'])
        chdir_sql_requests()
        new_df.to_csv(file_name)
    else:
        print("treatment already appended")


def append_treatment_to_sql_data():
    chdir_sql_requests()
    files=os.listdir()
    for file in files:
        if file.endswith("ama.csv"):
            append_treatment_to_data(file,"amadeus")
        if file.endswith("orbis.csv"):
            append_treatment_to_data(file,"orbis")

#financials_bvd_ama=pd.read_csv("sql_data/financialsbvd_ama.csv")
#ob_key_financials_eurbvd_orbis=pd.read_csv("sql_data/ob_key_financials_eurbvd_orbis.csv")
#append_treatment_to_data("ob_key_financials_eurbvd_orbis.csv","orbis")

#append_treatment_to_sql_data()

