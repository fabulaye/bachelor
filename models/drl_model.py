import numpy as np
import pandas as pd
from econml.dr import DRLearner
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from datahandling.change_directory import chdir_sql_requests
chdir_sql_requests()
data=pd.read_csv("treatmentfinancialsbvd_ama.csv")
from sklearn.model_selection import train_test_split, StratifiedKFold

# Separate the outcome, treatment, and covariates
Y = data['solr']
T = data["treatment"]
data.drop(columns=["solr","annual_subsidy","annual_subsidy","treatment_weight","summed_annual_subsidy","Fördersumme in EUR","bvdid"],inplace=True)
X = data  # Add more covariates as needed

# Split data into training and testing sets
#X_train, X_test, Y_train, Y_test, T_train, T_test = train_test_split(X, Y, T, test_size=0.2, random_state=123)

# Define the models for the outcome and treatment
model_y = RandomForestRegressor()
model_t = RandomForestClassifier()

stratified_split = StratifiedKFold(n_splits=5, shuffle=True, random_state=123)

# Instantiate the DR Learner
dr_learner = DRLearner(model_regression=model_y, model_propensity=model_t,cv=stratified_split)

# Fit the model
dr_learner.fit(Y, T, X=X)

# Estimate the treatment effect on the test set
treatment_effects = dr_learner.effect(X_test)

# Summarize the average treatment effect
ate = np.mean(treatment_effects)
print(f'Average Treatment Effect (ATE): {ate}')

# Optionally, you can analyze the treatment effect heterogeneity
# For example, plotting the treatment effects against a covariate
import matplotlib.pyplot as plt

plt.scatter(X_test['X1'], treatment_effects)
plt.xlabel('X1')
plt.ylabel('Estimated Treatment Effect')
plt.title('Estimated Treatment Effect vs. X1')
plt.show()

# Save the results to a CSV file if needed
results = pd.DataFrame({
    'X1': X_test['X1'],
    'X2': X_test['X2'],
    'Estimated_Treatment_Effect': treatment_effects
})


import os
os.chdir("C:/Users/lukas/Desktop/bachelor/data/treatment_effects")
results.to_excel('dlr_treatment_effects.xlsx', index=False)
