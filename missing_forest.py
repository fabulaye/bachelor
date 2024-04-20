import pandas as pd
from lukasdata.change_directory import chdir_data
chdir_data()
from lukasdata.get_number_columns import filter_numeric_columns
subsidized_financial_amadeus=pd.read_csv("subsidized_financial_amadeus.csv")
not_subsidized_financial_amadeus=pd.read_csv("not_subsidized_financial_amadeus.csv")
from lukasdata.count_nans import count_nan

complete_financial=pd.concat([subsidized_financial_amadeus,not_subsidized_financial_amadeus])
complete_financial_numerical=filter_numeric_columns(complete_financial)

complete_financial_numerical_compcat=complete_financial_numerical
complete_financial_numerical_compcat["compcat"]=complete_financial["compcat"]
print(complete_financial_numerical_compcat["compcat"])

def grouped_imputation(df,groupby_label):
    df_grouped=df.groupby(groupby_label)
    new_df=pd.DataFrame()
    for group_name,group_df in df_grouped:
        group_df.drop(columns=groupby_label,inplace=True)
        fillna_dict={}
        for column_name in group_df:
            fillna_dict[column_name]=group_df[column_name].mean()
        group_df=group_df.fillna(fillna_dict)
        print(group_df)
        new_df=pd.concat([new_df,group_df])
    new_df=new_df.fillna(new_df.mean)
    new_df=new_df.dropna(axis=1)
    return new_df

test_df=grouped_imputation(complete_financial_numerical_compcat,"compcat")
test_df.to_csv("imputation_test.csv")

def get_miss_values_hierachie(df):
    missing_values_dict=count_nan(df)
    sorted_by_value=dict(sorted(missing_values_dict.items(),key=lambda x: x[1]))
    sorted_list_of_column_names=[]
    for number,entry in enumerate(sorted_by_value):
        sorted_list_of_column_names.append(entry)
    return sorted_list_of_column_names

def my_miss_forest(df):
    missing_values_column_vector=get_miss_values_hierachie(complete_financial_numerical)

    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score

    # Handle missing values (e.g., using mean imputation)
    complete_financial.fillna(complete_financial.mean(), inplace=True)

    y = complete_financial["subsidized"]
    X = complete_financial.drop(columns=["subsidized"])

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the Random Forest Classifier
    rf_classifier = RandomForestClassifier()
    rf_classifier.fit(X_train, y_train)

    # Make predictions
    y_pred = rf_classifier.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)

