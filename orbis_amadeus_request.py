import os
import pandas as pd
def orbis_request(connection,names_tuple): #jetzt auch gecapped?
    try:
        os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
        sql_orbis_large=connection.raw_sql(f"SELECT * FROM bvd_orbis_large.ob_w_company_id_table_l WHERE UPPER(name_native) IN {names_tuple}")
        print("Orbis large done")
        sql_orbis_small=connection.raw_sql(f"SELECT * FROM bvd_orbis_small.ob_w_company_id_table_s WHERE UPPER(name_native) IN {names_tuple}")
        print("Orbis small done")
        sql_orbis_medium=connection.raw_sql(f"SELECT * FROM bvd_orbis_medium.ob_w_company_id_table_m WHERE UPPER(name_native) IN {names_tuple}")
        print("Orbis medium done")
        full_df=pd.concat([sql_orbis_large,sql_orbis_small,sql_orbis_medium])
    except Exception as error:
        print(f"orbis: {error}")
        full_df=pd.DataFrame()
    return full_df


def amadeus_request(connection,names_tuple): #names need to be capitalized and with rechtsform
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
    bvd_small="bvd_ama_small.amadeus_s"
    bvd_medium="bvd_ama_medium.amadeus_m"
    bvd_large="bvd_ama_large.amadeus_l" 
    bvd_verylarge="bvd_ama_verylarge.amadeus_v"   
    try:
        sql_small=connection.raw_sql(f"SELECT * FROM {bvd_small} WHERE name_nat IN {names_tuple}")
        sql_medium=connection.raw_sql(f"SELECT * FROM {bvd_medium} WHERE name_nat IN {names_tuple}")
        sql_large=connection.raw_sql(f"SELECT * FROM {bvd_large} WHERE name_nat IN {names_tuple}")
        sql_verylarge=connection.raw_sql(f"SELECT * FROM {bvd_verylarge} WHERE name_nat IN {names_tuple}")
        whole_df=pd.concat([sql_small,sql_medium,sql_large,sql_verylarge])
    except Exception as error:
        print(f"amadeus: {error}")
        whole_df=pd.DataFrame()
    return whole_df

def amadeus_pgdesc_request(connection,names_tuple,pg_description_tuple): #file_names need to be capitalized
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
    bvd_small="bvd_ama_small.amadeus_s"
    bvd_medium="bvd_ama_medium.amadeus_m"
    bvd_large="bvd_ama_large.amadeus_l" 
    bvd_verylarge="bvd_ama_verylarge.amadeus_v"   
    try:
        sql_small=connection.raw_sql(f"SELECT * FROM {bvd_small} WHERE name_nat IN {names_tuple} AND pgdesc IN {pg_description_tuple}")
        sql_medium=connection.raw_sql(f"SELECT * FROM {bvd_medium} WHERE name_nat IN {names_tuple} AND pgdesc IN {pg_description_tuple}")
        sql_large=connection.raw_sql(f"SELECT * FROM {bvd_large} WHERE name_nat IN {names_tuple} AND pgdesc IN {pg_description_tuple}")
        sql_verylarge=connection.raw_sql(f"SELECT * FROM {bvd_verylarge} WHERE name_nat IN {names_tuple} AND pgdesc IN {pg_description_tuple}")
        whole_df=pd.concat([sql_small,sql_medium,sql_large,sql_verylarge])
    except Exception as error:
        print(f"amadeus: {error}")
        whole_df=pd.DataFrame()
    return whole_df
