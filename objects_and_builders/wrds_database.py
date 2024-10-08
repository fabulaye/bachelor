
import os
import pandas as pd

from debugging.import_module_from_path import import_module_from_path


wrds_connection=import_module_from_path("wrds_connection",r"C:\Users\lukas\Documents\GitHub\bachelor\sql_requests\wrds_connection.py")
request_builder_module=import_module_from_path("request_builder",r"C:\Users\lukas\Documents\GitHub\bachelor\objects_and_builders\request_builder.py")




orbis_financial_tables=["ob_cflow_non_us_ind_eur_int",
                        "ob_cflow_non_us_ind_eur",
                        "ob_cflow_us_ind_eur",
                        "ob_detailed_fmt_ind_eur",
                        "ob_detailed_fmt_ind_eur_int",
                        "ob_ind_g_fins_eur_int",
                        "ob_ind_g_fins_eur",
                        "ob_key_financials_eur"]

orbis_principal_and_agents_tables=["ob_all_subs_first_level",
                      "ob_basic_shareholder_info",
                      "ob_controlling_shareholders",
                      "ob_dmc_current_only",
                      "ob_dmc_previous",
                      "ob_all_cur_shh_1st_level"
                ]

orbis_general_and_description_tables=[
                                      "ob_all_subs_first_level",
                                      
                                      
                                      "ob_identifiers",
                                      
                                      "ob_legal_info",
                                      
                                      "ob_contact_info",
                                      "ob_branches"
]

low_prio_orbis_tables=["ob_additional_company_info","ob_branches","ob_hq","ob_industry_classifications","ob_trade_description",] +orbis_principal_and_agents_tables

orbis_tables=orbis_financial_tables+orbis_general_and_description_tables

amadeus_tables=["company","activities","managers","overview","shareholders","subsidiaries","financials","ish_duo_guo"]

amadeus_size_dict={"small":"s","medium":"m","large":"l","verylarge":"v"}
orbis_sizes=["small","medium","large"]
amadeus_sizes=["small","medium","large","verylarge"]



class wrds_database():
    def __init__(self,tables,sizes,connection,path=None):
        self.connection=connection
        self.tables=tables
        self.sizes=sizes
        self.request_object=None #if orbis then
        self.request_builder=request_builder_module.request_builder()
        self.path=path
        self.names=None
    def request(self,how,ids=None,names=None):
        if self.path!=None:
            os.chdir(self.path)
        if how=="general":
            if isinstance(self,orbis_database):
                    self.request_object=self.request_builder.build_orbis(self.connection) 
                    self.request_object.table_name="ob_contact_info"
            elif isinstance(self,amadeus_database):
                    self.request_object=self.request_builder.build_amadeus(self.connection)
                    self.request_object.table_name="company"
            self.request_object.sizes=self.sizes
            self.request_object.set_names(names)
            self.request_object.general_request()
        elif how=="id":
            for table in self.tables:
                if isinstance(self,orbis_database):
                    self.request_object=self.request_builder.build_orbis(self.connection)   
                elif isinstance(self,amadeus_database):
                    self.request_object=self.request_builder.build_amadeus(self.connection)
                #müssen wir das request_object austauschen? neues initialisieren
                self.request_object.ids=ids
                self.request_object.sizes=self.sizes
                self.request_object.table_name=table
                if how=="id":
                    self.request_object.id_request()
                #parameter für id oder so in der functiion oder seperate functions?
                
        
class amadeus_database(wrds_database):
    def __init__(self,tables,sizes,connection,path):
        super().__init__(tables,sizes,connection,path)
        #use build request to pass size,etc.
        #self.request_object=self.request_builder.build_amadeus(connection)


class orbis_database(wrds_database):
    def __init__(self,tables,sizes,connection,path):
        super().__init__(tables,sizes,connection,path)
        #use build request to pass size,etc.
        #self.request_object=self.request_builder.build_orbis(connection)


#########

def full_workflow(how,path=None,ids=None,names=None):
    connection=wrds_connection.start_connection()
    orbis=orbis_database(orbis_tables,orbis_sizes,connection,path)
    orbis.request(how=how,ids=ids,names=names)
    amadeus=amadeus_database(amadeus_tables,amadeus_sizes,connection,path)
    amadeus.request(how=how,ids=ids,names=names)



