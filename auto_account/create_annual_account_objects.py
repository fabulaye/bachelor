from company_object import company
from json_to_dict import json_to_dict
import change_directory as cdir
from json_to_dict import json_to_dict
from pdf_to_txt import pdf_to_txt
from read_txt import read_txt
from annual_account import annual_account,account_item,flag
from create_company_objects import create_company_objects

      
def initialize_data_assignment_for_annual_accounts():
      for company_name,company_object in company_object_dict.items():
            for year,annual_account_object in company_object.annual_accounts.items(): #haben wir hier überhaupt die items schon?
                  annual_account_object.search_for_data()
                  annual_account_object.create_dict()
                  annual_account_object.check_flags()




def assign_text_to_account_objects():
      cdir.chdir_pdf()
      files=os.listdir("C:/Users/lukas/Desktop/bachelor/pdf")
      for file in files:
            if file.endswith("txt")==True:
                  year,company_name=deconstruct_file_name(file)
                  text=read_txt(file)
                  try:
                        company_object_dict[company_name].annual_accounts[year].text=text
                  except: 
                        print(f"couldn assign text to {company_name}")      
      os.chdir("C:/Users/lukas/Desktop/bachelor")   



def create_annual_account_objects(): 
      files=os.listdir("C:/Users/lukas/Desktop/bachelor/pdf")
      for file in files:
            if file.endswith("txt")==True:
                year,company_name=deconstruct_file_name(file) #wichtig das underscore ist
                try:
                    company_object_dict[company_name].annual_accounts[year]=annual_account() #wir kreieren den account wenn es ein text dokument fpr das Jahr gibt
                except:
                    print(f"{company_name} object doesn't exist") 



#vielleicht verschieben



