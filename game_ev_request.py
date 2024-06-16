import requests
from bs4 import BeautifulSoup
import pandas as pd
from datahandling.change_directory import chdir_data

request=requests.get("https://www.game.de/mitglieder/")

soup = BeautifulSoup(request.text, 'html.parser')

# Find all div tags with the data_name attribute
divs_with_data_name = soup.find_all('div', attrs={'data-name': True})
company_names = [div['data-name'] for div in divs_with_data_name]
company_names_series=pd.Series(company_names,name="name")
chdir_data()
company_names_series.to_csv("game_ev_members.csv")