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
nba_season_85_url="https://www.eskimo.com/~pbender/misc/salaries86.txt"
nba_season_86_url="https://www.eskimo.com/~pbender/misc/salaries87.txt"
nba_season_87_url="https://www.eskimo.com/~pbender/misc/salaries88.txt"
nba_season_88_url="https://www.eskimo.com/~pbender/misc/salaries89.txt"
nba_season_89_url="https://www.eskimo.com/~pbender/misc/salaries90.txt"
nba_season_90_url="https://www.eskimo.com/~pbender/misc/salaries91.txt"
nba_season_91_url="https://www.eskimo.com/~pbender/misc/salaries92.txt"
nba_season_92_url="https://www.eskimo.com/~pbender/misc/salaries93.txt"
nba_season_93_url="https://www.eskimo.com/~pbender/misc/salaries94.txt"
nba_season_94_url="https://www.eskimo.com/~pbender/misc/salaries95.txt"
nba_season_95_url="https://www.eskimo.com/~pbender/misc/salaries96.txt"
nba_season_96_url="https://www.eskimo.com/~pbender/misc/salaries97.txt"
nba_season_97_url="https://www.eskimo.com/~pbender/misc/salaries98.txt"
nba_season_98_url="https://www.eskimo.com/~pbender/misc/salaries99.txt"
nba_season_99_url="https://www.eskimo.com/~pbender/misc/salaries00.txt"
nba_season_90_url="https://www.eskimo.com/~pbender/misc/salaries02.txt"
nba_season_01_url="https://www.eskimo.com/~pbender/misc/salaries03.txt"
nba_season_02_url="https://www.eskimo.com/~pbender/misc/salaries01.txt"
nba_season_03_url="https://www.eskimo.com/~pbender/misc/salaries04.txt"
nba_season_04_url="https://www.eskimo.com/~pbender/misc/salaries05.txt"
nba_season_05_url="https://www.eskimo.com/~pbender/misc/salaries06.txt"
nba_season_06_url="https://www.eskimo.com/~pbender/misc/salaries07.txt"
nba_season_07_url="https://www.eskimo.com/~pbender/misc/salaries08.txt"
nba_season_08_url="https://www.eskimo.com/~pbender/misc/salaries09.txt"
nba_season_09_url="https://www.eskimo.com/~pbender/misc/salaries10.txt"
nba_season_10_url="https://www.eskimo.com/~pbender/misc/salaries11.txt"
nba_season_11_url="https://www.eskimo.com/~pbender/misc/salaries12.txt"
nba_season_12_url="https://www.eskimo.com/~pbender/misc/salaries13.txt"
nba_season_13_url="https://www.eskimo.com/~pbender/misc/salaries14.txt"
nba_season_14_url="https://www.eskimo.com/~pbender/misc/salaries15.txt"
nba_season_15_url="https://www.eskimo.com/~pbender/misc/salaries16.txt"

nba_season_85_86=requests.get(nba_season_85_86_url)

url_list=[nba_season_85_url,]


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
    def __init__(self,id,name) -> None:
        self.id=id
        self.name=name
        self.salary_dic={}

class season():
    def __init__(self,id,year,dict) -> None:
        self.id=id
        self.year=year
        self.salary_dict=dict

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


list_of_dicts=[season_85_dict,]
season_instances_dict={}
global_season_id=0

def create_season_objects(list_of_dicts):
    global global_season_id
    start_year=1985
    for dict in list_of_dicts:
        season_instances_dict[start_year+global_season_id]=season(global_season_id,start_year+global_season_id,dict)
        global_season_id+=1

create_season_objects(list_of_dicts)

player_instances_dict={}
global_player_id=0

def create_player_instances(list_of_season_objects):
    global global_player_id
    for season_object in list_of_season_objects:
        for player_name in season_object.dict:
            player_instances_dict[player_name]=player(global_player_id,player_name)
            global_player_id+=1

list_of_season_objects=[season_85]

create_player_instances(list_of_season_objects)

print(player_instances_dict["Larry Bird"].id)

def assign_salaries():
    for 