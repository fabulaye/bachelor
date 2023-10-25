from load_handelsregister import handelsregister
from json_to_dict import json_to_dict
from dict_to_json import dict_to_json
import regex as re
from change_directory import chdir_data

chdir_data()
gaming_company_names=json_to_dict("gaming_company_names.json")["names"]

#
def create_handelsregister_gaming_subset():
      dict={}          
      for company_entry in handelsregister:
            name=company_entry["name"]
            if name in gaming_company_names:
                  dict[name]=company_entry                    
      return dict #todo weakes naming


dict=create_handelsregister_gaming_subset()
dict_to_json(dict,"gaming_companies_handelsregister")


