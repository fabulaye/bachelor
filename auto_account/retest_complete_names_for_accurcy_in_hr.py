from import_manager import import_all_libraries
import_all_libraries()
from file_manager.json_to_dict import json_to_dict
from file_manager.change_directory import chdir_data
from file_manager.dict_to_json import dict_to_json



def create_list_of_matching_names_handelsregister(company_names):
      handelsregister_company_names=json_to_dict("handelsregister_company_names.json")
      matches=[]
      mismatches=[]
      for company_name in company_names:
            if company_name in handelsregister_company_names:
                  matches.append(company_name)
            else:            
                  mismatches.append(company_name)
                     
      return matches,mismatches


chdir_data()
gaming_company_names_handelsregister=json_to_dict("gaming_company_names_handelsregister.json")
matches,mismatches=create_list_of_matching_names_handelsregister(gaming_company_names_handelsregister)
dict_to_json(mismatches,"companies_not_found_in_hr")

