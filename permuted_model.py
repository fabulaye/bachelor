from lukasdata.drop_columns_permutation_score import drop_columns_permutation_score


permutation_scores=[-1.22124533e-15,  9.37500000e-02,  1.11607143e-01, -4.46428571e-03,
 -1.22124533e-15, -1.22124533e-15, -1.22124533e-15, -4.46428571e-03,
  5.80357143e-02,  1.02678571e-01,  3.57142857e-02,  1.33928571e-02,
  6.25000000e-02,  4.01785714e-02,  1.02678571e-01,  5.80357143e-02,
  8.48214286e-02,  2.27678571e-01,  1.42857143e-01,  4.91071429e-02,
  9.82142857e-02,  1.38392857e-01,  1.56250000e-01,  5.35714286e-02,
  7.58928571e-02,  4.46428571e-03,  2.32142857e-01,  1.11607143e-01,
  1.42857143e-01, -1.22124533e-15,  2.23214286e-01,  8.92857143e-03,
  8.03571429e-02, -4.46428571e-03,  4.46428571e-03,  1.02678571e-01,
  6.69642857e-02,  9.82142857e-02,  1.33928571e-02,  8.92857143e-03,
  8.48214286e-02,  1.42857143e-01,  2.72321429e-01,  8.92857143e-03,
 -1.22124533e-15,  6.25000000e-02,  4.01785714e-02,  4.91071429e-02,
  7.58928571e-02,  1.96428571e-01,  3.12500000e-02,  4.91071429e-02,
  2.67857143e-02,  1.78571429e-01,  1.33928571e-01,  9.37500000e-02,
  2.58928571e-01,  6.69642857e-02,  1.91964286e-01,  1.02678571e-01,
  2.67857143e-02, -1.22124533e-15,  1.78571429e-02,  1.25000000e-01,
 -1.22124533e-15,  5.80357143e-02,  1.51785714e-01,  1.96428571e-01,
  8.92857143e-03,  1.11607143e-01,  1.65178571e-01, -4.46428571e-03,
  5.35714286e-02,  1.83035714e-01,  1.38392857e-01,  8.92857143e-03,
  1.96428571e-01,  2.41071429e-01]


#print(type(imputed_data_idnr_index))
#soll das nicht ein df sein? kann der input auch ein df sein?


from lukasdata.change_directory import chdir_data
import tensorflow as tf
import pandas as pd
from lukasdata.keras_input import keras_input
chdir_data()

imputed_data=pd.read_csv("rf_imputed.csv")
imputed_data=imputed_data.set_index("idnr")

imputed_input=keras_input(imputed_data)
imputed_input.create_grouped("idnr")
imputed_input.create_array_from_grouped_df()
imputed_input.create_y("subsidized",10)
imputed_input.padding(10)
imputed_input.padded_sequences=drop_columns_permutation_score(imputed_input.padded_sequences,permutation_scores,0.1)
imputed_input.train_test_split()

x_train_shape=imputed_input.x_train.shape


model = tf.keras.Sequential([
    tf.keras.layers.LSTM(64, input_shape=(x_train_shape[1], x_train_shape[2]), return_sequences=True),
    tf.keras.layers.LSTM(32, return_sequences=True),
    tf.keras.layers.Dense(1, activation='sigmoid')  # Sigmoid activation for binary classification
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
#model.summary()

epochs=500
batch_size=1000

history=model.fit(imputed_input.x_train, imputed_input.y_train, epochs=epochs, batch_size=batch_size, validation_data=(imputed_input.x_test, imputed_input.y_test))

loss_in_sample, accuracy_in_sample = model.evaluate(imputed_input.x_test, imputed_input.y_test)
loss, accuracy = model.evaluate(imputed_input.x_train, imputed_input.y_train)

import os
def save_model(model,file_name):
    os.chdir("C:/Users/lukas/Desktop/bachelor/models")
    model.save(file_name)

from lukasdata.plot_metric_history import plot_metric_history  
plot_metric_history(history,["accuracy","val_accuracy"])
#accuracy für validation und training


save_model(model,"dense_gaming_permuted.keras")