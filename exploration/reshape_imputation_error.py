import pandas as pd
errors=pd.read_excel(r"C:\Users\lukas\Desktop\bachelor\data\miss_forest_errors.xlsx")
errors_pivoted=errors.pivot(index="variable",columns="iteration",values="NMSE")
errors_pivoted.drop(["STATUS","closdate_year","age","age.1"])
errors_pivoted = errors_pivoted.sort_values(by=3, ascending=False)

latex_code = errors_pivoted.iloc[:,:4].to_latex(index=True, float_format="%.2f", caption="NRMSE by Variable and Iteration", label="tab:nrmse")
print(latex_code)