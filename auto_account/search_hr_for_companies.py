from my_regex import return_regex_hits,create_company_regex
from import_manager import import_file_manager
import_file_manager()
from file_manager.json_to_dict import json_to_dict
from file_manager.dict_to_json import dict_to_json
from file_manager.change_directory import chdir_data
from runtime_test import runtime_test,start_timer


def search_hr_for_companies(incomplete_names): #the excel dataset doesnt include the full name of the company thats why we have to search it
      handelsregister_company_names=json_to_dict("handelsregister_company_names.json")["handelsregister_company_names"]
      full_names=[]
      not_found=[]
      for name in incomplete_names:
            print(name)
            regex=create_company_regex(name)
            for company in handelsregister_company_names: #for company in handelsregister: 
                  search=regex.findall(company)
                  result=return_regex_hits(search)
                  if result!=None:
                        result=result.rstrip()
                        full_names.append(result)
                        del(company) #neu
                        print(result)
                        break #problem bei namen die doppelt sind wie bei Crytek
                    
      return full_names      


chdir_data()
excel_names=json_to_dict("gaming_company_names_excel.json")["names"]
search_hr_for_companies(excel_names)
names=search_hr_for_companies(excel_names)
dict_to_json(names,"gaming_company_names_handelsregister")
