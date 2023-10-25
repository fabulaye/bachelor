def update_all_company_json():
      companies_dir="C:/Users/lukas/Desktop/bachelor/data/companies"
      data_dict={}
      for company_name,company_object in company_object_dict.items():
            for year,account_object in company_object.annual_accounts.items():
                  data_dict[year]=account_object.dict
            #data_dict=company_object.annual_accounts
            json_to_dict(data_dict,company_name,directory=companies_dir)

#update_all_company_json()