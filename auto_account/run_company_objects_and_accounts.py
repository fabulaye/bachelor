from create_company_objects import create_company_objects
from create_annual_account_objects import create_annual_account_objects,initialize_data_assignment_for_annual_accounts,assign_text_to_account_objects
from create_data_dict_from_company_objects import create_data_dict_from_company_objects
from check_flags import check_flags
from import_manager import import_file_manager
import_file_manager()
from file_manager.dict_to_json import dict_to_json
import pandas as pd
import os




company_object_dict=create_company_objects()
print(company_object_dict)

create_annual_account_objects(company_object_dict)
assign_text_to_account_objects(company_object_dict)
initialize_data_assignment_for_annual_accounts(company_object_dict)

recognized_data_dict=create_data_dict_from_company_objects(company_object_dict)
dict_to_json(recognized_data_dict,"recognized_data")

def create_pandas_dict():
    pandas_dict={}
    for company_name,company_object in company_object_dict.items():
        pandas_dict[company_name]={}
        for year,annual_account in company_object.annual_accounts.items():
            pandas_dict[company_name][year]={}
            for item in annual_account.all_items:
                pandas_dict[company_name][year].update({item.name:item.recognized_value})     
    return pandas_dict            

pandas_dict=create_pandas_dict()
dict_to_json(pandas_dict,"pandas_dict")


def create_dfs():
    os.chdir("C:/Users/lukas/Desktop/bachelor/data/recognized_data_tables")
    for company_name,data in pandas_dict.items():
        data_frame=pd.DataFrame(data)
        file_name=company_name+".xlsx"
        data_frame.to_excel(file_name)


#create_dfs()

flag_dict=check_flags(company_object_dict)
dict_to_json(flag_dict,"flags")

