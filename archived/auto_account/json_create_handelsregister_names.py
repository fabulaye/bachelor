
from load_handelsregister import handelsregister
from import_manager import import_file_manager
import_file_manager()
from file_manager.dict_to_json import dict_to_json

def create_handelsregister_companies_names_list():
      handelsregister_companies_names=[]
      for object in handelsregister:
            handelsregister_companies_names.append(object["name"])
      return handelsregister_companies_names   

names_list=create_handelsregister_companies_names_list()   


dict_to_json(names_list,"handelsregister_company_names")