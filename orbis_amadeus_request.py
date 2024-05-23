import os
import pandas as pd
def orbis_request(connection,names_tuple): #jetzt auch gecapped?
    try:
        os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
        orbis_request_string_small="bvd_orbis_small.ob_w_company_id_table_s"
        orbis_request_string_medium="bvd_orbis_medium.ob_w_company_id_table_m"
        orbis_request_string_large="bvd_orbis_large.ob_w_company_id_table_l"
        request_strings=[orbis_request_string_small,orbis_request_string_medium,orbis_request_string_large]
        full_df=pd.DataFrame()
        for name in names_tuple:
            for request_string in request_strings:
                request=connection.raw_sql(f"""SELECT * FROM {request_string} WHERE UPPER(name_native) LIKE '%%{name}%%'""")
                if not request.empty():
                    full_df=pd.concat(full_df,request)
        return full_df
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
    whole_df=pd.DataFrame()   
    try:
        for index,name in enumerate(names_tuple):
            if index%10==0:
                whole_df.to_csv("amadeus_backup.csv")
            print(name)
            sql_small_string=f"""SELECT * FROM {bvd_small} WHERE name_nat LIKE '%%{name}%%'"""
            sql_medium_sring=f"""SELECT * FROM {bvd_medium} WHERE name_nat LIKE '%%{name}%%'"""
            sql_large_string=f"""SELECT * FROM {bvd_large} WHERE name_nat LIKE '%%{name}%%'"""
            sql_verylarge_sring=f"""SELECT * FROM {bvd_verylarge} WHERE name_nat LIKE '%%{name}%%'"""
            print(sql_small_string)
            sql_small=connection.raw_sql(sql_small_string)
            sql_medium=connection.raw_sql(sql_medium_sring)
            sql_large=connection.raw_sql(sql_large_string)
            sql_verylarge=connection.raw_sql(sql_verylarge_sring)
            name_df=pd.concat([sql_small,sql_medium,sql_large,sql_verylarge])
            whole_df=pd.concat([whole_df,name_df])
    except Exception as error:
        print(f"amadeus: {error}")
        whole_df=pd.DataFrame()
    return whole_df


def excact_name_amadeus_request(connection,names_tuple):
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
    bvd_small="bvd_ama_small.amadeus_s"
    bvd_medium="bvd_ama_medium.amadeus_m"
    bvd_large="bvd_ama_large.amadeus_l" 
    bvd_verylarge="bvd_ama_verylarge.amadeus_v"
    whole_df=pd.DataFrame()   
    try:
        sql_small_string=f"""SELECT * FROM {bvd_small} WHERE name_nat IN {names_tuple}"""
        sql_medium_sring=f"""SELECT * FROM {bvd_medium} WHERE name_nat IN {names_tuple}"""
        sql_large_string=f"""SELECT * FROM {bvd_large} WHERE name_nat IN {names_tuple}"""
        sql_verylarge_sring=f"""SELECT * FROM {bvd_verylarge} WHERE name_nat IN {names_tuple}"""
        sql_small=connection.raw_sql(sql_small_string)
        sql_medium=connection.raw_sql(sql_medium_sring)
        sql_large=connection.raw_sql(sql_large_string)
        sql_verylarge=connection.raw_sql(sql_verylarge_sring)
        name_df=pd.concat([sql_small,sql_medium,sql_large,sql_verylarge])
        whole_df=pd.concat([whole_df,name_df])
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
        sql_small=connection.raw_sql(f"SELECT * FROM {bvd_small} WHERE"+"%"+"name_nat"+"%"+ f"IN {names_tuple}")
        sql_medium=connection.raw_sql(f"SELECT * FROM {bvd_medium} WHERE"+"%"+"name_nat"+"%"+ f"IN {names_tuple}")
        sql_large=connection.raw_sql(f"SELECT * FROM {bvd_large} WHERE"+"%"+"name_nat"+"%"+ f"IN {names_tuple}")
        sql_verylarge=connection.raw_sql(f"SELECT * FROM {bvd_verylarge} WHERE"+"%"+"name_nat"+"%"+ f"IN {names_tuple}")
        whole_df=pd.concat([sql_small,sql_medium,sql_large,sql_verylarge])
    except Exception as error:
        print(f"amadeus: {error}")
        whole_df=pd.DataFrame()
    return whole_df
