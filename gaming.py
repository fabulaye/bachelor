from PyPDF2 import PdfReader
import os
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import time 
import json
import jsonlines
import pytesseract as pyt
import pdf2image 



counter=0
handelsregister_dict={}
gaming_company_names=[]
found_companies_list=[]
gaming_company_dict={}
handelsregister_unternehmen=[]
json_dataset={}
company_object_dict={}
company_dict_time={}
gaming_company_names_dict={}
test_dict={}


def read_in_json_datasets():
      os.chdir("C:/Users/lukas/Desktop/bachelor/data")
      
      with open("handelsregister_dict.json","r") as f:
            data=f.readlines()[0]

      handelsregister_dict=json.loads(data) 
      
      with open("gaming_company_dict.json","r") as f:
            data=f.readlines()[0]
      gaming_company_dict=json.loads(data)
      print("gaming companies eingelesen")

      with open("gaming_company_names.json","r") as f:
            data=f.readlines()[0]
      gaming_company_names_dict=json.loads(data)
      print("gaming companies_names eingelesen")

      
      return handelsregister_dict,gaming_company_dict,gaming_company_names_dict





def find_all_companies(handelsregister):
      counter=0
      for object in handelsregister:
            
            handelsregister_unternehmen.append(object["name"])
            
            #test_dict[object["name"]]=object["all_attributes"]
            #print(object)
            #try:
                  #handelsregister_dict[object["name"]]=object["all_attributes"]#{'_registerArt':object["all_attributes"]['_registerArt'],'federal_state':object["all_attributes"]['federal_state'],'registered_office':object["all_attributes"]['registered_office'],'retrieved_at':object['retrieved_at']}
            #except:
                  #None
            #counter+=1
            #print(counter)
            #print(counter)
            #if counter==10:
      
                  #break
                  
               


os.chdir("C:/Users/lukas/Desktop/bachelor")

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
            json_file=json.dumps(dict)
            outfile.write(json_file)
            print("file changed")
      os.chdir("C:/Users/lukas/Desktop/bachelor")

rechtsform_regex=re.compile("GmbH|UG|AG|KG|Unternehmensgesellschaft")

def assign_company_data():
      global company_id
      #for index,row in company_dataset.iterrows():
            #company_object_dict[row["Unternehmen"]]=company(company_id,row["Unternehmen"],row["Time"])
      for company_name,attributes in gaming_company_dict.items():
            rechtsform=rechtsform_regex.findall(company_name)[0]
            #print(rechtsform)
            if rechtsform!="":
                  company_name=company_name.rstrip(rechtsform).lower().rstrip()
            else:
                  company_name=company_name.lower()      
            #print(company_name)
            try:
                  officers=attributes["officers"]
            except:
                  officers=None      
            if officers!=None:
                  company_object_dict[company_name]=company(company_id,company_name,rechtsform,attributes["all_attributes"]["federal_state"],attributes["officers"])
            else:      
                  company_object_dict[company_name]=company(company_id,company_name,rechtsform,attributes["all_attributes"]["federal_state"])
            company_id+=1





def get_names_from_excel():
      for gaming_company in company_dataset.Unternehmen:
            gaming_company_names.append(gaming_company)



def find_gaming_companies_in_handelsregister(handelsregister):
      counter=0
      for gaming_company in gaming_company_names:
            company_string=str(gaming_company+"\s*\w*\s*\w*\s*\w*\s*\w*") #vielleicht ohne klammern
            #print(company_string)
            gaming_company_regex=re.compile(company_string)
            for company in handelsregister_unternehmen: #for company in handelsregister: 
                  search=gaming_company_regex.findall(company)
                  
                  if search!=[]:
                        print(search)
                        found_companies_list.append(search[0])

                        

def check_if_company_is_gaming_company(handelsregister):
      names=gaming_company_names_dict["names"]
      for company_entry in handelsregister:
            #print(company_entry["name"][])
            
            try:
                  if company_entry["name"] in names:

                        print("entry_found")
                        gaming_company_dict[company_entry["name"]]=company_entry
            except:
                  None     

def update_company_dict_time():
      for company_name,company in company_dict.items():
             company_dict_time[company_name]=company.time

def update_json_files():
      create_json_from_dict(test_dict,"handelsregister_dict") 
      create_json_from_dict(gaming_company_dict,"gaming_company_dict")
      create_json_from_dict(gaming_company_names_dict,"gaming_company_names")

def create_datasets():
      handelsregister=jsonlines.open("C:/Users/lukas/Desktop/bachelor/data/handelsregister.jsonl")
      #print(handelsregister.values())
      print("executed")
      find_all_companies(handelsregister)
      print("all companies added")
      get_names_from_excel()
      find_gaming_companies_in_handelsregister(handelsregister) 
      print("gaming companies added")
      check_if_company_is_gaming_company(handelsregister) #funktioniert glaube ich nur wenn ich die liste reade
      update_json_files()
      print("finished")

def start_script(operation):
      if operation=="read":
            global handelsregister,handelsregister_dict,gaming_company_dict,gaming_company_names_dict
            handelsregister=jsonlines.open("C:/Users/lukas/Desktop/bachelor/data/handelsregister.jsonl")
            handelsregister_dict,gaming_company_dict,gaming_company_names_dict=read_in_json_datasets()
            update_json_files()
            
      if operation=="create":
            create_datasets()





start_script("read") 
#print(gaming_company_dict)
assign_company_data()
#print(company_object_dict)





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

dokument_link="https://www.unternehmensregister.de/ureg/result.html;jsessionid=CD652253DDDB0B2DEE19F279514012AE.web03-1?submitaction=showPrintDoc&id=31793656&pid=0"


os.chdir("C:/Users/lukas/Desktop/bachelor/pdf")
#hks_pdf=PdfReader("result.pdf")
#print(type(hks_pdf))
#seite=hks_pdf.pages[1]
#print(seite)
pyt.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'
#test_string=pyt.image_to_string("screenshot.png")
#print(test_string)



def get_text_from_pdf(pdf_name):
      os.chdir("C:/Users/lukas/Desktop/bachelor/pdf")
      pages=pdf2image.pdf2image.convert_from_path(pdf_name+".pdf",poppler_path="C:/Users/lukas/Desktop/bachelor/pdf/poppler-23.05.0/Library/bin")
      pdf_string=""
      for i in range(len(pages)):
            pages[i].save("page"+str(i)+".jpg","JPEG")
            page_string=pyt.image_to_string("page"+str(i)+".jpg",lang="deu")
            pdf_string=pdf_string+" "+page_string          
      with open(pdf_name+".txt","w") as f:
            f.write(pdf_string)     



def create_text_for_all_files_in_dir():
      dir_list=os.listdir("C:/Users/lukas/Desktop/bachelor/pdf")
      for file in dir_list:
            if file.endswith(".pdf"):
                  file=file.rstrip(".pdf")
                  text_name=file+".txt"
                  print(text_name)
                  print(dir_list)
                  if text_name not in dir_list:
                        print("new pdf found")
                        get_text_from_pdf(file)


create_text_for_all_files_in_dir()

get_text_from_pdf("crytek2012")  


pdf_text_dict={}


def load_pdf_text():
      files=os.listdir("C:/Users/lukas/Desktop/bachelor/pdf")
      for file in files:
            text_dict={}
            if file.endswith("txt")==True:
                  year=file[-8:-4]
                  with open(file,"r") as f:
                        text=f.readlines()
                        text_dict[year]=text
                        pdf_text_dict[file[:-8]]=text_dict #notation für filenames finden



                
company_annual_statements_dict={}
load_pdf_text()



numbers_string="[\s\d,.]*"
year_regex=re.compile("\d{4}")
immaterielle_vermögensgegestände_regex=re.compile("[I,i]materielle Vermögensgegenstände\s[\s\d,.]+")
sachanlagen_regex=re.compile("Sachanlagen\s[\s\d,.]+")  
finanzanlagen_regex=re.compile("[F,f]inanzanlagen\s[\s\d,.]+")
vermögensgegenstände_regex=re.compile("sonstige Vermögensgegenstände\s[\s\d,.]+")
kreditinstitute_regex=re.compile("Kreditinstituten*\s[\s\d,.]+")
aktiva_regex=re.compile("Summe Aktiva\s[\s\d,.]+")
eigenkapital_regex=re.compile("Eigenkapital\s[\s\d,.]+")
gezeichnetes_kapital_regex=re.compile("[g,G]ezeichnetes Kapital\s[\s\d,.]+")
gewinnvortrag_regex=re.compile("Gewinnvortrag\s[\s\d,.]+")
jahresüberschuss_regex=re.compile("Jahresüberschuss\s[\s\d,.]+")
rückstellungen_regex=re.compile("Rückstellungen\s[\s\d,.]+")
verbindlichkeiten_regex=re.compile("Verbindlichkeiten\s[\s\d,.]+")
rechnungsbegrenzungsposten_regex=re.compile("Rechnungsbegrenzungsposten\s[\s\d,.]+")
passiva_regex=re.compile("Summe Passiva\s[\s\d,.]+")

annual_acount_regex_dict={"imaterielle Vermögensgegenstände":immaterielle_vermögensgegestände_regex,"sachanlagen":sachanlagen_regex,"finanzanlagen":finanzanlagen_regex,"vermögesgegenstände":vermögensgegenstände_regex,"kreditinstitute":kreditinstitute_regex,"aktiva":aktiva_regex,"eigenkapital":eigenkapital_regex,"gezeichnetes_kapital":gezeichnetes_kapital_regex,"gewinnvortrag":gewinnvortrag_regex,"jahresüberschuss":jahresüberschuss_regex,"rückstellungen":rückstellungen_regex,"verbindlichkeiten":verbindlichkeiten_regex,"rechnungsbegrenzungsposten":rechnungsbegrenzungsposten_regex,"passiva":passiva_regex} 
single_number_pattern=re.compile("\d+[,.]\d*[,.]*\d*[,.]*")


def search_for_annual_account_items(text): #function returnt einen entry
      data_dict={}
      for string,pattern in annual_acount_regex_dict.items():
            if pattern.findall(text)!=[]:
                  print("pattern found")
                  entry=pattern.findall(text)[0].lstrip(string.capitalize())
                  dict_entry={string:entry} #regex dict hat strings als keys die den Regex beschreiben
                  return [dict_entry,string]
            #else:
                  #return []
      #data_dict["immaterielle_vermögensgegenstände"]=immaterielle_vermögensgegestände_regex.findall(text)
      #data_dict["sachanlagen"]=sachanlagen_regex.findall(text)
      

yearly_data={}

#def create_company_entries():
      #for 

#print(company_object_dict["crytek"])
def search_pdf_text_for_data():
      for company,dict in pdf_text_dict.items():
            for year,text in dict.items():
                  company_object_dict[company].annual_accounts[year]={} #wir erstellen für die Jahre zunächste ein leeres dict
                  for string in text:
                        item=search_for_annual_account_items(string)
                        
                        if item != None:
                              dict,key=item
                              print(dict[key])
                              numbers=single_number_pattern.findall(dict[key])
                              first=numbers[0]
                              first=re.sub(",\d+","",first)
                              dict[key]=first
                              company_object_dict[company].annual_accounts[year].update(dict) #function return ein dict mit den relevanten daten aus dem einen pdf file
                        #print(yearly_data) #wir überschreiben die Dinger?
                  #company_annual_statements_dict[company]=yearly_data


search_pdf_text_for_data()
#print(company_annual_statements_dict)
#print(company_object_dict["crytek"].annual_accounts)
#print(pdf_text_dict)