from company_object import company
from import_manager import import_all_libraries
from file_manager.json_to_dict import json_to_dict
from file_manager.change_directory import chdir_txt,chdir_data
import os
from txt_pdf.pdf_to_txt import pdf_to_txt
from txt_pdf.read_txt import read_txt
from annual_account import annual_account,account_item,flag
from txt_pdf.deconstruct_file_name import deconstruct_file_name
from create_company_objects import create_company_objects #brauchen wir hier eig nicht


def initialize_data_assignment_for_annual_accounts(company_object_dict):
      for company_name,company_object in company_object_dict.items():
            for year,annual_account_object in company_object.annual_accounts.items(): #haben wir hier überhaupt die items schon?
                  annual_account_object.search_for_data()
                  annual_account_object.create_dict()
                  annual_account_object.check_flags()
      return company_object_dict

def assign_text_to_account_objects(company_object_dict):
      
      chdir_txt()
      files=os.listdir("C:/Users/lukas/Desktop/bachelor/txt")
      for file in files:
            if file.endswith("txt")==True:
                  company_name,year,file_type=deconstruct_file_name(file)
                  text=read_txt(file)
                  try:
                        company_object_dict[company_name].annual_accounts[year].text=text
                  except: 
                        print(f"couldn assign text to {company_name}")      
      os.chdir("C:/Users/lukas/Desktop/bachelor")   



def create_annual_account_objects(company_object_dict): 
      files=os.listdir("C:/Users/lukas/Desktop/bachelor/txt")
      for file in files:
            if file.endswith("txt")==True:
                  company_name,year,file_type=deconstruct_file_name(file)
                  print(company_name)      
                  company_object_dict[company_name].annual_accounts[year]=annual_account() #wir kreieren den account wenn es ein text dokument fpr das Jahr gibt
                  #print(f"{company_name} object doesn't exist") 


#vielleicht verschieben



