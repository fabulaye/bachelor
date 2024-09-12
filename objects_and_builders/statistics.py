import numpy as np
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity
import pandas as pd
from sklearn.model_selection import GridSearchCV
import seaborn as sns
import os 
from matplotlib import pyplot as plt
import pandas as pd
from datahandling.change_directory import chdir_sql_requests

#design als attribute von einem df
class statistics():
    def __init__(self) -> None:
        self.df=None
        self.ndarray=df.to_numpy()
        self.mean=None
        self.median=None
        self.std=None
        self.nan_percentages=None
        self.numeric_df=None
        
    def build_nan_percentages(self):
        nan_df=self.df.isna()
        nan_dict={}
        df_len=len(df)
        sums=nan_df.sum(axis=0)
        percentages=sums.apply(lambda x: x/df_len)
        return percentages
    def create_hist_figs(self):
        os.chdir(r"C:\Users\Lukas\Desktop\bachelor\data\figures\hist")
        for col in self.numeric_df:
            values=self.numeric_df[col]
            lower_bound=np.quantile(values,0)
            upper_bound=np.quantile(values,0.8)
            plt.plot(label='Hist', color='blue')
            #range as a quantile maybe
            plt.hist(values,range=(lower_bound,upper_bound))
            plt.title(f'{col}')
            plt.show()
            plt.savefig(f"kde_{col}.png")
            plt.close()
            
    def create_kde_figs(self):
        os.chdir(r"C:\Users\Lukas\Desktop\bachelor\data\figures\kde")
        column_names=self.numeric_df.columns
        array=self.numeric_df.to_numpy()
        for i in range(len(self.df)):
            data=array[:,[i]]
            median = np.median(data)
            std = np.std(data)

            # Define the range dynamically
            range_min = median - std
            range_max = median + std

# Create a range of values
            x_d = np.linspace(range_min, range_max, 5000)[:, np.newaxis]
            bandwidths = np.linspace(0.1, 0.5, 30)

# Use GridSearchCV to find the best bandwidth
            grid = GridSearchCV(KernelDensity(kernel='gaussian'), {'bandwidth': bandwidths}, cv=5)
            grid.fit(data)
            
            # Best bandwidth
            best_bandwidth = grid.best_params_['bandwidth']
            kde = KernelDensity(kernel='gaussian', bandwidth=best_bandwidth).fit(array[:,[i]])
            #x = np.linspace(min(self.ndarray[:,i]), max(self.ndarray[:,i]), 1000)
            #log_dens = kde.score_samples(x[:, None])

# Compute the log density
            log_dens = kde.score_samples(x_d)

            # Plot the results
            #plt.figure(figsize=(8, 6))
            
            plt.plot(x_d[:, 0], np.exp(log_dens), label='KDE', color='blue')
            plt.hist(data, bins=30, density=True, alpha=0.5, color='gray', label='Histogram')
            plt.legend()
            plt.title(f'Kernel Density Estimation {column_names[i]}')
            plt.savefig(f"kde_{column_names[i]}.png")

    def corr_heatmap(self):
        columns = [f'{self.df.columns[i]}' for i in range(self.ndarray.shape[1])]
        print(self.ndarray.shape)
        df = pd.DataFrame(self.ndarray, columns=columns)
        # Compute correlation matrix
        corr_matrix = df.corr()
        
        # Create a heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', linewidths=0.5)
        plt.title('Correlation Heatmap')
        plt.show()
        

class statistics_builder():
    def __init__(self,df:mydf) -> None:
        self.df=df
        self.statistics=statistics()
    def build_statistics(self):
        self.statistics.df=self.df
        descrpition=self.statistics.df.describe()
        self.statistics.description=descrpition
        self.statistics.mean=descrpition.loc["mean"]
        self.statistics.min=descrpition.loc["min"]
        self.statistics.max=descrpition.loc["max"]
        self.statistics.std=descrpition.loc["std"]
        self.statistics.nan_percentages=self.statistics.build_nan_percentages()
        self.statistics.numeric_df=self.statistics.df.to_numeric()
        return self #or self.statistics

df=pd.read_excel(r"C:\Users\Lukas\Desktop\bachelor\data\financials_resolved.xlsx")
df=mydf(df).knn_impute()

stats=statistics_builder(df).build_statistics().statistics
stats.create_hist_figs()



#grouped statistics
#groupby compcat und dann describe oder ausgewählte statistikn printen
#kann auch multiple columns nehmen
#value counts bei kategorialen daten
#kann ich irgendwie factor forcen?
#nan ppercentags im description df?
#factorization



