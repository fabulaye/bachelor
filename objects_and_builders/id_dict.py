import pandas as pd
import os
from datahandling.change_directory import chdir_data

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
    def get_ids(self):
        return self["bvdid"].to_list()
    def to_csv(self,filename,drop_duplicates=True):
        os.chdir(f"C:/Users/Lukas/Desktop/bachelor/data/id")
        df=pd.DataFrame(self)
        if drop_duplicates:
            df.drop_duplicates(subset=["bvdid"],inplace=True)
        df.to_csv(filename,index=False)
    








