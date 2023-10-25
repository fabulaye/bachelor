from my_regex import return_regex_hits,create_company_regex
from json_to_dict import json_to_dict

def add_rechtsform_to_excel(incomplete_names): #the excel dataset doesnt include the full name of the company thats why we have to search it
      handelsregister_company_names=json_to_dict("handelsregister_company_names")["names"]
      full_names=[]
      for name in incomplete_names:
            regex=create_company_regex(name)
            for company in handelsregister_company_names: #for company in handelsregister: 
                  search=regex.findall(company)
                  result=return_regex_hits(search)
                  full_names.append(result)