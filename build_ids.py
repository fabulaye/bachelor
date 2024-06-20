import pandas as pd
import os
from datahandling.change_directory import chdir_data
from load_config import orbis_not_subsidized,amadeus_not_subsidized,orbis_subsidized_filtered,amadeus_subsidized_filtered,amadeus_not_subsidized_ids,orbis_not_subsidized_ids,amadeus_subsidized_ids,orbis_subsidized_ids

def create_amadeus_id_csv(amadeus_csv_name,id_csv_name):
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
    amadeus_df=pd.read_csv(amadeus_csv_name,index_col=False) #zu csv switchen
    df=amadeus_df["idnr"]
    df=df.drop_duplicates()
    df=df.rename("bvdid",inplace=True)
    print(df)
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data/id")
    df.to_csv(id_csv_name)
    return df

def create_orbis_id_csv(orbis_csv_name,id_csv_name):
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
    orbis_df=pd.read_csv(orbis_csv_name,index_col=False) #zu csv switchen
    print(orbis_df)
    df=orbis_df["bvdid"]
    df=df.drop_duplicates()
    #df.rename(column="bvdid")
    print(df)
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data/id")
    df.to_csv(id_csv_name)
    return df

def create_all_id_csv(): #vieleicht naming nochmal überarbeiten
    subsidized_ids_amadeus=create_amadeus_id_csv(amadeus_subsidized_filtered,amadeus_subsidized_ids)
    subsidized_ids_orbis=create_orbis_id_csv(orbis_subsidized_filtered,orbis_subsidized_ids)
    df=pd.concat([subsidized_ids_amadeus,subsidized_ids_orbis],ignore_index=True)
    df=df.to_frame(name="bvdid")
    df['treatment']=1
    not_subsidized_ids_orbis=create_orbis_id_csv(orbis_not_subsidized,amadeus_not_subsidized_ids)
    not_subsidized_ids_orbis=not_subsidized_ids_orbis.to_frame()
    not_subsidized_ids_amadeus=create_amadeus_id_csv(amadeus_not_subsidized,orbis_not_subsidized_ids)
    not_subsidized_ids_amadeus=not_subsidized_ids_amadeus.to_frame()
    not_subsidized_ids_orbis["treatment"]=0
    not_subsidized_ids_amadeus["treatment"]=0
    df=pd.concat([df,not_subsidized_ids_orbis,not_subsidized_ids_amadeus])
    df.drop_duplicates(subset="bvdid")
    df.to_csv("all_ids.csv")
    return df









