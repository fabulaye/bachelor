import pandas as pd
from datahandling.change_directory import chdir_data
from processing.my_list import unique_list
import regex as re
import numpy as np
from processing.format_string import format_df

chdir_data()

financial_tables=["ob_cflow_non_us_ind_eur_intbvd_orbis","ob_cflow_non_us_ind_eurbvd_orbis","ob_cflow_us_ind_eurbvd_orbis","ob_detailed_fmt_ind_eurbvd_orbis","ob_detailed_fmt_ind_eur_intbvd_orbis","ob_ind_g_fins_eur_intbvd_orbis","ob_ind_g_fins_eurbvd_orbis","ob_key_financials_eurbvd_orbis","financialsbvd_ama","ish_duo_guobvd_ama"]

cols_to_drop=["exchrate","currency","closdate_char","exchrate2","account_unit","filing_type","audit_status","orig_currency","orig_units","accounting_practice","number of months","subsidy_duration_days","rechtsform"]

class financial_table():
    def __init__(self) -> None:
        self._df=None
        self.duplicate_cols=None
        self.unique_cols=None  
        chdir_data()
        wrds_map=pd.read_csv("map.csv")
        self.wrds_map=dict(zip(wrds_map["old_name"],wrds_map["new_name"]))
    
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
        duplicate_regex=re.compile(r"(.+?)(?=_ama|_orb)")
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
    def resolve_double_ids(self):
        #selector._df=pd.merge(selector._df,all_ids[["bvdid","name"]],how="left",on="bvdid")
        all_ids=pd.read_csv(r"C:\Users\lukas\Desktop\bachelor\data\id\treatment_and_control_ids.csv")
        self._df=self._df.merge(all_ids[["bvdid","name"]],on="bvdid",how="left")
        bvdid_count=self._df.groupby("name")["bvdid"].unique()
        indices=[True if len(val)>1 else False for val in bvdid_count]
        double_names=bvdid_count.index[indices]
        
        doubles=self._df[self._df["name"].isin(double_names)]
        not_double=self._df[~self._df["name"].isin(double_names)]
        doubles_grouped=doubles.groupby("name")
        new_df=[]
        for name,group in doubles_grouped:
            id_groups=group.groupby("bvdid")
            max_not_na=0
            selected_id=""
            for name,group in id_groups:
                eligable_values=group[group["closdate_year"]>=2020]
                if eligable_values.notna().sum().sum()>max_not_na:
                    selected_id=name
                    max_not_na=eligable_values.notna().sum().sum()
            new_df.append(id_groups.get_group(selected_id))
            
            
        new_df=pd.concat(new_df)
        new_df=pd.concat([new_df,not_double])
        
        self._df=new_df


    def resolve_conflicts(self):
        self.find_duplicate_columns()
        name_list=[]
        for tuple in self.duplicate_cols_complete:
            name_list.extend([tuple[0],tuple[1]])
        try:
            self.duplicate_cols_partial.remove('exchange rate from local currency to usd')
        except ValueError:
            None
        unique_columns_values=[]
        cols_to_drop=[]
        for column_name in self.duplicate_cols_partial:
            values=self._df[[column_name+"_ama",column_name+"_orb",]]
            values=values.bfill(axis=1).ffill(axis=1).fillna("nan_placeholder")
            values=pd.concat([values,self._df[["bvdid","closdate_year"]]],axis=1)
            if values.iloc[:,0].equals(values.iloc[:,1]):
                value=values.iloc[:,0].rename(column_name)
                #value_series=pd.Series(value,name=column)
                unique_columns_values.append(value)
                cols_to_drop.extend([column_name+"_ama",column_name+"_orb"])
            else: 
                #vergleich welche mehr values hat und die nehmen? 
                comparison = values.iloc[:,0] != values.iloc[:,1]
                rows_with_diff = values[comparison]  
                number_diff=comparison.sum()
                value=values.iloc[:,0].rename(column_name)
                unique_columns_values.append(value)
                cols_to_drop.extend([column_name+"_ama",column_name+"_orb"])

        #conflict_indices=unique_list(conflict_indices) #indizes fürs Problem df
        resolved_conflict_df=pd.concat(unique_columns_values,axis=1)
        self._df.drop(columns=cols_to_drop,inplace=True)
        self._df=pd.concat([self._df,resolved_conflict_df],axis=1)
        self._df.replace("nan_placeholder",None,inplace=True)

    def delete_double_rows(self):
        #das hier ist nach dem merge von amadeus und orbis --> die Idee ist Informationen aus beiden Sets zu verknüpfen
        rows=[]
        for index,group in self._df.groupby(["bvdid","closdate_year"]): #nach my_id groupen vorher bvdid
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
                unconsolidated_codes=["U1","U2","nan_placeholder","UNCONSOLIDATED_DATA"]
                data=group[(group["conscode_ama"].isin(unconsolidated_codes))|(group["conscode_orb"].isin(unconsolidated_codes))]
                if len(data)==0:
                    data=group[~group["conscode"].isin(unconsolidated_codes)]
                data.replace("nan_placeholder",None)
                data.ffill(axis=0,limit=1,inplace=True)
                data.bfill(axis=0,limit=1,inplace=True)
                rows.append(data.iloc[0,:])
        rows_df=pd.concat(rows,axis=1)
        self._df=rows_df.T
        self._df.replace("nan_placeholder",None,inplace=True)
        return self
    def filter_12_months(self):
        self._df=filter_12_months(self._df)
        return self

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


def filter_12_months(df):
    twelve_months_df=df[df["months_ama"]==12]
    six_months_df=df[df["months_ama"]==6]
    return twelve_months_df

class financial_table_builder():
    def __init__(self) -> None:
        self.financial_table=financial_table()
    def build_financial_table(self,amadeus,orbis):
        #rename und replace davor?
        amadeus.rename(columns=self.financial_table.wrds_map,inplace=True)
        orbis.rename(columns=self.financial_table.wrds_map,inplace=True)
        amadeus.drop(columns=cols_to_drop,inplace=True,errors="ignore")
        orbis.drop(columns=cols_to_drop,inplace=True,errors="ignore")
        financials_merged=pd.merge(amadeus,orbis,on=["bvdid","closdate_year"],suffixes=["_ama","_orb"],how="outer") 
        financials_merged=format_df(financials_merged)
        self.financial_table._df=financials_merged
        
        self.financial_table.replace_wrds_data()
        self.financial_table.filter_12_months()
        self.financial_table.delete_double_rows()#war vorher letzte geht das?
        self.financial_table.resolve_double_ids()
        self.financial_table.find_duplicate_columns()
        self.financial_table.resolve_conflicts()
        self.financial_table._df.astype("float",errors="ignore")
        #ich habe bei den ids auch schon eine function
        return self.financial_table







