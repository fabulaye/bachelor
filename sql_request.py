import wrds

import pandas as pd
import os


#libraries=test.list_libraries()
#amadeus_tables=test.list_tables("bvd_ama_small")
#print(amadeus_tables)

#print(variablen)

#values=test.get_table("bvd_ama_small","amadeus_s",obs=100)
#print(values)

#help(test.get_table)

os.chdir("C:/Users/Lukas/Desktop/bachelor/data")
#games_förderung_df=pd.read_excel("Games_Förderung_df.xlsx")
#gaming_company_names=tuple(games_förderung_df["name"]+games_förderung_df["rechtsform"])

gaming_company_names=['Conquista GamUG (haftungsbeschränkt)', 'Real Human Games GmbH', 'Pangolin Park GmbH', 'Hekate GmbH', 'Moi Rai Games GmbH', 'Airborn Studios GmbH', 'Aerosoft GmbH Luftfahrt-DatentechnikGmbH', 'simulogics GmbH', 'Totally Not AliUG (haftungsbeschränkt)', 'Ascendancy GamUG (haftungsbeschränkt)', 'Angry Dynomites LUG (haftungsbeschränkt)', 'gameXcite  GmbH', 'Dexai Arts UG', 'Kaleidoscube GmbH', 'Kaleidoscube GmbH', 'Z-Software GmbH', 'Studio MUG (haftungsbeschränkt)', 'Sky-E Red GmbH', 'Lootzifr GmbH', 'Alchemical WoUG (haftungsbeschränkt)', 'Binary Impact GmbH', 'ByteRockers’ GamesGmbH & Co. KG', 'Wyrmgold GmbH', 'LAB132 GmbH', 'winterworks GmbH', 'KonspiracyUG (haftungsbeschränkt)', 'Tiny RoUG (haftungsbeschränkt)', 'ByteRockers`GamesGmbH & Co. KG', 'Aesir Interactive GmbH', 'Ergofox GmbH']

def start():
    connection=wrds.Connection(wrds_username="lukasmeyer")
    return connection


connection=wrds.Connection(wrds_username="lukasmeyer")
connection.create_pgpass_file()

#connection=start()
variablen=connection.describe_table(library="bvd_ama_small",table="amadeus_s")

def bvd_request():
    gaming_company_names_tuple=tuple(map(lambda x: x.upper(),gaming_company_names))
    sql=connection.raw_sql(f"SELECT * FROM bvd_ama_small.amadeus_s WHERE cntrycde='DE' AND name IN {gaming_company_names_tuple}")
    sql.to_excel("sql_request.xlsx")
    return sql

sql=bvd_request()


def find_missing():
    missing_list=[]
    for name in gaming_company_names:
        if name not in sql["name_nat"]:
            missing_list.append(name)
    return missing_list

missing_entries=find_missing()
print(missing_entries)



connection.close()

#bvd switchen
#namen liste verbessern --> 


