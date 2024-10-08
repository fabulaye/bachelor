from datahandling.change_directory import chdir_data
import pandas as pd
from processing.my_df import mydf

chdir_data()
imputed_df=pd.read_excel("treatment_and_control_merged_imputed.xlsx")
imputed_df=mydf(imputed_df)

imputed_df.build_statistics("treatment_and_control_imputed")

#print(bmwki_df.statistics)
imputed_df.statistics.create_kde_figs()
imputed_df.statistics.create_hist_figs()