import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
from datahandling.change_directory import chdir_sql_requests
from manipulation.filter_numeric_columns import filter_numeric_columns
from sklearn.neighbors import NearestNeighbors
from matplotlib import pyplot as plt
# Load your dataset
# Example: df = pd.read_csv('your_dataset.csv')

# Example data



def calculate_propensity_scores():
    chdir_sql_requests()
    df=pd.read_csv("financialsbvd_ama_imputed.csv")
    X=filter_numeric_columns(df)
# Define the features (X) and the target (y)
    y = X['treatment']
    X = X.drop('treatment', axis=1)

    covariates=X.columns

    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

    # Initialize the Random Forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Fit the model to the training data
    model.fit(X_train, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model
    #print("Test set classification report:")
    #print(classification_report(y_test, y_pred))
    #print("Accuracy:", accuracy_score(y_test, y_pred))

    # Predict the propensity scores (probabilities of being in the treatment group)
    propensity_scores = model.predict_proba(X)[:, 1]
    df['propensity_score'] = propensity_scores
    return df,covariates

def average_propensity_score(df):
    grouped_df=df.groupby("bvdid")
    average_scores=[]
    for group_name,group_df in grouped_df:
        group_mean=group_df["propensity_score"].mean()
        for _ in range(len(group_df)):
            average_scores.append(group_mean)
    df["average_propensity_scores"]=average_scores
    return df

df,covariates=calculate_propensity_scores()
df=average_propensity_score(df)

def matching(covariates):
    treatment_group = df[df['treatment'] == 1].copy()
    control_group = df[df['treatment'] == 0].copy()

    # Fit the nearest neighbors model on the control group
    nn = NearestNeighbors(n_neighbors=1) #den hier ich kann ich anpassen
    nn.fit(control_group[['propensity_score']])

    # Find the nearest control for each treatment unit
    distances, indices = nn.kneighbors(treatment_group[['propensity_score']])
    print(indices)

    # Create matched pairs
    matched_pairs = treatment_group.copy()
    matched_pairs['matched_control_id'] = control_group.iloc[indices.flatten()]['bvdid'].values
    matched_pairs['matched_control_propensity_score'] = control_group.iloc[indices.flatten()]['propensity_score'].values

    # Check the matched pairs
    print(matched_pairs)

    # For further analysis, you might want to merge the matched pairs back with the original control group data
    matched_control_group = control_group.iloc[indices.flatten()].copy()
    matched_control_group['treatment_id'] = treatment_group["bvdid"].values

    # Initialize results DataFrame
    results = pd.DataFrame(columns=['covariate', 'average_treatment_effect'])

    # Loop through each covariate and calculate treatment effect
    for covariate in covariates:
        matched_control_group[f'treatment_{covariate}'] = treatment_group[covariate].values
        matched_control_group[f'treatment_effect_{covariate}'] = matched_control_group[f'treatment_{covariate}'] - matched_control_group[covariate]
        
        avg_treatment_effect = matched_control_group[f'treatment_effect_{covariate}'].mean()
        results.loc[len(results)] = {
            'covariate': covariate,
            'average_treatment_effect': avg_treatment_effect
        }

    return results

#Propensity Score Distribution: Ensure that the propensity score distributions of the treatment and control groups overlap sufficiently (common support).

treatment_effects=matching(covariates)
print(treatment_effects)



#covariate balance



def compute_smd(df, treatment_col, covariate_cols):
    means_treated = df[df[treatment_col] == 1][covariate_cols].mean()
    means_control = df[df[treatment_col] == 0][covariate_cols].mean()
    stds = df[covariate_cols].std()
    smd = (means_treated - means_control) / stds
    return smd


treatment_group = df[df['treatment'] == 1].copy()
control_group = df[df['treatment'] == 0].copy()

nn = NearestNeighbors(n_neighbors=1) #den hier ich kann ich anpassen
nn.fit(control_group[['propensity_score']])
distances, indices = nn.kneighbors(treatment_group[['propensity_score']])

matched_control_group = control_group.iloc[indices.flatten()].copy()

covariate_cols=X.columns

smd_before = compute_smd(df, 'treatment', covariate_cols)
smd_after = compute_smd(pd.concat([treatment_group, matched_control_group]), 'treatment', covariate_cols)

print("Standardized Mean Differences Before Matching:")
print(smd_before)
print("Standardized Mean Differences After Matching:")
print(smd_after)

# Plotting covariate balance before and after matching
smd_df = pd.DataFrame({
    'covariate': covariate_cols,
    'SMD_before': smd_before,
    'SMD_after': smd_after
})

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(smd_df['covariate'], smd_df['SMD_before'], marker='o', linestyle='-', label='Before Matching')
ax.plot(smd_df['covariate'], smd_df['SMD_after'], marker='o', linestyle='-', label='After Matching')
ax.axhline(0.1, color='red', linestyle='--', label='Threshold')
ax.axhline(-0.1, color='red', linestyle='--')
ax.set_ylabel('Standardized Mean Difference')
ax.set_title('Covariate Balance Before and After Matching')
ax.legend()
plt.show()
