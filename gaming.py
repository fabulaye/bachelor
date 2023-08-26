import os
import re
import pandas as pd
import jsonlines
import pytesseract as pyt
import change_directory as cdir
from json_to_dict import json_to_dict
from pdf_to_txt import pdf_to_txt
from get_list_of_keys import get_list_of_keys
from annual_account import annual_account,account_item,flag

game_state=None
#from __future__ import print_function

counter=0
company_object_dict={}
company_id=0
rechtsform_regex=re.compile("GmbH|UG|AG|KG|Unternehmensgesellschaft")

#ich möchte eigentlich das die strings aus dem excel dokument und sonst alle anderen matchen
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



handelsregister=load_handelsregister()
handelsregister_companies_names=create_handelsregister_companies_names_list()  
company_dataset=pd.read_excel("test.xlsx")
company_names_excel=get_names_from_excel(company_dataset)
company_names=json_to_dict("gaming_company_names.json")["names"]
company_names_underscored=json_to_dict("gaming_company_names_underscored_dict.json")


#gaming_companies_handelsregister=create_dict_of_specific_companies_in_handelsregister(company_names)
gaming_companies_handelsregister=json_to_dict("gaming_company_dict.json")
handelsregister_dict=json_to_dict("handelsregister_dict.json")
gaming_company_names_dict=json_to_dict("gaming_company_names_dict.json")
company_object_dict_keys=get_list_of_keys(company_object_dict)

mismatches=check_mismatches_in_lists(company_names_underscored,company_object_dict_keys)



#functions
create_company_objects() #hier erstellen wir die company objects´
create_annual_account_objects()
assign_text_to_account_objects()   
initialize_data_assignment_for_annual_accounts()
update_all_company_json()

#fixliste:
#die dinger saven
#replace double entries
#rechnungsposten im theoretical von den aktiva nicht berücksichtigt
#eigenkapital/gezeichnetes Kapital, Kapitalrücklage,Bilanzverlust#
#dátaframe dat shit
#gewinn und verlustrechnung
#replace doubles in json mit namen und underscorede

