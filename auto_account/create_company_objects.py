from import_manager import import_all_libraries
import_all_libraries()
from cleaner.name_cleaning import return_rechtsform,standardize_name
from file_manager.json_to_dict import json_to_dict
from file_manager.change_directory import chdir_data
from company_object import company


def create_company_objects():
    chdir_data()
    company_id=0
    gaming_companies_handelsregister=json_to_dict("gaming_companies_handelsregister.json")
    company_object_dict={}
    #global company_id
    for company_name,attributes in gaming_companies_handelsregister.items(): #aktuell sind die namen noch nicht standadized!!!
      rechtsform=return_rechtsform(company_name)
      standardized_company_name=standardize_name(company_name)
      company_object_dict[standardized_company_name]=company(company_id,standardized_company_name,rechtsform,attributes["all_attributes"]["federal_state"])
      company_id+=1
    return company_object_dict

              
name=standardize_name("3d-io Games GmbH")    
print(name)          