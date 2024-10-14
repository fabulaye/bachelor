from econml.dml import DML
from sklearn.linear_model import LassoCV, LogisticRegressionCV
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd
from processing.my_df import mydf
from joblib import dump,load
from datahandling.change_directory import chdir_data
from matplotlib import pyplot as plt


def run_dml_model_with_weights(X, T, Y, W=None, model_y='lasso', model_t='logistic', model_final='lasso', random_state=0):
    """
    Function to run a Double Machine Learning (DML) model from econml with matched weights.
    
    Parameters:
    - X: array-like, shape (n_samples, n_features)
        Covariates/features.
    - T: array-like, shape (n_samples,)
        Treatment indicator/variable.
    - Y: array-like, shape (n_samples,)
        Outcome/target variable.
    - W: array-like, shape (n_samples, n_controls), optional
        Controls/exogenous variables. If None, defaults to an empty list (i.e., no controls).
    - weights: array-like, shape (n_samples,), optional
        Weights from the matching process (e.g., inverse propensity score weights).
    - model_y: str, optional
        Model to estimate the outcome regression (Y | X, W). Options: 'lasso', 'random_forest'. Default is 'lasso'.
    - model_t: str, optional
        Model to estimate the treatment (T | X, W). Options: 'logistic', 'random_forest'. Default is 'logistic'.
    - model_final: str, optional
        Model to use for final effect estimation. Options: 'lasso', 'random_forest'. Default is 'lasso'.
    - random_state: int, optional
        Seed for random number generator.

    Returns:
    - dml_model: Fitted DML model.
    """

    # Choose the outcome model
    if model_y == 'lasso':
        model_y = LassoCV(cv=5, random_state=random_state)
    elif model_y == 'random_forest':
        model_y = RandomForestRegressor(random_state=random_state)
    else:
        raise ValueError(f"Unknown model_y '{model_y}'. Choose 'lasso' or 'random_forest'.")

    # Choose the treatment model
    if model_t == 'logistic':
        model_t = LogisticRegressionCV(cv=5, random_state=random_state)
    elif model_t == 'random_forest':
        model_t = RandomForestRegressor(random_state=random_state)
    else:
        raise ValueError(f"Unknown model_t '{model_t}'. Choose 'logistic' or 'random_forest'.")

    # Choose the final model
    if model_final == 'lasso':
        model_final = LassoCV(cv=5, random_state=random_state)
    elif model_final == 'random_forest':
        model_final = RandomForestRegressor(random_state=random_state)
    else:
        raise ValueError(f"Unknown model_final '{model_final}'. Choose 'lasso' or 'random_forest'.")

    # If no controls are provided, set to empty list
    if W is None:
        W = np.empty((X.shape[0], 0))

    # Define the DML model with model_final
    dml_model = DML(model_y=model_y, model_t=model_t, model_final=model_final, random_state=random_state)

    # Fit the model with weights
    dml_model.fit(Y, T, X=X)

    return dml_model



excluded_vars=["treatment","total_annual_subsidy","subsidy","subsidy_duration_day","reverse_treatment","distance","weights","subclass","shfd","bvdid"]
#matched_data=pd.read_excel(r"C:\Users\lukas\Desktop\bachelor\data\matched_data.xlsx")
#input_data=matched_data.drop(columns=excluded_vars)

#input_data=filter_input(input_data)

input_data=pd.read_excel(r"C:\Users\lukas\Desktop\bachelor\data\financials_merge_treatment_and_control_categorials_cleaned_imputed_dropped.xlsx")

input_mydf=mydf(input_data)
input_mydf["rechtsform"],factor_map=input_mydf.factorize_series(input_mydf["rechtsform"])
input_mydf["compcat"],factor_map=input_mydf.factorize_series(input_mydf["compcat"],{"SMALL":0,"MEDIUM":1,"LARGE":2,"VERY_LARGE":3})
treatment_data=input_data["treatment"]
shfd=input_data["shfd"]
#weights=input_data["weights"]

def run_and_save():
    bachelor_dml=run_dml_model_with_weights(input_mydf,treatment_data,shfd,W=input_data[["empl","sales"]],model_y="random_forest",model_final="random_forest",model_t="random_forest")
    chdir_data()
    dump(bachelor_dml,"dml_bachelor.jolib")

run_and_save()
chdir_data()
bachelor_dml=load("dml_bachelor.jolib")

treatment_effects=bachelor_dml.effect(input_mydf)

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


def plot_var_treatment_scatter(var,treatment_effects=treatment_effects):
    plt.scatter(input_mydf[var], treatment_effects, alpha=0.5)
    plt.plot()
    plt.show()

startup_analysis()
plot_var_treatment_scatter("empl")

#quantile analysis with empl

def plot_var_treatment_quantile():
    df['Quantile'] = pd.qcut(df['Company_Size'], q=4)  # Dividing into 4 quantiles
    quantile_effects = df.groupby('Quantile')['Treatment_Effect'].mean()
    print(quantile_effects)


#analyze variance 
#shap values
#use mydf bachelor statistics like histograms etc. 
#x should be moderators of the treatment effect, in general or just heterogeneity?


