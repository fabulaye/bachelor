from import_manager import import_file_manager,import_cleaner
import_file_manager()
import_cleaner()
from file_manager.json_to_dict import json_to_dict
from file_manager.dict_to_json import dict_to_json
from file_manager.change_directory import chdir_data
from cleaner.return_rechtsform import return_rechtsform

chdir_data()
gaming_company_names_handelsregister=json_to_dict("gaming_company_names_handelsregister.json")
companies_not_found_in_handelsregister=json_to_dict("companies_not_found_in_hr.json")
gaming_company_data_handelsregister=json_to_dict("gaming_company_data_handelsregister.json")



#rechtsform regex haben wir

def create_gaming_company_names_and_rechtsform():
    full_dict={}
    for company_with_rechtsform in gaming_company_names_handelsregister:
        rechtsform=return_rechtsform(company_with_rechtsform)
        company_name=company_with_rechtsform.rstrip(rechtsform).rstrip()
        full_dict[company_name]={"rechtsform":rechtsform,"in_hr":True}
    for company_without_rechtsform in companies_not_found_in_handelsregister:
        full_dict[company_without_rechtsform]={rechtsform:None,"in_hr":False}
    return full_dict    

gaming_company_names_and_rechtsform=create_gaming_company_names_and_rechtsform()
dict_to_json(gaming_company_names_and_rechtsform,"gaming_company_names_and_rechtsform")


def add_hr_data(dict): #wir fügen unserem dict die handelsregister_data hinzu
    for company_name,data_dict in gaming_company_data_handelsregister.items():
        rechtsform=return_rechtsform(company_name)
        print(rechtsform)
        company_name=company_name.rstrip(rechtsform).rstrip()
        print(company_name)
        try:
            dict[company_name].update(data_dict)
        except:
            print(f"{company_name} not found in dict")    
    return dict    
      
gaming_company_names_and_rechtsform=json_to_dict("gaming_company_names_and_rechtsform.json")


gaming_companies_data=add_hr_data(gaming_company_names_and_rechtsform)
dict_to_json(gaming_companies_data,"gaming_company_data")


