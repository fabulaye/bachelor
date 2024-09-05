import sqlite3
import pandas as pd
from datahandling.change_directory import chdir_data,chdir_sql_requests
from sql_table import sql_table,sql_table_builder
import os


class sql_db_error(Exception):
    pass


class sql_db():
    def __init__(self,name) -> None:
        pass
        self.name=name
        self.connection=None
        self.cursor=None
    def connect(self):
        self.connection=sqlite3.connect(self.name)
        self.cursor=self.connection.cursor()
    def execute(self,statement):
        query=self.cursor.execute(statement)
        return query
    def get_table_names(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables=self.cursor.fetchall()
        table_names = [table[0] for table in tables]
        return table_names
    def create_table(self,sql_table:sql_table):
        if sql_table.table_name in self.get_table_names():
            raise sql_db_error(f"{sql_table.table_name} already exists")
        column_definitions=sql_table.build_column_definitions()
        table_name=sql_table.table_name
        request_string=f'''CREATE TABLE IF NOT EXISTS {sql_table.table_name} ({column_definitions});''' 
        self.execute(request_string) #fördersumme in euro streichen
        self.commit()
        return self
    def commit(self):
        self.connection.commit()
    def insert_data(self,sql_table:sql_table):
        if sql_table.table_name not in self.get_table_names():
            raise sql_db_error(f"{sql_table.table_name} doesn't exist")
        sql = f'INSERT INTO {sql_table.table_name} {tuple(sql_table.columns)} VALUES ({sql_table.placeholders})'
        #sql_data=self.cursor.fetchall()
        for row in sql_table.data_matrix:
            try:
                self.cursor.execute(sql,row)
            except sqlite3.IntegrityError:
                print(f"already in table")
       # self.cursor.executemany(sql,sql_table.data_matrix)
        self.commit() 
        return self
    def del_table(self,table_name):
        sql_drop= f"DROP TABLE IF EXISTS {table_name}"
        self.cursor.execute(sql_drop)
        self.commit()
    def clear(self):
        table_list=self.get_table_names()
        for table in table_list:
            self.del_table(table)
    def vacuum(self):
        self.execute("VACUUM;")
    def rename_columns_from_table():
        None
    




















if __name__=="__main__":
    bachelor_db=sql_db("bachelor.db")
    bachelor_db.connect()
    #bachelor_db.clear()
    def create_table_for_all_files():
        #chdir_sql_requests()
        for file in os.listdir(r"C:\Users\lukas\Desktop\bachelor\data\sql_data"):
            chdir_sql_requests()
            table=sql_table_builder().build_table(file)
            bachelor_db.create_table(table) #funzt nicht
            table_names=bachelor_db.get_table_names()
            bachelor_db.insert_data(table) 
    chdir_data()
    bmwi_data=pd.read_csv("bmwi_request.csv")
    #create_table_for_all_files()


    #rename idnr with bvdid
    #join orbis with amadeus, join on bvdid and closdate
    ##create new table
    #joined=bachelor_db.cursor.execute(f"SELECT * FROM ob_ind_g_fins_eurbvd_orbis FULL OUTER JOIN financialsbvd_ama ON ob_ind_g_fins_eurbvd_orbis.bvdid = financialsbvd_ama.idnr AND ob_ind_g_fins_eurbvd_orbis.closdate_year=financialsbvd_ama.closdate_year")
    #columns=[description[0] for description in bachelor_db.cursor.description]
    #joined_data=joined.fetchall()
    #joined_data_df=pd.DataFrame(joined_data,columns=columns)
    #chdir_data()
    #joined_data_df.to_excel("joined_sql_test.xlsx")
    #print(joined_data_df)


#was mache ich mit joined?
#rename
#create new table in db
#sql_df functionality is better suited sql_db
#Will ich mir sql requests einfacher machen table creation etc.?