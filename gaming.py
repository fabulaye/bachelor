from PyPDF2 import PdfReader
import os
import requests
import re
from bs4 import BeautifulSoup


os.chdir("C:/Users/lukas/Desktop/bachelor/bachelor")

aeria_games = PdfReader('aeria_games.pdf')

test=aeria_games.pages[5]


url="https://www.unternehmensregister.de/ureg/result.html;jsessionid=3DC7B3CCD3A1313FEC4BB840738586DD.web01-1"
request=requests.get(url)
request_text=request.text
#print(request_text)

#pattern=re.compile("\d{2}\.\d{2}\.\d{4}")
#ergebnisse=pattern.findall(request_text)
#print(ergebnisse)

soup = BeautifulSoup(request_text,"lxml")
daten=soup.find_all("div",_class="company_result")
print(daten)


