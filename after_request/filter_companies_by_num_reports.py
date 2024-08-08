from datahandling.change_directory import chdir_data,chdir_sql
import pandas as pd

chdir_data()
treatment_df=pd.read_excel("treatmentfinancialsbvd_ama.xlsx",index_col=False)

def filter_companies_by_num_reports(df):
    filtered=df.groupby("bvdid").filter(lambda x:len(x)>=3)
    return filtered


new_df=filter_companies_by_num_reports(treatment_df)
new_df.to_excel("treatmentfinancialsbvd_ama_filtered.xlsx",index=False)


#filter out observations where the difference is to large