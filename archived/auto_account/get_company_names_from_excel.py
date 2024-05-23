import pandas as pd
from import_manager import import_all_libraries
import_all_libraries()
from file_manager.dict_to_json import dict_to_json
from file_manager.change_directory import chdir_data
chdir_data()
gaming_company_names_excel=pd.read_excel("test.xlsx")

def get_names_from_excel(gaming_company_names_excel):
      company_names_excel=[]
      for gaming_company in gaming_company_names_excel.Unternehmen:
            company_names_excel.append(gaming_company)
      return company_names_excel    
list=get_names_from_excel(gaming_company_names_excel)
dict={"names":list}
dict_to_json(dict,"gaming_company_names_excel")




