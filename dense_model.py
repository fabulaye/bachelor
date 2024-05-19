from datahandler.change_directory import chdir_data
#from machine_learning.keras_input import keras_input
#from machine_learning.ml_model import ml_model
import tensorflow as tf
from sklearn.model_selection import train_test_split
import pandas as pd

chdir_data()

import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

class keras_input():
    def __init__(self,df) -> None:
        self.df=df
        self.grouped_df=self.create_grouped("idnr")
        self.array=None
        self.padded_sequences=None
        self.x_train=None
        self.x_test=None
        self.y_train=None
        self.y_test=None
    def create_grouped(self,group):
        self.grouped_df=self.df.groupby(group)
    def drop_column(self,dropped_columns):
        self.df.drop(columns=dropped_columns)
    def create_y(self,column_name,entry_len):
        series=self.df[column_name]
        outer_list=[]
        for group_name,group_data in self.grouped_df:
            series_data=series[group_name]
            if isinstance(series_data,(np.int64)):
                list=[series_data]*entry_len
            else: 
                list=[series_data.iloc[0]]*entry_len
            outer_list.append(list)
        array=np.array(outer_list)
        self.y=array
    def create_array_from_grouped_df(self):
        big_array=[]
        #big_array=np.array(big_array)
        for group_name,group_data in self.grouped_df:
            array=np.array(group_data) #ist das notwendig?
            array_list=array.tolist()
            big_array.append(array_list)
        self.array=big_array
    def padding(self,max_len):
        self.padded_sequences = tf.keras.preprocessing.sequence.pad_sequences(self.array, maxlen=max_len, padding='post', truncating='post') 
    def train_test_split(self):
        self.x_train,self.x_test,self.y_train,self.y_test=train_test_split(self.padded_sequences,self.y,test_size=0.33)
    def init_input(self,group_name="idnr",entry_len=10,y_column_name="subsidized"):
        self.create_grouped(group_name)
        self.create_array_from_grouped_df()
        self.create_y(y_column_name,entry_len)
        self.padding(entry_len)
        self.train_test_split()

imputed_data=pd.read_csv("rf_imputed.csv")
imputed_data=imputed_data.set_index("idnr")

imputed_input=keras_input(imputed_data)
imputed_input.init_input()

#init_input in die keras input class

x_train_shape=imputed_input.x_train.shape



import os
#from machine_learning.keras_input import keras_input
from matplotlib import pyplot as plt
import tensorflow as tf

class ml_model():
    def __init__(self,model,keras_input) -> None:
        self.model=model
        self.input=keras_input
        self.history=None
        self.validation_history=[]
    def compile(self,lr=0.001):
        self.model.compile(optimizer=tf.keras.optimizers.Adam(lr),metrics=["accuracy"],loss="categorical_crossentropy")
    def fit(self,epochs,batch_size):
        self.history=self.model.fit(self.input.x_train, self.input.y_train, epochs=epochs, batch_size=batch_size, validation_data=(self.input.x_test, self.input.y_test))
    def save(self,file_name):
        os.chdir("C:/Users/lukas/Desktop/bachelor/models")
        self.model.save(file_name)
    def plot_metric(self,metrics_list):
        metrics_values_list=[]
        for metric in metrics_list:
            metrics_values_list.append(self.history.history[metric])
        for index,metric in enumerate(metrics_values_list):
            print(index)
            plt.subplot(1,2,1+index)
            plt.plot(metric,label=metrics_list[index])
            plt.title(metrics_list[index])
        plt.tight_layout()
        plt.show()   
    def validation_curve(self,learning_rates):
        for lr in learning_rates:
            self.compile(lr)
            self.fit(500,200)
            self.validation_history.append(self.history.history['val_accuracy'][-1])
        plt.plot(learning_rates, self.validation_history, marker='o')
        plt.xscale('log')
        plt.xlabel('Learning Rate')
        plt.ylabel('Validation Accuracy')
        plt.title('Validation Curve')
        plt.grid(True)
        plt.show()
        print(self.validation_history)


model = tf.keras.Sequential([
    tf.keras.layers.LSTM(64, input_shape=(x_train_shape[1], x_train_shape[2]), return_sequences=True),
    tf.keras.layers.LSTM(32, return_sequences=True),
    tf.keras.layers.Dense(1, activation='sigmoid')  # Sigmoid activation for binary classification
])

my_model=ml_model(model,imputed_input)
my_model.compile()
my_model.fit(100,200)
#my_model.plot_metric(["accuracy","accuracy"])
my_model.validation_curve([0.001, 0.01, 0.1, 0.5])

