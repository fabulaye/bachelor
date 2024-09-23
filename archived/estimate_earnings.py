import pandas as pd
from datahandling.change_directory import chdir_sql_requests

def estimate_earnings():
    chdir_sql_requests()
    data=pd.read_csv("treatmentfinancialsbvd_ama.csv")
    data["earnings"]=[pd.NA]*len(data)
    grouped_data=data.groupby("bvdid")
    data_list=[]
    for bvdid,group_data in grouped_data:
        earnings_list=[pd.NA]
        for index in range(len(group_data)):
            if index>=1:
                difference=group_data[["closdate_year","shfd"]].iloc[index,:]-group_data[["closdate_year","shfd"]].iloc[index-1,:]
                year_difference=difference["closdate_year"]
                earnings=difference["shfd"]
                if year_difference==1:
                    earnings_list.append(earnings)
                else:
                    earnings_list.append(pd.NA)
        group_data["earnings"]=earnings_list
        data_list.append(group_data)
    new_data=pd.concat(data_list)
    new_data
    return new_data

test=estimate_earnings()
test.to_excel("treatmentfinancialsbvd_ama.xlsx")
test.to_csv("treatmentfinancialsbvd_ama.csv")
