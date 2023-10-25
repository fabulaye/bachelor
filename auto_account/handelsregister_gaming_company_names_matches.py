from json_to_dict import json_to_dict()



def create_list_of_matching_names_handelsregister(company_names):
      handelsregister_company_names=json_to_dict("handelsregister_company_names")["names"]
      companies_in_handelsregister=[]
      for company_name in company_names:

            try:
                  if company_name in handelsregister_company_names:
                        companies_in_handelsregister.append(company_name)
            except:
                  None     
      return companies_in_handelsregister