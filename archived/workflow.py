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
from bachelor.clean_merged import pre_financial_merge_workflow
#complete workflow general
#complete workflow id
#financials mergen



def add_my_id_to_id(df_with_my_id,id_df):
    id_df=id_df.merge(df_with_my_id[["bvdid","my_id"]],on="bvdid",how="left")
    return id_df

#######treatment
def treatment_workflow(bmwi_request=True,base_request=True,id_request=True,merge_financials=True,treatment=True):
    control=control_df()
    if bmwi_request:
        clean_bmwi_request()
        add_id_to_bmwi_data("treatment_ids.csv")
    if base_request:
        chdir_data()
        names=pd.read_csv("bmwi_request.csv")["Zuwendungsempfänger"].to_list()
        full_workflow("general",path=r"C:\Users\lukas\Desktop\bachelor\data\treatment",names=names)
    if id_request:
        treatment_base_ama=pd.read_csv(r"C:\Users\lukas\Desktop\bachelor\data\treatment\companybvd_ama.csv")
        treatment_base_ob=pd.read_csv(r"C:\Users\lukas\Desktop\bachelor\data\treatment\ob_contact_infobvd_orbis.csv")
        treatment_ids_object=ids([treatment_base_ama,treatment_base_ob])
        treatment_ids=treatment_ids_object.get_ids()
        full_workflow("id",path=r"C:\Users\lukas\Desktop\bachelor\data\treatment",ids=treatment_ids)
        pd.Series(treatment_ids).to_csv("treatment_ids.csv")
    if merge_financials:
        os.chdir(r"C:\Users\lukas\Desktop\bachelor\data\treatment")
        amadeus_financials=pd.read_csv("financialsbvd_ama.csv")
        amadeus_financials=pre_financial_merge_workflow(amadeus_financials)
        orbis_financials=pd.read_csv("ob_ind_g_fins_eurbvd_orbis.csv")
        orbis_financials=pre_financial_merge_workflow(orbis_financials)
        table=financial_table_builder().build_financial_table(amadeus_financials,orbis_financials)
        os.chdir(r"C:\Users\lukas\Desktop\bachelor\data\treatment")
        table._df.to_excel("financials_merge.xlsx")
        data=table._df
        treatment_ids=pd.read_csv(r"C:\Users\lukas\Desktop\bachelor\data\id\treatment_ids.csv")
        treatment_ids=add_my_id_to_id(data,treatment_ids)
        treatment_ids.to_csv(r"C:\Users\lukas\Desktop\bachelor\data\id\treatment_ids.csv")
    
        
    if treatment:
        data=treatment_group_treatment_workflow()
    return data

##############control
def control_workflow(base_request=True,id_request=True,merge_financials=True,treatment=True):
    control=control_df()

    if base_request:
        control.manual_del().check_not_treated().general_request()
    if id_request:
        control_base_ama=pd.read_csv(r"C:\Users\lukas\Desktop\bachelor\data\control\companybvd_ama.csv")
        control_base_ob=pd.read_csv(r"C:\Users\lukas\Desktop\bachelor\data\control\ob_contact_infobvd_orbis.csv")
        control_ids_object=ids([control_base_ama,control_base_ob])
        control_ids=control_ids_object.get_ids()
        control.id_request(control_ids)
        control_ids.to_csv("control_ids.csv")
    
    
    if merge_financials:
        os.chdir(r"C:\Users\lukas\Desktop\bachelor\data\control")
        amadeus_financials=pd.read_csv("financialsbvd_ama.csv")
        amadeus_financials=pre_financial_merge_workflow(amadeus_financials)
        orbis_financials=pd.read_csv("ob_ind_g_fins_eurbvd_orbis.csv")
        orbis_financials=pre_financial_merge_workflow(orbis_financials)
        table=financial_table_builder().build_financial_table(amadeus_financials,orbis_financials)
        os.chdir(r"C:\Users\lukas\Desktop\bachelor\data\control")
        table._df.to_excel("financials_merge.xlsx")
        data=table._df
        control_ids=pd.read_csv(r"C:\Users\lukas\Desktop\bachelor\data\id\control_ids.csv")
        control_ids=add_my_id_to_id(data,control_ids)
        control_ids.to_csv(r"C:\Users\lukas\Desktop\bachelor\data\id\control_ids.csv")
    


    if treatment:
        if not merge_financials:
            os.chdir(r"C:\Users\lukas\Desktop\bachelor\data\control")
            data=pd.read_excel("financials_merge.xlsx")
        data=treatment_data_control_group(data).add_treatment_cols()
        data.to_excel("financials_with_treatment.xlsx")
        #control.filter_control()
    return data

def complete_workflow(treatment=True,control=True,categorials=True,imputation=True,combine_ids=True,clean=True,matching=True):
    if treatment:
        financials_merge_treatment=treatment_workflow(bmwi_request=False,base_request=False,id_request=True,merge_financials=True,treatment=True)
    elif not treatment:
        financials_merge_treatment=pd.read_excel(r"C:\Users\lukas\Desktop\bachelor\data\treatment\financials_with_treatment.xlsx")


    if control:
        financials_merge_control=control_workflow(base_request=False,id_request=True,merge_financials=True,rechtsform=True,treatment=True)
    elif not control:
        financials_merge_control=pd.read_excel(r"C:\Users\lukas\Desktop\bachelor\data\control\financials_with_treatment.xlsx")

    data=pd.concat([financials_merge_control,financials_merge_treatment])
    #hier droppen
    data.to_excel(r"C:\Users\lukas\Desktop\bachelor\data\financials_merge_treatment_and_control.xlsx",index=False)
    if categorials:
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
        data.to_excel(r"C:\Users\lukas\Desktop\bachelor\data\financials_merge_treatment_and_control.xlsx",index=False)
    if imputation:
        
        data=miss_forest_imputation_wrapper(data,"data","treatment_and_control_merged_imputed.xlsx")
    
    if combine_ids:
        chdir_root_search("id")
        treatment_ids=pd.read_csv("treatment_ids.csv")
        control_ids=pd.read_csv("control_ids.csv")

        combined=ids([treatment_ids,control_ids])
        combined.to_csv("treatment_and_control_ids.csv")
        
    
    
    if clean==True:
        if not imputation:
            chdir_data()
            data=pd.read_excel("treatment_and_control_merged_imputed.xlsx",index_col=False)
        data=drop_unnamed_columns(data)
        data=drop_nan_columns(data,0)
        data=format_df(data)
        try:
            data.drop(columns=vars_ignored,inplace=True)
        except KeyError:
            None
        def nmse_threshold(treshhold):
            chdir_data()
            errors=pd.read_excel("miss_forest_errors.xlsx",index_col=False)
            index_map=errors.isna().sum(axis=1)<5
            errors=errors[index_map]
            var_to_drop=errors["variable"][(errors["iteration"]==max(errors["iteration"])) & (errors["NMSE"]>=treshhold)]
            return var_to_drop
        cols_to_drop=nmse_threshold(0.6).to_list()
        exceptions=["bvdid","closdate_year","compcat","annual_subsidy"]
        cols_to_drop=[col for col in cols_to_drop if col not in exceptions]
        data.drop(columns=cols_to_drop,inplace=True)
        
        data.to_excel("treatment_and_control_merged_imputed_dropped.xlsx",index=False)
    if matching:
        matching_wrapper()


vars_ignored=("country","consolidation code","country iso code","accounting_practice","source (for publicly quoted companies)","estimated operating revenue","estimated employees","employees original range value","closdate")

complete_workflow(treatment=True,control=True,categorials=True,imputation=True,combine_ids=True,clean=True,matching=True)

