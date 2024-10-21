from datahandling.change_directory import chdir_data
import pandas as pd
from processing.my_df import mydf
from matplotlib import pyplot as plt
import seaborn as sns

chdir_data()
imputed_df=pd.read_excel("matched_data.xlsx")
#imputed_df=mydf(imputed_df)
#imputed_df_numeric=imputed_df.to_numeric()
#imputed_df.build_statistics("treatment_and_control_imputed")

#print(bmwki_df.statistics)
#imputed_df.statistics.create_kde_figs()
#imputed_df.statistics.create_hist_figs()


#cor_matrix=imputed_df_numeric.corr()
#treatment_cor=cor_matrix["treatment"]
#total_annual_subsidy_cor=cor_matrix["total_annual_subsidy"]
#shfd_cor=cor_matrix["shfd"]
#print(total_annual_subsidy_cor)


def create_violin_plot(data,y_var):
    plt.figure(figsize=(10, 6))
    #sns.violinplot(series)
    sns.violinplot(data=data, x="treatment", y=y_var)
    plt.show()

create_violin_plot(imputed_df,"shfd")

#colinearity

