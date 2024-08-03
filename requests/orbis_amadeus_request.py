import os
import pandas as pd

rechtsformen=["GmbH","UG","UG (haftungsbeschränkt)","AG","eG","Unternehmensgesellschaft","e.k","GmbH & Co. KG","mbH","PartG","GbR","PartG","StGes","bSE","KGaA","Handelsgesellschaft mit beschränkter Haftung","Gesellschaft mit beschränkter Haftung","KG"]
rechtsformen_short=["GmbH","UG","UG (haftungsbeschränkt)","AG"]

def orbis_request(connection,names_tuple,output_file_name,backup_name,continue_from_backup=False,*args): #jetzt auch gecapped?
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
    orbis_request_string_small="bvd_orbis_small.ob_w_company_id_table_s"
    orbis_request_string_medium="bvd_orbis_medium.ob_w_company_id_table_m"
    orbis_request_string_large="bvd_orbis_large.ob_w_company_id_table_l"
    request_strings=[orbis_request_string_small,orbis_request_string_medium,orbis_request_string_large]
    full_df=pd.read_csv("orbis_backup.csv",index_col=False)
    for name in names_tuple:
        print(f"{name} is currently being searched")
        for request_string in request_strings:
            request=connection.raw_sql(f"""SELECT * FROM {request_string} WHERE UPPER(name_native) LIKE '%%{name}%%'""")
            if not request.empty:
                full_df=pd.concat([full_df,request])
                full_df.to_csv("orbis_backup.csv")
    full_df.to_csv(output_file_name)     
    return full_df

def orbis_exact_request(connection,names_tuple,output_file_name,backup_name,continue_from_backup=False,*args):
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
    orbis_request_string_small="bvd_orbis_small.ob_w_company_id_table_s"
    orbis_request_string_medium="bvd_orbis_medium.ob_w_company_id_table_m"
    orbis_request_string_large="bvd_orbis_large.ob_w_company_id_table_l"
    request_strings=[orbis_request_string_small,orbis_request_string_medium,orbis_request_string_large]
    if continue_from_backup==True: 
        full_df=pd.read_csv(backup_name,index_col=False)
    else:
        full_df=pd.DataFrame()
    for name in names_tuple:
        print(f"{name} is currently being searched")
        for request_string in request_strings:
            request=connection.raw_sql(f"""SELECT * FROM {request_string} WHERE UPPER(name_native) = '{name}'""")
            if not request.empty:
                full_df=pd.concat([full_df,request])
                full_df.to_csv(backup_name)   
                break  
    full_df.to_csv(output_file_name)
    return full_df


def amadeus_request(connection,names_tuple,output_file_name,backup_name,continue_from_backup=False,*args): #names need to be capitalized and with rechtsform
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
    bvd_small="bvd_ama_small.amadeus_s"
    bvd_medium="bvd_ama_medium.amadeus_m"
    bvd_large="bvd_ama_large.amadeus_l" 
    bvd_verylarge="bvd_ama_verylarge.amadeus_v"
    request_strings=[bvd_small,bvd_medium,bvd_large,bvd_verylarge] 
    for name in names_tuple:
        print(f"{name} is currently being searched")
        for request_string in request_strings:
            request=connection.raw_sql(f"""SELECT * FROM {request_string} WHERE Upper(name_nat) LIKE '%%{name}%%'""")
            if not request.empty:
                full_df=pd.concat([full_df,request])
                full_df.to_csv(backup_name)  
                #break  
    full_df.to_csv(output_file_name)  
    return full_df

def amadeus_exact_request(connection,names_tuple,output_file_name,backup_name,continue_from_backup=False,*args): #names need to be capitalized and with rechtsform
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
    bvd_small="bvd_ama_small.amadeus_s"
    bvd_medium="bvd_ama_medium.amadeus_m"
    bvd_large="bvd_ama_large.amadeus_l" 
    bvd_verylarge="bvd_ama_verylarge.amadeus_v"
    request_strings=[bvd_small,bvd_medium,bvd_large,bvd_verylarge]
    if continue_from_backup==True: 
        full_df=pd.read_csv(backup_name,index_col=False)
    else:
        full_df=pd.DataFrame()
    for name in names_tuple:
        print(f"{name} is currently being searched")
        for request_string in request_strings:
            request=connection.raw_sql(f"""SELECT * FROM {request_string} WHERE Upper(name_nat) = '{name}'""")
            if not request.empty:
                full_df=pd.concat([full_df,request])
                full_df.to_csv(backup_name)   
                break  
    full_df.to_csv(output_file_name)  
    return full_df


def orbis_combination_request(connection,names_tuple,backup):
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
    orbis_request_string_small="bvd_orbis_small.ob_w_company_id_table_s"
    orbis_request_string_medium="bvd_orbis_medium.ob_w_company_id_table_m"
    orbis_request_string_large="bvd_orbis_large.ob_w_company_id_table_l"
    request_strings=[orbis_request_string_small,orbis_request_string_medium,orbis_request_string_large]
    try:
        full_df=pd.read_csv(backup,index_col=False)
    except FileNotFoundError:
        print("no backup")
        full_df=pd.DataFrame()
    for name in names_tuple:
        for rechtsform in rechtsformen_short:
            full_name=name+" "+rechtsform
            print(f"{full_name} is currently being searched")
            for request_string in request_strings:
                request=connection.raw_sql(f"""SELECT * FROM {request_string} WHERE UPPER(name_native) = '{full_name}'""")
                if not request.empty:
                    full_df=pd.concat([full_df,request])
                    full_df.to_csv("orbis_combinatin_backup.csv")
                    break   
    return full_df

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
