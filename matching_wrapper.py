import subprocess
import os
import pandas as pd
from wrapper.r_wrapper import rwrapper
from processing.my_df import drop_unnamed_columns
from datahandling.change_directory import chdir_data

def matching_wrapper(input_path=r"C:\Users\lukas\Desktop\bachelor\data\treatment_and_control_merged_imputed_dropped.xlsx"):
    input=pd.read_excel(input_path)
    input=drop_unnamed_columns(input)
    input.to_excel("matching_input.xlsx")
    rwrapper(r"C:\Users\lukas\Documents\GitHub\bachelor\prop_matching.R")
    chdir_data()
    output=pd.read_excel("matching_output.xlsx")
    os.remove("matching_input.xlsx")
    os.remove("matching_output.xlsx")
    output.to_excel("matched_data.xlsx")
    



