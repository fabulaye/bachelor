import pandas as pd
import subprocess
import os
from processing.my_df import mydf,drop_unnamed_columns
from datahandling.change_directory import root_search



factorized_cols=["compcat",]

def miss_forest_imputation_wrapper(df:pd.DataFrame,directory,output_file_name=None,categorial_vars=["compcat","bvdid","rechtsform","age"]):
    df=mydf(df)
    df.reset_index(inplace=True,drop=True)
    #compcat_map={"SMALL":0,"MEDIUM":1,"LARGE":2,"VERY LARGE":3}
    #compcat_factorized,factorization_mapping=df.factorize_series(df["compcat"],compcat_map)
    #df["compcat"]=compcat_factorized  
    #noise_columns=["account_unit","exchrate","number of months"]   
    numeric_df=df.to_numeric()#.drop(columns=noise_columns,errors="ignore") #wieso workt das? Inplace =False?
    categorial_df=df[categorial_vars]
    root=root_search(directory)
    os.chdir(root)
    miss_forest_input_df=pd.concat([categorial_df,numeric_df],axis=1)
    #miss_forest_input_df.drop(columns="Unnamed: 0",errors="ignore",inplace=True)
    miss_forest_input_df=drop_unnamed_columns(miss_forest_input_df)
    miss_forest_input_df.to_csv("miss_forest_input.csv",index=False)
    file_name=r"C:\Users\Lukas\Documents\GitHub\bachelor\imputation\miss_forest_imputation.R"
    result=subprocess.run([f"Rscript",file_name,root],capture_output=True,text=True)
    print(result.stdout)
    print(result.stderr)
    os.chdir(root)
    imputed=pd.read_excel("miss_forest_output.xlsx")
    non_numeric_columns=[item for item in df.non_numeric_cols() if item not in categorial_vars]
    non_numeric_df=df[non_numeric_columns]
    complete=pd.concat([non_numeric_df,imputed],axis=1)
    os.remove("miss_forest_input.csv")
    os.remove("miss_forest_output.xlsx")
    if output_file_name!=None:
         complete.to_excel(output_file_name)
    return complete

#treatment oder control parameter --> wirkt sich auf directories aus