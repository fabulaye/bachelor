import pandas as pd

def delete_game_ev_members():
    new_list=[]
    game_ev_members=pd.read_csv("game_ev_members.csv")
    to_be_deleted=pd.read_csv("manual_deleted.csv").to_list()
    for member in game_ev_members["name"]:
        if member not in to_be_deleted:
            new_list.append(member)
    new_series=pd.Series(new_list,name="name")
    new_series.to_csv("manual_deleted.csv")


delete_game_ev_members()



#I should manually filter out all of them that are not publishers/developers
#Can I search steam/mobygames for german companies
#foreign companies


#what are advantages of using these matching techniques as opposed to just comparing the effects?
#read literature on what new matching ml techniques there are


#aplly matching to discard control companies that are dissimilar

#propensity score matching
#Mahalanobis Distance Matching
#use compcat for matching 
#Coarsened Exact Matching (CEM)
#neares neighbor matching
#Synthetic Control Method

#how Can I compare different matching methods?


