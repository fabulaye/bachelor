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


#CausalForestDML().shap_values



#matched_data=pd.read_excel(r"C:\Users\lukas\Desktop\bachelor\data\matched_data.xlsx")
#input_data=matched_data.drop(columns=excluded_vars)

#input_data=filter_input(input_data)


class bachelor_model():
    def __init__(self,model,name,treatment_names,controls=None,scale_y=False):
        self.name=name
        self.treatment_names=treatment_names
        self.model=model
        input_data=pd.read_excel(r"C:\Users\lukas\Desktop\bachelor\data\financials_merge_treatment_and_control_categorials_cleaned_imputed_dropped.xlsx")
        input_data=drop_unnamed_columns(input_data)
        input_data.drop(columns=["annual_subsidy","total_subsidy","country","ctryiso","filing type","audit status","original units","original currency","estimated operating revenue","estimated employees","accounting practice","closdate","conscode","historic_statusdate","account.unit","exchange.rate.from.local.currency.to.usd_ama","name","text.format.of.closing.date..created.from.closdate..","name_x","Name","Rechtsform","age.1","tshf","shareholder.funds..capital",],inplace=True,errors="ignore")

        input_data["compcat"]=input_data["compcat"].replace({"MEDIUM_SIZED":"MEDIUM"})
        input_mydf=mydf(input_data)
        input_mydf["rechtsform"],rechtsform_factor_map=input_mydf.factorize_series(input_mydf["rechtsform"])
        input_mydf["compcat"],compcat_factor_map=input_mydf.factorize_series(input_mydf["compcat"],{"SMALL":0,"MEDIUM":1,"LARGE":2,"VERY_LARGE":3})
        input_mydf["bvdid"],bvdid_factor_map=input_mydf.factorize_series(input_mydf["bvdid"])

        #categorical_variables=["compcat","rechtsform","bvdid"]
        to_scale_variables=["cash","cuas","culi","current.assets..debtors","current.assets..stocks","fias","ifas","ltdb","ncas","ncli","ocas","ofas","oncl","other.shareholders.funds","provisions","tfas","toas","working.capital"]
        treatment_variables=["treatment","subsidy","subsidy_duration_day","one_year_lag_total_annual_subsidy","total_annual_subsidy","integrated_dummy","conc_treatment","cum_treatment","cum_treatment_toas_ratio","subsidy_expectation_sum","subsidy_expectation_sum_toas_ratio","total_annual_subsidy_toas_ratio","treatment_weight"]
        control_variables=["compcat","age","STATUS","closdate_year","total_annual_subsidy","toas"]
        #control_variables=["total_annual_subsidy"]
        control_variables=controls

        self.scaler=StandardScaler()
        input_scaled=self.scaler.fit_transform(input_mydf[to_scale_variables])
        scaled_df=pd.DataFrame(input_scaled,columns=to_scale_variables)

        not_scaled_columns=input_mydf.columns.difference(scaled_df.columns)
        not_scaled_df=input_mydf[not_scaled_columns]
        self.df=pd.concat([scaled_df,not_scaled_df],axis=1)

        self.shfd_scaler=StandardScaler()
        shfd=np.array(self.df["shfd"])
        if scale_y:
            shfd_reshaped=shfd.reshape(-1, 1)
            self.df["shfd"]=self.shfd_scaler.fit_transform(shfd_reshaped)
        self.shfd=np.array(self.df["shfd"])
        #self.sales=np.array(self.df["sales"])
        self.feature_matrix_cols=[col for col in self.df.columns if col not in treatment_variables and col not in control_variables and col!="shfd"]
        feauture_matrix=self.df[self.feature_matrix_cols]
        index=feauture_matrix.isna().sum()
        self.treatment_df=self.df[treatment_variables]
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
        self.feature_names=self.feature_matrix_cols
        
        
    def fit(self,T,Y="shfd"):
        if Y=="shfd":
            Y=self.shfd
        if Y=="sales":
            Y=self.sales
        T=self.df[T]
        T=np.array(T)
        self.model.fit(Y,X=self.feature_matrix,W=self.control_matrix,T=T)
        return self
    def shap_values(self):
        self.shap_values = self.model.shap_values(self.feature_matrix,feature_names=self.feature_names,treatment_names=self.treatment_names)
        self.explainer=self.shap_values["Y0"]
    def load(self):
        chdir_data()
        self.model=load(self.name)
    def dump(self):
        dump(self.model,self.name+".jolib")
    def shap_barplot(self,treatment_var,show=False):
        treatment_explainer=self.explainer[treatment_var]
        shap.initjs()
        bar_plot=shap.plots.bar(treatment_explainer, max_display=12,show=show)
        plt.savefig(f'{self.name}_{treatment_var}_bar.png')
        plt.close()
    def shap_barplot_cohort(self,treatment_var,show=False):
        treatment_explainer=self.explainer[treatment_var]
        shap.initjs()
        bar_plot=shap.plots.bar(treatment_explainer.cohorts(2).abs.mean(0), max_display=12,show=show)
        plt.savefig(f'{self.name}_{treatment_var}_bar_cohort.png')
        plt.close()
    def shap_barplot_cluster(self,treatment_var,show=False):
        treatment_explainer=self.explainer[treatment_var]
        shap.initjs()
        bar_plot=shap.plots.bar(treatment_explainer,clustering=True,clustering_cutoff=0.5,max_display=12,show=show)
        plt.savefig(f'{self.name}_{treatment_var}_bar_cluster.png')
        plt.close()
    def shap_scatter_plot(self,treatment_var,feature,show=False):
        treatment_explainer=self.explainer[treatment_var]
        shap.initjs()
        scatter_plot=shap.plots.scatter(treatment_explainer[:,feature],show=show)
        plt.savefig(f'{self.name}_{treatment_var}_{feature}_scatter.png')
        plt.close()
    def shap_force_plot(self,treatment_var,show=False):
        treatment_explainer=self.explainer[treatment_var]
        shap.initjs()
        force_plot=shap.plots.force(treatment_explainer,feature_names=self.feature_names,show=show)
        shap.save_html(f'{self.name}_shap_force_plot.html', force_plot)
    def shap_summary_plot(self,treatment_var,show=False):
        treatment_explainer=self.explainer[treatment_var]
        shap.initjs()
        shap.summary_plot(treatment_explainer,feature_names=self.feature_names,show=show)
        plt.savefig(f'{self.name}_{treatment_var}_summary.png')
        plt.close()
    def shap_heatmap(self,treatment_var,show=False):
        treatment_explainer=self.explainer[treatment_var]
        shap.initjs()
        shap.plots.heatmap(treatment_explainer, max_display=12,show=show)
        plt.savefig(f'{self.name}_{treatment_var}_heatmap.png')
        plt.close()
    def shap_violin(self,treatment_var,show=False):
        treatment_explainer=self.explainer[treatment_var]
        shap.initjs()
        violin=shap.plots.violin(treatment_explainer,show=show)
        plt.savefig(f'{self.name}_{treatment_var}_violin.png')
        plt.close()
    def shap_beeswarm(self,treatment_var,show=False):
        treatment_explainer=self.explainer[treatment_var]
        shap.initjs()
        shap.plots.beeswarm(treatment_explainer,show=show)
        plt.savefig(f'{self.name}_{treatment_var}_beeswarm.png')
        plt.close()
    def test(featurized):   
        if featurized:
            feature_name_map=self.feature_matrix_map()
            #shap.plots.force(expected_value,shap_values['Y0']['conc_treatment'], matplotlib=True)
            #,feature_names=self.feature_matrix_cols

            feature_names = [feature_name_map.get(item, item) for item in shap_values['Y0'][treatment_var].feature_names]
       
        
        

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

def create_signal_model():
    signal_treatment=["integrated_dummy","conc_treatment","number_projects"]
    featurizer = PolynomialFeatures(degree=2,interaction_only=True,include_bias=False)
    signal_model=bachelor_model(CausalForestDML(random_state=1444,discrete_treatment=True,categories=signal_treatment),"signal_model_shfd.jolib")
    cmd=fit_or_load(signal_model.name)
    cmd="fit"
    if cmd=="fit":
        signal_model.fit(signal_treatment)
        signal_model.dump()
    elif cmd=="load":
        signal_model.load()
    return signal_model


#signal_model=create_signal_model()
#signal_model.shap_analysis("T1")
#print(signal_model.model.marginal_effect())


def create_financial_model():
    financial_treatment=["subsidy_expectation_sum","subsidy_expectation_sum_toas_ratio","conc_treatment"]
    
    featurizer = PolynomialFeatures(degree=2,interaction_only=True,include_bias=False)
    financial_model=bachelor_model(CausalForestDML(random_state=1444),"finance_model_shfd",financial_treatment,scale_y=True)
    cmd=fit_or_load(financial_model.name)
    cmd="fit"
    if cmd=="fit":
        financial_model.fit(financial_treatment)
        financial_model.dump()
    elif cmd=="load":
        financial_model.load()
    return financial_model

def full_shap_workflow(model:bachelor_model,dir_path):
    os.chdir(dir_path)
    folders=os.listdir()
    model.shap_values()
    for treatment_var in model.treatment_names:
        if treatment_var not in folders:
            os.makedirs(treatment_var)
        os.chdir(treatment_var)
        model.shap_violin(treatment_var)
        model.shap_beeswarm(treatment_var)
        model.shap_heatmap(treatment_var)
        model.shap_summary_plot(treatment_var)
        model.shap_barplot(treatment_var)
        model.shap_barplot_cohort(treatment_var)
        #model.shap_barplot_cluster(treatment_var)
        model.shap_force_plot(treatment_var)
        os.chdir(dir_path)
    
    

#financial_model=create_financial_model()
#full_shap_workflow(financial_model,r"E:\bachelor_figures\shap_financial_model")





#marginal_ate=financial_model.model.marginal_ate(financial_model.treatment_df["subsidy_expectation_sum"],financial_model.feature_matrix).reshape(-1, 1)
#marginal_ate_lower_rescaled=financial_model.shfd_scaler.inverse_transform(marginal_ate)
#print(marginal_ate_lower_rescaled)
#print(financial_model.model.const_marginal_effect_interval(X=financial_model.feature_matrix))
#print(financial_model.model.effect(financial_model.feature_matrix,T0=np.zeros(financial_model.treatment_df["subsidy_expectation_sum"].shape),T1=financial_model.treatment_df["subsidy_expectation_sum"]))
#feat_importance=financial_model.model.feature_importances()
#feat_importance_df=pd.Series(feat_importance,index=financial_model.feature_matrix_cols)
#print(feat_importance_df)
#shfd_financial_workflow()


def create_direct_model():
    direct_treatment=["one_year_lag_total_annual_subsidy","total_annual_subsidy_toas_ratio","cum_treatment","cum_treatment_toas_ratio"]
    direct_controls=["age","STATUS","closdate_year","toas"]
    featurizer = PolynomialFeatures(degree=2,interaction_only=True,include_bias=False)
    direct_model=bachelor_model(CausalForestDML(random_state=1444),"direct_model",direct_treatment,scale_y=True,controls=direct_controls)
    cmd=fit_or_load(direct_model.name)
    if cmd=="fit":
        direct_model.fit(direct_treatment)
        direct_model.dump()
    elif cmd=="load":
        direct_model.load()
    return direct_model
    
direct_model=create_direct_model()
full_shap_workflow(direct_model,r"E:\bachelor_figures\shap_direct_model")



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




