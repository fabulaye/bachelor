import os
import pandas as pd

def publisher_amadeus_request(connection):
    os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
    video_game_pgdesc=create_pgdesc(("Publishing of computer games",""))
    print(video_game_pgdesc)
    bvd_small="bvd_ama_small.amadeus_s"
    bvd_medium="bvd_ama_medium.amadeus_m"
    bvd_large="bvd_ama_large.amadeus_l"    
    try:
        sql_small=connection.raw_sql(f"SELECT * FROM {bvd_small} WHERE pgdesc IN {video_game_pgdesc}")
        sql_medium=connection.raw_sql(f"SELECT * FROM {bvd_medium} WHERE pgdesc IN {video_game_pgdesc}")
        sql_large=connection.raw_sql(f"SELECT * FROM {bvd_large} WHERE pgdesc IN {video_game_pgdesc}")
        whole_df=pd.concat([sql_small,sql_medium,sql_large])
    except Exception as error:
        print(f"amadeus: {error}")
        whole_df=pd.DataFrame()
    return whole_df


amadeus_publishers=publisher_amadeus_request(connection)
amadeus_publishers.to_csv("publishers_amadeus.csv")