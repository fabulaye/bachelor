import pandas as pd
import wrds
import os
import sys
print(sys.path)

import pandas as pd

from lukasdata.concat_dfs import concat_dfs

def get_amadeus_financials(connection,ids,file_name="sql_amadeus_financial.csv"):
    small_companies_df=connection.raw_sql(f"SELECT * FROM bvd_ama_small.financials_s WHERE idnr IN {ids}")
    medium_companies_df=connection.raw_sql(f"SELECT * FROM bvd_ama_medium.financials_m WHERE idnr IN {ids}")
    large_companies_df=connection.raw_sql(f"SELECT * FROM bvd_ama_large.financials_l WHERE idnr IN {ids}")
    verylarge_companies_df=connection.raw_sql(f"SELECT * FROM bvd_ama_verylarge.financials_v WHERE idnr IN {ids}")
    df=concat_dfs([small_companies_df,medium_companies_df,large_companies_df,verylarge_companies_df])
    #df.set_index("idnr",inplace=True)
    df.to_csv(file_name,index=False)
    return df


connection=wrds.Connection(wrds_username="lukasmeyer")
os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
subsidized_ids=pd.read_csv("id/subsidized_ids_de.csv").iloc[:,1]
subsidized_ids=tuple(subsidized_ids)
subsidized_financials=get_amadeus_financials(connection,subsidized_ids,"subsidized_financial_amadeus.csv")


not_subsidized_ids=pd.read_csv("id/not_subsidized_ids_de.csv")["idnr"]
print(type(not_subsidized_ids))
not_subsidized_ids=tuple(not_subsidized_ids)
print(not_subsidized_ids)
not_subsidized_financials=get_amadeus_financials(connection,not_subsidized_ids,"not_subsidized_financial_amadeus.csv")

connection.close()
