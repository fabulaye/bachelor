from load_handelsregister import handelsregister
from import_manager import import_file_manager
import_file_manager()
from file_manager.json_to_dict import json_to_dict
from file_manager.dict_to_json import dict_to_json
import regex as re
from file_manager.change_directory import chdir_data

chdir_data()
gaming_company_names=json_to_dict("gaming_company_names.json")["names"]

#
def create_handelsregister_subset(list_of_subset_names):
      dict={}          
      for company_entry in handelsregister:
            name=company_entry["name"]
            if name in list_of_subset_names:
                  dict[name]=company_entry                    
      return dict #todo weakes naming


dict=create_handelsregister_subset(gaming_company_names)
dict_to_json(dict,"gaming_companies_handelsregister")

#lasse ich das hier so oder probiere ich irgenwie das hr dataset zu strippen?
