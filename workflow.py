from objects_and_builders.control_df import control_df
import pandas as pd
from objects_and_builders.id_dict import id_dict
from imputation.miss_forest_imputation_wrapper import miss_forest_imputation_wrapper
from merge_financial_data import financial_table_builder
import os
from objects_and_builders.wrds_database import full_workflow
from bmwi_request import clean_bmwi_request,add_id_to_bmwi_data
from datahandling.change_directory import chdir_data
from objects_and_builders.treatment import treatment_group_treatment_workflow,treatment_data_control_group
#complete workflow general
#complete workflow id
#financials mergen



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
        treatment_id_dict=id_dict(treatment_base_ama).append_ids(treatment_base_ob)
        treatment_ids=treatment_id_dict.get_ids()
        full_workflow("id",path=r"C:\Users\lukas\Desktop\bachelor\data\treatment",ids=treatment_ids)
        treatment_id_dict.to_csv("treatment_ids.csv")
    if merge_financials:
        os.chdir(r"C:\Users\lukas\Desktop\bachelor\data\treatment")
        amadeus_financials=pd.read_csv("financialsbvd_ama.csv")
        orbis_financials=pd.read_csv("ob_ind_g_fins_eurbvd_orbis.csv")
        table=financial_table_builder().build_financial_table(amadeus_financials,orbis_financials)
        os.chdir(r"C:\Users\lukas\Desktop\bachelor\data\treatment")
        table._df.to_excel("financials_merge.xlsx")
        data=table._df
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
        control_id_dict=id_dict(control_base_ama).append_ids(control_base_ob)
        control_ids=control_id_dict.get_ids()
        control.id_request(control_ids)
        control_id_dict.to_csv("control_ids.csv")

    if merge_financials:
        os.chdir(r"C:\Users\lukas\Desktop\bachelor\data\control")
        amadeus_financials=pd.read_csv("financialsbvd_ama.csv")
        orbis_financials=pd.read_csv("ob_ind_g_fins_eurbvd_orbis.csv")
        table=financial_table_builder().build_financial_table(amadeus_financials,orbis_financials)
        os.chdir(r"C:\Users\lukas\Desktop\bachelor\data\control")
        table._df.to_excel("financials_merge.xlsx")
        data=table._df
    if treatment:
        if not merge_financials:
            os.chdir(r"C:\Users\lukas\Desktop\bachelor\data\control")
            data=pd.read_excel("financials_merge.xlsx")
        data=treatment_data_control_group(data).add_treatment_cols()
        data.to_excel("financials_with_treatment.xlsx")
    return data


def complete_workflow(treatment=True,control=True,imputation=True,clean=True):
    if treatment:
        financials_merge_treatment=treatment_workflow(bmwi_request=False,base_request=False,id_request=False,merge_financials=False,treatment=True)
    elif not treatment:
        financials_merge_treatment=pd.read_excel(r"C:\Users\lukas\Desktop\bachelor\data\treatment\financials_with_treatment.xlsx")
    if control:
        financials_merge_control=control_workflow(base_request=False,id_request=False,merge_financials=False,treatment=True)
    elif not control:
        financials_merge_control=pd.read_excel(r"C:\Users\lukas\Desktop\bachelor\data\control\financials_with_treatment.xlsx")
    if imputation:
        merged=pd.concat([financials_merge_control,financials_merge_treatment])
        merged.to_excel(r"C:\Users\lukas\Desktop\bachelor\data\financials_merge_treatment_and_control.xlsx",index=False)
        merged=miss_forest_imputation_wrapper(merged,"data","treatment_and_control_merged_imputed.xlsx")
    if clean==True:
        merged.drop(columns=vars_ignored,inplace=True)

vars_ignored=("country","consolidation code","country iso code","accounting_practice","source (for publicly quoted companies)","estimated operating revenue","estimated employees","employees original range value","closdate")

complete_workflow(treatment=False,control=False,imputation=True,clean=False)
