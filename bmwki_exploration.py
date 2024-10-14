from processing.my_df import mydf
from datahandling.change_directory import chdir_data
import pandas as pd
from processing.format_numbers import german_to_us_numbers
from processing.format_dates import get_year
from datetime import datetime
from processing.format_string import format_df
from datahandling.change_directory import chdir_root_search
import os

chdir_data()
bmwki_df=pd.read_csv("bmwi_request.csv")
bmwki_df=format_df(bmwki_df)
bmwki_df=mydf(bmwki_df)
bmwki_df["subsidy"]=bmwki_df["subsidy"].apply(german_to_us_numbers)
#bmwki_df["subsidy_start"]=bmwki_df["subsidy_start"].apply(get_year)
#bmwki_df["subsidy_end"]=bmwki_df["subsidy_end"].apply(get_year)

#bmwki_colname_map={"Zuwendungsempfänger":"name","Laufzeit von":"subsidy_start","Laufzeit bis":"subsidy_end","Fördersumme in EUR":"subsidy"}
bmwki_dtype_map={"subsidy_start":datetime,"subsidy_end":datetime,"subsidy":float}

bmwki_df.build_statistics("bmwki",bmwki_dtype_map)
#print(bmwki_df.statistics.numeric_and_datetime)
#print(bmwki_df.statistics)
#bmwki_df.statistics.create_kde_figs()
#bmwki_df.statistics.create_hist_figs()



treted_names_reduced=pd.read_excel(r"C:\Users\lukas\Desktop\bachelor\data\financials_merge_treatment_and_control_categorials_cleaned_imputed.xlsx")["name"].drop_duplicates().to_list()

bmwki_df_reduced=bmwki_df[bmwki_df["name"].isin(treted_names_reduced)]
bmwki_df_reduced=mydf(bmwki_df_reduced)
bmwki_df_reduced.build_statistics("bmwki_reduced",bmwki_dtype_map)
#bmwki_df_reduced["subsidy_start"]=bmwki_df_reduced["subsidy_start"].apply(get_year)
#bmwki_df_reduced["subsidy_end"]=bmwki_df_reduced["subsidy_end"].apply(get_year)
#print(bmwki_df.statistics.numeric_and_datetime)
#print(bmwki_df.statistics)
# bmwki_df_reduced.statistics.create_kde_figs()
# bmwki_df_reduced.statistics.create_hist_figs()

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

bmwki_description=bmwki_df["subsidy"].describe()
print(bmwki_description)
bmwki_reduced_description=bmwki_df_reduced["subsidy"].describe()
print(bmwki_reduced_description)



def sturges_rule(data):
    n = len(data)
    return int(np.ceil(np.log2(n) + 1))
def create_hist_comparison(values,dataset_names,var_name,dtype,log=False):
    values_1=values[0]
    values_2=values[1]
    if dtype=="date":
        values_1=pd.to_datetime(values_1,format="%d.%m.%Y").apply(lambda x:x.year)
        values_2=pd.to_datetime(values_2,format="%d.%m.%Y").apply(lambda x:x.year)

    bins=max(sturges_rule(values_1),sturges_rule(values_2))
    # Get the minimum and maximum values from both datasets
    min_val = min(values_1.min(), values_2.min())
    max_val = max(values_1.max(), values_2.max())
    # Create common bins based on the range of both datasets
    #bins=sturges_rule(max_n)
    
    bins = np.linspace(min_val, max_val, bins)
    if dtype=="date":
        bins=range(min_val,max_val+1)  # 30 bins (adjust as needed)
    # Create a new figure for each variable
    plt.figure(figsize=(10, 6))
    # Histogram for dataset1 using the common bins
    if log==False:
        sns.histplot(values_1, color='blue', label=dataset_names[0], kde=True, stat="count", bins=bins, alpha=0.5)
        # Histogram for dataset2 using the same bins
        sns.histplot(values_2, color='red', label=dataset_names[1], kde=True, stat="count", bins=bins, alpha=0.5)
    elif log==True:
        sns.histplot(values_1, color='blue', label=dataset_names[0], kde=True, stat="count", bins=bins, alpha=0.5,log_scale=True)
        # Histogram for dataset2 using the same bins
        sns.histplot(values_2, color='red', label=dataset_names[1], kde=True, stat="count", bins=bins, alpha=0.5,log_scale=True)
    # Add labels, title, and legend
    plt.title(f"Comparison of Variable '{var_name}' in Two Datasets")
    plt.xlabel(f"Value of {var_name}")
    plt.ylabel("Density")
    plt.legend()
    # Show the plot
    plt.show()



#subsidy_starts=(bmwki_df["subsidy_start"],bmwki_df_reduced["subsidy_start"])
#create_hist_comparison(subsidy_starts,("bmwki","bmwki_reduced"),"Subsidy Start","date")
#
#subsidy_ends=(bmwki_df["subsidy_end"],bmwki_df_reduced["subsidy_end"])
#create_hist_comparison(subsidy_ends,("bmwki","bmwki_reduced"),"Subsidy End","date")
#
#subsidy=(np.log(bmwki_df["subsidy"]),np.log(bmwki_df_reduced["subsidy"]))
#create_hist_comparison(subsidy,("bmwki","bmwki_reduced"),"Subsidy","num")

def create_violin_plot(data,y_var):
    plt.figure(figsize=(10, 6))
    #sns.violinplot(series)
    sns.violinplot(data=data, x="reduced", y=y_var)
    plt.show()


bmwki_df["reduced"]=[0]*len(bmwki_df)
bmwki_df_reduced["reduced"]=[1]*len(bmwki_df_reduced)
reduced_and_not_reduced=pd.concat([bmwki_df_reduced,bmwki_df])

create_violin_plot(reduced_and_not_reduced,"subsidy")
