from processing.my_df import mydf
from datahandling.change_directory import chdir_data
import pandas as pd
from processing.format_numbers import german_to_us_numbers
from processing.format_dates import get_year
from datetime import datetime

chdir_data()
bmwki_df=pd.read_csv("bmwi_request.csv")
bmwki_df=mydf(bmwki_df)
bmwki_df["Fördersumme in EUR"]=bmwki_df["Fördersumme in EUR"].apply(german_to_us_numbers)
bmwki_df["start_year"]=bmwki_df["Laufzeit von"].apply(get_year)
bmwki_df["end_year"]=bmwki_df["Laufzeit bis"].apply(get_year)


bmwki_colname_map={"Zuwendungsempfänger":"name","Laufzeit von":"subsidy_start","Laufzeit bis":"subsidy_end","Fördersumme in EUR":"subsidy"}
bmwki_dtype_map={"subsidy_start":datetime,"subsidy_end":datetime,"subsidy":float}

bmwki_df.rename(columns=bmwki_colname_map,inplace=True)

bmwki_df.build_statistics("bmwki",bmwki_dtype_map)
print(bmwki_df.statistics.numeric_and_datetime)
#print(bmwki_df.statistics)
bmwki_df.statistics.create_kde_figs()
bmwki_df.statistics.create_hist_figs()

#print(bmwki_df.describe())
#bmwki_data=data(bmwki_df)
#bmwki_statistics=statistics()

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


