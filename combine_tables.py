import pandas as pd
from file_manager.change_directory import chdir_data,chdir_fig
chdir_data()
import matplotlib.pyplot as plt
from scipy.stats import linregress

released_steam=pd.read_excel("released_steam.xlsx")
games_förderung_df=pd.read_excel("Games_Förderung_df.xlsx")
jahresberichte_game_ev=pd.read_excel("Jahresberichte_game_ev.xlsx")
#jahresberichte_game_ev=jahresberichte_game_ev.set_index(jahresberichte_game_ev["year"])


#print(games_förderung_df.index)
new_df=pd.concat([games_förderung_df,released_steam["published"]],axis=1)
new_df.to_excel("combined_df.xlsx")
published_projects_df=new_df[new_df["published"]==True]



class year_data():
    def __init__(self,year) -> None:
        self.year=year
        self.length=None
        self.average_fördersumme=None
        self.median_fördersumme=None
        self.summed_fördersumme=None
        self.started_projects=None
        self.ended_projects=None
        self.data_dict={}
    def create_data_dict(self):
        self.data_dict={"year":self.year,"length":self.length,"summed_fördersumme":self.summed_fördersumme,"average_fördersumme":self.average_fördersumme,"median_fördersumme":self.median_fördersumme}    
        


end2020=new_df[new_df["end"]==2020]
end2021=new_df[new_df["end"]==2021]
end2022=new_df[new_df["end"]==2022]
end2023=new_df[new_df["end"]==2023]
end2024=new_df[new_df["end"]==2024]
end2025=new_df[new_df["end"]==2025]
end2026=new_df[new_df["end"]==2026]

end_year_df_dictionary={2020:end2020,2021:end2021,2022:end2022,2023:end2023,2024:end2024,2025:end2025,2026:end2026}


columns=["year","lenght","summed_fördersumme","average_fördersumme","median_fördersumme"]

def collect_year_data(year_df_dictionary):
    whole_df=pd.DataFrame()
    year_objects_dict={}
    counter=0
    for year in range(2020,2026):
        df=year_df_dictionary[year]
        year_objects_dict[year]=year_data(year)
        year_objects_dict[year].length=len(df.index)
        year_objects_dict[year].summed_fördersumme=df["fördersumme"].sum()
        year_objects_dict[year].average_fördersumme=year_objects_dict[year].summed_fördersumme/year_objects_dict[year].length
        year_objects_dict[year].median_fördersumme=df["fördersumme"].median()
        year_objects_dict[year].create_data_dict()
        #whole_df.loc[counter]=year_objects_dict[year].data_dict
        series=pd.DataFrame(year_objects_dict[year].data_dict,index=[year])
        print(series)
        whole_df=pd.concat([whole_df,series])
    print(whole_df)    
    return year_objects_dict,whole_df

dict,whole_df=collect_year_data(end_year_df_dictionary)

#plt.bar(whole_df.index,whole_df["length"])
#plt.bar(whole_df.index,whole_df["average_fördersumme"])
#plt.bar(whole_df.index,whole_df["median_fördersumme"])

#plt.show()



def create_and_save_fig(x_data,y_data,title,x_lable,y_lable,ylim=None,xlim=None):
    plt.plot(x_data,y_data)
    plt.title(title)
    plt.ylabel(y_lable)
    plt.xlabel(x_lable)
    if ylim!=None:
        plt.ylim(ylim)
    if xlim!=None:
        plt.ylim(xlim) 
    chdir_fig()
    plt.savefig(title)    
    plt.show()
           


#create_and_save_fig(jahresberichte_game_ev["year"],jahresberichte_game_ev["companies_total"],"Number of Gaming Companies Germany","Year","Number of Companies",xlim=[0,1000])

print(jahresberichte_game_ev)
print(range(2015,2023))
game_rev_ger=jahresberichte_game_ev.iloc[1:-1,2]
companies_total=jahresberichte_game_ev.iloc[1:-1,-3]
print(linregress(game_rev_ger,companies_total))
