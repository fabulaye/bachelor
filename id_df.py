import pandas as pd
import os

def create_amadeus_id_csv(amadeus_csv_name,id_csv_name):
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
    amadeus_df=pd.read_csv(amadeus_csv_name) #zu csv switchen
    df=amadeus_df["idnr"]
    df=df.drop_duplicates()
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data/id")
    df.to_csv(id_csv_name)
    return df

def create_orbis_id_csv(orbis_csv_name,id_csv_name):
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
    orbis_df=pd.read_csv(orbis_csv_name) #zu csv switchen
    df=orbis_df["bvdid"]
    df=df.drop_duplicates()
    df.columns=["id"]
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data/id")
    df.to_csv(id_csv_name)
    return df


subsidized_ids_amadeus=create_amadeus_id_csv("subsidized_amadeus.csv","subsidized_amadeus_ids_de.csv")

subsidized_ids_orbis=create_orbis_id_csv("subsidized_orbis.csv","subsidized_orbis_ids_de.csv")

subsidized_ids=pd.concat([subsidized_ids_amadeus,subsidized_ids_orbis]).unique()
pd.DataFrame(subsidized_ids).to_csv("subsidized_ids_de.csv")

german_companies=pd.read_csv("german_companies_amadeus.csv")
from manipulation.create_mask import create_in_mask

subsidized_mask=create_in_mask(german_companies.iloc[:,1],subsidized_ids)

not_subsidized_de=german_companies.reset_index(drop=True)[~subsidized_mask]
not_subsidized_de.to_csv("not_subsidized_amadeus_de.csv")

not_subsidized_ids_de=not_subsidized_de["idnr"]
not_subsidized_ids_de.to_csv("id/not_subsidized_ids_de.csv")





