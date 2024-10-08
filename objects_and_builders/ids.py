import pandas as pd
import os
from datahandling.change_directory import chdir_data
import regex as re
from processing.format_string import format_df

class ids():
    def __init__(self,df_list) -> None:
        combined_df=pd.concat(df_list)
        combined_df=format_df(combined_df)
        combined_df=delete_branch_ids(combined_df)
        try:
            combined_df.drop_duplicates(subset=["bvdid","name"],inplace=True)
        except TypeError:
            print("combined df is series")
        self._df=combined_df
    def concat_ids(self,csv_df):
        if isinstance(csv_df,str):
            csv_df=pd.read_csv(csv_df)
        csv_df=format_df(csv_df)
        csv_df=delete_branch_ids(csv_df)
        concat_df=pd.concat(self._df,csv_df)
        self._df=concat_df
        return self
    def get_ids(self):
        if isinstance(self._df,pd.Series):
            return self._df.to_list()
        if isinstance(self._df,pd.DataFrame):
            return self._df["bvdid"].to_list()
    def to_csv(self,filename):
        os.chdir(f"C:/Users/Lukas/Desktop/bachelor/data/id")
        self._df.to_csv(filename,index=False)
    



def delete_branch_ids(df):
        branch_regex=re.compile("-\d{4}$")
        def check_if_not_branch(id):
            try:
                search=branch_regex.findall(id)
            except TypeError:
                return False
            if len(search)==0:
                return True
            else:
                return False
        bvdid=df["bvdid"]
        bvdid_data=[]
        
        for i in range(len(bvdid.columns)):
            bvdid_data.append(bvdid.iloc[:,i])
        bvdid=pd.concat(bvdid_data)
        #einfach combinen ist scheißt egal hier.
        indexer=list(map(check_if_not_branch,bvdid.to_list()))
        bvdid=bvdid[indexer]
        return bvdid
