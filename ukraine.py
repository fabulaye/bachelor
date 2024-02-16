from bs4 import BeautifulSoup as bs
import requests
from my_html_requests import *
from file_manager.string_to_text import string_to_txt
from file_manager.dict_to_json import dict_to_json
import os
import datetime


url_list=["https://www.president.gov.ua/en/news/glava-derzhavi-mi-ne-znimayemo-pitannya-pro-vstup-ukrayini-d-72885","https://www.president.gov.ua/en/news/glava-derzhavi-mi-ne-znimayemo-pitannya-pro-vstup-ukrayini-d-72885"]
data_dict={}
path="E:/ukraine_db"

def url_loop(url_list): #hier möglicherweuise auch ins package packen
    id=0
    for url in url_list:
        text=text_request(url)
        string_to_txt(text,str(id),path)
        id+=1



text='''President at a meeting with educators and winners of international academic competitions: A teacher is one who fills a person with meaning, light and values
1 October 2021 - 13:15

President at a meeting with educators and winners of international academic competitions: A teacher is one who fills a person with meaning, light and values

President Volodymyr Zelenskyy met with the winners of international academic competitions, their teachers, winners of the Teacher of the Year competition and members of the Board of the Presidential Fund for Education, Science and Sports.

The President congratulated the teachers on the upcoming holiday - the Day of Educators, which is celebrated annually on the first Sunday of October. He noted that today more than 1 million people work in the field of education, not all of them are teachers by education, but everyone does a very important job.

“The teacher is much broader, much deeper than lessons, tests and notebooks. The teacher is the one who changed you. Gave something very valuable. Not what you learned for the first time, but what you learned forever. Not what was on the surface, but what you saw between the lines, understood and solved," the President said.

Volodymyr Zelenskyy said that on the example of his father - a teacher and professor of mathematics - he realized that teaching is really a matter of life.

“The teacher is not the one who fills in the journal, but the one who fills others - little people - with meaning, light and values. Not the one who signs your academic diary, but the one who leaves his signature in your memory and in your character. The teacher is his students. And a great teacher is his students who raised other students. The teacher is the ability to spread good and light in a geometric progression. Because he alone can inspire hundreds, thousands and even tens of thousands of people to change this world for the better," the Head of State said, adding that it is enough to be a decent person for this.

He stressed that the role of teachers and educators is of great importance for society and for the country.

"We can't yet reflect your role in the salaries you really deserve - it's true. We are building and repairing kindergartens and schools, but we haven’t done everything yet. And there are problems with the Internet, buses, equipment. All this is also true. But I will tell you frankly that I am working to fix all this, together with the government, together with the ministers. Because I meet with you every year, and I don't want to hide my face every year,” Volodymyr Zelenskyy said.

The Head of State also said that today the meeting is attended by the students who are the pride not only of their teachers, but also of Ukraine, because they are the winners of international academic competitions.

"Last year we talked about it a lot, and finally this year, in January, I established the Prize of the President of Ukraine for the winners of such competitions," he said.

Volodymyr Zelenskyy added that, in addition to students who have won international competitions, the prizes of the President of Ukraine will be given to the teachers who trained them.'''

def replace_month(month):
    months_dict={"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,"July":7,"August":8,"September":9,"October":10,"November":11,"December":12}
    for month_char,month_number in months_dict.items():
        if month==month_char:
            return month_number

def deconstruct_text(text):
    text=str(text)
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

test=deconstruct_text(text)
id=int(os.listdir(path)[-1][:-5])+1
dict_to_json(test,str(id),path)
