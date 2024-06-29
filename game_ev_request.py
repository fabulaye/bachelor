import requests
from bs4 import BeautifulSoup
import pandas as pd
from datahandling.change_directory import chdir_data



# Find all div tags with the data_name attribute
def game_ev_request():
    request=requests.get("https://www.game.de/mitglieder/")
    lst=[]
    soup = BeautifulSoup(request.text, 'html.parser')    
    divs_with_data_name = soup.find_all('div', attrs={'data-name': True})
    company_names = [div['data-name'] for div in divs_with_data_name]
    for company in company_names:
        company=str(company)
        if not company.startswith(("hochschule","prof")):
            lst.append(company)
    
    company_names_series=pd.Series(lst,name="name")
    chdir_data()
    
    company_names_series.to_csv("game_ev_members.csv")

