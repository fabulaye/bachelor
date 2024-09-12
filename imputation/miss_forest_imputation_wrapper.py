import pandas as pd
import subprocess
import os
from datahandling.change_directory import chdir_sql_requests

def miss_forest_imputation_wrapper(df:pd.DataFrame):
    df.to_csv("miss_forest_input.csv")
    #os.chdir(r"C:\Users\Lukas\Documents\GitHub\bachelor\imputation")
    file_name=r"C:\Users\Lukas\Documents\GitHub\bachelor\imputation\miss_forest_imputation.R"
    subprocess.run(["Rscript",file_name])
    imputed=pd.read_csv("miss_forest_output.csv")
    os.remove("miss_forest_input.csv")
    os.remove("miss_forest_output.csv")
    return imputed

chdir_sql_requests()
test_df=pd.read_csv("ob_ind_g_fins_eurbvd_orbis.csv")
imputed=miss_forest_imputation_wrapper(test_df)
print(imputed)