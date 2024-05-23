from import_manager import import_file_manager,import_cleaner
import_cleaner()
import_file_manager()
from file_manager.json_to_dict import json_to_dict
from file_manager.change_directory import chdir_data
from file_manager.list_to_string import list_to_string
from file_manager.dict_to_json import dict_to_json
import regex as re


chdir_data()
excel_names=json_to_dict("gaming_company_names_excel.json")["names"]
full_names=json_to_dict("gaming_company_names_handelsregister.json")


def search_gaming_companies(excel_names,full_names):
    full_names=list_to_string(full_names)
    not_found=[]
    for name in excel_names:
        regex_pattern=re.compile(name)
        search=regex_pattern.findall(full_names)
        print(search)
        if search==[]:
            not_found.append(name)
    return not_found
        #if search


not_found=search_gaming_companies(excel_names,full_names)

print(len(excel_names))
print(len(full_names))
print(len(not_found))
dict_to_json(not_found,"companies_not_found_in_hr")






