from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import regex as re

nba_season_85_86_url="https://www.eskimo.com/~pbender/misc/salaries86.txt"
nba_season_85_86=requests.get(nba_season_85_86_url)

nba_season_85_86=nba_season_85_86.text
nba_season_85_86=nba_season_85_86.replace(".","")
print(nba_season_85_86)


#test=re.search(r"\w\w",nba_season_85_86)

#print(test.string)