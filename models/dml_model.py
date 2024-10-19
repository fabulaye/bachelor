from econml.dml import DML
from sklearn.linear_model import LassoCV, LogisticRegressionCV
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd
from processing.my_df import mydf
from joblib import dump,load
from datahandling.change_directory import chdir_data
from matplotlib import pyplot as plt
from econml.dml import CausalForestDML
from econml.cate_interpreter import SingleTreeCateInterpreter
from processing.my_df import drop_unnamed_columns
from matplotlib import pyplot as plt
import shap
from sklearn.preprocessing import StandardScaler
from econml.panel.dml import DynamicDML
import os
from sklearn.preprocessing import PolynomialFeatures






#matched_data=pd.read_excel(r"C:\Users\lukas\Desktop\bachelor\data\matched_data.xlsx")
#input_data=matched_data.drop(columns=excluded_vars)

#input_data=filter_input(input_data)

def scale_financial_variables(df,variables_to_scale):
    scaler=StandardScaler()
    input_scaled=scaler.fit_transform(df[variables_to_scale])
    input_scaled=pd.DataFrame(input_scaled,columns=variables_to_scale)
    return input_scaled

class bachelor_model():
    def __init__(self,model,name):
        self.name=name
        input_data=pd.read_excel(r"C:\Users\lukas\Desktop\bachelor\data\financials_merge_treatment_and_control_categorials_cleaned_imputed_dropped.xlsx")
        input_data=drop_unnamed_columns(input_data)
        input_data.drop(columns=["annual_subsidy","total_subsidy","country","ctryiso","filing type","audit status","original units","original currency","estimated operating revenue","estimated employees","accounting practice","closdate","conscode","subsidy_start","subsidy_end","project_ids","historic_statusdate","account.unit","exchange.rate.from.local.currency.to.usd_ama","name","text.format.of.closing.date..created.from.closdate.."],inplace=True)

        input_data["compcat"]=input_data["compcat"].replace({"MEDIUM_SIZED":"MEDIUM"})
        input_mydf=mydf(input_data)
        input_mydf["rechtsform"],rechtsform_factor_map=input_mydf.factorize_series(input_mydf["rechtsform"])
        input_mydf["compcat"],compcat_factor_map=input_mydf.factorize_series(input_mydf["compcat"],{"SMALL":0,"MEDIUM":1,"LARGE":2,"VERY_LARGE":3})
        input_mydf["bvdid"],bvdid_factor_map=input_mydf.factorize_series(input_mydf["bvdid"])

        #categorical_variables=["compcat","rechtsform","bvdid"]
        to_scale_variables=["cash","cred","cuas","culi","current.assets..debtors","current.assets..stocks","fias","ifas","ltdb","ncas","ncli","ocas","ocli","ofas","oncl","operating.revenue..turnover.","other.shareholders.funds","provisions","sales","shareholder.funds..capital","shfd","tfas","toas","tshf","working.capital"]
        treatment_variables=["treatment","subsidy","subsidy_duration_day","one_year_lag_total_annual_subsidy","total_annual_subsidy","integrated_dummy","conc_treatment","cum_treatment","cum_treatment_toas_ratio"]
        control_variables=["compcat","age","startup","STATUS"]
        scaled_df=scale_financial_variables(input_mydf,to_scale_variables)
        not_scaled_columns=input_mydf.columns.difference(scaled_df.columns)
        not_scaled_df=input_mydf[not_scaled_columns]
        self.df=pd.concat([scaled_df,not_scaled_df],axis=1)
        self.shfd=np.array(self.df["shfd"])
        self.sales=np.array(self.df["sales"])
        self.feature_matrix_cols=[col for col in self.df.columns if col not in treatment_variables and col not in control_variables]
        #feature_df=self.df[self.feature_matrix_cols]
        #
        #featurizer = PolynomialFeatures(degree=2,interaction_only=True,include_bias=False)
#
#
# Step 1#: Transform the data
        #X_transformed = featurizer.fit_transform(feature_df)
#
        ## Step 2: Get the transformed feature names
        #transformed_feature_names = featurizer.get_feature_names_out(self.feature_matrix_cols)
#
        ## Step 3: Create a DataFrame with the transformed data and column names
        #df_transformed = pd.DataFrame(X_transformed, columns=transformed_feature_names)
        #df_with_interaction=pd.concat([feature_df,df_transformed],axis=1)
        #self.feature_matrix_cols=df_with_interaction.columns

        #feature_matrix_cols_ex_bvdid=[col for col in feature_matrix_cols if col!="bvdid"]
        self.feature_matrix=np.array(self.df[self.feature_matrix_cols])
        self.control_matrix=np.array(self.df[control_variables])
        self.treatment_matrix=np.array(self.df[treatment_variables])
        self.model=model
    def fit(self,T,Y="shfd"):
        if Y=="shfd":
            Y=self.shfd
        if Y=="sales":
            Y=self.sales
        T=self.df[T]
        T=np.array(T)
        self.model.fit(Y,X=self.feature_matrix,W=self.control_matrix,T=T)
        return self
    def load(self):
        chdir_data()
        self.model=load(self.name)
    def dump(self):
        dump(self.model,self.name)
    def shap_analysis(self,treatment_var,featurized=False):
        expected_value = self.model.const_marginal_ate(self.feature_matrix)
# Ge    t SHAP values without checking additivity
        shap_values = self.model.shap_values(self.feature_matrix)

        #explainer_data = shap.Explanation(shap_values, base_values=expected_value, data=feature_matrix)
        #explainer=shap.TreeExplainer(model.model_final)
        plt.figure()
        #ind=0
        feature_names=self.feature_matrix_cols
        if featurized:
            feature_name_map=self.feature_matrix_map()
            #shap.plots.force(expected_value,shap_values['Y0']['conc_treatment'], matplotlib=True)
            #,feature_names=self.feature_matrix_cols

            feature_names = [feature_name_map.get(item, item) for item in shap_values['Y0'][treatment_var].feature_names]
        shap.summary_plot(shap_values['Y0'][treatment_var],feature_names=feature_names)

        plt.show()
    def feature_matrix_map(self):
        counter=0
        dict_map={}
        for column in self.feature_matrix_cols:
            key="X"+str(counter)
            counter+=1
            dict_map[key]=column
        new_dict={}
        for key_1,value_1 in dict_map.items():
            for key_2,value_2 in dict_map.items():
                if key_2!=key_1:
                    composite_key=key_1+" "+key_2
                    compsite_value=value_1+" "+value_2
                    new_dict[composite_key]=compsite_value
        dict_map.update(new_dict)
        return dict_map
        

            


def dynamic_model():
    feature_matrix_dynamic_model=input_df_with_scaled[feature_matrix_cols_ex_bvdid]
    dynamic_treatment_vars=["one_year_lag_total_annual_subsidy","total_annual_subsidy"]
    model=DynamicDML()
    groups=input_df_with_scaled["bvdid"]
    model.fit(Y=shfd,X=feature_matrix_dynamic_model,W=control_matrix,T=treatment_matrix[dynamic_treatment_vars],groups=groups)
    dump(model,"dynamic_model.jolib")
    return model

def fit_or_load(name):
    chdir_data()
    if name not in os.listdir():
        return "fit"
    else:
        return "load"

featurizer = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)

def shfd_signal_workflow():
    signal_treatment=["integrated_dummy","conc_treatment"]
    featurizer = PolynomialFeatures(degree=2,interaction_only=True,include_bias=False)
    signal_model=bachelor_model(CausalForestDML(random_state=1444),"signal_model_shfd.jolib")
    cmd=fit_or_load(signal_model.name)
    if cmd=="fit":
        signal_model.fit(signal_treatment)
        signal_model.dump()
    elif cmd=="load":
        signal_model.load()
    signal_model.shap_analysis("T1")
    #signal_model.shap_analysis("T0")


def sales_signal_workflow():
    signal_treatment=["integrated_dummy","conc_treatment"]
    signal_model=bachelor_model(CausalForestDML(random_state=1444),"signal_model_sales.jolib")
    cmd=fit_or_load(signal_model.name)
    if cmd=="fit":
        signal_model.fit(signal_treatment,Y="sales")
        signal_model.dump()
    elif cmd=="load":
        signal_model.load()
    signal_model.shap_analysis("T1")


shfd_signal_workflow()
sales_signal_workflow()


financial_treatment=["subsidy","subsidy_toas_ratio"]
direct_treatment=["total_annual_subsidy","total_annual_subsidy","total_annual_subsidy_lagged"]

def single_tree_int():
    interpretation=SingleTreeCateInterpreter()
    cate_interpretation=interpretation.interpret(model,feature_matrix) #wtf do I do with you?
    print(cate_interpretation)
    plt.figure()
    interpretation.plot(feature_names=feature_matrix_cols,fontsize=12)
    plt.show()

def startup_analysis():
    startup=input_mydf[input_mydf["startup"]==True]
    treatment_effects_startup = bachelor_dml.effect(startup)
    print("Estimated treatment effect:", np.mean(treatment_effects_startup))
    plt.hist(treatment_effects_startup,bins=30)
    plt.plot()
    plt.show()

    not_startup=startup=input_mydf[input_mydf["startup"]==False]
    treatment_effects_not_startup = bachelor_dml.effect(not_startup)
    print("Estimated treatment effect:", np.mean(not_startup))
    plt.hist(treatment_effects_not_startup,bins=30)
    plt.plot()
    plt.show()




