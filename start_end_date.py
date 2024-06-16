import pandas as pd
from datahandling.change_directory import chdir_data,chdir_fig

chdir_data()
bmwi_request=pd.read_csv("bmwi_request.csv")

start=bmwi_request["Laufzeit von"].to_list()
end=bmwi_request["Laufzeit bis"].to_list()

import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame(end, columns=['date'])

# Convert the 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')

# Plotting the histogram
plt.figure(figsize=(10, 6))
plt.hist(df['date'], bins=10, edgecolor='black')

# Adding labels and title
plt.xlabel('Date')
plt.ylabel('Frequency')
plt.title('End Dates')
chdir_fig()
plt.savefig("end_data_hist.jpg")
# Show plot
plt.show()


print(start)