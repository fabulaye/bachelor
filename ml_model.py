import pandas as pd
from lukasdata.file_manager.change_directory import chdir_data

chdir_data()
subsidized_financial_amadeus=pd.read_csv("subsidized_financial_amadeus.csv")
not_subsidized_financial_amadeus=pd.read_csv("not_subsidized_financial_amadeus.csv")

complete_financial=pd.concat([subsidized_financial_amadeus,not_subsidized_financial_amadeus])

min_values_df=complete_financial.dropna(thresh=40)
min_values_df.to_excel("financials_übersicht.xlsx")

selected_columns=["closdate_year","toas","empl","capi","debt","ifas","tfas","subsidized"]

min_values_df=min_values_df[selected_columns]
min_values_df=min_values_df.dropna()

y_values_train=min_values_df["subsidized"][:len(min_values_df)-100]
y_values_validation=min_values_df["subsidized"][len(min_values_df)-100:]

min_values_df=min_values_df.drop("subsidized",axis=1)
min_values_df_training=min_values_df.iloc[:len(min_values_df)-100,:]

values_validation=min_values_df.iloc[len(min_values_df)-100:,:]

import numpy as np

def create_training_dataset_grouped(grouped_df):
    big_array=[]
    #big_array=np.array(big_array)
    for group_name,group_data in grouped_df:
        group_data=group_data.iloc[:,2:]
        array=np.array(group_data)
        array_list=array.tolist()
        big_array.append(array_list)
    return big_array

def create_training_dataset(df):
    big_array=[]
    for index,row in df.iterrows():
        big_array.append(row)
    big_array=np.array(big_array)
    return big_array


training_data=create_training_dataset(min_values_df_training)
import tensorflow as tf

num_rows, num_columns=training_data.shape

model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, input_shape=(num_columns,)),  # LSTM layer
    tf.keras.layers.Dense(32, activation='relu'),  # Dense layer with ReLU activation
    tf.keras.layers.Dense(1,activation="sigmoid")  # Output layer
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

epochs=200
batch_size=100

history=model.fit(training_data, y_values_train, epochs=epochs, batch_size=batch_size, validation_data=(values_validation, y_values_validation))

loss_in_sample, accuracy_in_sample = model.evaluate(values_validation, y_values_validation)
loss, accuracy = model.evaluate(training_data, y_values_train)





print(loss_in_sample, accuracy_in_sample)
print(loss)
print(accuracy)

import os
def save_model(model,file_name):
    os.chdir("C:/Users/lukas/Desktop/bachelor/models")
    model.save(file_name)


from plot_metric_history import plot_metric_history  
plot_metric_history(history,["accuracy"],"validation")