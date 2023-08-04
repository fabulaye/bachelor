import os
import re
import pandas as pd
import time 
import json
import jsonlines
import pytesseract as pyt
import pdf2image 
import requests
#from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload



counter=0
json_dataset={}
company_object_dict={}
company_dict_time={}
gaming_company_names_dict={}


def chdir_bachelor():
      os.chdir("C:/Users/lukas/Desktop/bachelor")

def chdir_data():
      os.chdir("C:/Users/lukas/Desktop/bachelor/data")

chdir_bachelor()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']


def token():
      creds = None
      if os.path.exists('token.json'):
          creds = Credentials.from_authorized_user_file('token.json', SCOPES)
      # If there are no (valid) credentials available, let the user log in.
      if not creds or not creds.valid:
          if creds and creds.expired and creds.refresh_token:
              creds.refresh(Request())
          else:
              flow = InstalledAppFlow.from_client_secrets_file(
                  'credentials.json', SCOPES)
              creds = flow.run_local_server(port=0)
          # Save the credentials for the next run
          with open('token.json', 'w') as token:
              token.write(creds.to_json())
      return creds

#creds=token()

def build_service():
      try:
          service = build('drive', 'v3', credentials=creds)
      except HttpError as error:
          # TODO(developer) - Handle errors from drive API.
          print(f'An error occurred: {error}')
      return service

#service=build_service()
chdir_data()




def upload_pdfs():
      os.chdir("C:/Users/lukas/Desktop/bachelor/pdf")
      files=os.listdir()
      headers={"Content-Type":"text","Content-Length":"50000"}
      url="https://www.googleapis.com/upload/drive/v3/files?uploadType=media"
      for file in files:
            f=open(file,"r")
            print(f)
            requests.post(url=url,data=f,headers=headers)

#upload_pdfs()


def create_dict_from_json(filename,dir="C:/Users/lukas/Desktop/bachelor/data"):
      os.chdir(dir)
      with open(filename,"r") as f:
            data=f.readlines()[0]

      dict=json.loads(data) 
      return dict





def create_handelsregister_companies_names_list():
      handelsregister_companies_names=[]
      counter=0
      for object in handelsregister:
            handelsregister_companies_names.append(object["name"])
      return handelsregister_companies_names      
                  
            




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

           


def create_json_from_dict(dict,title,directory="C:/Users/lukas/Desktop/bachelor/data"):
      os.chdir(directory)
      with open(title+".json", "w") as outfile:
            json_file=json.dumps(dict)
            outfile.write(json_file)
            print("file changed")
      os.chdir("C:/Users/lukas/Desktop/bachelor")

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



def get_names_from_excel(company_dataset):
      company_names_excel=[]
      for gaming_company in company_dataset.Unternehmen:
            company_names_excel.append(gaming_company)
      return company_names_excel      





      
def create_gaming_company_names_underscored_json():
      os.chdir("C:/Users/lukas/Desktop/bachelor/data")
      dict={}
      dict["names"]=[]
      names=create_dict_from_json("gaming_company_names_dict.json")
      names=names["names"]
      for name in names:
            new_name=name.replace(" ","_")
            dict["names"].append(new_name) 
      create_json_from_dict(dict,"gaming_company_names_underscored_dict")  

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



def create_dict_of_specific_companies_in_handelsregister(list_of_names):
      gaming_companies_handelsregister={}          
      for name in list_of_names:
            for company_entry in handelsregister:
                  try:
                        data=company_entry[name]
                        gaming_companies_handelsregister[name]=data
                  except:
                        None      
      return gaming_companies_handelsregister #todo weakes naming



os.chdir("C:/Users/lukas/Desktop/bachelor/pdf")

pyt.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'
tesserect_link="https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html"


def get_text_from_pdf(pdf_name): #create jpgs from the pdf, create txt from the pictures, and delete the pictures
      os.chdir("C:/Users/lukas/Desktop/bachelor/pdf")
      pages=pdf2image.pdf2image.convert_from_path(pdf_name+".pdf",poppler_path="C:/Users/lukas/Desktop/bachelor/pdf/poppler-23.05.0/Library/bin")
      pdf_string=""
      for i in range(len(pages)):
            pages[i].save("page"+str(i)+".jpg","JPEG")
            page_string=pyt.image_to_string("page"+str(i)+".jpg",lang="deu",config="--psm 4")
            pdf_string=pdf_string+" "+page_string          
      with open(pdf_name+".txt","w") as f:
            f.write(pdf_string) 
      delete_jpg()          

def delete_jpg():
      for file in os.listdir("C:/Users/lukas/Desktop/bachelor/pdf"):
            if file.endswith(".jpg"):
                  os.remove(file)

def create_text_for_all_files_in_dir():
      dir_list=os.listdir("C:/Users/lukas/Desktop/bachelor/pdf")
      for file in dir_list:
            if file.endswith(".pdf"):
                  file=file.rstrip(".pdf")
                  text_name=file+".txt"
                  if text_name not in dir_list:
                        print("new pdf found")
                        get_text_from_pdf(file) #hier werden die texdokumente erstellt etc.




def check_mismatches_in_lists(list_1,list_2):
      mismatch=[]
      for i in list_1:
            if i not in list_2:
                  mismatch.append(i)
      return mismatch





def read_text(file):
  with open(file,"r") as f:
      text=f.readlines()
  return text   

def deconstruct_file_name(file):
      year=file[-8:-4]
      company_name=file[:-8].lower()
      return year,company_name

def create_annual_account_objects():
      files=os.listdir("C:/Users/lukas/Desktop/bachelor/pdf")
      for file in files:
            if file.endswith("txt")==True:
                  year,company_name=deconstruct_file_name(file)
                  try:
                              company_object_dict[company_name].annual_accounts[year]=annual_account() #wir kreieren den account wenn es ein text dokument fpr das Jahr gibt
                  except:
                              print("company object doesnt exist") 

def assign_text_to_account_objects():
      os.chdir("C:/Users/lukas/Desktop/bachelor/pdf")
      files=os.listdir("C:/Users/lukas/Desktop/bachelor/pdf")
      for file in files:
            if file.endswith("txt")==True:
                  year,company_name=deconstruct_file_name(file)
                  text=read_text(file)
                  company_object_dict[company_name].annual_accounts[year].text=text
      os.chdir("C:/Users/lukas/Desktop/bachelor")     


   

class flag():
      def __init__(self) -> None:
            self.status=False
            self.logical_error=False
            self.true_value_missing=False
            self.findings=[]

class account_item():
      def __init__(self,name,regex,numbers=0,items=[],children=[],account_id=None):
            self.name=name
            self.regex=regex
            self.items=items
            self.has_children=False  
            self.flag=flag()
            self.numbers=numbers   
            self.true_value=0 
            self.theoretical_value=0
            self.children=children
            self.account_id=account_id
      def update_data(self):
            if type(self.numbers)==list and len(self.numbers)>=2:            
                  self.true_value=self.numbers[0]
            if len(self.children)>=1:
                  sum=0
                  #self.theoretical_value=[sum,[]]
                  for child in self.children:	
                              #self.theoretical_value[1].append(child.true_value)
                              sum+=child.true_value

                  #self.theoretical_value=sum 
                  self.theoretical_value=sum
      def int_data(self):
            if type(self.numbers)==list and len(self.numbers)>=2:
                  for number in self.numbers:
                        number=float(number)
            self.true_value=float(self.true_value)
            self.theoretical_value=float(self.theoretical_value)                
      def flag_entry(self):
            if self.theoretical_value!=self.true_value and self.theoretical_value!=0:
                  self.flag.logical_error=True
                  self.flag.status=True        
            if int(self.true_value)==0:
                  self.flag.true_value_missing=True
                  self.flag.status=True 
      def search_numbers(self): #function für die annual_account class
            for string in self.account_id.text:
                  if self.regex.findall(string)!=[]:
                  #print("pattern found")
                        item=self.regex.findall(string)[0] #return immer eine liste mit nur einem eintrag
                        numbers=all_numbers_pattern.findall(item)
                        self.numbers=clean_numbers(numbers)
                                           
      def __str__(self) -> str:
            return self.name      
         
      #verbindlichkeiten,kassenbestand          

 

class annual_account():
      def __init__(self,):
            self.text=""
            
            #children umlaufvermögen
            self.vorräte=account_item("vorräte",vorräte_regex,account_id=self)
            self.forderungen=account_item("forderungen",forderungen_regex,account_id=self)
            self.kassenbestand=account_item("kassenbestand",kassenbestand_regex,account_id=self)
            
            #self.jahresfehlbetrag=account_item("jahresfehlbetrag",jahresfehlbetrag_regex)
            self.fehlbetrag=account_item("fehlbetrag",fehlbetrag_regex,account_id=self)
            #children aktiva
            self.umlaufvermögen=account_item("umlaufvermögen",umlaufvermögen_regex,children=[self.vorräte,self.forderungen,self.kassenbestand],account_id=self)

            self.sachanlagen=account_item("sachanlagen",sachanlagen_regex,account_id=self)
            self.finanzanlagen=account_item("fehlbetrag",finanzanlagen_regex,account_id=self)
            self.anlagevermögen=account_item("anlagevermögen",anlagevermögen_regex,children=[self.sachanlagen,self.finanzanlagen],account_id=self)
            self.rechnungsabgrenzungsposten=account_item("rechnungsabgrenzungsposten",rechnungsabgrenzungsposten_regex,account_id=self)
            
            self.aktiva=account_item("aktiva",aktiva_regex,children=[self.anlagevermögen,self.umlaufvermögen,self.rechnungsabgrenzungsposten,self.fehlbetrag],account_id=self)
            #children passiva
            self.gezeichnetes_kapital=account_item("gezeichnetes_kapital",gezeichnetes_kapital_regex,account_id=self)
            self.eingefordertes_kapital=account_item("eingefordertes_kapital",eingefordertes_kapital_regex,children=[self.gezeichnetes_kapital],account_id=self)
            self.verlustvortrag=account_item("verlustvortrag",verlustvortrag_regex,account_id=self)
            self.überschuss=account_item("überschuss",überschuss_regex,account_id=self)
            self.gewinnvortrag=account_item("gewinnvortrag",gewinnvortrag_regex,account_id=self)
            
            #bei activision: gezeichnetes kapital,kapitalrücklage,gewinnvortrag.jahresüberschuss teil von ek
            self.eigenkapital=account_item("eigenkapital",eigenkapital_regex,children=[self.gewinnvortrag,self.fehlbetrag,self.verlustvortrag,self.eingefordertes_kapital],account_id=self)
            self.rückstellungen=account_item("rückstellungen",rückstellungen_regex,account_id=self)
            #es gibt restlaufzeit unter einem jahr,sonstige verbindlichkeiten
            self.verbindlichkeiten=account_item("verbindlichkeiten",verbindlichkeiten_regex,account_id=self)

            self.passiva=account_item("passiva",passiva_regex,children=[self.eigenkapital,self.rückstellungen,self.verbindlichkeiten],account_id=self)

            self.all_items=[self.vorräte,self.forderungen,self.kassenbestand,self.gewinnvortrag,self.fehlbetrag,self.umlaufvermögen,self.anlagevermögen,self.rechnungsabgrenzungsposten,self.eigenkapital,
                            self.aktiva,self.rückstellungen,self.verbindlichkeiten,self.passiva,self.gezeichnetes_kapital,self.eingefordertes_kapital,self.überschuss,self.gewinnvortrag,
                            ] #reihenfolge in all_items produziert bugs
            

            self.first_layer=[self.aktiva,self.passiva]
            self.second_layer=[self.anlagevermögen,self.umlaufvermögen,self.rechnungsabgrenzungsposten,self.fehlbetrag,self.eigenkapital,self.rückstellungen,self.verbindlichkeiten]
            self.third_layer=[self.vorräte,self.forderungen,self.kassenbestand,self.gewinnvortrag,self.fehlbetrag,self.verlustvortrag,self.eingefordertes_kapital,self.finanzanlagen,self.sachanlagen]
            self.fourth_layer=[self.gezeichnetes_kapital]
            self.dict={}
            self.flag_dict={}

                  

      def create_dict(self):
            for aktivapassiva in self.first_layer:
                  self.dict[aktivapassiva.name]={"true_value":aktivapassiva.true_value,"theoretical_value":aktivapassiva.theoretical_value,"children":{}}
                  for child in aktivapassiva.children:
                        dict={}
                        dict[child.name]={"true_value":child.true_value,"theoretical_value":child.theoretical_value,"children":{}}
                        self.dict[aktivapassiva.name]["children"].update(dict)
                        if len(child.children)>=1:
                              for grandchild in child.children:
                                    dict_two={}
                                    dict_two[grandchild.name]={"true_value":grandchild.true_value,"theoretical_value":grandchild.theoretical_value}

                                    self.dict[aktivapassiva.name]["children"][child.name]["children"].update(dict_two)
                        #hier müssen noch mehr layer kommen


      def search_for_data(self):
            if self.text!="":
                  for item in self.fourth_layer:
                        item.search_numbers()
                        item.flag.findings.append(item.numbers)
                        item.int_data()
                        item.update_data()
                  for item in self.third_layer:
                        item.search_numbers()
                        item.flag.findings.append(item.numbers)
                        item.int_data()
                        item.update_data()  
                  for item in self.second_layer:
                        item.search_numbers()
                        item.flag.findings.append(item.numbers)
                        item.int_data()
                        item.update_data() 
                  for item in self.first_layer:
                        item.search_numbers()
                        item.flag.findings.append(item.numbers)
                        item.int_data()
                        item.update_data()               
      def check_flags(self):
            for item in self.all_items:
                  item.flag_entry()
                  if item.flag.status==True:
                        self.flag_dict[item.name]={"logical_error":item.flag.logical_error,"true_value_missing":item.flag.true_value_missing,"findings":item.flag.findings,"thoretical value":item.theoretical_value,"true value": item.true_value}


                                                      
def initialize_data_assignment_for_annual_accounts():
      for company_name,company_object in company_object_dict.items():
            for year,annual_account_object in company_object.annual_accounts.items(): #haben wir hier überhaupt die items schon?
                  annual_account_object.search_for_data()
                  annual_account_object.create_dict()
                  annual_account_object.check_flags()


numbers_string="[\w\d\s,öä.]+\d$"

#aktiva
aktiva_regex=re.compile("Aktiva"+numbers_string,flags=re.I)
anlagevermögen_regex=re.compile("Anlagevermögen"+numbers_string,flags=re.I) #oberkategorie von sachanlagen
sachanlagen_regex=re.compile("Sachanlagen"+numbers_string,flags=re.I)  
umlaufvermögen_regex=re.compile("umlaufvermögen"+numbers_string,flags=re.I)
#umlaufvermögen children
vorräte_regex=re.compile("vorräte"+numbers_string,flags=re.I)
forderungen_regex=re.compile("forderungen"+numbers_string,flags=re.I)
kassenbestand_regex=re.compile("kassenbestand"+numbers_string,flags=re.I)

rechnungsabgrenzungsposten_regex=re.compile("Rechnungsabgrenzungsposten"+numbers_string,flags=re.I)
fehlbetrag_regex=re.compile("fehlbetrag"+numbers_string,flags=re.I)
#rechnungsabgrenzungspostren+anlagevermögen+umlaufvermögen=Aktiva

#passiva
passiva_regex=re.compile("Passiva"+numbers_string,flags=re.I)
eigenkapital_regex=re.compile("Eigenkapital"+numbers_string,flags=re.I)
#eigenkapital children
eingefordertes_kapital_regex=re.compile("eingefordertes kapital"+numbers_string,flags=re.I)
gezeichnetes_kapital_regex=re.compile("gezeichnetes kapital"+numbers_string,flags=re.I) #teil von eingefordertem kapital
einlagen_regex=re.compile("einlagen"+numbers_string,flags=re.I)#teil von eingefordertem kapital
gewinnvortrag_regex=re.compile("Gewinnvortrag"+numbers_string,flags=re.I)
jahresüberschuss_regex=re.compile("Jahresüberschuss"+numbers_string,flags=re.I)
rückstellungen_regex=re.compile("Rückstellungen"+numbers_string,flags=re.I)

immaterielle_vermögensgegestände_regex=re.compile("[I,i]materielle Vermögensgegenstände\s[\s\d,.]+")
finanzanlagen_regex=re.compile("finanzanlagen"+numbers_string,flags=re.I)
vermögensgegenstände_regex=re.compile("sonstige Vermögensgegenstände"+numbers_string,flags=re.I)
kreditinstitute_regex=re.compile("Kreditinstituten"+numbers_string,flags=re.I)
verbindlichkeiten_regex=re.compile("verbindlichkeiten"+numbers_string,flags=re.I)
jahresfehlbetrag_regex=re.compile("jahresfehlbetrag"+numbers_string,flags=re.I)
verlustvortrag_regex=re.compile("verlustvortrag"+numbers_string,flags=re.I)
überschuss_regex=re.compile("überschuss"+numbers_string,flags=re.I)
rechnungsbegrenzungsposten_regex=re.compile("rechnungsbegrenzungsposten"+numbers_string,flags=re.I)


character_pattern=re.compile("[^\d,.\s]\w*")
annual_acount_regex_dict={"imaterielle Vermögensgegenstände":immaterielle_vermögensgegestände_regex,"sachanlagen":sachanlagen_regex,"finanzanlagen":finanzanlagen_regex,"vermögesgegenstände":vermögensgegenstände_regex,"kreditinstitute":kreditinstitute_regex,"aktiva":aktiva_regex,"eigenkapital":eigenkapital_regex,"gezeichnetes_kapital":gezeichnetes_kapital_regex,"gewinnvortrag":gewinnvortrag_regex,"jahresüberschuss":jahresüberschuss_regex,"rückstellungen":rückstellungen_regex,"verbindlichkeiten":verbindlichkeiten_regex,"rechnungsbegrenzungsposten":rechnungsbegrenzungsposten_regex,"passiva":passiva_regex} 
single_number_pattern=re.compile("\d+[,.]\d*[,.]*\d*[,.]*")
all_numbers_pattern=re.compile(numbers_string)




def get_list_of_keys(dict):
      keys_list=[]
      keys=dict.keys()
      for key in keys:
            keys_list.append(key)
      return keys_list




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
            create_json_from_dict(data_dict,company_name,directory=companies_dir)

#update_all_company_json()


chdir_data()
handelsregister=jsonlines.open("C:/Users/lukas/Desktop/bachelor/data/handelsregister.jsonl")
handelsregister_companies_names=create_handelsregister_companies_names_list()  
company_dataset=pd.read_excel("test.xlsx")
company_names_excel=get_names_from_excel(company_dataset)
company_names=create_dict_from_json("gaming_company_names_underscored_dict.json")["names"]
company_names_underscored=create_dict_from_json("gaming_company_names_underscored_dict.json")



gaming_companies_handelsregister=create_dict_of_specific_companies_in_handelsregister(company_names)
print(gaming_companies_handelsregister) #klappt die function
handelsregister_dict=create_dict_from_json("handelsregister_dict.json")
gaming_company_names_dict=create_dict_from_json("gaming_company_names_dict.json")
company_object_dict_keys=get_list_of_keys(company_object_dict)
mismatches=check_mismatches_in_lists(company_names_underscored,company_object_dict_keys)



#functions
create_company_objects() #hier erstellen wir die company objects´
create_text_for_all_files_in_dir()
create_annual_account_objects()
assign_text_to_account_objects()   
initialize_data_assignment_for_annual_accounts()
print(company_object_dict["2tainment"].annual_accounts["2019"].dict)
update_all_company_json()
print("script finished")


#fixliste:
#replace double entries
#rechnungsposten im theoretical von den aktiva nicht berücksichtigt
#eigenkapital/gezeichnetes Kapital, Kapitalrücklage,Bilanzverlust#
#dátaframe dat shit
#gewinn und verlustrechnung
#replace doubles in json mit namen und underscorede

