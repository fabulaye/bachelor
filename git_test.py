from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import regex as re

team_list=["Los Angeles Lakers","New Jersey Nets","Philadelphia 76ers","New York Knicks","Boston Celtics","Seattle Supersonics","Los Angeles Clippers","Detroit Pistons","Chicago Bulls","Washington Bullets", "Goldon State Warriors", "Houston Rockets","Houston Rockets", "Phoenix Suns","San Antonio Spurs", "Dallas Mavericks", "Sacramento Kings","Cleveland Cavaliers", "Portland Trailblaizers","Indiana Pacers", "Atlanta Hawks", "Milwaukee Bucks","Denver Nuggets","Utah Jazz"]
team_list=team_list.split()
nba_season_85_86_url="https://www.eskimo.com/~pbender/misc/salaries86.txt"
nba_season_85_86=requests.get(nba_season_85_86_url)

nba_season_85_86=nba_season_85_86.text


def strip_data(text):
    text.replace(".","")
    text.replace("Total","")
    text.replace("$","")
    text.replace(",","")
    for word in team_list:
        text.replace(word,"")
    return text

nba_season_85_86=strip_data(nba_season_85_86)
#nba_season_85_86_split=nba_season_85_86.split("\n")
print(nba_season_85_86) #tested den bumms


#test=re.search("[A-Z]",nba_season_85_86)

#print(test.string)

class player():
    def __init__(self,name,salary_dic) -> None:
        self.name=name
        self.salary_dic=salary_dic


salary_dict={}#player als key dictionary als value, dic enthält saisons als key und gehalt als value

spieler_liste=[]

def int_data(text):
    int_data=[]
    for word in text.split():
        try: 
            int_data.append(int(word))
        except:
            int_data.append(word)
    return int_data        





def extract_names(text):
    data=int_data(text)
    counter=0
    player_list=[]
    player_name=[]
    for word in data:
        if type(word)==str:
            player_name.append(word)
        if type(word)==int:
            if len(player_name)>=2:
                player_list.append(player_name)
                player_name=[]
            else:     
                player_name=[]  
    return player_list         


nba_season_cleaned=extract_names(nba_season_85_86)
#print(nba_season_cleaned)