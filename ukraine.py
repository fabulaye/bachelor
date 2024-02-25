from bs4 import BeautifulSoup as bs
import requests
from my_html_requests import *
from file_manager.string_to_text import string_to_txt
from file_manager.dict_to_json import dict_to_json
import os
import datetime
import pandas as pd

url_list=["https://www.president.gov.ua/en/news/glava-derzhavi-mi-ne-znimayemo-pitannya-pro-vstup-ukrayini-d-72885","https://www.president.gov.ua/en/news/glava-derzhavi-mi-ne-znimayemo-pitannya-pro-vstup-ukrayini-d-72885"]
data_dict={}
path="E:/ukraine_db/txt"
#path="C:/Users/Lukas/Desktop/ukraine"

def url_loop(url_list): #hier möglicherweuise auch ins package packen
    id=0
    for url in url_list:
        text=text_request(url)
        string_to_txt(text,str(id),path)
        id+=1


#from txt_pdf.read_txt import txt_to_str
#input_1=txt_to_str(path+"/txt/1.txt")


def replace_month(month):
    months_dict={"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,"July":7,"August":8,"September":9,"October":10,"November":11,"December":12}
    for month_char,month_number in months_dict.items():
        if month==month_char:
            return month_number

def deconstruct_text(text):
    text_split=text.split("\n")
    #möglicherweise die leeren deleten
    title=text_split[0]
    date=text_split[1]
    date_split=date.split()[:3]
    day=int(date_split[0])
    month=replace_month(date_split[1])
    year=int(date_split[2])
    date_time_obj=datetime.datetime(year,month,day)
    calender_week=date_time_obj.strftime("%V")
    date=date_time_obj.strftime("%x")
    body=text_split[2:]
    dict={"title":title,"body":body,"date":date,"week":calender_week}
    return dict



#countries,Institutions,emotions,war,russia,Personen,victory,defeat,ukraine,
#justice,Defense,Crimea,border
#word_cloud erstellen und untersuchen
#Mit welchen Kateogorien möchte ich das Model trainieren? Peace, Victory, Defeat, Justice, Allies,power,Military,collective pronouns
#Datastructure:
#Kalenderwoche als class
#rede als class?
#absolute und relative häufigkeit der wordcloud
#länge,datum,be
#dataframe: Woche auf Y, X Wort --> pro wort
#problem mit us und united kingdom

EU_terms=["EU","European Union","Von der Leyen", "European Comission","Council of the EU"]

nato_terms=["nato","stoltenberg",]
history=["Memory","Holodomor",]

regions=["kyiv","sumy","zaporizhzhia","cherkasy","chernihiv","chernivtsi","dnipropretrovsk","donetsk","kharkiv","ivano-frankivsk","kherson","khmelnytskyi","kirovohrad","luhansk","lviv","mykolaiv","odesa","poltova","rivne","ternopil","vinnytsia","volyn","zakarpattia","zhytomyr"]

cities_df=pd.read_csv("C:/Users/lukas/Desktop/ukraine/cities.csv",)
cities=cities_df["City name"]

print(type(cities))

countries=["ukraine","poland","germany","italy","bulgaria","romania","estonia","latvia","lithuania","sweden","norway","finland","denmark","belarus","czech","slovakia","netherlands","belgium","russia","portugal","japan","spain","turkey","canada"]

azov=["azov","mariupol","azovstal"]

peace=["peace","negotiations"]

def create_week_data_dict():
    weeks_dict={}
    for id,speech in speech_object_dict.items():
        if speech.calender_week not in weeks_dict.keys():
            weeks_dict[speech.calender_week]={}
            week=weeks_dict[speech.calender_week]
        else:
            week=weeks_dict[speech.calender_week]
        for word,count in speech.words.items():
            if word not in week.keys():
                week[word]=count
            else: 
                sum=week[word]+count
                week[word]=sum
    return weeks_dict

        
def word_cloud():
    words_dict={}
    for id,speech in speech_object_dict.items():
        for word,count in speech.words.items():
            if word not in words_dict.keys():
                words_dict[word]=count
            else:
                words_dict[word]=words_dict[word]+count
    return words_dict







class speech():
    def __init__(self,text,id) -> None:
        self.id=id
        self.date=None
        self.len=None
        self.words=None
        self.calender_week=None
        self.text=text
        self.title=None
    def get_date_title(self):
        text_split=self.text.split("\n")
        self.title=text_split[0]
        date=text_split[1]
        date_split=date.split()[:3]
        day=int(date_split[0])
        month=replace_month(date_split[1])
        year=int(date_split[2])
        date_time_obj=datetime.datetime(year,month,day)
        self.calender_week=date_time_obj.strftime("%V")
        date=date_time_obj.strftime("%x")
        self.date=date
    def word_counter(self):
        dict={}
        text=self.text.lower()
        text_split=text.split()
        for word in text_split:
            if word not in dict.keys():
                dict[word]=1
            else:
                dict[word]+=1
        self.words=dict


from txt_pdf.read_txt import txt_to_str
def create_speech_objects():
    speech_object_dict={}
    os.chdir(path)
    for text_file in os.listdir():
        string=txt_to_str(text_file)
        id=text_file[:-4]
        speech_object=speech(string,id)
        speech_object_dict[id]=speech_object
        print(f"Object {id} created")
    return speech_object_dict

speech_object_dict=create_speech_objects()

def assign_data_to_speech_objects():
    for id,speech_object in speech_object_dict.items():
        speech_object.word_counter()
        speech_object.get_date_title()
        print(f"Data Assigned to file {id}")

assign_data_to_speech_objects()
week_data=create_week_data_dict()
week_data=dict(sorted(week_data.items()))

word_cloud_dict=word_cloud()
word_cloud_dict=dict(sorted(word_cloud_dict.items(),key=lambda x: x[1],reverse=True))

countries_dict={country:word_cloud_dict[country] for country in countries}



def sort_dict_by_values(dictionary,reverse=True):
    new_dict=dict(sorted(dictionary.items(),key=lambda x: x[1],reverse=reverse))
    return new_dict

countries_dict=sort_dict_by_values(countries_dict)


del_grammar_list=["those","how","when","already","an","or","if","even","these","everything","been","adress","such","because","any","many","than","day",]


#df=pd.DataFrame(week_data)
#print(df.describe())
#peace_df=df.loc["eu"]
#print(peace_df)
#from matplotlib import pyplot as plt
#figure=plt.stairs(peace_df)
#plt.show()
