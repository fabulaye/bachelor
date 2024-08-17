import regex as re
import pandas as pd
from datahandler.change_directory import chdir_data
from lukasdata.cleaning.return_rechtsform import return_rechtsform,strip_rechtsform
from my_strip import my_rstrip


class project():
    def __init__(self,data) -> None:
        self.data=data
    def clean_subsidy(self):
        self.data["subsidy"]=re.sub("€|Euro","",self.data["subsidy"])
        self.data["subsidy"]=re.sub(",00","",self.data["subsidy"]).replace(".","").rstrip()
    def clean_date(self):
        date_regex=re.compile("\d\d\.\d\d\.\d\d\d\d")
        dates=date_regex.findall(self.data["length"])
        try:
            start=dates[0]
            end=dates[1]
            self.data["start_date"]=start
            self.data["end_date"]=end

        except IndexError:
            print(f"Dates is not correctly formatted: {dates}")
    def seperate_company_and_location(self):
        split=re.split(",|;",self.data["company"])
        name_and_rechtsform=split[0].strip()
        city=split[1].strip()
        if city in gemeinden_list:
            bundesland=gemeinde_bundesland_dict[city]
            self.data["city"]=city
            self.data["bundesland"]=bundesland
        else:
            None
            #errorhandling
        rechtsform=return_rechtsform(name_and_rechtsform)
        name=my_rstrip(name_and_rechtsform,rechtsform)
        print(name)
        print(rechtsform)
        self.data["rechtsform"]=rechtsform
        self.data["name"]=name
    def drop_columns(self):
        self.data.drop(["length","company","content"],inplace=True)

chdir_data()
gemeinden_and_bundesländer=pd.read_csv("gemeinden_und_bundesländer.csv")
gemeinden_list=gemeinden_and_bundesländer["gemeinden"].to_list()
bundesländer_list=gemeinden_and_bundesländer["bundesländer"].to_list()
gemeinde_bundesland_dict=dict(zip(gemeinden_list,bundesländer_list))


def clean_spider_output():
    output=pd.read_csv("E:/crawler/bmwicrawler/output.csv").iloc[:20,]
    shape=output.shape
    #columns=["bundesland","city"]
    
    for index,project_data in output.iterrows():
        project_instance=project(project_data)
        project_instance.clean_date()
        project_instance.clean_subsidy()
        project_instance.seperate_company_and_location()
        project_instance.drop_columns()
        #data=pd.Series(project_instance.data)
        if index==0:
            new_df=pd.DataFrame(columns=project_instance.data.index) 
        new_df.loc[index]=project_instance.data
    return new_df


cleaned_output=clean_spider_output()
cleaned_output.to_csv("cleaned_output.csv")
