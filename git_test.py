from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import regex as re

nba_season_85_86_url="https://www.eskimo.com/~pbender/misc/salaries86.txt"
nba_season_85_86=requests.get(nba_season_85_86_url)

nba_season_85_86=nba_season_85_86.text
nba_season_85_86=nba_season_85_86.replace(".","")
nba_season_85_86=nba_season_85_86.replace("Total","").replace("$","").replace(",","")

nba_season_85_86_split=nba_season_85_86.split("\n")
print(nba_season_85_86) #tested den bumms


test=re.search("[A-Z]",nba_season_85_86)

print(test.string)

class player():
    def __init__(self,name,salary_dic) -> None:
        self.name=name
        self.salary_dic=salary_dic


salary_dict={}#player als key dictionary als value, dic enthält saisons als key und gehalt als value

spieler_liste=[]

def data_cleaning_nba(text):
    for word in text.split():
        try: 
            int(word)
        except:
            spieler_liste.append(word)

data_cleaning_nba(nba_season_85_86)
print(spieler_liste)