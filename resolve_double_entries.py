from datahandling.change_directory import chdir_data
import pandas as pd

chdir_data()
financials=pd.read_excel("financials_merge_test.xlsx")

duplicates=financials.duplicated(subset=["bvdid","closdate_year"],keep=False)
#duplicates_consolidation=financials.duplicated(subset=["bvdid","closdate_year","consolidation code"])


#vielleicht ffill and bfill und dann schauen ob same

problem_columns=["exchrate",]

financial_duplicates=financials[duplicates]
financial_unique=financials[~duplicates]
financial_duplicates.to_excel("duplicates_debug.xlsx")
financial_duplicates.drop(columns=["exchrate"],inplace=True)


def resolve_conflict(df):
    identical_groups=[]
    for index,group in df.groupby(["bvdid","closdate_year"]):
        if len(group)==2:
            group_filled=group.ffill(axis=0,limit=1).bfill(axis=0,limit=1)
            group_filled.fillna("nan_placeholder",inplace=True)
            #if len ==2 ?
            if group_filled.iloc[0,:].equals(group_filled.iloc[1,:]):
                identical_groups.append(group_filled.iloc[0,:])
            else: 
                diff_cols=[]
                for column in group_filled.columns:
                    duplicated_bool=group_filled[column].duplicated(keep=False)
                    if any(duplicated_bool)==False:
                        diff_cols.append(column)
                    else:
                        pass
                problems=group_filled[diff_cols]
                problems.replace(0,None,inplace=True)
                problems.ffill(axis=0,limit=1,inplace=True)
                problems.bfill(axis=0,limit=1,inplace=True)
                if problems.iloc[0,:].equals(problems.iloc[1,:]):
                    group_filled[diff_cols]=problems[diff_cols]
                    identical_groups.append(group_filled.iloc[0,:])
                else:
                    pass #hier als placeholder einfach eine row selecten und dann irgendwie flaggen

                #replace 0 with non 0 values,
                #indexes speichern. 
        else:
            group.fillna("nan_placeholder",inplace=True)
            unconsolidated_codes=["U1","U2","nan_placeholder"]
            unconsolidated=group[group["consolidation code"].isin(unconsolidated_codes)]
            unconsolidated.replace("nan_placeholder",None)
            unconsolidated.ffill(axis=0,limit=1,inplace=True)
            unconsolidated.bfill(axis=0,limit=1,inplace=True)
            identical_groups.append(unconsolidated.iloc[0,:])

    df=pd.concat(identical_groups,axis=1).T
    return df


#replace nan placeholder
resolved_rows=resolve_conflict(financial_duplicates)
financials_resolved=pd.concat([financial_unique,resolved_rows])
financials_resolved.replace("nan_placeholder",None,inplace=True)
financials_resolved.to_excel("financials_resolved.xlsx")
print(financials_resolved.index)

#wir verlieren ein column?

