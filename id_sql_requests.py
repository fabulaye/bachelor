import pandas as pd
import wrds
import os
#from datahandling.change_directory import chdir_sql_requests()
def chdir_sql_requests():
    os.chdir("C:/Users/lukas/Desktop/bachelor/data/sql_data")

orbis_tables=["ob_legal_info_","ob_key_financials_eur_","ob_all_cur_shh_1st_level_","ob_all_subs_first_level_","ob_detailed_fmt_ind_eur_int_","ob_dmc_previous_","ob_dmc_current_only_","ob_ind_g_fins_eur_int_","ob_ind_g_fins_eur_","ob_trade_description_"] #financials_orbis?

amadeus_tables=["company_","activities_","managers_","overview_","shareholders_","subsidiaries_","financials_"]

def fetch_all(connection,database):
    connection=wrds.Connection(wrds_username="lukasmeyer")
    all_ids=pd.read_csv("C:/Users/lukas/Desktop/bachelor/data/id/all_ids.csv")
    chdir_sql_requests()
    ids=tuple(all_ids["bvdid"])
    if database=="amadeus":
        tables=amadeus_tables
        size_dict=amadeus_size_dict
        database_prefix="bvd_ama_"
        id_name="idnr"
    if database=="orbis":
        tables=orbis_tables
        size_dict=orbis_size_dict
        database_prefix="bvd_orbis_"
        id_name="bvdid"
    for table in tables:
        df_table=pd.DataFrame()
        for size_long,size_short in size_dict.items():
            table_name=table+size_short
            df_subtable=connection.raw_sql(f"SELECT * FROM {database_prefix}{size_long}.{table_name} WHERE {id_name} IN {ids}")
            #sub_ids=df_subtable[id_name]
            #filtered_df = all_ids.loc[all_ids['bvdid'].isin(sub_ids)]
            #df_subtable["treatment"]=filtered_df["treatment"]
            df_table=pd.concat([df_table,df_subtable],ignore_index=True)
        csv_name=table[:-1]+database_prefix[:-1]+".csv"
        df_table.to_csv(csv_name,index=False)
    connection.close()

amadeus_size_dict={"small":"s","medium":"m","large":"l","verylarge":"v"}
orbis_size_dict={"small":"s","medium":"m","large":"l"}




#treatment variable adden

