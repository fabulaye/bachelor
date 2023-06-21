from PyPDF2 import PdfReader
import os
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import time 
import json
import jsonlines



counter=0
handelsregister_dict={}
gaming_company_names=[]
found_companies_list=[]
gaming_company_dict={}
handelsregister_unternehmen=[]
json_dataset={}
company_object_dict={}
company_dict_time={}



def read_in_json_datasets():
      global handelsregister_dict,gaming_company_dict
      os.chdir("C:/Users/lukas/Desktop/bachelor/data")
      handelsregister_dict=json.loads("handelsregister_dict.json")
      gaming_company_dict=json.loads("gaming_company_dict.json")

read_in_json_datasets()


def find_all_companies():
      counter=0
      for object in handelsregister:
            #print(object)
            handelsregister_unternehmen.append(object["name"])
            try:
                  handelsregister_dict[object["name"]]={'_registerArt':object["all_attributes"]['_registerArt'],'federal_state':object["all_attributes"]['federal_state'],'registered_office':object["all_attributes"]['registered_office'],'retrieved_at':object['retrieved_at']}
            except:
                  None
            #counter+=1
            #if counter==1000:
                  #break
               


os.chdir("C:/Users/lukas/Desktop/bachelor")

company_id=0

class company():
    def __init__(self,id,name,time) -> None:
          self.id=id
          self.name=name
          self.active=True
          self.link=""
          self.time=time
          self.html=""
          self.dict={"id":self.id,"status":self.active,"time":self.time}
    def update_time(self):
          self.time=time.time() 


def update_json(): #wir updaten das Json file mit den Infos aus dem excel file
      for company_name,company_object in company_dict.items():
            json_dataset[company_name]=company_object.dict

def update_company_data_from_excel(): #excel
      company_dataset=pd.read_excel("data/test.xlsx")
      return company_dataset

company_dataset=update_company_data_from_excel() #brauchen wir nicht mehr


def create_json_from_dict(dict,title):
      os.chdir("C:/Users/lukas/Desktop/bachelor/data")
      with open(title+".json", "w") as outfile:
            json.dump(dict, outfile)
      os.chdir("C:/Users/lukas/Desktop/bachelor")

def assign_company_data():
      global company_id
      for index,row in company_dataset.iterrows():
            company_object_dict[row["Unternehmen"]]=company(company_id,row["Unternehmen"],row["Time"])
            company_id+=1





def get_names_from_excel():
      for gaming_company in company_dataset.Unternehmen:
            gaming_company_names.append(gaming_company)



def find_gaming_companies_in_handelsregister():
      counter=0
      for gaming_company in gaming_company_names:
            company_string=str(gaming_company+"\s*\w*\s*\w*\s*\w*\s*\w*") #vielleicht ohne klammern
            #print(company_string)
            gaming_company_regex=re.compile(company_string)
            for company in handelsregister_unternehmen: #for company in handelsregister: 
                  search=gaming_company_regex.findall(company)
                  if search!=[]:
                        found_companies_list.append(search)
                        gaming_company_dict[company]=handelsregister_dict[company]
                  counter+=1


def update_company_dict_time():
      for company_name,company in company_dict.items():
             company_dict_time[company_name]=company.time


def create_datasets():
      handelsregister=jsonlines.open("C:/Users/lukas/Desktop/bachelor/data/handelsregister.jsonl")
      find_all_companies()
      get_names_from_excel()
      find_gaming_companies_in_handelsregister() 
      create_json_from_dict(handelsregister_dict,"handelsregister_dict")
      create_json_from_dict(gaming_company_dict,"gaming_company_dict")



def create_company_objects_from_excel():
      company_dataset=update_company_data_from_excel() #brauchen wir das hier?
      assign_company_data() #wir brauchen das company dict



def download_htlm():
      os.chdir("C:/Users/lukas/Desktop/bachelor/html_files")
      index=0
      for company_name,company in company_dict.items():

            if company.link!="" and index<=5 and (time.time()-company.time)>=1200000:
      
                  request=requests.get(company.link).text
                  with open(str(company_name),"w") as f:
                        for line in request:
                              f.write(line)
                  company.update_time()  
                  print(company_name+" updated")                      
                  index+=1
      os.chdir("C:/Users/lukas/Desktop/bachelor")   


#update_company_dict_time()
#company_dataset["Time"]=company_dict_time.values()   
os.chdir("C:/Users/lukas/Desktop/bachelor/data")
#company_dataset.to_excel("test.xlsx")  


def read_html_files():
      os.chdir("C:/Users/lukas/Desktop/bachelor/html_files")
      for company_name,company_object in company_dict.items():
            try:
                  with open(company_name) as f:
                        company_object.html=f.readlines()
            except:
                  None



datum_regex=re.compile("\d{2}\.\d{2}\.\d{4}")
date_23=re.compile("\d{2}\.\d{2}\.2023")

abschluss_date=re.compile(";\d{2}\.\d{2}\.\d{4}")
title_abschluss=re.compile("Jahresabschluss")#bis zum 31.12.2021

def search_for_annual_account(text):
      for string in text:
            goal=title_abschluss.findall(string)
            if goal!=[]:
                  print(goal)

