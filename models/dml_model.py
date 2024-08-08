import numpy as np
import pandas as pd
from econml.dr import DRLearner
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from datahandling.change_directory import chdir_sql_requests,chdir_data

from sklearn.model_selection import train_test_split, StratifiedKFold
from econml.dml import LinearDML,DML,SparseLinearDML
import shap
from sklearn.linear_model import LassoCV,Ridge
from sklearn.preprocessing import StandardScaler
#lasso konvergiert nicht
# Separate the outcome, treatment, and covariates

scaler=StandardScaler()


#chdir_sql_requests()
chdir_data()
data=pd.read_excel("treatmentfinancialsbvd_ama_filtered.xlsx")

def create_test_train(data,y_feature):

    Y = data[y_feature]
    columns_to_drop=["annual_subsidy","treatment_weight","treatment","Fördersumme in EUR","bvdid","closdate_year","unit","exchrate","exchrate2",y_feature,"country","repbas","closdate","accpra","currency","Unnamed: 0_y","earnings","name","id","game_name","moby_id","release_date","platform_releases","publishers","score","rank","critics","genre","steam_link","title","review_count","review_percentage","price","genres","year","review_percentage_mean","review_count_mean","score_mean","rank_mean","critics_mean","price_mean","review_count_sum"]
    data["compcat"],uniques=pd.factorize(data["compcat"])
    data.drop(columns=columns_to_drop,inplace=True)
    cols = list(data.columns)
    cols.insert(-1, cols.pop(cols.index('summed_annual_subsidy')))
    data = data[cols]
    data=scaler.fit_transform(data)
    X = data[:,:-1]
    T =data[:,1]

    
    X_train, X_test, Y_train, Y_test, T_train, T_test = train_test_split(X, Y, T, test_size=0.2, random_state=123)
    return X_train, X_test, Y_train, Y_test, T_train, T_test,cols

def dml_model(Y_train,T_train,X_train):
    model_y = RandomForestRegressor()
    model_t = RandomForestRegressor()

    dml_learner = DML(model_y=model_y, model_t=model_t, cv=5,model_final=Ridge(fit_intercept=False, max_iter=20000))
    #dml_learner=SparseLinearDML(model_y=model_y, model_t=model_t)

        # Fit the model
    dml_learner.fit(Y_train, T_train, X=X_train)
    return dml_learner


X_train, X_test, Y_train, Y_test, T_train, T_test,cols=create_test_train(data,"shfd")

dml_learner=dml_model(Y_train,T_train,X_train)

feature_importance=dml_learner.model_final_.coef_
# Estimate the treatment effect on the test set
treatment_effects = dml_learner.effect(X_test)
feature_importance_df=pd.DataFrame(feature_importance,cols)
print(feature_importance_df)


X_test=np.column_stack((X_test,treatment_effects))

# Summary of average treatment effect
ate = np.mean(treatment_effects)
print(f'Average Treatment Effect (ATE): {ate}')

# Subgroup analysis
X_test=pd.DataFrame(X_test,columns=cols)
X_test.rename(columns={"summed_annual_subsidy":"treatment_effect"})

#subgroup_effects = X_test.groupby('empl')['treatment_effect'].mean()
chdir_sql_requests()
X_test.to_excel("X_test_with_treatment_effects.xlsx")
#print(subgroup_effects)

# SHAP analysis for model interpretation
#explainer = shap.TreeExplainer(dml_learner)
shap_values=dml_learner.shap_values(X)
shap.plots.beeswarm(shap_values["solr"]["summed_annual_subsidy"])
#shap_values = explainer.shap_values(X_test)

# Plot the SHAP values
#shap.summary_plot(shap_values, X_test)

