from name_cleaning import return_rechtsform,standardize_name

company_id=0

def create_company_objects():
    company_object_dict={}
      global company_id
      for company_name,attributes in gaming_companies_handelsregister.items(): #aktuell sind die namen noch nicht standadized!!!
                  rechtsform=return_rechtsform(company_name)
                  standardized_company_name=standardize_name(company_name)
                  company_object_dict[standardized_company_name]=company(company_id,standardized_company_name,rechtsform,attributes["all_attributes"]["federal_state"])
                  company_id+=1