from create_dict_from_handelsregister import create_dict_of_specific_companies_in_handelsregister
from json_to_dict import json_to_dict
from dict_to_json import dict_to_json
from change_directory import chdir_data
chdir_data()
company_names_excel=json_to_dict("gaming_company_names_excel.json")["names"]
print(company_names_excel)
dict=create_dict_of_specific_companies_in_handelsregister(company_names_excel)
print(dict)
dict_to_json(dict,"gaming_companies_handelsregister")

#wir brauchen 3dio im dataset