from bs4 import BeautifulSoup as bs
import requests
from my_html_requests import *
from file_manager.string_to_text import string_to_txt
from file_manager.dict_to_json import dict_to_json
import os
import datetime


url_list=["https://www.president.gov.ua/en/news/glava-derzhavi-mi-ne-znimayemo-pitannya-pro-vstup-ukrayini-d-72885","https://www.president.gov.ua/en/news/glava-derzhavi-mi-ne-znimayemo-pitannya-pro-vstup-ukrayini-d-72885"]
data_dict={}
#path="E:/ukraine_db"
path="C:/Users/Lukas/Desktop/ukraine"

def url_loop(url_list): #hier möglicherweuise auch ins package packen
    id=0
    for url in url_list:
        text=text_request(url)
        string_to_txt(text,str(id),path)
        id+=1


from txt_pdf.read_txt import txt_to_str
input_1=txt_to_str(path+"/txt/1.txt")


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

test=deconstruct_text(input_1)
id=len(os.listdir(path+"/txt"))
dict_to_json(test,str(id),path+"/json")

