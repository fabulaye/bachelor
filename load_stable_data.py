from load_handelsregister import handelsregister
from json_to_dict import json_to_dict
import pandas as pd


handelsregister_companies_names=json_to_dict("handelsregister_company_names.json")["names"]
company_names_excel=json_to_dict("gaminng_company_names_excel.json")["names"]
gaming_companies_handelsregister=create_dict_of_specific_companies_in_handelsregister(company_names_excel)
