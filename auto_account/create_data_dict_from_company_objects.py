def create_data_dict_from_company_objects(company_object_dict):
      data_dict={}
      for company_name,company_object in company_object_dict.items():
            data_dict[company_name]={}
            for year,annual_account_object in company_object.annual_accounts.items():
                  data_dict[company_name][year]=annual_account_object.dict
      return data_dict            