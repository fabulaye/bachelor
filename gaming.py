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

def create_dict_from_json(filename,dir="C:/Users/lukas/Desktop/bachelor/data"):
      os.chdir(dir)
      with open(filename,"r") as f:
            data=f.readlines()[0]

      dict=json.loads(data) 
      return dict

def read_in_json_datasets():
      os.chdir("C:/Users/lukas/Desktop/bachelor/data")
      
      with open("handelsregister_dict.json","r") as f:
            data=f.readlines()[0]

      handelsregister_dict=json.loads(data) 
      
      with open("gaming_company_dict.json","r") as f:
            data=f.readlines()[0]
      gaming_company_dict=json.loads(data)
      print("gaming companies eingelesen")

      with open("gaming_company_names_dict.json","r") as f:
            data=f.readlines()[0]
      gaming_company_names_dict=json.loads(data)
      print("gaming companies_names eingelesen")

      
      return handelsregister_dict,gaming_company_dict,gaming_company_names_dict





def find_all_companies(handelsregister):
      counter=0
      for object in handelsregister:
            
            handelsregister_unternehmen.append(object["name"])
            
                  
               


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

def assign_company_data(): #hier erstellen wir die company objects
      global company_id
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





def get_names_from_excel(company_dataset):
      for gaming_company in company_dataset.Unternehmen:
            gaming_company_names.append(gaming_company)




def create_gaming_company_names_json():
      os.chdir("C:/Users/lukas/Desktop/bachelor/data")
      company_dataset=pd.read_excel("test.xlsx")
      get_names_from_excel(company_dataset)
      handelsregister=jsonlines.open("C:/Users/lukas/Desktop/bachelor/data/handelsregister.jsonl")
      find_all_companies(handelsregister)
      find_gaming_companies_in_handelsregister(handelsregister)
      gaming_company_names_dict={"names":found_companies_list}
      create_json_from_dict(gaming_company_names_dict,"gaming_company_names_dict")
      
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


def find_gaming_companies_in_handelsregister(handelsregister):
      counter=0
      for gaming_company in gaming_company_names:
            company_string=str(gaming_company+"\s*\w*\s*\w*\s*\w*\s*\w*") #vielleicht ohne klammern
            #print(company_string)
            gaming_company_regex=re.compile(company_string)
            for company in handelsregister_unternehmen: #for company in handelsregister: 
                  search=gaming_company_regex.findall(company)
                  
                  if search!=[]:
                        search=search[0]
                        #search=search.replace(" ","_")
                        found_companies_list.append(search)
                        
def iter_through_jsonl():
     counter=0
     jsonl=jsonlines.open("C:/Users/lukas/Desktop/bachelor/data/handelsregister.jsonl")
     for object in jsonl.iter(type=dict):
           counter+=1
           print(object)                       



def check_if_company_is_gaming_company():
      handelsregister=jsonlines.open("C:/Users/lukas/Desktop/bachelor/data/handelsregister.jsonl")
      gaming_company_names_dict=read_in_json_datasets()[2]           
      names=gaming_company_names_dict["names"]
      print("sind in function")
      for company_entry in handelsregister:
            try:
                  if company_entry["name"] in names:
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
      os.chdir("C:/Users/lukas/Desktop/bachelor/data")
      company_dataset=pd.read_excel("test.xlsx")
      get_names_from_excel(company_dataset)
      find_gaming_companies_in_handelsregister(handelsregister) 
      print(found_companies_list)
      print("gaming companies added")
      check_if_company_is_gaming_company() #funktioniert glaube ich nur wenn ich die liste reade
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






os.chdir("C:/Users/lukas/Desktop/bachelor/data")



os.chdir("C:/Users/lukas/Desktop/bachelor/pdf")

pyt.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'
#test_string=pyt.image_to_string("screenshot.png")
#print(test_string)
  
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


#create_text_for_all_files_in_dir() #kann jedes mal durchlaufen




pdf_text_dict={}


def load_pdf_text():
      os.chdir("C:/Users/lukas/Desktop/bachelor/pdf")
      files=os.listdir("C:/Users/lukas/Desktop/bachelor/pdf")
      text_dict={}
      for file in files:
            if file.endswith("txt")==True:
                  year=file[-8:-4]
                  company_name=file[:-8].lower()
                  with open(file,"r") as f:
                        text=f.readlines()
                        text_dict[year]=text
                        pdf_text_dict[company_name]=text_dict #notation für filenames finden
                        company_object_dict[company_name].annual_accounts[year]=annual_account() #wir kreieren den account wenn es ein text dokument fpr das Jahr gibt
                        account=company_object_dict[company_name].annual_accounts[year]
                        account.text=text

      os.chdir("C:/Users/lukas/Desktop/bachelor")                  
class flag():
      def __init__(self) -> None:
            self.status=False
            self.logical_error=False
            self.true_value_missing=False

class account_item():
      def __init__(self,name,regex,numbers=0,items=[],children=[]):
            self.name=name
            self.regex=regex
            self.items=items
            self.has_children=False  
            self.flag=flag()
            self.numbers=numbers   
            self.true_value=0 
            self.theoretical_value=0
            self.children=children
      def update_data(self):
            if type(self.numbers)==list and len(self.numbers)>=2:            
                  self.true_value=self.numbers[0]
            if len(self.children)>=1:
                  sum=0
                  for child in self.children:
                        if type(child.true_value)==float:
                              sum+=child.true_value
                        else:
                              print("str in den numbers")      
                  self.theoretical_value=sum 
      def int_data(self):
            if type(self.numbers)==list and len(self.numbers)>=2:
                  for number in self.numbers:
                        number=float(number)
            self.true_value=float(self.true_value)
            self.theoretical_value=float(self.theoretical_value)                
      def flag_entry(self):
            if self.theoretical_value!=self.true_value:
                  self.flag.logical_error=True
                  self.flag.status=True        
            if int(self.true_value)==0:
                  self.flag.true_value_missing=True
                  self.flag.status=True    
      def __str__(self) -> str:
            return self.name      
         
      #verbindlichkeiten,kassenbestand          

 

class annual_account():
      def __init__(self,):
            self.aktiva=account_item("aktiva",aktiva_regex,aktiva_items)
            self.passiva=account_item("passiva",passiva_regex,items=passiva_items) 
            self.text=""
            
            #children umlaufvermögen
            self.vorräte=account_item("vorräte",vorräte_regex)
            self.forderungen=account_item("forderungen",forderungen_regex)
            self.kassenbestand=account_item("kassenbestand",kassenbestand_regex)
            
            #self.jahresfehlbetrag=account_item("jahresfehlbetrag",jahresfehlbetrag_regex)

            #children aktiva
            self.umlaufvermögen=account_item("umlaufvermögen",umlaufvermögen_regex,children=[self.vorräte,self.forderungen,self.kassenbestand])
            self.anlagevermögen=account_item("anlagevermögen",anlagevermögen_regex)
            self.rechnungsabgrenzungsposten=account_item("rechnungsabgrenzungsposten",rechnungsabgrenzungsposten_regex)
            
            self.aktiva=account_item("aktiva",aktiva_regex,children=[self.anlagevermögen,self.umlaufvermögen,self.rechnungsabgrenzungsposten,self.fehlbetrag])
            #children passiva
            self.gezeichnetes_kapital=account_item("gezeichnetes_kapital",gezeichnetes_kapital_regex,)
            self.verlustvortrag=account_item("verlustvortrag",verlustvortrag_regex)
            self.überschuss=account_item("überschuss",überschuss_regex)
            self.gewinnvortrag=account_item("gewinnvortrag",gewinnvortrag_regex)
            self.fehlbetrag=account_item("fehlbetrag",fehlbetrag_regex)

            self.eigenkapital=account_item("eigenkapital",eigenkapital_regex,children=[self.gewinnvortrag,self.fehlbetrag,self.verlustvortrag,self.gezeichnetes_kapital])
            self.rückstellungen=account_item("rückstellungen",rückstellungen_regex)
            self.verbindlichkeiten=account_item("verbindlichkeiten",verbindlichkeiten_regex)

            self.passiva=account_item("passiva",passiva_regex,children=[self.eigenkapital,self.rückstellungen,self.verbindlichkeiten])

            self.all_items=[self.vorräte,self.forderungen,self.kassenbestand,self.gewinnvortrag,self.jahresfehlbetrag,self.umlaufvermögen,self.anlagevermögen,self.eigenkapital,self.eigenkapital,
                            self.aktiva,self.rückstellungen,self.verbindlichkeiten,self.passiva]
            self.first_layer=[self.aktiva,self.passiva]
            self.dict={"aktiva":{"true_value":self.aktiva.true_value}}
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
                                    print(child.name)
                                    print(self.dict[aktivapassiva.name]["children"][child.name])
                                    print(grandchild.name)
                                    self.dict[aktivapassiva.name]["children"][child.name]["children"].update(dict_two)
                        #hier müssen noch mehr layer kommen
      def search_for_data(self):
            if self.text!="":
                  for item in self.all_items:
                        data=pattern_finder(item.regex,self.text)
                        item.numbers=data
                        item.int_data()
                        item.update_data()
                        print(data)
      def check_flags(self):
            for item in self.all_items:
                  item.flag_entry()
                  if item.flag.status==True:
                        self.flag_dict[item.name]={"logical_error":item.flag.logical_error,"true_value_missing":item.flag.true_value_missing}


                                                      
def initialize_data_assignment_for_annual_accounts():
      for company_name,company_object in company_object_dict.items():
            for year,annual_account_object in company_object.annual_accounts.items(): #haben wir hier überhaupt die items schon?
                  annual_account_object.search_for_data()
                  annual_account_object.create_dict()
                  annual_account_object.check_flags()


company_annual_statements_dict={}


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
verbindlichkeiten_regex=re.compile("\w*\s*verbindlichkeiten"+numbers_string,flags=re.I)
jahresfehlbetrag_regex=re.compile("jahresfehlbetrag"+numbers_string,flags=re.I)
verlustvortrag_regex=re.compile("verlustvortrag"+numbers_string,flags=re.I)
überschuss_regex=re.compile("überschuss"+numbers_string,flags=re.I)


character_pattern=re.compile("[^\d,.\s]\w*")
annual_acount_regex_dict={"imaterielle Vermögensgegenstände":immaterielle_vermögensgegestände_regex,"sachanlagen":sachanlagen_regex,"finanzanlagen":finanzanlagen_regex,"vermögesgegenstände":vermögensgegenstände_regex,"kreditinstitute":kreditinstitute_regex,"aktiva":aktiva_regex,"eigenkapital":eigenkapital_regex,"gezeichnetes_kapital":gezeichnetes_kapital_regex,"gewinnvortrag":gewinnvortrag_regex,"jahresüberschuss":jahresüberschuss_regex,"rückstellungen":rückstellungen_regex,"verbindlichkeiten":verbindlichkeiten_regex,"rechnungsbegrenzungsposten":rechnungsbegrenzungsposten_regex,"passiva":passiva_regex} 
single_number_pattern=re.compile("\d+[,.]\d*[,.]*\d*[,.]*")
all_numbers_pattern=re.compile(numbers_string)




#rechnungsabgrenzungsposten
#aktiva,passiva klappen jetzt?



umlaufvermögen_items=[account_item("vorräte",vorräte_regex),account_item("forderungen",forderungen_regex),account_item("kassenbestand",kassenbestand_regex)]
eigenkapital_items=[account_item("gewinnvortrag",gewinnvortrag_regex),account_item("jahresfehlbetrag",jahresfehlbetrag_regex)]
passiva_items=[account_item("eigenkapital",eigenkapital_regex,eigenkapital_items),account_item("rückstellungen",rückstellungen_regex),account_item("verbindlichkeiten",verbindlichkeiten_regex)]
aktiva_items=[account_item("anlagevermögen",anlagevermögen_regex,items=[account_item("sachanlagen",sachanlagen_regex)]),account_item("umlaufvermögen",umlaufvermögen_regex,items=umlaufvermögen_items)]    

y=account_item("klappts",aktiva_regex)

early_items=[]
#create_gaming_company_names_underscored_json()
start_script("read") #die drei nochmal in ne func?

assign_company_data() #hier erstellen wir die company objects
load_pdf_text() #muss jetzt nach den regex kommen

    

def pattern_finder(pattern,text): #function für die annual_account class
      for string in text:
            if pattern.findall(string)!=[]:
                  #print("pattern found")
                  item=pattern.findall(string)[0] #return immer eine liste mit nur einem eintrag
                  words=character_pattern.findall(item)#könnte das ein problem sein das ich für das erste selecte?
                  key=""

                  for word in words:
                        key=key+" "+word
                  key=key.lstrip()      
                  numbers=all_numbers_pattern.findall(item)
                  numbers=clean_numbers(numbers)
                  print(numbers)
                  return numbers


def search_for_annual_account_items(text): #function returnt einen entry
      data_dict={}
      for string,pattern in annual_acount_regex_dict.items():
            if pattern.findall(text)!=[]:
                  #print("pattern found")
                  item=pattern.findall(text)[0] #return immer eine liste mit nur einem eintrag
                  
                  words=character_pattern.findall(item)#könnte das ein problem sein das ich für das erste selecte?
                  key=""

                  for word in words:
                        key=key+" "+word
                  key=key.lstrip()      
                  numbers=all_numbers_pattern.findall(item)
                  numbers=clean_numbers(numbers)
                  print(numbers)
                  save=False
                  for string in numbers:
                        if string!=" " or ",":
                              save=True
                  if save==True:            
                        dict_entry={key:numbers}
                        #flag_entries(dict_entry)
                        return dict_entry  #regex dict hat strings als keys die den Regex beschreiben
                  #print(dict_entry)
                  #nicht den vorgefertigten String nehmen sondern was davor steht! als key
                  
                  break


flagged_entries={}

def clean_numbers(list):
      new_list=[]
      for entry in list:
            if single_number_pattern.findall(entry)!=[]:

                  split=entry.split()
                  for string in split:
                        print(string)
                        try: #wir haben hier anscheinend auch strings drin
                              string=string.replace(".","")
                              string=string.replace(",",".") #deutsche schreibeweise zur englischen
                              string=float(string)
                              new_list.append(string)
                        except:
                              None      
      return new_list   

def flag_entries(dict):
      for key,list in dict.items(): #das hier muss ich noch ändern
            if len(list)>=3:
                  flagged_entries.update({key:list})

       

yearly_data={}



item_list=[]

#print(company_object_dict["crytek"])
def search_pdf_text_for_data(): #erstellt das dict das unabhängig von den company objects ist
      for company,dict in pdf_text_dict.items():
            for year,text in dict.items():
                  company_object_dict[company].annual_accounts[year]={} #wir erstellen für die Jahre zunächste ein leeres dict
                  for string in text:
                        item=search_for_annual_account_items(string)
                        
                        if item != None:
                              item_list.append(item)
                              flag_entries(item)
                              key=list(item.keys())[0]
                              number=item[key][0]
                              company_object_dict[company].annual_accounts[year].update({key:number})
                        

            

#search_pdf_text_for_data()

def update_all_company_json():
      companies_dir="C:/Users/lukas/Desktop/bachelor/data/companies"
      for company_name,company_object in company_object_dict.items():
            data_dict=company_object.annual_accounts
            create_json_from_dict(data_dict,company_name,directory=companies_dir)

#update_all_company_json()


initialize_data_assignment_for_annual_accounts()
print(company_object_dict["a4vr"].annual_accounts["2021"].dict)
print(company_object_dict["a4vr"].annual_accounts["2021"].flag_dict)
print("script finished")


#fixliste
#kassenbestand, 