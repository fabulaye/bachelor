
def check_flags(company_object_dict):
    flag_dict={}
    for company_name,company_object in company_object_dict.items():
           flag_dict[company_name]={}
           for year,annual_account_object in company_object.annual_accounts.items():
                 annual_account_object.check_flags()
                 flag_dict[company_name][year]=annual_account_object.flag_dict
    return flag_dict

