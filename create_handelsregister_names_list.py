from load_handelsregister import handelsregister
from dict_to_json import dict_to_json

def create_handelsregister_companies_names_list():
      handelsregister_companies_names=[]
      counter=0
      for object in handelsregister:
            handelsregister_companies_names.append(object["name"])
      return handelsregister_companies_names   

names_list=create_handelsregister_companies_names_list()   

dict={"handelsregister_company_names":names_list}
dict_to_json(dict,"handelsregister_company_names")