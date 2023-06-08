from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import regex as re
import os

"Los Angeles Lakers","New Jersey Nets","Philadelphia 76ers","New York Knicks","Boston Celtics","Seattle Supersonics","Los Angeles Clippers","Detroit Pistons","Chicago Bulls","Washington Bullets", "Goldon State Warriors", "Houston Rockets", "Phoenix Suns","San Antonio Spurs", "Dallas Mavericks", "Sacramento Kings","Cleveland Cavaliers", "Golden State Warriors", "Portland Trailblazers","Indiana Pacers", "Atlanta Hawks", "Milwaukee Bucks","Denver Nuggets","Utah Jazz"
os.chdir("C:/Users/lukas/Desktop/bachelor/bachelor")
string_pattern=re.compile("[A-Z]{1}[\.a-z']*.[A-Z,1-9]{1}[\.a-z',1-9]*.[A-Z]*[.a-z']*.[A-Z]*[a-z]*")
salary_pattern=re.compile("\d+,\d+,*\d*")
delete_list=['Michael Siewenie for', 'Team Payrolls','Patricia Bender']
#team_list=team_list.split()
nba_season_85_86_url="https://www.eskimo.com/~pbender/misc/salaries86.txt"
nba_season_85_86=requests.get(nba_season_85_86_url)



nba_season_85_86=nba_season_85_86.text


with open('season85.txt', 'w') as f:
    f.write(nba_season_85_86)

with open("season85.txt", "r") as f:
    lines = f.readlines()



index=0
with open('season85.txt', 'w') as fw:
    for line in lines:
       
        # we want to remove 5th line
        if index >=70:
            fw.write(line)
        index+=1
    

def strip_data(text):
    for string in text:#input is liste
         for character in string:
             print(character)
             if character==".":
                 del character
         string.strip()
         
    return text

with open("season85.txt","r") as f:
    nba_season_85_86=f.readlines()


#nba_season_85_86=strip_data(nba_season_85_86)
nba_season_85_86=str(nba_season_85_86)


nba_season_85_86=nba_season_85_86.replace(".","")





def clean_data(text):
    for item in text.split():
        if item in delete_list:
            text.remove(item)
    return text 



results=string_pattern.findall(nba_season_85_86)
results.pop()


def strip_whitespace(list):
    new_list=[]
    for string in list:
        string=string[:-2]
        new_list.append(string)
    return new_list    

results=strip_whitespace(results)


class player():
    def __init__(self,name,salary_dic) -> None:
        id=id
        self.name=name
        self.salary_dic=salary_dic

class season():
    def __init__(self) -> None:
        self.id=id
        self.year=year
        self.salary_dict=dictionary

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



salaries=salary_pattern.findall(nba_season_85_86)




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
season_85_dict=dict(zip(results,salaries))

print(season_85_dict["Larry Bird"])
nba_dict={85:season_85_dict}
