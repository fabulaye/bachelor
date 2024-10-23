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
from econml.cate_interpreter import SingleTreeCateInterpreter,SingleTreePolicyInterpreter
from processing.my_df import drop_unnamed_columns
from matplotlib import pyplot as plt
import shap
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from econml.panel.dml import DynamicDML
import os
from sklearn.preprocessing import PolynomialFeatures
from econml.validate import DRtester
from sklearn.model_selection import train_test_split
from datahandling.string_to_text import string_to_txt

#CausalForestDML().shap_values



#matched_data=pd.read_excel(r"C:\Users\lukas\Desktop\bachelor\data\matched_data.xlsx")
#input_data=matched_data.drop(columns=excluded_vars)

#input_data=filter_input(input_data)


class bachelor_model():
    def __init__(self,model:CausalForestDML,name,treatment_names,controls=None,scale_y=False):
        self.name=name
        self.treatment_names=treatment_names
        self.model=model
        chdir_data()
        input_data=pd.read_excel(r"financials_merge_treatment_and_control_categorials_cleaned_imputed_dropped.xlsx")
        input_data=drop_unnamed_columns(input_data)
        input_data.drop(columns=["annual_subsidy","total_subsidy","country","ctryiso","filing type","audit status","original units","original currency","estimated operating revenue","estimated employees","accounting practice","closdate","conscode","historic_statusdate","account.unit","exchange.rate.from.local.currency.to.usd_ama","name","text.format.of.closing.date..created.from.closdate..","name_x","Name","Rechtsform","age.1","distance","reverse_treatment","subclass","...1","name_underscore"],inplace=True,errors="ignore")

        input_data["compcat"]=input_data["compcat"].replace({"MEDIUM_SIZED":"MEDIUM"})
        input_mydf=mydf(input_data)
        input_mydf.rename(columns={"current.assets..debtors":"cuas_debtors","current.assets..stocks":"cuas_stocks","solvency.ratio....":"solvency_ratio"},inplace=True)
        input_mydf["rechtsform"],rechtsform_factor_map=input_mydf.factorize_series(input_mydf["rechtsform"])
        input_mydf["compcat"],self.compcat_factor_map=input_mydf.factorize_series(input_mydf["compcat"],{"SMALL":0,"MEDIUM":1,"LARGE":2,"VERY_LARGE":3})
        input_mydf["bvdid"],self.bvdid_factor_map=input_mydf.factorize_series(input_mydf["bvdid"])

        #categorical_variables=["compcat","rechtsform","bvdid"]
        to_scale_variables=["cash","cuas","culi","cuas_debtors","cuas_stocks","fias","ifas","ltdb","ncas","ncli","oncl","provisions","tfas","toas"]
        treatment_variables=["treatment","subsidy_duration_day","one_year_lag_total_annual_subsidy","total_annual_subsidy","integrated_dummy","conc_treatment","cum_treatment","cum_treatment_toas_ratio","subsidy_expectation","subsidy_expectation_toas_ratio","total_annual_subsidy_toas_ratio","treatment_weight"]

        possibly_drop=["published","rechtsform","startup","ofas","ocas","tshf","shareholder.funds..capital","other.shareholders.funds","last_release","number_projects","STATUS"]
        input_mydf.drop(columns=possibly_drop,inplace=True,errors="ignore")

        dependent_variables=["shfd","shfd_rescaled","shfd_min_cum_treatment_rescaled","shfd_min_cum_treatment"]#
        control_variables=[]
        
        self.weights=[]
        
        #small_model_covariates=["bvdid","cash","compcat","age","cuas","empl","ifas","ltdb","ncas","ncli","solvency.ratio....","tfas","culi","provisions","oncl"]
        #to_scale_variables=["cash","cuas","culi","ifas","ltdb","ncas","ncli","tfas","toas","provisions","oncl"]
        #    
        #self.weights=input_mydf["weights"]
        self.scaler=StandardScaler()
        input_scaled=self.scaler.fit_transform(input_mydf[to_scale_variables])
        scaled_df=pd.DataFrame(input_scaled,columns=to_scale_variables)

        not_scaled_columns=input_mydf.columns.difference(scaled_df.columns)
        not_scaled_df=input_mydf[not_scaled_columns]
        self.df=pd.concat([scaled_df,not_scaled_df],axis=1)

        #self.shfd_scaler=MinMaxScaler()
        #if scale_y:
        #    shfd_reshaped=shfd.reshape(-1, 1)
        #    self.df["shfd"]=self.shfd_scaler.fit_transform(shfd_reshaped)
        self.shfd=np.array(self.df["shfd_min_cum_treatment_rescaled"])
        #self.sales=np.array(self.df["sales"])
        self.feature_matrix_cols=[col for col in self.df.columns if col not in treatment_variables and col not in control_variables and col not in dependent_variables]
        #self.feature_matrix_cols=small_model_covariates
        feauture_matrix=self.df[self.feature_matrix_cols]
        self.financial_df=self.df[self.feature_matrix_cols].drop(columns=["bvdid"])
        self.financial_matrix=self.financial_df.to_numpy()
        self.treatment_df=self.df[treatment_variables]
        feauture_matrix.columns.to_frame().to_csv("model_features.csv")
        self.feature_matrix=np.array(self.df[self.feature_matrix_cols])
        self.control_matrix=np.array(self.df[control_variables])
        self.treatment_matrix=np.array(self.df[treatment_names])
        self.feature_names=self.feature_matrix_cols
        
        
    def fit(self,T,Y="shfd",cache_values=True):
        if Y=="shfd":
            Y=self.shfd
        if len(T)==1:
            T=T[0]
        T=self.df[T]
        T=np.array(T)
        if len(self.weights)>0:
            if self.control_matrix.shape[1]>0:
                self.model.tune(Y,X=self.feature_matrix,T=T,sample_weight=self.weights,W=self.control_matrix,groups=self.df["bvdid"])
                self.model.fit(Y,X=self.feature_matrix,T=T,sample_weight=self.weights,W=self.control_matrix,groups=self.df["bvdid"])
            else:
                self.model.tune(Y,X=self.feature_matrix,T=T,sample_weight=self.weights,groups=self.df["bvdid"])
                self.model.fit(Y,X=self.feature_matrix,T=T,sample_weight=self.weights,groups=self.df["bvdid"])
        else:
            if self.control_matrix.shape[1]>0:
                self.model.tune(Y,X=self.feature_matrix,T=T,W=self.control_matrix,groups=self.df["bvdid"])
                self.model.fit(Y,X=self.feature_matrix,T=T,W=self.control_matrix,groups=self.df["bvdid"],cache_values=cache_values)
            else:
                self.model.tune(Y,X=self.feature_matrix,T=T,groups=self.df["bvdid"])
                self.model.fit(Y,X=self.feature_matrix,T=T,groups=self.df["bvdid"],cache_values=cache_values)
        return self
    def shap_values(self):
        self.shap_values = self.model.shap_values(self.feature_matrix,feature_names=self.feature_names,treatment_names=self.treatment_names)
        self.explainer=self.shap_values["Y0"]
    def load(self):
        chdir_data()
        self.model=load(self.name)
    def dump(self):
        chdir_data()
        dump(self.model,self.name+".jolib")
    def shap_barplot(self,treatment_var,show=False):
        treatment_explainer=self.explainer[treatment_var]
        shap.initjs()
        plt.figure(figsize=(10, 8))
        plt.subplots_adjust(left=0.2, right=0.9)
        plt.yticks(rotation=45)
        plt.title(self.name + " Feature Importance Bar Plot",fontsize=14)
        bar_plot=shap.plots.bar(treatment_explainer, max_display=12,show=show)
        plt.savefig(f'{self.name}_{treatment_var}_bar.png')
        plt.close()
    def shap_barplot_size_cohort(self,treatment_var,show=False):
        treatment_explainer=self.explainer[treatment_var]
        #cohorts=treatment_explainer
        shap.initjs()
        plt.figure(figsize=(10, 9))
        plt.subplots_adjust(left=0.2, right=0.9)
        plt.yticks(rotation=45)
        plt.title(self.name + " Feature Importance Size Cohorts Bar Plot",fontsize=14)
        cohorts=shap.Cohorts(small=treatment_explainer[treatment_explainer[:, "compcat"].data == 0],medium_and_large=treatment_explainer[treatment_explainer[:, "compcat"].data >= 1])
        bar_plot=shap.plots.bar(cohorts, max_display=12,show=show)
        plt.savefig(f'{self.name}_{treatment_var}_size_bar_cohort.png')
        plt.close()
    def shap_barplot_cohort(self,treatment_var,show=False):
        treatment_explainer=self.explainer[treatment_var]
        #cohorts=treatment_explainer
        shap.initjs()
        plt.figure(figsize=(10, 8))
        plt.subplots_adjust(left=0.2, right=0.9)
        plt.yticks(rotation=45)
        plt.title(self.name + " Automatic Cohort Plot",fontsize=14)
        bar_plot_2=shap.plots.bar(treatment_explainer.cohorts(2).abs.mean(0), max_display=12,show=show)
        plt.savefig(f'{self.name}_{treatment_var}_bar_cohort.png')
        plt.close()
    def shap_scatter_plot(self,treatment_var,feature,show=False):
        treatment_explainer=self.explainer[treatment_var]
        shap.initjs()
        plt.figure(figsize=(10, 8))
        plt.yticks(rotation=45)
        plt.title(self.name + " Scatter Plot",fontsize=14)
        scatter_plot=shap.plots.scatter(treatment_explainer[:,feature],show=show)
        plt.title(self.name + "Scatter Plot",fontsize=14)
        plt.savefig(f'{self.name}_{treatment_var}_{feature}_scatter.png')
        plt.close()
    def shap_force_plot(self,treatment_var,show=False):
        treatment_explainer=self.explainer[treatment_var]
        shap.initjs()
        plt.title(self.name + " Force Plot",fontsize=14)
        force_plot=shap.plots.force(treatment_explainer,feature_names=self.feature_names,show=show)
        shap.save_html(f'{self.name}_shap_force_plot.html', force_plot)
    def shap_summary_plot(self,treatment_var,show=False):
        treatment_explainer=self.explainer[treatment_var]
        shap.initjs()
        plt.figure(figsize=(10, 8))
        plt.yticks(rotation=45)
        plt.title(self.name + " Summary Plot",fontsize=14)
        shap.summary_plot(treatment_explainer,feature_names=self.feature_names,show=show)
        plt.savefig(f'{self.name}_{treatment_var}_summary.png')
        plt.close()
    def shap_heatmap(self,treatment_var,show=False):
        treatment_explainer=self.explainer[treatment_var]
        shap.initjs()
        #plt.figure(figsize=(10, 9))
        
        plt.yticks(rotation=45)
        plt.title(self.name + " Heatmap Plot",fontsize=14)
        shap.plots.heatmap(treatment_explainer, max_display=12,show=show)
        plt.savefig(f'{self.name}_{treatment_var}_heatmap.png')
        plt.close()
    def shap_violin(self,treatment_var,show=False):
        treatment_explainer=self.explainer[treatment_var]
        shap.initjs()
        plt.figure(figsize=(10, 8))
        plt.subplots_adjust(left=0.2, right=0.9)
        plt.yticks(rotation=45)
        plt.title(self.name + " Violin Plot",fontsize=14)
        violin=shap.plots.violin(treatment_explainer,show=show)
        plt.savefig(f'{self.name}_{treatment_var}_violin.png')
        plt.close()
    def shap_beeswarm(self,treatment_var,show=False):
        treatment_explainer=self.explainer[treatment_var]
        shap.initjs()
        plt.figure(figsize=(10, 8))
        plt.subplots_adjust(left=0.3, right=0.9,bottom=0.2)
        plt.yticks(rotation=45)
        plt.title(self.name + " Beeswarm Plot",fontsize=14)
        shap.plots.beeswarm(treatment_explainer,show=show)
        plt.savefig(f'{self.name}_{treatment_var}_beeswarm.png')
        plt.close()
    def full_shap_workflow(self,dir_path):
        os.chdir(dir_path)
        folders=os.listdir()
        self.shap_values()
        for treatment_var in self.treatment_names:
            if treatment_var not in folders:
                os.makedirs(treatment_var)
            os.chdir(treatment_var)
            self.shap_violin(treatment_var)
            self.shap_beeswarm(treatment_var)
            self.shap_heatmap(treatment_var)
            self.shap_summary_plot(treatment_var)
            self.shap_barplot(treatment_var)
            self.shap_barplot_cohort(treatment_var)
            self.shap_barplot_size_cohort(treatment_var)
            #model.shap_barplot_cluster(treatment_var)
            self.shap_force_plot(treatment_var)
            os.chdir(dir_path)
    def ate_workflow(self,base_treatment,target_treatment):
        #self.ate=self.model.ate(X=self.feature_matrix)
        self.ate=self.model.ate(T0=base_treatment,T1=target_treatment,X=self.feature_matrix)
        print(f"ATE: {self.ate}")
        self.ate_inference=self.model.ate_inference(T0=base_treatment,T1=target_treatment,X=self.feature_matrix)
        print(f"ATE Inference: {self.ate_inference}")
        self.ate_interval=self.model.ate_interval(self.feature_matrix)
        print(f"ATE CI: {self.ate_interval}")
    def const_marginal_ate_workflow(self):
        self.const_marginal_ate=self.model.const_marginal_ate(self.feature_matrix)
        print(f"Const. Marginal ATE: {self.const_marginal_ate}")
        self.const_marginal_ate_inference=self.model.const_marginal_ate_inference(self.feature_matrix)
        print(f"Const. Marginal ATE Inference: {self.const_marginal_ate_inference}")
        self.const_marginal_ate_interval=self.model.const_marginal_ate_inference(self.feature_matrix)
        print(f"Const. Marginal ATE CI: {self.const_marginal_ate_interval}")
    def cate_workflow(self):
        print(self.name)
        feature_df=self.df[self.feature_matrix_cols]
        for original,new in self.compcat_factor_map.items():
            mask=feature_df["compcat"]==new
            data=self.feature_matrix[mask,:]
            cate_matrix=self.model.const_marginal_ate(data)
            print(f"{original}: {cate_matrix}")
            cate_inference_matrix=self.model.const_marginal_ate_inference(data)
            print(f"{original}: {cate_inference_matrix}")
            cate_interval_matrix=self.model.const_marginal_ate_interval(data)
            print(f"{original}: {cate_interval_matrix}")
            filename=self.name+original+"cate.txt"
            string_to_txt(cate_inference_matrix.__str__(),file_name=filename,path=r"C:\Users\lukas\Desktop\bachelor\data\cate_output")
        mask=feature_df["age"]<=5
        data=self.feature_matrix[mask,:]
        cate_matrix=self.model.const_marginal_ate(data)
        print(f"Startup False: {cate_matrix}")
        cate_inference_matrix=self.model.const_marginal_ate_inference(data)
        print(f"Startup False: {cate_inference_matrix}")
        cate_interval_matrix=self.model.const_marginal_ate_interval(data)
        print(f"Startup False: {cate_interval_matrix}")
        filename=self.name+"not_startup"+"cate.txt"
        string_to_txt(cate_inference_matrix.__str__(),file_name=filename,path=r"C:\Users\lukas\Desktop\bachelor\data\cate_output")
        mask=feature_df["age"]>5
        data=self.feature_matrix[mask,:]
        cate_matrix=self.model.const_marginal_ate(data)
        print(f"Startup True: {cate_matrix}")
        cate_inference_matrix=self.model.const_marginal_ate_inference(data)
        print(f"Startup True: {cate_inference_matrix}")
        cate_interval_matrix=self.model.const_marginal_ate_interval(data)
        print(f"Startup True: {cate_interval_matrix}")
        filename=self.name+"startup"+"cate.txt"
        string_to_txt(cate_inference_matrix.__str__(),file_name=filename,path=r"C:\Users\lukas\Desktop\bachelor\data\cate_output")
    def hte_workflow(self,base_treatment=None,target_treatment=None):
        self.hte=self.model.effect(T0=base_treatment,T1=target_treatment,X=self.feature_matrix)
        print(f"HTE: {self.hte}")
        self.hte_inference=self.model.effect_inference(T0=base_treatment,T1=target_treatment,X=self.feature_matrix)
        print(f"HTE Inference: {self.hte_inference}")
        self.hte_interval=self.model.effect_interval(T0=base_treatment,T1=target_treatment,X=self.feature_matrix)
        print(f"HTE CI: {self.hte_interval}")
    def single_tree_int(self):
        interpretation=SingleTreeCateInterpreter(max_leaf_nodes=20)
        cate_interpretation=interpretation.interpret(self.model,self.feature_matrix) #wtf do I do with you?
        os.chdir(r"E:\bachelor_figures\cate")
        cate_interpretation.render(self.name+"cate_tree_interpretation",feature_names=self.feature_names)
        #cate_interpretation.export_graphviz("cate_tree_interpretation.gv",feature_names=self.feature_names)
    def single_tree_policy_int(self):
        
        interpretation=SingleTreePolicyInterpreter()
        cate_interpretation=interpretation.interpret(self.model,self.feature_matrix) #wtf do I do with you?
        os.chdir(r"E:\bachelor_figures\cate")
        cate_interpretation.render(self.name+"cate_tree_policy_interpretation",feature_names=self.feature_names)
        #cate_interpretation.export_graphviz("cate_tree_interpretation.gv",feature_names=self.feature_names)
    def validation(self):
        model=self.model
        regression=model.models_y
        propensity=model.models_t
        cate=model.model_cate
        cate_fitted=cate.fit(X=self.feature_matrix,T=self.treatment_matrix,y=self.shfd)
        tester=DRtester(model_regression=regression,model_propensity=propensity,cate=cate_fitted)
        X_train, X_test=train_test_split(self.feature_matrix,test_size=0.3)
        evaluation=tester.evaluate_blp(X_test,X_train)
        print(evaluation)


        	

        

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
    
        

def fit_or_load(name):
    chdir_data()
    if name not in os.listdir():
        return "fit"
    else:
        return "load"

featurizer = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)

def stats_table_to_latex(table,name_prefix):
    latex_table = table.as_latex_tabular()
    file_name=name_prefix+table.title+".txt"
    with open(file_name,"w") as w:
        w.write(latex_table)


def create_signal_model():
    signal_treatment=["conc_treatment"]
    
    featurizer = PolynomialFeatures(degree=2,interaction_only=True,include_bias=False)
    signal_model=bachelor_model(CausalForestDML(random_state=1444),"signal_model",signal_treatment)
    cmd=fit_or_load(signal_model.name)
    if cmd=="fit":
        signal_model.fit(signal_treatment,cache_values=True)
        signal_model.dump()
    elif cmd=="load":
        signal_model.load()
    summary=signal_model.model.summary()
    for table in summary.tables:
        stats_table_to_latex(table,signal_model.name)
    #summary_df=pd.DataFrame(summary)
    return signal_model


#signal_model=create_signal_model()
#signal_model.full_shap_workflow(r"E:\bachelor_figures\shap_signal_model")
#signal_model.cate_workflow()
#signal_model.single_tree_int()
#signal_model.single_tree_policy_int()



def create_financial_model():
    financial_treatment=["subsidy_expectation_toas_ratio"]
    
    featurizer = PolynomialFeatures(degree=2,interaction_only=True,include_bias=False)
    financial_model=bachelor_model(CausalForestDML(random_state=1444),"finance_model",financial_treatment)
    cmd=fit_or_load(financial_model.name)
    if cmd=="fit":
        financial_model.fit(financial_treatment)
        financial_model.dump()
    elif cmd=="load":
        financial_model.load()
    summary=financial_model.model.summary()
    for table in summary.tables:
        stats_table_to_latex(table,financial_model.name)
    return financial_model



#financial_model=create_financial_model()
#financial_model.full_shap_workflow(r"E:\bachelor_figures\shap_financial_model")
#financial_model.cate_workflow()
#financial_model.single_tree_int()
#financial_model.single_tree_policy_int()


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
    direct_treatment=["cum_treatment_toas_ratio"]
    featurizer = PolynomialFeatures(degree=2,interaction_only=True,include_bias=False)
    direct_model=bachelor_model(CausalForestDML(random_state=1444),"subsidy_transformation_model",direct_treatment,scale_y=True)
    cmd=fit_or_load(direct_model.name)
    if cmd=="fit":
        direct_model.fit(direct_treatment)
        direct_model.dump()
    elif cmd=="load":
        direct_model.load()
    summary=direct_model.model.summary()
    for table in summary.tables:
        stats_table_to_latex(table,direct_model.name)
    return direct_model
    

direct_model=create_direct_model()
direct_model.full_shap_workflow(r"E:\bachelor_figures\shap_direct_model")
#direct_model.cate_workflow()
#direct_model.single_tree_int()
#direct_model.single_tree_policy_int()




