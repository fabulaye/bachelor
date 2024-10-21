from objects_and_builders.control_df import control_df
import pandas as pd
from objects_and_builders.ids import ids
from imputation.miss_forest_imputation_wrapper import miss_forest_imputation_wrapper
from merge_financial_data import financial_table_builder
import os
from objects_and_builders.wrds_database import full_workflow
from bmwi_request import clean_bmwi_request,add_id_to_bmwi_data
from datahandling.change_directory import chdir_data,chdir_root_search
from objects_and_builders.treatment import treatment_group_treatment_workflow,treatment_data_control_group
from processing.format_string import format_df
from processing.my_df import drop_unnamed_columns
from processing.rechtsform import return_rechtsform
from objects_and_builders.data_selector import data_selector
from matching_wrapper import matching_wrapper
from processing.my_df import drop_nan_columns
from clean_merged import clean_workflow
from objects_and_builders.balance_sheet import balance_sheet
from sklearn.preprocessing import StandardScaler
from processing.format_string import format_df


class workflow():
    def __init__(self) -> None:
        self._df=None
    def bmwi_request() :
        clean_bmwi_request()
        add_id_to_bmwi_data("treatment_ids.csv")
    def treatment_control_workflow(self,treatment_or_control="treatment",base_request=False,id_request=False,merge_financials=False,treatment=False):
        if treatment_or_control=="control":
            control=control_df()
            
        if base_request:
            chdir_data()
            if treatment_or_control=="treatment":
                names=pd.read_csv("bmwi_request.csv")["Zuwendungsempfänger"].to_list()
            elif treatment_or_control=="control":
                control.manual_del().check_not_treated().general_request()
            full_workflow("general",path=rf"C:\Users\lukas\Desktop\bachelor\data\{treatment_or_control}",names=names)
        if id_request:
            base_ama=pd.read_csv(fr"C:\Users\lukas\Desktop\bachelor\data\{treatment_or_control}\companybvd_ama.csv")
            base_ob=pd.read_csv(fr"C:\Users\lukas\Desktop\bachelor\data\{treatment_or_control}\ob_contact_infobvd_orbis.csv")
            ids_object=ids([base_ama,base_ob])
            ids_list=ids_object.get_ids()
            #kann ich hier full workflow benutzen?
            full_workflow("id",path=rf"C:\Users\lukas\Desktop\bachelor\data\{treatment_or_control}",ids=ids_list)
            pd.Series(ids_list).to_csv(f"{treatment_or_control}_ids.csv")
        if merge_financials:
            os.chdir(rf"C:\Users\lukas\Desktop\bachelor\data\{treatment_or_control}")
            amadeus_financials=pd.read_csv("financialsbvd_ama.csv")
            orbis_financials=pd.read_csv("ob_ind_g_fins_eurbvd_orbis.csv")
            table=financial_table_builder().build_financial_table(amadeus_financials,orbis_financials)
            os.chdir(fr"C:\Users\lukas\Desktop\bachelor\data\{treatment_or_control}")
            table._df.to_excel("financials_merge.xlsx")
            ######## brauchen wir das??
            #ids=pd.read_csv(fr"C:\Users\lukas\Desktop\bachelor\data\id\{treatment_or_control}_ids.csv")
            #ids=add_my_id_to_id(data,treatment_ids)
            #ids.to_csv(fr"C:\Users\lukas\Desktop\bachelor\data\id\{treatment_or_control}_ids.csv")
        if treatment:
            
            #ich könnte einfach immer readen 
            #self.last_stage oder sowas
            if treatment_or_control=="treatment":
                data=treatment_group_treatment_workflow()
                #müssen wir hier directory changen?
                data.to_excel("financials_with_treatment.xlsx")
            elif treatment_or_control=="control":
                chdir_root_search(treatment_or_control)
                data=pd.read_excel("financials_merge.xlsx")
                data=treatment_data_control_group(data).add_treatment_cols()
                data.to_excel("financials_with_treatment.xlsx")
        return self
    def merge_and_concat(self,run=True):
        if run:
            financials_merge_control=pd.read_excel(r"C:\Users\lukas\Desktop\bachelor\data\control\financials_with_treatment.xlsx")
            financials_merge_control=drop_unnamed_columns(financials_merge_control)
            financials_merge_treatment=pd.read_excel(r"C:\Users\lukas\Desktop\bachelor\data\treatment\financials_with_treatment.xlsx")
            financials_merge_treatment=drop_unnamed_columns(financials_merge_treatment)
            data=pd.concat([financials_merge_control,financials_merge_treatment])
            #hier droppen
            data.to_excel(r"C:\Users\lukas\Desktop\bachelor\data\financials_merge_treatment_and_control.xlsx",index=False)
        return self
    def categorials(self,run=True):
        if run:
            data=pd.read_excel(r"C:\Users\lukas\Desktop\bachelor\data\financials_merge_treatment_and_control.xlsx")
            def add_rechtsform(data):
                chdir_root_search("id")
                #read all ids 
                #add new column
                id_df=pd.read_csv("treatment_and_control_ids.csv")
                id_df["rechtsform"]=id_df["name"].apply(lambda x: return_rechtsform(x))
                rechtsform_and_id=id_df[["rechtsform","bvdid","name"]].replace("GESELLSCHAFT_MIT_BESCHRÄNKTER_HAFTUNG","GMBH")
                data=format_df(data)
                #game_ev_members=game_ev_members.apply(lambda x: list(map(bachelor_format,x)))
                return id_df[["bvdid","rechtsform"]].replace()
            rechtsform_df=add_rechtsform(data)
            data=data.merge(rechtsform_df,on="bvdid",how="left")
            def add_startup():
                chdir_root_search("id")
                combined_ids=pd.read_csv("treatment_and_control_ids.csv")
                chdir_root_search("treatment")
                company_bvdama_treatment=pd.read_csv("companybvd_ama.csv")
                ob_contact_infobvd_orbis_treatment=pd.read_csv("ob_legal_infobvd_orbis.csv")
                chdir_root_search("control")
                company_bvdama_control=pd.read_csv("companybvd_ama.csv")
                ob_contact_infobvd_orbis_control=pd.read_csv("ob_legal_infobvd_orbis.csv")
                selector=data_selector([combined_ids]).add_data([company_bvdama_treatment,company_bvdama_control,ob_contact_infobvd_orbis_treatment,ob_contact_infobvd_orbis_control],["dateinc_year"])
                date_inc_column=selector._df[["dateinc_year"]]
                selector._df["startup"]=date_inc_column>=2017
                selector._df["startup"]=selector._df["startup"].apply(lambda x: int(x))
                selector._df["age"]=selector._df["dateinc_year"].apply(lambda x: 2024-x)
                return selector._df[["bvdid","startup","age"]]
            startup_df=add_startup()
            data=data.merge(startup_df,on="bvdid",how="left")
            
            def add_state_inc():
                chdir_root_search("id")
                combined_ids=pd.read_csv("treatment_and_control_ids.csv")
                chdir_root_search("treatment")
                #company_bvdama_treatment=pd.read_csv("companybvd_ama.csv")
                ob_contact_infobvd_orbis_treatment=pd.read_csv("ob_legal_infobvd_orbis.csv")
                chdir_root_search("control")
                #company_bvdama_control=pd.read_csv("companybvd_ama.csv")
                ob_contact_infobvd_orbis_control=pd.read_csv("ob_legal_infobvd_orbis.csv")
                selector=data_selector([combined_ids]).add_data([ob_contact_infobvd_orbis_treatment,ob_contact_infobvd_orbis_control],["historic_status_str","historic_statusdate"])
                states=selector._df["historic_status_str"].to_list()
                selector._df["STATUS"]=[1 if state=="ACTIVE" else 0 for state in states]
                return selector._df[["STATUS","bvdid","historic_statusdate"]]
            state_df=add_state_inc()
            data=data.merge(state_df,on="bvdid",how="left")
            def add_published(data):
                chdir_data()
                ids=pd.read_csv(r"id\treatment_and_control_ids.csv")
                ids.rename(columns={"name":"name_underscore"},inplace=True)
                data=data.merge(ids,on="bvdid")
                published_data=pd.read_csv("published_dummy.csv")
                published_data=format_df(published_data)
                published_data.rename(columns={"name":"name_underscore"},inplace=True)
                new_data=pd.merge(data,published_data[["name_underscore","last_release"]],on="name_underscore",how="left")
                new_data["last_release"]=new_data["last_release"].replace("na",0)
                new_data["last_release"]=new_data["last_release"].replace("NA",0)
                new_data["last_release"]=new_data["last_release"].fillna(0)
                new_data["last_release"]=new_data["last_release"].apply(lambda x: int(x))
                #new_data["end_year"]=new_data["end_year"].apply(lambda x: int(x))
                published=[]
                for name,group in new_data.groupby("bvdid"):
                    #try:
                    if max(group["last_release"])>min(group["end_year"]):
                        ones=[1]*len(group)
                        published.extend(ones)
                    else:
                        zeros=[0]*len(group)
                        published.extend(zeros)
                    #except TypeError:
                            #zeros=[0]*len(group)
                            #published.extend(zeros)
                new_data["published"]=published
                return new_data
            data=add_published(data)
            data.to_excel(r"C:\Users\lukas\Desktop\bachelor\data\financials_merge_treatment_and_control_categorials.xlsx",index=False)
        return self
    

    def balance_sheet_vars():
        None
        #compare the theorical values after imputation with their actual
    def clean(self,run=True):
        if run:
            data=pd.read_excel(r"C:\Users\lukas\Desktop\bachelor\data\financials_merge_treatment_and_control_categorials.xlsx")
            self._df=clean_workflow(data)
            self._df.to_excel(r"C:\Users\lukas\Desktop\bachelor\data\financials_merge_treatment_and_control_categorials_cleaned.xlsx")
        return self
    def drop_imputed_cols(self,run=True):
        if run:
            data=pd.read_excel(r"C:\Users\lukas\Desktop\bachelor\data\financials_merge_treatment_and_control_categorials_cleaned_imputed_ratios.xlsx")
            def nmse_threshold(treshhold):
                chdir_data()
                errors=pd.read_excel("miss_forest_errors.xlsx",index_col=False)
                index_map=errors.isna().sum(axis=1)<5
                errors=errors[index_map]
                var_to_drop=errors["variable"][(errors["iteration"]==max(errors["iteration"])) & (errors["NMSE"]>=treshhold)]
                return var_to_drop
            cols_to_drop=nmse_threshold(0.6).to_list()
            exceptions=["bvdid","closdate_year","compcat","annual_subsidy","treatment","subsidy","total_subsidy","total_annual_subsidy","integrated_dummy","published","STATUS","rechtsform","one_year_lag_total_annual_subsidy"]
            cols_to_drop=[col for col in cols_to_drop if col not in exceptions]
            data.drop(columns=cols_to_drop,inplace=True)
            data.to_excel(r"C:\Users\lukas\Desktop\bachelor\data\financials_merge_treatment_and_control_categorials_cleaned_imputed_dropped.xlsx")
        return self
    def impute(self,run=True):
        if run:
            data=pd.read_excel(r"C:\Users\lukas\Desktop\bachelor\data\financials_merge_treatment_and_control_categorials_cleaned.xlsx")
            data=miss_forest_imputation_wrapper(data,"data","financials_merge_treatment_and_control_categorials_cleaned_imputed.xlsx")
        return self
    def treatment_ratios(self,run=True):
        if run:
            data=pd.read_excel(r"C:\Users\lukas\Desktop\bachelor\data\financials_merge_treatment_and_control_categorials_cleaned_imputed.xlsx")
            data_grouped=data.groupby("bvdid")
            new_df=[]
            for name,group in data_grouped:
                if all(group["treatment"]==0):
                    group["cum_treatment_toas_ratio"]=0
                    group["total_annual_subsidy_toas_ratio"]=0
                    group["subsidy_expectation_sum_toas_ratio"]=0
                    new_df.append(group)
                else:
                    if len(group)>1:
                        indexes=group["conc_treatment"]==1
                        divisor=group.loc[indexes,:]["toas"]
                        divisor=divisor.iloc[0]
                    elif len(group)==1:
                        divisor=group["toas"]
                    group["cum_treatment_toas_ratio"]=group["cum_treatment"]/divisor
                    group["total_annual_subsidy_toas_ratio"]=group["total_annual_subsidy"]/divisor
                    group["subsidy_expectation_sum_toas_ratio"]=group["subsidy_expectation_sum"]/divisor
                    new_df.append(group)
            new_df=pd.concat(new_df)
            new_df.to_excel(r"C:\Users\lukas\Desktop\bachelor\data\financials_merge_treatment_and_control_categorials_cleaned_imputed_ratios.xlsx")
        return self
    def shfd_rescale(self,run=True):
        if run:
            data=pd.read_excel(r"C:\Users\lukas\Desktop\bachelor\data\financials_merge_treatment_and_control_categorials_cleaned_imputed_ratios.xlsx")
            data_grouped=data.groupby("bvdid")
            new_col=[]
            scaler=StandardScaler()
            for name,group in data_grouped:
                values=group["shfd"]
                values=values.to_numpy().reshape(-1,1)
                #rescaled_values=values.div(values.iloc[0])
                rescaled_values=scaler.fit_transform(values)
                rescaled_values = rescaled_values.flatten()
                new_col.extend(rescaled_values)
            data["shfd_rescaled"]=new_col
            data.to_excel(r"C:\Users\lukas\Desktop\bachelor\data\financials_merge_treatment_and_control_categorials_cleaned_imputed_ratios.xlsx")
        return self
    def balance_sheet_items(self):
        data=None
        for index,observation in data.iterrows():
            balance_sheet_object=balance_sheet(observation)
            equity=balance_sheet_object.theoreticals.equity


    def match(self,run=True):
        if run:
            matching_wrapper(r"C:\Users\lukas\Desktop\bachelor\data\financials_merge_treatment_and_control_categorials_cleaned_imputed_dropped.xlsx")
    def read_csv(self,path):
        data=pd.read_csv(path)
        data=drop_unnamed_columns(data)
        return data


bachelor_workflow=workflow()
bachelor_workflow.treatment_control_workflow("treatment",id_request=False,merge_financials=False,treatment=False).treatment_control_workflow("control",id_request=False,merge_financials=False,treatment=False).merge_and_concat(False).categorials(False).clean(False).impute(False).treatment_ratios(False).shfd_rescale(False).drop_imputed_cols(True).match(True) 

