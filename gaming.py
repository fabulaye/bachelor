from PyPDF2 import PdfReader
import os
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import time 
import json
import jsonlines

os.chdir("C:/Users/lukas/Desktop/bachelor/data")

namens_liste=["Crytek GmbH","Aruba Studios GmbH","Bigpoint GmbH"]

handelsregister=jsonlines.open("C:/Users/lukas/Desktop/bachelor/data/handelsregister.jsonl")
counter=0
#for object in handelsregister:
      #print(object)
      #counter+=1
      #if counter ==100:
            #break

handelsregister_dict={}

handelsregister_unternehmen=[]
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
               

find_all_companies()
#print(handelsregister_dict)




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

json_dataset={}

def update_json():
      for company_name,company_object in company_dict.items():
            json_dataset[company_name]=company_object.dict

def update_company_data():
      company_dataset=pd.read_excel("data/test.xlsx")
      return company_dataset

company_dataset=update_company_data()

company_dict={}
company_dict_time={}

def create_json_from_dict(dict,title):
      with open(title+".json", "w") as outfile:
            json.dump(dict, outfile)

create_json_from_dict(handelsregister_dict,"handelsregister_dict")

def assign_company_data():
      global company_id
      for index,row in company_dataset.iterrows():
            company_dict[row["Unternehmen"]]=company(company_id,row["Unternehmen"],row["Time"])
            company_id+=1

gaming_company_names=[]
def get_names_from_excel():
      for gaming_company in company_dataset.Unternehmen:
            gaming_company_names.append(gaming_company)

get_names_from_excel()
#print(gaming_company_names)

found_companies_list=[]
gaming_company_dict={}
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
find_gaming_companies_in_handelsregister()
print(found_companies_list)



def create_gaming_company_subset():
      for object in handelsregister:
            #print(object["name"])
            if object["name"] in found_companies_list:
                  print("gefunden")
                  gaming_company_dict[object["name"]]=object

#create_gaming_company_subset()            
print(gaming_company_dict)
create_json_from_dict(gaming_company_dict,"gaming_company_dict")
def update_company_dict_time():
      for company_name,company in company_dict.items():
             company_dict_time[company_name]=company.time




assign_company_data() #das hier steht immer am anfang 


aeria_games = PdfReader('aeria_games.pdf')

test=aeria_games.pages[5]

url="https://www.unternehmensregister.de/ureg/result.html;jsessionid=3DC7B3CCD3A1313FEC4BB840738586DD.web01-1"
crytek_url="https://www.unternehmensregister.de/ureg/result.html;jsessionid=62A19A447C2F281BE748FFC562E238B9.web01-1"
twotainment_url="https://www.unternehmensregister.de/ureg/result.html;jsessionid=4E62DDE89F02A8DF09894BF6A1251BCD.web01-1"
#request=requests.get(crytek_url)
#request_text=request.text

#with open("html_file_test","w") as f:
    #for line in request_text:
            #f.write(line)

company_dict["Crytek"].link=crytek_url
company_dict["2tainment"].link=twotainment_url
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

download_htlm()
#update_company_dict_time()
#company_dataset["Time"]=company_dict_time.values()   
os.chdir("C:/Users/lukas/Desktop/bachelor/data")
#company_dataset.to_excel("test.xlsx")  
update_json()
#print(json_dataset)


def read_html_files():
      os.chdir("C:/Users/lukas/Desktop/bachelor/html_files")
      for company_name,company_object in company_dict.items():
            try:
                  with open(company_name) as f:
                        company_object.html=f.readlines()
            except:
                  None
read_html_files() #hier bin ich


#print(request_text)

#pattern=re.compile("\d{2}\.\d{2}\.\d{4}")
#ergebnisse=pattern.findall(request_text)
#print(ergebnisse)

datum_regex=re.compile("\d{2}\.\d{2}\.\d{4}")
date_23=re.compile("\d{2}\.\d{2}\.2023")
crytek_regex=re.compile("Crytek")

abschluss_date=re.compile(";\d{2}\.\d{2}\.\d{4}")
title_abschluss=re.compile("Jahresabschluss")#bis zum 31.12.2021

def search_for_annual_account(text):
      for string in text:
            goal=title_abschluss.findall(string)
            if goal!=[]:
                  print(goal)

testvar=company_dict["Crytek"].html

#search_for_annual_account(company_dict["Crytek"].html)
      
#date_results=abschluss_date.findall(request_text)
#print(date_results)

#soup = BeautifulSoup(request_text,"lxml")
#crytek_search=soup.find_all(string=crytek_regex) #works with regex
#search_2023=soup.find_all(string=abschluss_date) #works with regex
#title_serch=soup.find_all(title=title_abschluss)
#print(title_serch)






