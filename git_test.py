from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import regex as re
import os


os.chdir("C:/Users/lukas/Desktop/bachelor/bachelor")
pattern=re.compile("[A-Z]{1}[a-z]+.[A-Z]{1}[a-z]+.[A-Z]*[a-z]+")
salary_pattern=re.compile("^\d+,\d+,*\d*")
delete_list=['Michael Siewenie for', 'Team Payrolls','Patricia Bender',"Los Angeles Lakers","New Jersey Nets","Philadelphia 76ers","New York Knicks","Boston Celtics","Seattle Supersonics","Los Angeles Clippers","Detroit Pistons","Chicago Bulls","Washington Bullets", "Goldon State Warriors", "Houston Rockets", "Phoenix Suns","San Antonio Spurs", "Dallas Mavericks", "Sacramento Kings","Cleveland Cavaliers", "Golden State Warriors", "Portland Trailblazers","Indiana Pacers", "Atlanta Hawks", "Milwaukee Bucks","Denver Nuggets","Utah Jazz"]
#team_list=team_list.split()
nba_season_85_86_url="https://www.eskimo.com/~pbender/misc/salaries86.txt"
nba_season_85_86=requests.get(nba_season_85_86_url)


nba_season_85_86=nba_season_85_86.text
#print(nba_season_85_86)

with open('season85.txt', 'w') as f:
    f.write(nba_season_85_86)
    
   
lines=f.readlines() 
print(lines)
index=0
with open('season85.txt', 'w') as fw:
    for line in lines:
       
        # we want to remove 5th line
        if index <=5:
            fw.write(line)
        index+=1
    

def strip_data(text):
    text.replace(".","")
    text.replace("Total","")
    text.replace("$","")
    text.replace(",","")
    #for team in team_list:
        #text.replace(team,"")
        #print(team)
    return text

nba_season_85_86=strip_data(nba_season_85_86)
#nba_season_85_86_split=nba_season_85_86.split("\n")
#print(nba_season_85_86) #tested den bumms

def clean_data(list):
    for item in list:
        if item in delete_list:
            list.remove(item)
    return list        

results=pattern.findall(nba_season_85_86)
results=clean_data(results)

salaries=salary_pattern.findall(nba_season_85_86)
#print(salaries)



#print(results)

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
        #print(word)        
    return player_list         


nba_season_cleaned=extract_names(nba_season_85_86)
#print(nba_season_cleaned)