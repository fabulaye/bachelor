import pandas as pd
from datahandling.change_directory import chdir_data


chdir_data()

def add_id_to_bmwi_data():
    amadeus_general=pd.read_csv("filtered_subsidized_amadeus.csv")
    amadeus_general=amadeus_general.loc[:,["name_nat","idnr"]]
    bmwi_data=pd.read_csv("bmwi_request.csv")
    bmwi_data["Zuwendungsempfänger"]=bmwi_data["Zuwendungsempfänger"].map(lambda x:x.upper())
    new_df=pd.merge(amadeus_general,bmwi_data,right_on="Zuwendungsempfänger",left_on="name_nat")
    new_df.to_csv("bwmi_request.csv",index=False)
    print(new_df)

add_id_to_bmwi_data()

bmwi_data=pd.read_csv("bwmi_request.csv")
amadeus_financials=pd.read_csv("sql_data/financialsbvd_ama.csv")

merged=pd.merge(amadeus_financials,bmwi_data.loc[:,["Laufzeit von","idnr"]],on="idnr")
merged.to_csv("bmwi_request_with_ids.csv",index=False)

#problem ich tue so als würde das unternehmen gefördertw erden aber es wird ja doppelt gemerged. Ich brauhce noch ne Projekt id

