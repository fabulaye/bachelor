import pandas as pd
from datahandling.determine_file_type import determine_file_type,strip_file_ending
dtype_to_sql = {
            	'int64': 'INTEGER',
            	'int32': 'INTEGER',
            	'float64': 'REAL',
            	'float32': 'REAL',
            	'bool': 'BOOLEAN',
            	'datetime64[ns]': 'TIMESTAMP',
            	'timedelta64[ns]': 'TEXT',  # TIMESTAMP difference usually stored as text or integer
            	'object': 'TEXT',  # Typically for strings
            	'string': 'TEXT',  # String dtype in newer versions of Pandas
            	'category': 'TEXT'  # Categories can be stored as TEXT or INTEGER
                                    } 

class sql_table():
    def __init__(self):
        #super().__init__()
        self.table_name=None
        self.composite_keys=None
        self.columns=None
        self.column_definitions=None
        self.df=None
        self.data_matrix=None
        self.potential_keys=["idnr","bvdid","year","closdate_year","prevname","_9300","natid_number","conscode"]
    def build_column_definitions(self):
        column_datatypes=self.df.dtypes
        string_list=[]
        for column in self.df.columns:
            py_datatype=str(column_datatypes[column])
            string=f"{column} {dtype_to_sql[py_datatype]}"
            string_list.append(string)
        present_key_columns=[column for column in self.df.columns if column in self.composite_keys]
        key_string=",".join(present_key_columns)
        key_string=f"PRIMARY KEY ({key_string})"
        string_list.append(key_string)
        columns_and_description=",".join(string_list)
        self.column_definitions=columns_and_description
        return self.column_definitions
    def check_existing_values(self):
        self[self.present_keys]    
    
file_endings=["pdf","json","txt","xlsx","db","csv"]
def determine_file_type(file_name): #vielleicht in einem anderen module?
      #datatype=re.search(datatype_regex,file_name).group()
      for file_ending in file_endings:
            if file_name.endswith(file_ending):
                  return file_ending
      #file_type=file_type_regex.findall(file_name)[0].lstrip(".")
      #return file_type

import regex as re

re.search

def strip_file_ending(file_name):
      file_type=determine_file_type(file_name)
      to_strip="."+file_type
      stripped=file_name.replace(to_strip,"")
      return stripped

class sql_table_builder():
    def __init__(self) -> None:
        self.sql_table=sql_table()
    def build_table(self,df_path):
        self.sql_table.df=pd.read_csv(df_path)
        self.sql_table.file_type=determine_file_type(df_path)
        self.sql_table.table_name=strip_file_ending(df_path)
        self.sql_table.columns=self.sql_table.df.columns
        self.sql_table.composite_keys=[key for key in self.sql_table.potential_keys if key in self.sql_table.columns]
        self.sql_table.placeholders = ', '.join(['?' for _ in self.sql_table.df.columns])
        self.sql_table.data_matrix=[row.to_list() for index,row in self.sql_table.df.iterrows()]
        return self.sql_table

#use it as a interface between a df and a sql table:
    #from the df : build 




