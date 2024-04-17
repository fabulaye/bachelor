from file_manager.change_directory import chdir_data
import pandas as pd

gemeinden_df=pd.read_excel("C:/Users/lukas/Downloads/Anschriften_der_Gemeinde_und_Stadtverwaltungen_Stand_31012023_final.xlsx",sheet_name="Anschriften_31_01_2023")

gemeinden_und_bundesländer=gemeinden_df.iloc[:,[7,1]].dropna()

def remove_description(gemeinden_und_bundesländer):
    gemeinde_list=[]
    for i in range(len(gemeinden_und_bundesländer)):
        gemeinde=gemeinden_und_bundesländer.iloc[i,0]
        gemeinde_split=gemeinde.split(",")
        if len(gemeinde_split)>1:
            gemeinde=gemeinde_split[0]
        gemeinden_und_bundesländer.iloc[i,0]=gemeinde
    return gemeinden_und_bundesländer

gemeinden_und_bundesländer=remove_description(gemeinden_und_bundesländer).reset_index(drop=True)
gemeinden_und_bundesländer.columns=["gemeinden","bundesländer"]
print(gemeinden_und_bundesländer)
chdir_data()
gemeinden_und_bundesländer.to_csv("gemeinden_und_bundesländer.csv")