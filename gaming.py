from PyPDF2 import PdfReader
import os
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import time 
import openpyxl


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
    def update_time(self):
          self.time=time.time() 



def update_company_data():
      company_dataset=pd.read_excel("data/test.xlsx")
      return company_dataset

company_dataset=update_company_data()

company_dict={}
company_dict_time={}


def assign_company_data():
      global company_id
      for index,row in company_dataset.iterrows():
            company_dict[row["Unternehmen"]]=company(company_id,row["Unternehmen"],row["Time"])
            company_id+=1



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
                  print(time.time())
                  print(company.time)
                  print((time.time()-company.time))
                  request=requests.get(company.link).text
                  with open(str(company_name),"w") as f:
                        for line in request:
                              f.write(line)
                  company.update_time()  
                  print(company_name+" updated")                      
                  index+=1
      os.chdir("C:/Users/lukas/Desktop/bachelor")   

download_htlm()
update_company_dict_time()
company_dataset["Time"]=company_dict_time.values()   
os.chdir("C:/Users/lukas/Desktop/bachelor/data")
company_dataset.to_excel("test.xlsx")  



def read_html_files():
      for company_name,company_object in company_dict.items():
            with open(company_name+".html") as f:
                  company_object.html=f.readlines()

read_html_files() #hier bin ich

def search_for_annual_account(text):
      list=datum_regex.findall(text)
      print(list)

search_for_annual_account()
#print(request_text)

#pattern=re.compile("\d{2}\.\d{2}\.\d{4}")
#ergebnisse=pattern.findall(request_text)
#print(ergebnisse)

datum_regex=re.compile("\d{2}\.\d{2}\.\d{4}")
date_23=re.compile("\d{2}\.\d{2}\.2023")
crytek_regex=re.compile("Crytek")

abschluss_date=re.compile(";\d{2}\.\d{2}\.\d{4}")
title_abschluss=re.compile("Jahresabschluss")
#date_results=abschluss_date.findall(request_text)
#print(date_results)

#soup = BeautifulSoup(request_text,"lxml")
#crytek_search=soup.find_all(string=crytek_regex) #works with regex
#search_2023=soup.find_all(string=abschluss_date) #works with regex
#title_serch=soup.find_all(title=title_abschluss)
#print(title_serch)






