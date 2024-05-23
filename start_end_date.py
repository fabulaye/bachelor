import pandas as pd
from datahandling.change_directory import chdir_data

chdir_data()
bmwi_request=pd.read_csv("bmwi_request.csv")

start=bmwi_request["Laufzeit von"]
end=bmwi_request["Laufzeit bis"]



import matplotlib.pyplot as plt
import pandas as pd

data = pd.date_range(start='1/1/2019', periods=100)
plt.hist(data, bins=30)  # Bins can be adjusted for different intervals
plt.xlabel('Date')
plt.ylabel('Frequency')
plt.show()

print(start)