from processing.my_df import mydf
import pandas as pd
import os
from datahandling.change_directory import chdir_data
import requests
#from bs4 import BeautifulSoup
import pandas as pd
from datahandling.change_directory import chdir_data,chdir_root_search
from processing.my_list import list_difference
from objects_and_builders.wrds_database import full_workflow
#from thefuzz import process

def list_difference(list_1, list_2,case_sensitive=True):
    if case_sensitive==True:
        return [item for item in list_1 if item not in list_2]
    elif case_sensitive==False:
        list_1=upper_list(list_1)
        list_2=upper_list(list_2)
        return [item for item in list_1 if item not in list_2]

def rstrip_list(iterable):
    list=[]
    for string in iterable:
        string=str(string)
        list.append(string.rstrip())
    return list

def upper_list(lst):
    lst=list(map(lambda x: x.upper(),lst))
    return lst



class control_df():
    def __init__(self):
        chdir_data()
        self.treated_names=pd.read_csv("bmwi_request.csv")["name"].to_list()
        os.chdir("control")
        #self.control_names=pd.read_csv("game_ev_members.csv")["name"].to_list()
        self.control_names=pd.read_excel("control_mobygames_modified.ods")
        self.control_names=self.control_names[self.control_names["dev_pub"]==1]["name"]
        self.to_be_deleted=pd.read_csv("manual_deleted.csv")["name"].to_list()
        self.ids=None
    def manual_del(self):
        new_list=[]
        for member in self.control_names:
            if member not in self.to_be_deleted:
                new_list.append(member)
        self.control_names=new_list
        return self
    def check_not_treated(self): 
        self.control_names=list_difference(self.control_names,self.treated_names,case_sensitive=False)
        self.control_names=self.control_names
        return self
    def fuzzy_check_not_treated(self,threshhold):
        fuzzy_matches={}
        for name in self.control_names:
            best_match=process.extractOne(name,self.treated_names)
            if int(best_match[1])>=threshhold:
                fuzzy_matches[name]=best_match
        return fuzzy_matches
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
    def general_request(self):
        full_workflow("general",path=r"C:\Users\lukas\Desktop\bachelor\data\control",names=self.control_names)
    def id_request(self,ids):
        full_workflow("id",path=r"C:\Users\lukas\Desktop\bachelor\data\control",ids=ids)
    def filter_control(self):
        chdir_root_search("control")
        filter_df=pd.read_excel("control_mobygames_modified.ods",index_col=False)
        filter_df=filter_df[filter_df["def_pub"]==1]
        #what about the the double ids etc. lieber nicht mergen sondern filtern
        financials=pd.read_excel("financials_with_treatment.xlsx")
        financials_reduced=financials[financials["bvdid"].isin(filter_df["bvdid"].to_list())]
        financials_reduced.to_excel("financials_with_treatment.xlsx",index=False)
        return filter_df

#csv_to_excel(r"C:\Users\lukas\Desktop\bachelor\data\control\control_mobygames.csv")



