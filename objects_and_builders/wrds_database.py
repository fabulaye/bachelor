import importlib.util
import sys
import os
import pandas as pd

def import_module_from_path(module_name, file_path):
    # Ensure the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Create a module spec from the file location
    spec = importlib.util.spec_from_file_location(module_name, file_path)

    if spec is None:
        raise ImportError(f"Cannot create a module spec for {module_name} from {file_path}")

    # Create a module object from the spec
    module = importlib.util.module_from_spec(spec)

    # Add the module to sys.modules
    sys.modules[module_name] = module

    # Execute the module
    spec.loader.exec_module(module)

    return module


wrds_connection=import_module_from_path("wrds_connection",r"C:\Users\lukas\Documents\GitHub\bachelor\sql_requests\wrds_connection.py")

#from sql_requests import wrds_connection



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
                                      
                                      "ob_contact_info"
]

low_prio_orbis_tables=["ob_additional_company_info","ob_branches","ob_hq","ob_industry_classifications","ob_trade_description",] +orbis_principal_and_agents_tables

orbis_tables=orbis_financial_tables+orbis_general_and_description_tables

amadeus_tables=["company","activities","managers","overview","shareholders","subsidiaries","financials","ish_duo_guo"]

amadeus_size_dict={"small":"s","medium":"m","large":"l","verylarge":"v"}
orbis_sizes=["small","medium","large"]
amadeus_sizes=["small","medium","large","verylarge"]

from request_builder import amadeus_request,orbis_request,wrds_request,request_builder

class wrds_database():
    def __init__(self,tables,sizes,connection):
        self.connection=connection
        self.tables=tables
        self.sizes=sizes
        self.request_object=None #if orbis then
        self.request_builder=request_builder()
    def id_requests(self,ids):
        for table in self.tables:
            if isinstance(self,orbis_database):
                self.request_object=self.request_builder.build_orbis(connection)   
            elif isinstance(self,amadeus_database):
                self.request_object=self.request_builder.build_amadeus(connection)
            #müssen wir das request_object austauschen? neues initialisieren
            self.request_object.ids=ids
            self.request_object.sizes=self.sizes
            self.request_object.table_name=table
            self.request_object.id_request(self.connection) #parameter für id oder so in der functiion oder seperate functions?
    def general_requests():
        None
        



class amadeus_database(wrds_database):
    def __init__(self,tables,sizes,connection):
        super().__init__(tables,sizes,connection)
        #use build request to pass size,etc.
        #self.request_object=self.request_builder.build_amadeus(connection)
    def id_requests(self, ids):
        #self.request_object=self.request_builder.build_amadeus(connection)
        return super().id_requests(ids)



class orbis_database(wrds_database):
    def __init__(self,tables,sizes,connection):
        super().__init__(tables,sizes,connection)
        #use build request to pass size,etc.
        #self.request_object=self.request_builder.build_orbis(connection)
    def id_requests(self, ids):
       # self.request_object=self.request_builder.build_orbis(connection) #ich kann hier nicht bauen weil ich im id requests loop bleibe das heißt loop muss hier gebaut werden
        return super().id_requests(ids)

#########
ids=tuple(pd.read_csv(r"C:\Users\lukas\Desktop\bachelor\data\id\all_treatment_ids.csv")["bvdid"].to_list())
#das hier teil der objekte machen
connection=wrds_connection.start_connection()
#orbis=orbis_database(orbis_tables,orbis_sizes,connection)
#orbis.id_requests(ids)
amadeus=amadeus_database(amadeus_tables,amadeus_sizes,connection)
amadeus.id_requests(ids)
