from exploration.count_nans import count_nan
import pandas as pd
import os
from matplotlib import pyplot as plt

from exploration.nan_heatmap import nan_heatmap

def chdir_sql_requests():
    os.chdir("C:/Users/lukas/Desktop/bachelor/data/sql_data")
chdir_sql_requests()
amadeus_financials=pd.read_csv("financialsbvd_ama.csv")
amadeus_nans=count_nan(amadeus_financials)
orbis_financials=pd.read_csv("ob_ind_g_fins_eurbvd_orbis.csv")
orbis_nans=count_nan(orbis_financials)

# Ensure the company column is named correctly, e.g., 'Company'
# If not, rename it accordingly
# df.rename(columns={'your_company_column': 'Company'}, inplace=True)

# Group by company and count the number of records for each company
def number_comp():
    company_counts = amadeus_financials['idnr'].value_counts()
    value_counts=company_counts.value_counts()
    print(value_counts)

    # Creating the bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(value_counts.index, value_counts, color='blue')
    plt.xlabel('Number of Reports')
    plt.ylabel('Number of Companies')
    plt.title('Frequency Bar Chart')
    #plt.xticks(range(len(labels)), labels, rotation=90)  # Rotate the x labels for better readability
    plt.tight_layout()  # Adjust layout to make room for the labels
    plt.show()

    # Show the plot
    plt.show()

nan_heatmap(orbis_financials,"Orbis Nans")