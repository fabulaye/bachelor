from import_manager import import_file_manager
import_file_manager()
from file_manager.json_to_dict import json_to_dict
from file_manager.change_directory import chdir_data
import os
from openpyxl import Workbook
import pandas as pd

chdir_data()

flag_dict=json_to_dict("flags.json")

def check_if_file_exists(file_name,parent):
    items=os.listdir(parent)
    if file_name in items:
        return True
    else:
        return False

def create_flag_directories(parent="C:/Users/lukas/Desktop/bachelor/data/flags_excel"):
    os.chdir(parent)
    for company_name,dict in flag_dict.items():
        try:
            os.mkdir(company_name)
        except FileExistsError:
            print(f"{company_name} already exists")

def create_excel_files():
    for company_name,dict in flag_dict.items():
        parent="C:/Users/lukas/Desktop/bachelor/data/flags_excel"
        path=parent+"/"+company_name
        os.chdir(path)
        for year,data in dict.items():
            excel_file_name=company_name+year+".xlsx"
            bool=check_if_file_exists(excel_file_name,parent)
            if bool==False:
                test=Workbook()
                test.save(excel_file_name)
                test.create_sheet()
            else:
                print(f"{excel_file_name} already exists")

#ich sollte pandas machen und dann df als excel exportieren



create_excel_files()
