import pandas as pd
import os
import numpy as np
from manipulation.create_mask import create_in_mask

os.chdir("C:/Users/lukas/Desktop/bachelor/data")

amadeus_request=pd.read_csv("subsidized_amadeus.csv")
bmwi_request=pd.read_csv("bmwi_request.csv")

def filter_wrong_companies(amadeus_request,bmwi_request):
    names=[]
    for index_amadeus,company in enumerate(amadeus_request["name_nat"]):
        for index_bmwi,company_name_bmwi in enumerate(bmwi_request["Zuwendungsempfänger"]):
            if company_name_bmwi.upper()==company:
                try:
                    bmwi_ort=bmwi_request["Ort"].loc[index_bmwi].upper()
                    #amadeus_ort_small=amadeus_request["city_nat"].loc[index_amadeus]
                    amadeus_ort=amadeus_request["city_nat"].loc[index_amadeus].upper()
                    if bmwi_ort==amadeus_ort:
                        names.append(company)
                except AttributeError:
                    print("Nan")
    names=list(np.unique(np.array(names)))
    return names
names=filter_wrong_companies(amadeus_request,bmwi_request)
print(names)
print(len(names))

correct_amadeus=amadeus_request[create_in_mask(amadeus_request["name_nat"],names)]
print(correct_amadeus)
correct_amadeus.to_csv("filtered_subsidized_amadeus.csv")

