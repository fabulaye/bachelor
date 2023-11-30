from import_manager import import_file_manager
from file_manager.determine_file_type import determine_file_type

def deconstruct_file_name(file_name,replace_underscore=True):
    file_type=determine_file_type(file_name)
    file_name_without_suffix=file_name[:-(len(file_type)+1)]
    year=file_name_without_suffix[-4:]
    company_name=file_name_without_suffix[:-4]
    if replace_underscore==True:
        company_name=company_name.replace("_"," ")
    return company_name,year,file_type

