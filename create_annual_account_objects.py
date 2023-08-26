from annual_account import annual_account
from company_object import company
from json_to_dict import json_to_dict
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

rechtsform_regex=re.compile("GmbH|UG|AG|KG|Unternehmensgesellschaft")


def strip_rechtsform(company_name):
    rechtsform_regex_search=rechtsform_regex.findall(company_name)[0]
    if rechtsform_regex_search!="":
        company_name=company_name.rstrip(rechtsform_regex_search).lower().rstrip()
    return company_name     

      

def standardize_name(company_name):
    company_name=strip_rechtsform(company_name)  
    company_name=company_name.lower()
    company_name=company_name.replace(" ","_") 
    company_name=company_name.rstrip()
    return company_name  



def standardize_company_names(data): #that shits now bugged
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

                     
def initialize_data_assignment_for_annual_accounts():
      for company_name,company_object in company_object_dict.items():
            for year,annual_account_object in company_object.annual_accounts.items(): #haben wir hier überhaupt die items schon?
                  annual_account_object.search_for_data()
                  annual_account_object.create_dict()
                  annual_account_object.check_flags()


character_pattern=re.compile("[^\d,.\s]\w*")
single_number_pattern=re.compile("\d+[,.]\d*[,.]*\d*[,.]*")

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

def deconstruct_file_name(file):
      year=file[-8:-4]
      company_name=file[:-8].lower()
      return year,company_name

def return_rechtsform(company_name):
      rechtsform=rechtsform_regex.findall(company_name)[0]
      return rechtsform


def create_company_objects():
      global company_id
      for company_name,attributes in gaming_companies_handelsregister.items(): #aktuell sind die namen noch nicht standadized!!!
                  rechtsform=return_rechtsform(company_name)
                  print(rechtsform)
                  standardized_company_name=standardize_name(company_name)
                  company_object_dict[standardized_company_name]=company(company_id,standardized_company_name,rechtsform,attributes["all_attributes"]["federal_state"])
                  company_id+=1


def create_annual_account_objects(): 
      files=os.listdir("C:/Users/lukas/Desktop/bachelor/pdf")
      for file in files:
            if file.endswith("txt")==True:
                year,company_name=deconstruct_file_name(file) #wichtig das underscore ist
                try:
                    company_object_dict[company_name].annual_accounts[year]=annual_account() #wir kreieren den account wenn es ein text dokument fpr das Jahr gibt
                except:
                    print(f"{company_name} object doesn't exist") 




cdir.chdir_data()
gaming_companies_handelsregister=json_to_dict("gaming_companies_handelsregister.json")
create_company_objects() #hier erstellen wir die company objects´
print(company_object_dict)
create_annual_account_objects()
assign_text_to_account_objects()   
initialize_data_assignment_for_annual_accounts()


for company_name,company_object in company_object_dict.items():
      print(company_object.annual_accounts)


#fehler einmal mit rechtsform einmal ohne
