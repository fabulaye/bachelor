import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors
import statsmodels.api as sm
from datahandling.change_directory import chdir_data

chdir_data()
financials=pd.read_csv("financialsbvd_ama_imputed.csv")

import pandas as pd
import statsmodels.api as sm
from sklearn.neighbors import NearestNeighbors

def drop_uninformative(df:pd.DataFrame):
    df=df.copy()
    drop_names=["idnr","closdate","closdate_year","months","treatment","cuas"]
    for column_name in drop_names:
        try:
            df.drop(columns=column_name,inplace=True)
        except KeyError:
            print(f"{column_name} not in indexes")
    return df



# Load financials
# Define treatment, covariates, and outcome
treatment = 'treatment'
covariates = drop_uninformative(financials)

outcome = 'cuas'

# Estimate propensity scores
model = sm.Logit(financials[treatment], covariates)
result = model.fit()
financials['propensity_score'] = result.predict(covariates)

# Split financials into treated and control groups
treated = financials[financials[treatment] == 1]
control = financials[financials[treatment] == 0]

# Match on propensity scores
nn = NearestNeighbors(n_neighbors=1)
nn.fit(control[['propensity_score']])
distances, indices = nn.kneighbors(treated[['propensity_score']])
matched_control_indices = indices.flatten()
matched_controls = control.iloc[matched_control_indices]
matched_financials = pd.concat([treated, matched_controls])

# Check balance
for covariate in covariates:
    print(f"{covariate} balance:")
    print(matched_financials.groupby(treatment)[covariate].mean())

# Estimate treatment effect
treatment_effect = matched_financials.groupby(treatment)[outcome].mean().diff().iloc[-1]
print(f"Estimated Treatment Effect: {treatment_effect}")


