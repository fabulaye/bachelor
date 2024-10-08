from processing.my_df import mydf
import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant
from processing.format_string import format_df

matched_data=pd.read_excel(r"C:\Users\lukas\Desktop\bachelor\data\matched_data.xlsx")


def filter_input(df):
    column_sums=df.isna().sum()==0
    column_sums=column_sums.to_list()
    df=df.loc[:,column_sums]
    df=format_df(df)
    df.drop(columns=["...1"],inplace=True)
    return df


#matched_data=format_df(matched_data)
matched_data=mydf(matched_data)
matched_data.build_statistics("matched")
matched_data_numeric=matched_data.to_numeric()
#matched_data_numeric=format_df(matched_data_numeric)

def vif(df):
    X = df
    # Compute VIF for each feature
    vif = pd.DataFrame()
    vif['Variable'] = X.columns
    vif['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    return vif

vif_df=vif(matched_data_numeric)
print(vif_df)