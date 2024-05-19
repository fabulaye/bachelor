import pandas as pd
from lukasdata.change_directory import chdir_data

chdir_data()

imputed_data=pd.read_csv("rf_imputed.csv")
#muss noch verschoben werden
def get_len_of_groups(df: pd.DataFrame,groupby_string: str):
    len_dict={}
    grouped_df=df.groupby(groupby_string)
    for group_name,group_data in grouped_df:
        length=len(group_data)
        if length in len_dict.keys():
            len_dict[length]+=1
        else:
            len_dict[length]=1
    return len_dict


length_of_groups=get_len_of_groups(imputed_data,"idnr")

def order_dict_by_key(dictionary):
    sorted_dict=dict(sorted(dictionary.items(), key=lambda x: x[0]))
    return sorted_dict

length_of_groups=order_dict_by_key(length_of_groups)

print(length_of_groups)