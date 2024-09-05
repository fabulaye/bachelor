import pandas as pd
import os
from datahandling.change_directory import chdir_data
#from load_config import orbis_not_subsidized,amadeus_not_subsidized,orbis_subsidized_filtered,amadeus_subsidized_filtered,amadeus_not_subsidized_ids,orbis_not_subsidized_ids,amadeus_subsidized_ids,orbis_subsidized_ids

#ich mache das id zeug und validierung kommt in die company structure

def chdir_id():
      os.chdir(f"C:/Users/Lukas/Desktop/bachelor/data/id")

class id_dict(dict):
    def __init__(self,df) -> None:
        super().__init__()
        self=self.append_ids(df)
        self.database=None
    def append_ids(self,csv_df):
        if isinstance(csv_df,str):
            csv_df=pd.read_csv(csv_df)
        columns=list(csv_df.columns)
        dict_to_append={}
        if "bvdid" in columns:
            self.database="orbis"
            dict_to_append["bvdid"]=csv_df["bvdid"]
            dict_to_append["names"]=csv_df["name_native"]
        elif "idnr" in columns:
            self.database="amadeus"
            dict_to_append["bvdid"]=csv_df["idnr"]
            dict_to_append["names"]=csv_df["name_nat"]
        self.update(dict_to_append)
        return self
    def to_csv(self,filename,drop_duplicates=True):
        os.chdir(f"C:/Users/Lukas/Desktop/bachelor/data/id")
        df=pd.DataFrame(self)
        if drop_duplicates:
            df.drop_duplicates(subset=["bvdid"],inplace=True)
        df.to_csv(filename,index=False)
    


    #treatment,drop_duplicates?,combined=combined.drop_duplicates(subset=["bvdid"])

#os.chdir(r"C:\Users\lukas\Desktop\bachelor\data\complete_search")
#data_df=pd.read_csv("like_request_orbis_subsidized.csv")
#more_data=pd.read_csv("orbis_exact_search_incomplete.csv")

#ids=id_dict(data_df)
#ids=ids.append_ids(more_data)








