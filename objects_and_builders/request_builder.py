import os
import pandas as pd
from objects_and_builders.query_builder import query_builder
from processing.my_list import upper_list
from objects_and_builders.wrds_table import wrds_table,table_builder
from datahandling.json_to_dict import json_to_dict



class search_list(list):
    def __init__(self,*args):
        super().__init__(*args)
    def to_csv(self,filename):
        pd.Series(self,name="name_nat").to_csv(filename,index=False)
    def remove_list(self,lst):
        for item in lst:
            try:
                self.remove(item)
            except ValueError:
                None


class wrds_request():
    def __init__(self) -> None:
        self.connection=None
        self.names_tuple=()
        self._df=pd.DataFrame()
        self.found=search_list()
        self.not_found=search_list(self.names_tuple)
        self.ids=None
        self.query=None 
        self.table=None
        self.table_builder=table_builder()
        self.query_builder=query_builder()
        self.table_name=None
        self.sizes=None
    def set_names(self,names):
        self.names_tuple=tuple(list(map(lambda x:x.upper(),names)))
        self.not_found=search_list(self.names_tuple)
        #wir machen hier nur requests die abhängig von der größe sind, das heißt wir initiaten die class mit einem table name
    def table_workflow(self,size_long):
        if type(self)==orbis_request:
            self.table=self.table_builder.build_orbis()
        elif type(self)==amadeus_request:
            self.table=self.table_builder.build_amadeus()
             #ich muss hier wissen ob ich amadeus oder orbis bauen soll
        self.table.set_size_and_name(size_long,self.table_name)
    def general_request(self,search_params={"how":"exact"},output_file_name=None,output_path=None):
        if len(self.not_found)!=0:
            len_tuple=len(self.not_found) #not_found
            for index,name in enumerate(self.not_found):
                print(f"{name} is currently being searched ({index}/{len_tuple})")
                for size_long in self.sizes: #this is the sizes small,large etc.
                    self.table_workflow(size_long)
                    #self.table=wrds_table(self.table_name,size_long)
                    path=self.table.build_path()
                    request_str=self.query.build_general_query_string(path,name,search_params) 
                    request=self.connection.raw_sql(request_str)
                    if not request.empty:
                        #full_df=concat_dfs([full_df,request])
                        self._df=pd.concat([self._df,request])  
            try:
                found_entries=upper_list(list(self._df[self.name_id]))
                self.found = found_entries
            except KeyError:
                print("no entries found")
            self.not_found.remove_list(self.found)
            if output_path!=None:
                os.chdir(path)
            #if output_file_name!=None:
                #self._df.to_csv(output_file_name)  
        csv_name=self.table_name+self.table.database_prefix+".csv"
        self._df.to_csv(csv_name)
        self.not_found.to_csv("not_found.csv")
        return self
    def id_request(self):
        #chdir_sql_requests()
        wrds_map=pd.read_csv(r"C:\Users\lukas\Desktop\bachelor\data\map.csv").to_dict()
        for size_long in self.sizes:
            self.table_workflow(size_long)
            path=self.table.build_path() #hier müssen wir parameter einfügen um zu setten
            sql=self.query.build_id_query_string(path,self.ids)
            #ids_as_array = '{' + ','.join(map(str, self.ids)) + '}'
            request_table=self.connection.raw_sql(sql)
            self._df=pd.concat([self._df,request_table],ignore_index=True)
        csv_name=self.table_name+self.table.database_prefix+".csv"
        self._df.rename(wrds_map)
        self._df.to_csv(csv_name,index=False)
    #def get_ids(self):
        #self.ids=id_dict(self._df)
        #return self.ids



class orbis_request(wrds_request):
    def __init__(self) -> None:
        super().__init__()
        self.name_id="name_native"       

class amadeus_request(wrds_request):
    def __init__(self) -> None:
        super().__init__()
        self.name_id="name_nat"        

class request_builder():
    def __init__(self) -> None:
        self.table=None
        self.query=None
    def build_amadeus(self,connection):
        amadeus=amadeus_request()
        amadeus.connection=connection
        amadeus.table=table_builder().build_amadeus()
        amadeus.query=query_builder().build_amadeus() #wir returnen nicht den string, wir müssen determinen ob wir id oder generel query wollen, könnte auch build query machen und danach build id_string oder so nochmal drauf
        return amadeus
        #and so forth
    def build_orbis(self,connection):
        orbis=orbis_request()
        orbis.connection=connection
        orbis.table=table_builder().build_orbis()
        orbis.query=query_builder().build_orbis()
        return orbis

    #lieber eine buld amadeus_request method hier im allgmeinen builder


