from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
from cleaner.return_rechtsform import return_rechtsform
import regex as re
from file_manager.change_directory import chdir_data
from cleaner.return_rechtsform import rechtsform_regex


#html=requests.get("https://www.bmwk.de/Redaktion/DE/Artikel/Wirtschaft/Games/Games-Projekte/blookid3.html")
#print(html.text)


path="C:/Users/lukas/Desktop/bachelor/html_files"

names=["1630-the-thirty-years-war","kinetarium","50-alien","ad-infinitum",
       "aethermancer","airborn-prototyp","airbusneo","airlinesim","all-quiet-in-the-trenches",
       "angry-dynomites-lab","asterix","atlas-a-tongue-like-a-sword",
       "auszeit","auszeit-produktion","autobahnpolizeisimulator3","baby-royale","battle-frontier","battle-wizard-attack",
       "battlejuice-alchemist","beam","beatslayer","behemoth","beryllium","blookid3","blossomanddecay",
       "bombbots_arena","Bonsai","boston-district-bos","botrace-33","break-a-leg","car","card-crawl",
       "catan-big-game","cathedral","chai","chillbiom","cic-pc-port","civitates","climatetimemachine",
       "clockworld","codename-eisenfaust","commandos-origins",
       "constance","construction-simulator-year-one-dlc1","construction-simulator-year-one-dlc1","construction-simulator-year-one-dlc1",
       "coreborn-the-liquidmeadows","Cortex-Station","cove","curious-caves-dlc","dead-age-survivors",
       "dlc-ruffy","drova","drumgame","dungeon-full-dive","dungeons-4","dystopia-evolvingcardgame","earthscaper",
       "eisenfaust_produktion","eisenfaust_produktion","elementokles","elysium","emergency-one","everspace-2-the-companions",
       "fernbus-simulator-dlc-polen","fi-fc","fireside","flightsim-vr","fruits-of-the-forest","fun-fair","g-rebels","game-38",
       "geist-arena","genesis","go-red","goal-2025","goetz","hafermilch","happy","harrison-steel-in-death-awaits",
       "hcc-highrisers-couch-coop","hexxen-1733-morgenstern","hidden-champion","highrise-city-dlc-oepnv","hrc-dlc2",
       "horse-club-adventures-2","humboldt","into-the-cold-projekt","jetpacker","jump-royale","kalle-und-die-zeit",
       "koboldkroniken","last-premiere","leilas-play","lmbas","loc","lost-glitches","lou-s-lagoon","lucky-tower-ultimate",
       "madvalley","mambio","mandibles","marscape","mein-kh","menace","mindbug","miniarena","mission-tatau",
       "mystery-me","neo-berlin-2087","of-pawns-and-kings","ofm-mobile","onlineliga","parking-world-simulator","persist-online","pflaumenmus",
       "pi-preservation-instinct","prim","prime-sim-sports-company-manager","project_5","project-black","project-habanero",
       "project-iron-snail","project-kokidone","project_minerva","project-orca","projekt-stasis","projekt-gonsenheim","pchd",
       "prometheus-produktion","pupi","realms-at-war","reshooter","runewars_ageofsummoning","schiesseisen","schleich-zombie","schwerlast-simulator-2020",
       "serious-game-security-simulator","Shadow-Gambit","solos","sonnenblume","space1889","space-ranger-45","splitrealm","storyvania",
       "super-catboy","taverntalk","the-apartment","the-district-vr-dlc","the-great-sassanelli","thetribemustsurvive","the-wagadu-chronicles",
       "wicked-souls","townitect","tport","tramsim2","tropico6-seasonpass","tropico-7","venice-after-dark-produktion","volksfestspiel-prototyp",
       "waf2","wattwanderung","wild-woods","x24","x26","yoma","you-be-carl"

       ]

abgeschlossen_url=["a-climate-change-rougelike","altwaldheim-2-town-in-trouble","closerthedistance-produktion","closerthedistance",]


def download_html_from_bmwi(names,abgeschlossen_url):
    html_base="https://www.bmwk.de/Redaktion/DE/Artikel/Wirtschaft/Games/Games-Projekte/"
    ending=".html"
    files=os.listdir(path)
    for name in names:
        if name+".txt" not in files:
            url=html_base+name+ending
            request=requests.get(url)
            html_text=request.text
            if request.status_code==200:   
                string_to_txt(html_text,name,path)
            else: print("problem with request")    
    for name in abgeschlossen_url:
        if name+".txt" not in files:
            url=html_base+"Abgeschlossen/"+name+ending
            request=requests.get(url)
            html_text=request.text
            if request.status_code==200:   
                string_to_txt(html_text,name,path)
            else: print("problem with request")   


def string_to_txt(string,file_name,path):
    os.chdir(path)
    with open(file_name+".txt","w",encoding="utf-8") as f:
        f.write(string,)

download_html_from_bmwi(names,abgeschlossen_url)

date_regex=re.compile("\d\d\.\d\d\.\d\d\d\d")

double_entry_regex=re.compile("[\w+\s+]+\w+[,;]\s*[\wäöü]+",flags=re.I)
german_number=re.compile("[\d,\.]+")

def read_txt(path):
  with open(path,"r",encoding="utf-8") as f:
      text=f.readlines()
  return text  

def get_info_from_html(txt_file):
    string=str(txt_file)
    soup=BeautifulSoup(string,features="html.parser")
    table=soup.find_all("td")
    h2_search=soup.find_all("h2")
    data=table[1].text
    name_and_rechtsform=re.split(",|;",table[1].text)[0]
    try:
        project_name=h2_search[-1].text.split(",")[1].lstrip().lstrip("'")
    except:
        project_name=None 
    multiple_entries=double_entry_regex.findall(data)   
    rechtsform_list=[]
    name_list=[]
    place_list=[]
    if len(multiple_entries)<=1:
        rechtsform_list=return_rechtsform(name_and_rechtsform)
        name_list=name_and_rechtsform.rstrip(rechtsform_list)
        place_list=re.split(",|;",table[1].text)[1:]
    else:
        split_data=[]
        for entry in multiple_entries:
            split=re.split("[,;]",entry)
            split_data.append(split[0])
            split_data.append(split[1])
        print(split_data)    
        name_and_rechtsform_1=split_data[0]
        rechtsform_1=return_rechtsform(name_and_rechtsform_1)
        name_1=name_and_rechtsform_1.rstrip(rechtsform_1)
        print(name_1)
        print(rechtsform_1)
        name_and_rechtsform_2=split_data[2]
        rechtsform_2=return_rechtsform(name_and_rechtsform_2)
        name_2=name_and_rechtsform_2.rstrip(rechtsform_2)
        print(name_2)
        print(rechtsform_2)
        place_1=split_data[1]
        place_2=split_data[2]
        name_list.append([name_1,name_2])
        rechtsform_list.append([rechtsform_1,rechtsform_2])
        place_list.append([place_1,place_2])
    fördersumme=re.split("€|Euro",table[5].text)[0]
    fördersumme=german_number.findall(fördersumme)[0]
    fördersumme=int(re.sub(",00","",fördersumme).replace(".","").rstrip())
    datum=table[7].text
    start=date_regex.findall(datum)[0][-4:]
    end=date_regex.findall(datum)[1][-4:]
    return name_list,rechtsform_list,project_name,place_list,fördersumme,start,end
    







def create_dataset(path):
    df=pd.DataFrame(columns=["name","rechtsform","project_name","place","fördersumme","start","end"])
    counter=0
    for file in os.listdir(path):
        html_text=read_txt(path+"/"+file)
        name,rechtsform,project_name,place,fördersumme,start,end=get_info_from_html(html_text)
        data_dict={"name":name,"rechtsform":rechtsform,"project_name":project_name,"place":place,"fördersumme":fördersumme,"start":start,"end":end}
        df.loc[counter]=data_dict
        counter+=1
    return df    


df=create_dataset(path)

print(df)    
chdir_data()
df.to_excel("Games_Förderung_df.xlsx")    




