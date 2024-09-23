import pandas as pd
from datahandling.change_directory import chdir_data
from processing.my_list import unique_list
import regex as re
import numpy as np

chdir_data()

financial_tables=["ob_cflow_non_us_ind_eur_intbvd_orbis","ob_cflow_non_us_ind_eurbvd_orbis","ob_cflow_us_ind_eurbvd_orbis","ob_detailed_fmt_ind_eurbvd_orbis","ob_detailed_fmt_ind_eur_intbvd_orbis","ob_ind_g_fins_eur_intbvd_orbis","ob_ind_g_fins_eurbvd_orbis","ob_key_financials_eurbvd_orbis","financialsbvd_ama","ish_duo_guobvd_ama"]

cols_to_drop=["exchrate","currency","closdate_char","exchrate2","account_unit","filing_type","audit_status","orig_currency","orig_units","accounting_practice","number of months"]

class financial_table():
    def __init__(self) -> None:
        self._df=None
        self.duplicate_cols=None
        self.unique_cols=None  
        chdir_data()
        wrds_map=pd.read_csv("map.csv")
        self.wrds_map=dict(zip(wrds_map["name"],wrds_map["description"]))
    
    def to_csv(self,filename):
        self.merged.to_csv(filename)
    def replace_wrds_data(self):
        self._df.replace("Unconsolidated data","nan_placeholder",inplace=True)
        self._df.replace("No recent & Limited Fin.","nan_placeholder",inplace=True) #vorher mit u1 replaced
        self._df.replace("Limited Fin. Data","nan_placeholder",inplace=True)
        self._df.replace("SMALL COMPANY","SMALL",inplace=True)
        self._df.replace("MEDIUM SIZED COMPANY","MEDIUM",inplace=True)
        self._df.replace("MEDIUM SIZED","MEDIUM",inplace=True)
        self._df.replace("LARGE COMPANY","LARGE",inplace=True)
        self._df.replace("VERY LARGE COMPANY","VERY LARGE",inplace=True)
    def find_duplicate_columns(self):
        duplicate_regex=re.compile(r"^(.*?)(?=_\d)")
        #duplicate_regex=re.compile(r".*_\d{1}$")
        
        partial_name_matches_list=[]
        not_matched_list=[]
        for column in self._df.columns:
            matches=duplicate_regex.findall(column)
            if len(matches)>=1:
                if len(matches)==1:
                    partial_name_matches_list.extend(matches)
            else:
                not_matched_list.append(column)
        complete_name_match=[(name+"_1",name+"_2") for name in partial_name_matches_list]
        self.duplicate_cols_partial=unique_list(partial_name_matches_list)
        self.duplicate_cols_complete=complete_name_match
        self.unique_cols=not_matched_list
    def rename_cols(df:pd.DataFrame):
        df.rename(columns=self.wrds_map,inplace=True)
    
    def resolve_conflicts(self):
        self.find_duplicate_columns()
        name_list=[]
        for tuple in self.duplicate_cols_complete:
            name_list.extend([tuple[0],tuple[1]])

        test_df=self._df[name_list]
        test_df.to_excel("duplicate_cols_debug.xlsx")

        #warum hat unser df nur so wenige cols? Welche doubled fehlen?
        try:
            self.duplicate_cols_partial.remove('exchange rate from local currency to usd')
        except ValueError:
            None
        unique_columns_values=[]
        cols_to_drop=[]
        for column_name in self.duplicate_cols_partial:
            values=self._df[[column_name+"_1",column_name+"_2"]]
            values=values.bfill(axis=1).ffill(axis=1).fillna("nan_placeholder")
            if values.iloc[:,0].equals(values.iloc[:,1]):
                value=values.iloc[:,0].rename(column_name)
                #value_series=pd.Series(value,name=column)
                unique_columns_values.append(value)
                cols_to_drop.extend([column_name+"_1",column_name+"_2"])
            #else: 
            #    comparison = values.iloc[:,0] != values.iloc[:,1]
            #    rows_with_diff = values[comparison]  
            #    number_diff=comparison.sum()
#
            #    if number_diff>=20:
            #        print(column)
            #    conflict_indices.extend(list(rows_with_diff.index))
            #cols_to_drop.extend([column+"_1",column+"_2"])
            
        #conflict_indices=unique_list(conflict_indices) #indizes fürs Problem df
        resolved_conflict_df=pd.concat(unique_columns_values,axis=1)
        self._df.drop(columns=cols_to_drop,inplace=True)
        self._df=pd.concat([self._df,resolved_conflict_df],axis=1)
        self._df.replace("nan_placeholder",None,inplace=True)

    def delete_double_rows(self):
        rows=[]
        for index,group in self._df.groupby(["bvdid","closdate_year"]):
            if len(group)==1:
                rows.append(group.iloc[0,:])
            if len(group)==2: 
                group.ffill(axis=0,limit=1,inplace=True)
                group.bfill(axis=0,limit=1,inplace=True)
                group.fillna("nan_placeholder",inplace=True)
                #if len ==2 ?
                
                if group.iloc[0,:].equals(group.iloc[1,:]):
                    rows.append(pd.Series(group.iloc[0,:]))
                else: 
                    duplicates_index=duplicated_col(group)
                    diff_col_names=list(group.columns[~duplicates_index])
                    diff_df=group[diff_col_names]
                    diff_df.drop(columns=diff_col_names,inplace=True) #aktuell verdoppeln sich die cols aus irgendeinem grund
                    problems=group.loc[:,diff_col_names]
                    problems.replace(0,None,inplace=True)
                    problems.ffill(axis=0,limit=1,inplace=True)
                    problems.bfill(axis=0,limit=1,inplace=True)
                    if problems.iloc[0,:].equals(problems.iloc[1,:]):
                        group.loc[:,diff_col_names]=problems[diff_col_names]
                        rows.append(group.iloc[0,:])
                    else:
                        #muss noch fehler loggen, erstmal einfach row 0 appenden
                        #group[diff_col_names]=problems
                        continue
                        #rows.append(group.iloc[0,:])
            if len(group)>2:
                group.fillna("nan_placeholder",inplace=True)
                unconsolidated_codes=["U1","U2","nan_placeholder","C2"]
                unconsolidated=group[group["consolidation code"].isin(unconsolidated_codes)]
                unconsolidated.replace("nan_placeholder",None)
                unconsolidated.ffill(axis=0,limit=1,inplace=True)
                unconsolidated.bfill(axis=0,limit=1,inplace=True)
                rows.append(unconsolidated.iloc[0,:])
        rows_df=pd.concat(rows,axis=1)
        self._df=rows_df.T
        self._df.replace("nan_placeholder",None,inplace=True)


def duplicated_col(df):
    bool_index=[]
    for index,column_name in enumerate(df.columns):
        col_values=df[column_name]
        duplicate_bool=col_values.duplicated(keep=False)
        if all(duplicate_bool)==True:
            bool_index.append(True)
        else:
            bool_index.append(False)
    bool_index=np.array(bool_index)
    return bool_index


class financial_table_builder():
    def __init__(self) -> None:
        self.financial_table=financial_table()
    def build_financial_table(self,df_1,df_2):
        #rename und replace davor?
        df_1.rename(columns=self.financial_table.wrds_map,inplace=True)
        df_2.rename(columns=self.financial_table.wrds_map,inplace=True)
        df_1.drop(columns=cols_to_drop,inplace=True,errors="ignore")
        df_2.drop(columns=cols_to_drop,inplace=True,errors="ignore")
        financials_merged=pd.merge(df_1,df_2,on=["bvdid","closdate_year","consolidation code"],suffixes=["_1","_2"],how="outer")
        self.financial_table._df=financials_merged
        #self.financial_table._df.drop(columns=cols_to_drop,inplace=True)#geht nicht so einf
        #self.financial_table.rename_cols(self.financial_table._df) #brauchen wir das noch?
        self.financial_table.replace_wrds_data()
        self.financial_table.find_duplicate_columns()
        self.financial_table.resolve_conflicts()
        self.financial_table._df.astype("float",errors="ignore")
        self.financial_table.delete_double_rows()
        return self.financial_table



#Wie handle ich consolidation codes--> vielleicht die Partens einfach droppen
#duplicates für closdate_year,bvdid columns selecten. consolidation codes vergleichen 
#units:thousands millions etc.
#imputation mit groups







