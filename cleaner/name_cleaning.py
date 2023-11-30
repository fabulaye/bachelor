import regex as re





def strip_rechtsform(company_name):
    rechtsform_regex_search=rechtsform_regex.findall(company_name)[0]
    if rechtsform_regex_search!="":
        company_name=company_name.rstrip(rechtsform_regex_search).lower().rstrip()
    return company_name     

      

def standardize_name(company_name):
    company_name=company_name.lower()
    #company_name=company_name.replace(" ","_") 
    company_name=company_name.rstrip()
    return company_name  


def standardize_company_names(data): #that shits now bugged
      if type(data)==dict:
            if len(dict)>1:
                  for company_name,attributes in data.items():
                        standardized_names=standardize_name(company_name)
            if len(dict)==1:            
                  for company_name in data.values()[0]:
                        standardized_names=standardize_name(company_name)
      if type(data)==list:
            for company_name in data:
                  standardized_names=standardize_name(company_name)           
      return standardized_names


