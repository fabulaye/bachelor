from PyPDF2 import PdfReader
import os
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd


os.chdir("C:/Users/lukas/Desktop/bachelor")

company_id=0

class company():
    def __init__(self,id,name) -> None:
          self.id=id
          self.name=name
          self.active=True

company_dataset=pd.read_excel("data/test.xlsx")

company_dict={}

def assign_company_data():
      global company_id
      for company_name in company_dataset.Unternehmen:
            company_dict[company_name]=company(company_id,company_name)
            company_id+=1
            
assign_company_data() 
print(company_dict)     
      


aeria_games = PdfReader('aeria_games.pdf')

test=aeria_games.pages[5]

url="https://www.unternehmensregister.de/ureg/result.html;jsessionid=3DC7B3CCD3A1313FEC4BB840738586DD.web01-1"
crytek_url="https://www.unternehmensregister.de/ureg/result.html;jsessionid=62A19A447C2F281BE748FFC562E238B9.web01-1"

request=requests.get(crytek_url)
request_text=request.text

with open("html_file_test","w") as f:
    for line in request_text:
            f.write(line)
    

#print(request_text)

#pattern=re.compile("\d{2}\.\d{2}\.\d{4}")
#ergebnisse=pattern.findall(request_text)
#print(ergebnisse)

datum_regex=re.compile("\d{2}\.\d{2}\.\d{4}")
date_23=re.compile("\d{2}\.\d{2}\.2023")
crytek_regex=re.compile("Crytek")

abschluss_date=re.compile(";\d{2}\.\d{2}\.\d{4}")
title_abschluss=re.compile("Jahresabschluss")
date_results=abschluss_date.findall(request_text)
print(date_results)

soup = BeautifulSoup(request_text,"lxml")
#crytek_search=soup.find_all(string=crytek_regex) #works with regex
search_2023=soup.find_all(string=abschluss_date) #works with regex
title_serch=soup.find_all(title=title_abschluss)
print(title_serch)






