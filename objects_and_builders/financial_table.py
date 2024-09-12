
import pandas as pd
#from lukasdata import import_manager
from datahandling.change_directory import chdir_data
import sqlite3
from datahandling.json_to_dict import json_to_dict
from datahandling.change_directory import chdir_data,chdir_sql_requests

chdir_data()
var_map=json_to_dict("map.json")

chdir_sql_requests()
financial_tables=["ob_cflow_non_us_ind_eur_intbvd_orbis","ob_cflow_non_us_ind_eurbvd_orbis","ob_cflow_us_ind_eurbvd_orbis","ob_detailed_fmt_ind_eurbvd_orbis","ob_detailed_fmt_ind_eur_intbvd_orbis","ob_ind_g_fins_eur_intbvd_orbis","ob_ind_g_fins_eurbvd_orbis","ob_key_financials_eurbvd_orbis","financialsbvd_ama","ish_duo_guobvd_ama"]


#cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# Fetch all table names
#tables = cursor.fetchall()

class financial_table():
    def __init__(self) -> None:
        self.tables=None
        self.map=None
        self.merged=None
    def merge_financial(self):
        for index,table in enumerate(self.tables):
            if index==0:
                df=table
            else:
                df=df.merge(table,on="bvdid",how="outer")
        self.merged=df
    def to_csv(self,filename):
        self.merged.to_csv(filename)


class financial_table_builder():
    def __init__(self) -> None:
        self.financial_table=financial_table()
        

    def build_financial_table(self):
        table_objects=[]
        for table_name in financial_tables:
            table=sql_table(table_name).build_df()
            table_objects.append(table)
        self.financial_table.tables=table_objects
        self.financial_table.map=var_map
        return self.financial_table

financial_table=financial_table_builder().build_financial_table()
financial_table.merge_financial()
financial_table.to_csv("merged_table_test.csv")
#get all neccesary tables
#df merge mit financial_table
#map zum renamen nutzen??


