from sklearn.ensemble import RandomForestClassifier
from datahandling.change_directory import chdir_sql_requests
import pandas as pd
from manipulation.filter_numeric_columns import filter_numeric_columns
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.tree import export_graphviz


from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

chdir_sql_requests()
data=pd.read_csv("financialsbvd_ama_imputed.csv")
data=filter_numeric_columns(data)

# Step 3: Split the data into training and testing sets
X = data.drop(columns=['solr'])
y = data['solr']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Train the Random Forest model
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Step 5: Evaluate the model's performance
y_pred = rf.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

# Step 6: Analyze treatment effects
X_test_treated = X_test.copy()
X_test_treated['treatment'] = 1
y_pred_treated = rf.predict(X_test_treated)

X_test_untreated = X_test.copy()
X_test_untreated['treatment'] = 0
y_pred_untreated = rf.predict(X_test_untreated)

treatment_effect = y_pred_treated - y_pred_untreated
X_test['treatment_effect'] = treatment_effect

# Display the first few rows of the test set with the treatment effect
print(X_test.head())

# Save the test set with treatment effects to a CSV file for further analysis
X_test.to_csv('test_set_with_treatment_effects.csv', index=False)

# Step 7: Visualize some trees from the Random Forest model using plot_tree
def visualize_tree(tree, feature_names, tree_index):
    plt.figure(figsize=(20,10))
    plot_tree(tree, feature_names=feature_names, filled=True, rounded=True,)
    plt.title(f'Tree {tree_index}')
    plt.savefig(f'random_forest_tree_{tree_index}.png')
    plt.show()

# Extract individual trees
#trees = rf.estimators_

# Visualize the first 3 trees
#for i in range(3):
#    visualize_tree(trees[i], X_train.columns, i)

#print("Tree visualizations saved as PNG files.")