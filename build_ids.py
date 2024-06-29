import pandas as pd
import os
from datahandling.change_directory import chdir_data
from load_config import orbis_not_subsidized,amadeus_not_subsidized,orbis_subsidized_filtered,amadeus_subsidized_filtered,amadeus_not_subsidized_ids,orbis_not_subsidized_ids,amadeus_subsidized_ids,orbis_subsidized_ids

def chdir_id():
      os.chdir(f"C:/Users/Lukas/Desktop/bachelor/data/id")

def create_amadeus_id_csv(amadeus_csv_name,id_csv_name):
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
    amadeus_df=pd.read_csv(amadeus_csv_name,index_col=False) #zu csv switchen
    df=amadeus_df[["idnr","name_nat"]]
    df=df.drop_duplicates()
    df.rename(columns={"idnr":"bvdid","name_nat":"name"},inplace=True)
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data/id")
    df.to_csv(id_csv_name,index=False) #index=False neu
    return df



def create_orbis_id_csv(orbis_csv_name,id_csv_name):
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
    orbis_df=pd.read_csv(orbis_csv_name,index_col=False) #zu csv switchen
    print(orbis_df)
    df=orbis_df[["bvdid","name_native"]]
    df.rename(columns={"name_native":"name"},inplace=True)
    df=df.drop_duplicates()
    #df.rename(column="bvdid")
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data/id")
    df.to_csv(id_csv_name,index=False) #index=False neu
    #df mit den jahren+bvdid und financials etc. mergen
    return df

def create_concurrent_orbis_id_csv(orbis_csv_name,id_csv_name):
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
    orbis_df=pd.read_csv(orbis_csv_name,index_col=False) #zu csv switchen
    print(orbis_df)
    df=orbis_df[["bvdid","name_native"]]
    df.rename(columns={"name_native":"name"},inplace=True)
    #df.rename(column="bvdid")
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data/id")
    df.to_csv(id_csv_name,index=False) #index=False neu
    return df

def combine_ids_unique(amadeus_df_name,orbis_df_name):
    amadeus_df=pd.read_csv(amadeus_df_name)
    orbis_df=pd.read_csv(orbis_df_name)
    amadeus_df.rename(columns={"idnr":"bvdid"})
    combined=pd.concat([amadeus_df,orbis_df],ignore_index=True)
    combined=combined.drop_duplicates()
    return combined

def all_subsidized_ids():
    subsidized_ids_amadeus=create_amadeus_id_csv(amadeus_subsidized_filtered,amadeus_subsidized_ids)
    subsidized_ids_orbis=create_orbis_id_csv(orbis_subsidized_filtered,orbis_subsidized_ids)
    chdir_id()
    combined=combine_ids_unique(amadeus_subsidized_ids,orbis_subsidized_ids) #input soll name sein nicht df
    combined["treatment"]=1
    combined.to_csv("all_subsidized_ids.csv")


def all_not_subsidized_ids():
    #not_subsidized_ids_orbis=create_orbis_id_csv(orbis_not_subsidized,amadeus_not_subsidized_ids)
    #not_subsidized_ids_amadeus=create_amadeus_id_csv(amadeus_not_subsidized,orbis_not_subsidized_ids)
    #if isinstance(not_subsidized_ids_orbis,pd.Series):
        #not_subsidized_ids_orbis=not_subsidized_ids_orbis.to_frame()
    #if isinstance(not_subsidized_ids_amadeus,pd.Series):
        #not_subsidized_ids_amadeus=not_subsidized_ids_amadeus.to_frame()
    create_amadeus_id_csv("control_variables_amadeus.csv","amadeus_control_ids.csv")
    create_orbis_id_csv("control_variables_orbis.csv","orbis_control_ids.csv")
    control_ids=combine_ids_unique("amadeus_control_ids.csv","orbis_control_ids.csv")
    
    chdir_id()
    #combined=combine_ids_unique(amadeus_not_subsidized_ids,orbis_not_subsidized_ids) #namen nicht df
    control_ids["treatment"]=0
    control_ids.to_csv("all_not_subsidized_ids.csv")

def create_all_id_csv(): #vieleicht naming nochmal überarbeiten
    all_subsidized_ids()
    all_not_subsidized_ids()
    combined=combine_ids_unique("all_subsidized_ids.csv","all_not_subsidized_ids.csv")
    combined.to_csv("all_ids.csv")









