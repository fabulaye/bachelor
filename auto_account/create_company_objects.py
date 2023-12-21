from import_manager import import_all_libraries
import_all_libraries()
from cleaner.name_cleaning import standardize_name
from file_manager.json_to_dict import json_to_dict
from file_manager.change_directory import chdir_data
from company_object import company


def create_company_objects():
   chdir_data()
   company_id=0
   gaming_company_data=json_to_dict("gaming_company_data.json") #wir wollen full nicht den bumms hier renamen!!!!
   company_object_dict={}
   #global company_id
   for company_name,attributes in gaming_company_data.items(): #aktuell sind die namen noch nicht standadized!!!
      standardized_company_name=standardize_name(company_name)
      print(standardized_company_name)
      try:
         fed_state=attributes["all_attributes"]["federal_state"]
         rechtsform=attributes["rechtsform"]
      except:
         fed_state=None
         rechtsform=None
      company_object_dict[standardized_company_name]=company(company_id,standardized_company_name,rechtsform,fed_state)
      company_id+=1   
   return company_object_dict

