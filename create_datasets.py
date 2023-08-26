import os
import re
import pandas as pd
import jsonlines
import pytesseract as pyt
import change_directory as cdir
from json_to_dict import json_to_dict
from pdf_to_txt import pdf_to_txt
from read_txt import read_txt
from get_list_of_keys import get_list_of_keys
from annual_account import annual_account,account_item,flag

#from __future__ import print_function

counter=0
company_object_dict={}
                  
company_id=0

class company():
      def __init__(self,id,name,legal_form,state,employees=None) -> None:
          self.id=id
          self.name=name
          self.active=True
          self.link=""
          self.html=""
          self.dict={"id":self.id,"status":self.active}
          self.legal_form=legal_form
          self.state=state
          self.employees=employees
          self.annual_accounts={}
      def __str__(self) -> str:
            return self.name


rechtsform_regex=re.compile("GmbH|UG|AG|KG|Unternehmensgesellschaft")

def standardize_name(company_name):
      rechtsform_regex_search=rechtsform_regex.findall(company_name)[0]
      standadized_names=[]
      if rechtsform_regex_search!="":
            company_name=company_name.rstrip(rechtsform_regex_search).lower().rstrip()
            company_name=company_name.replace(" ","_")
      else:
            company_name=company_name.lower()
            company_name=company_name.replace(" ","_")   
      standadized_names.append(company_name)

def standardize_company_names(data):
      if type(data)==dict:
            if len(dict)>1:
                  for company_name,attributes in data.items():
                        standardized_names=standardize_name(company_name)
            if len(dict)==1:            
                  for company_name in data.values()[0]:
                        standardized_names=standardize_name(company_name)
      if type(data)==list:
            for company_name in data:
                  standardized_names=standardize_name(company_name)           
      return standardized_names


def add_officers_company_objects(): #hier erstellen wir die company objects
      global company_id
      for company_name,attributes in gaming_companies_handelsregister.items():
            try:
                  officers=attributes["officers"]
                  company_object_dict[company_name].officers=officers
            except:
                  None
        
def return_rechtsform(company_name):
      rechtsform=rechtsform_regex.findall(company_name)[0]
      return rechtsform

def create_company_objects():
      global company_id
      for company_name,attributes in gaming_companies_handelsregister.items(): #aktuell sind die namen noch nicht standadized!!!
                  print(company_name)
                  rechtsform=return_rechtsform(company_name)
                  company_object_dict[company_name]=company(company_id,company_name,rechtsform,attributes["all_attributes"]["federal_state"])
                  company_id+=1

  
#ich möchte eigentlich das die strings aus dem excel dokument und sonst alle anderen matchen

def create_company_regex(name):
      company_string=str(name+"\s*\w*\s*\w*\s*\w*\s*\w*") #vielleicht ohne klammern
      company_regex=re.compile(company_string) 
      return company_regex

def return_regex_hits(regex_search):
      if regex_search!=[]:
            hits=regex_search[0]
            return hits
               
def create_list_with_full_names(incomplete_names):
      full_names=[]
      for name in incomplete_names:
            regex=create_company_regex(name)
            for company in handelsregister_companies_names: #for company in handelsregister: 
                  search=regex.findall(company)
                  result=return_regex_hits(search)
                  full_names.append(result)
            

def create_list_of_matches_handelsregister(company_names):
      companies_in_handelsregister=[]
      for company_name in company_names:

            try:
                  if company_name in handelsregister_companies_names:
                        companies_in_handelsregister.append(company_name)
            except:
                  None     
      return companies_in_handelsregister




def create_annual_account_objects():
      files=os.listdir("C:/Users/lukas/Desktop/bachelor/pdf")
      for file in files:
            if file.endswith("txt")==True:
                  year,company_name=deconstruct_file_name(file)
                  try:
                              company_object_dict[company_name].annual_accounts[year]=annual_account() #wir kreieren den account wenn es ein text dokument fpr das Jahr gibt
                  except:
                              print(f"{company_name} object doesn't exist") 
  

                                                 
def initialize_data_assignment_for_annual_accounts():
      for company_name,company_object in company_object_dict.items():
            for year,annual_account_object in company_object.annual_accounts.items(): #haben wir hier überhaupt die items schon?
                  annual_account_object.search_for_data()
                  annual_account_object.create_dict()
                  annual_account_object.check_flags()


character_pattern=re.compile("[^\d,.\s]\w*")
single_number_pattern=re.compile("\d+[,.]\d*[,.]*\d*[,.]*")


def create_data_dict_from_annual_accounts():
      data_dict={}
      for company in company_object_dict:
            data_dict[company.name]={}
            for annual_account in company.annual_accounts:
                  data_dict[company.name][annual_account.year]=annual_account.dict



def clean_numbers(list):
      new_list=[]
      for entry in list:
            if single_number_pattern.findall(entry)!=[]:

                  split=entry.split()
                  for string in split:
                        try: #wir haben hier anscheinend auch strings drin
                              string=string.replace(".","")
                              string=string.replace(",",".") #deutsche schreibeweise zur englischen
                              string=float(string)
                              new_list.append(string)
                        except:
                              None      
      return new_list   

def update_all_company_json():
      companies_dir="C:/Users/lukas/Desktop/bachelor/data/companies"
      data_dict={}
      for company_name,company_object in company_object_dict.items():
            for year,account_object in company_object.annual_accounts.items():
                  data_dict[year]=account_object.dict
            #data_dict=company_object.annual_accounts
            json_to_dict(data_dict,company_name,directory=companies_dir)

#update_all_company_json()



cdir.chdir_data()

#der block alles in load stable data


company_object_dict_keys=get_list_of_keys(company_object_dict)

#functions
create_company_objects() #hier erstellen wir die company objects´
create_annual_account_objects()
assign_text_to_account_objects()   
initialize_data_assignment_for_annual_accounts()
create_data_dict_from_annual_accounts()
update_all_company_json()


