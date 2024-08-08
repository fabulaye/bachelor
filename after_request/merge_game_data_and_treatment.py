from datahandling.change_directory import chdir_data
import pandas as pd

chdir_data()

game_data=pd.read_csv("games_data_mobygames_steam_merged.csv",index_col=False)
treatment_data=pd.read_csv("sql_data/treatmentfinancialsbvd_ama.csv",index_col=False)

merged_df=pd.merge(treatment_data,game_data,how="left",left_on=["closdate_year","bvdid"],right_on=["year","bvdid"])

columns=["review_percentage","review_count","score","rank","critics","price"]

def float_columns(df,columns):
    def try_int(value):
        try:
            value=float(value)
        except ValueError:
            None
        return value
        
    for column in columns:
        df[column]=df[column].apply(lambda x: try_int(x))
    return df

def delete_euro(value):
    try: 
        value=value.rstrip("€")
        value=value.replace(",",".")
        value=value.replace("Free To Play","0")
        value=value.replace("Free","0")
    except AttributeError:
        print(value)
    return value

merged_df["price"]=merged_df["price"].apply(lambda x: delete_euro(x))
merged_df=float_columns(merged_df,columns)

def add_average_cols(df:pd.DataFrame):

    mean_df=df.groupby(["bvdid","closdate_year"]).agg({"review_percentage":"mean",
          "review_count":"mean",
          "score":"mean",
          "rank":"mean",
          "critics":"mean",
          "price":"mean"})
    
    mean_df.rename(columns={"review_percentage":"review_percentage_mean",
          "review_count":"review_count_mean",
          "score":"score_mean",
          "rank":"rank_mean",
          "critics":"critics_mean",
          "price":"price_mean"},inplace=True)
    
    sum_df=df.groupby(["bvdid","closdate_year"]).agg({"review_count":"sum",})
    
    sum_df.rename(columns={"review_count":"review_count_sum"},inplace=True)
    sum_df["review_count_sum"]=sum_df["review_count_sum"].replace(0,None)
    new_df=pd.merge(df,mean_df,how="left",on=["bvdid","closdate_year"])
    new_df=pd.merge(new_df,sum_df,how="left",on=["bvdid","closdate_year"])
    return new_df

merged_df=add_average_cols(merged_df)
merged_df.drop_duplicates(["bvdid","closdate_year"],inplace=True)
 
def custom_fill(series:pd.Series):
    series.ffill(inplace=True)


def forward_fill_columns(df,columns):
    for column in columns:
        df[column] = df.groupby('bvdid')[column].ffill()
        #.apply(custom_fill)
        #df[column] = df[column].fillna(method='ffill').replace(0, method='ffill')
    return df

new_columns=["review_percentage_mean","review_count_mean","score_mean","rank_mean","critics_mean","price_mean","review_count_sum"]

merged_df=forward_fill_columns(merged_df,new_columns)


merged_df.to_excel("treatmentfinancialsbvd_ama.xlsx")


#def add_sum_cols():

#def drop_multiple_rows():

