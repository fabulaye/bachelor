import os
import pandas as pd
def orbis_request(connection,names_tuple): #jetzt auch gecapped?
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
    orbis_request_string_small="bvd_orbis_small.ob_w_company_id_table_s"
    orbis_request_string_medium="bvd_orbis_medium.ob_w_company_id_table_m"
    orbis_request_string_large="bvd_orbis_large.ob_w_company_id_table_l"
    request_strings=[orbis_request_string_small,orbis_request_string_medium,orbis_request_string_large]
    full_df=pd.DataFrame()
    counter=0
    for name in names_tuple:
        for request_string in request_strings:
            request=connection.raw_sql(f"""SELECT * FROM {request_string} WHERE UPPER(name_native) LIKE '%%{name}%%'""")
            if not request.empty:
                print(name)
                counter+=1
                if counter==1:
                    full_df=request
                else:
                    full_df=pd.concat([full_df,request])
        if counter%5==0:
            full_df.to_csv("orbis_test.csv")     
    return full_df

def amadeus_request(connection,names_tuple): #names need to be capitalized and with rechtsform
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
    bvd_small="bvd_ama_small.amadeus_s"
    bvd_medium="bvd_ama_medium.amadeus_m"
    bvd_large="bvd_ama_large.amadeus_l" 
    bvd_verylarge="bvd_ama_verylarge.amadeus_v"
    request_strings=[bvd_small,bvd_medium,bvd_large,bvd_verylarge] 
    for name in names_tuple:
        for request_string in request_strings:
            request=connection.raw_sql(f"""SELECT * FROM {request_string} WHERE name_nat LIKE '%%{name}%%'""")
        if not request.empty:
            counter+=1
            if counter==1:
                full_df=request
            else:
                full_df=pd.concat([full_df,request])
        
    return full_df

#Amadeus:
#company_l
#activities_l
#managers_l
#overview_l
#shareholders_l
#subsidiaries_l
#stocks??

#Orbis:
#ob_legal_info_l
#ob_key_financials_eur_l
#ob_all_cur_shh_1st_level_l
#ob_all_subs_first_level_l
#ob_detailed_fmt_ind_eur_int_l
#ob_dmc_previous_l
#ob_dmc_current_only_l
#ob_ind_g_fins_eur_int_l
#ob_ind_g_fins_eur_l
#ob_trade_description_l



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
