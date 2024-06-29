import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np
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


import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import NearestNeighbors

# Example df_numeric
chdir_sql_requests()
df=pd.read_csv("financialsbvd_ama_imputed.csv")
df_numeric=filter_numeric_columns(df).iloc[:,9:]

df_numeric_without_treatment=df_numeric.drop(columns={"treatment"})
features=list(df_numeric_without_treatment.columns)
df_numeric["bvdid"]=df["bvdid"]
#müssen wir treatment noch droppen?

# Define treatment and control groups
treatment_group = df_numeric[df_numeric['treatment'] == 1]
control_group = df_numeric[df_numeric['treatment'] == 0]

# Calculate propensity scores using a random forest classifier
#features = ['feature1', 'feature2']
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(df_numeric[features], df_numeric['treatment'])
df_numeric['propensity_score'] = rf.predict_proba(df_numeric[features])[:, 1]

# Update treatment and control groups with propensity scores
treatment_group = df_numeric[df_numeric['treatment'] == 1]
control_group = df_numeric[df_numeric['treatment'] == 0]

# Calculate standard deviations of propensity scores
std_treatment = treatment_group['propensity_score'].std()
std_control = control_group['propensity_score'].std()
pooled_std = np.sqrt((std_treatment**2 + std_control**2) / 2)

# Set SMD threshold
smd_threshold = 10

# Initialize and fit the nearest neighbors model on the combined df_numeric
nn = NearestNeighbors(n_neighbors=1)
scores=control_group[['propensity_score']]
nn.fit(scores)

# Create lists to store matched pairs and distances
matched_pairs = []
matched_distances = []

# Find the nearest neighbors for each treatment group
for i, row in treatment_group.iterrows():
    propensity_score = row[['propensity_score']].values.reshape(1, -1)
    propensity_score_df=pd.DataFrame(propensity_score,columns=["propensity_score"])
    distances, indices = nn.kneighbors(propensity_score_df)
    
    # Calculate the standardized mean difference
    distance = distances[0][0]
    smd = distance / pooled_std
    
    # Only accept the match if the SMD is within the threshold
    if smd <= smd_threshold:
        index = indices[0][0]
        control_company_id = control_group.iloc[index]['bvdid'] #habe bvdid rausgelöscht
        
        # Store the match
        matched_pairs.append((row["bvdid"], control_company_id))
        matched_distances.append(smd)
    

# Convert the matched pairs to a df_numericFrame for better readability
matched_df = pd.DataFrame(matched_pairs, columns=['treatment_company_id', 'control_company_id'])
matched_df['smd'] = matched_distances

print(matched_df)
