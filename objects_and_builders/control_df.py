from processing.my_df import mydf
import pandas as pd
import os
from datahandling.change_directory import chdir_data
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datahandling.change_directory import chdir_data
from wrds_database import full_workflow
from processing.my_list import list_difference
from build_ids import id_dict
import subprocess

class control_df(mydf):
    def __init__(self,df) -> None:
        super().__init__(df)
        chdir_data()
        self.treated_names=pd.read_csv("bmwi_request.csv")["Zuwendungsempfänger"].to_list()
        os.chdir("control")
        self.control_names=pd.read_csv("game_ev_members.csv")["name"]
        self.to_be_deleted=pd.read_csv("manual_deleted.csv").to_list()
    def manual_del(self):
        new_list=[]
        for member in self.control_names:
            if member not in self.to_be_deleted:
                new_list.append(member)
        self.control_names=new_list
        return self
    def check_not_treated(self):
        self.control_names=list_difference(self.control_names,self.treated_names)
        return self
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


# Find all div tags with the data_name attribute
#struktur von mydf überlegen, brauche ich hier ein df?

control=control_df()
control.manual_del().check_not_treated()
control_names=control.control_names

full_workflow("general")
os.chdir("control")
control_financials_ama=pd.read_csv("financialsbvd_ama.csv")
control_financials_ob=pd.read_csv("ob_ind_g_fins_eurbvd_orbis.csv") #welches generic df um ids zu extrahieren
control_ids=id_dict(control_financials_ama).append_ids(control_financials_ob)
full_workflow("id",ids=control_ids)
subprocess.run("")

#dann matching anhand von den fiancials

#
#function saves df as specific name
#subprocess run r script:
#r reads df
#r imputes
#r outputs specifc name
#python script reads in df 
