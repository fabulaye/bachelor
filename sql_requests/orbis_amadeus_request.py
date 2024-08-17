import os
import pandas as pd

rechtsformen=["GmbH","UG","UG (haftungsbeschränkt)","AG","eG","Unternehmensgesellschaft","e.k","GmbH & Co. KG","mbH","PartG","GbR","PartG","StGes","bSE","KGaA","Handelsgesellschaft mit beschränkter Haftung","Gesellschaft mit beschränkter Haftung","KG"]
rechtsformen_short=["GmbH","UG","UG (haftungsbeschränkt)","AG"]

from sql_requests.request_string_builder import amadeus_request_string,orbis_request_string

def general_request(connection,database_name,names_tuple,output_file_name,search_params={"how":"exact"},backup_name=None,path=None):
    amadeus_tables=["bvd_ama_small.amadeus_s","bvd_ama_medium.amadeus_m","bvd_ama_large.amadeus_l","bvd_ama_verylarge.amadeus_v"] 
    orbis_tables=["bvd_orbis_small.ob_w_company_id_table_s","bvd_orbis_medium.ob_w_company_id_table_m","bvd_orbis_large.ob_w_company_id_table_l"]
    if database_name=="amadeus":
        tables=amadeus_tables
    elif database_name=="orbis":
        tables=orbis_tables
    if backup_name!=None: 
        full_df=pd.read_csv(backup_name,index_col=False)
    else:
        full_df=pd.DataFrame()
    for name in names_tuple:
        print(f"{name} is currently being searched")
        for table in tables:
            if database_name=="amadeus":
                request_str=amadeus_request_string().build_request_string(table,name,search_params).request_string
            elif database_name=="orbis":
                request_str=orbis_request_string().build_request_string(table,name,search_params).request_string
            request=connection.raw_sql(request_str)
            if not request.empty:
                full_df=pd.concat([full_df,request])
                full_df.to_csv(backup_name)  
                #break  
    if path!=None:
        os.chdir(path)
    full_df.to_csv(output_file_name)  
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
