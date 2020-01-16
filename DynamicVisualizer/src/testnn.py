from patient.patientgroup import PatientGroup
from config import config 
from datatest import generate
import pandas as pd
import numpy as np

import tensorflow as tf 


from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import LSTM
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from keras.layers import Dropout
from keras.layers import Dense, Activation, Flatten, Conv2D, MaxPooling2D

# from neuralnetwork import run

import itertools
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.executing_eagerly()

coordinates = np.random.randint(0, 100, size=(30, 10, 2))
dx_train = tf.data.Dataset.from_tensor_slices(coordinates)

patient_groups = [
    PatientGroup(config.basepath.format(groupid=1)),
    # PatientGroup(config.basepath.format(groupid=4)),
    PatientGroup(config.basepath.format(groupid=2)),
    PatientGroup(config.basepath.format(groupid=3)),
]

# Retreiving the data like we know it (5 exercise * column-count * frame count)
np_combination_train, np_combination_test, np_indicator_train, np_indicator_test = generate(patient_groups)

print(np_combination_train.shape, np_combination_test.shape, np_indicator_train.shape, np_indicator_test.shape)

# train_x = np_combination_train
# test_x = np_combination_test

cnn_train_x = np.reshape(np_combination_train, (np_combination_train.shape[0], np_combination_train.shape[1], np_combination_train.shape[2], 1))
cnn_test_x =  np.reshape(np_combination_test, (np_combination_test.shape[0], np_combination_test.shape[1], np_combination_test.shape[2], 1))

print(cnn_train_x.shape, cnn_test_x.shape)

# train_y = tf.data.Dataset.from_tensor_slices(np_indicator_train)
# test_y = tf.data.Dataset.from_tensor_slices(np_indicator_test)


custom_optimizer_adam = tf.keras.optimizers.Adam()
SCEL = tf.keras.losses.SparseCategoricalCrossentropy() 
CEL = tf.keras.losses.CategoricalCrossentropy()
callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=2)

#hyperparameters 
verbose = 2
epochs = 70
batch_size = 25
hidden_layers_size = 25

#parameters
n_timesteps = 100 # 
n_features = 130 #
n_outputs = 3

def lstm(train_x, train_y, test_x, test_y):
    # define model
    model = Sequential()
    model.add(LSTM(30, activation='relu', input_shape=(n_timesteps, n_features), return_sequences=True))
    # model.add(Dropout(0.2))
    model.add(LSTM(30, activation='relu'))
    # model.add(Dropout(0.2))
    # model.add(Dense(hidden_layers_size, activation='relu'))
    # model.add(Dropout(0.2))
    model.add(Dense(n_outputs, activation='softmax'))

    print(model.summary(90))
                            
    model.compile(optimizer= custom_optimizer_adam , loss=SCEL, metrics= ['accuracy'])

    # fit network
    model.fit(train_x, train_y, epochs=epochs, 
            validation_data=(test_x, test_y),  
            verbose=verbose,  batch_size=batch_size)
            # callbacks=[callback])
    
    return model

def Deco_enc_LSTM(train_x, train_y, test_x, test_y):
    model = Sequential()
    model.add(LSTM(100, activation='relu', input_shape=(n_timesteps, n_features),  return_sequences=True))
    model.add(RepeatVector(n_outputs))
    model.add(LSTM(50, activation='relu', return_sequences=False))
    model.add(TimeDistributed(Dense(hidden_layers_size, activation='relu')))
    model.add(TimeDistributed(Dense(n_outputs, activation='softmax')))

    model.compile(optimizer= custom_optimizer_adam , loss=SCEL, metrics= ['accuracy'])

    # fit network
    model.fit(train_x, train_y, epochs=epochs, 
            validation_data=(test_x, test_y),  
            verbose=verbose,  batch_size=batch_size,
            callbacks=[callback])


def CNN(train_x, train_y, test_x, test_y):
    model = Sequential()
    model.add(Conv2D(64, (3,3), input_shape=(n_timesteps, n_features, 1)))
    model.add(Activation('relu'))

    model.add(MaxPooling2D(pool_size=(3,3)))
    model.add(Conv2D(64, (3,3)))
    model.add(Activation('relu'))

    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Flatten())
    model.add(Dense(64))
    model.add(Dense(n_outputs))

    model.add(Activation('softmax'))

    print(model.summary(90))

    model.compile(loss=SCEL, optimizer=custom_optimizer_adam, metrics=['accuracy'])

    # fit network
    model.fit(train_x, train_y, epochs=epochs, 
            validation_data=(test_x, test_y),  
            verbose=verbose,  batch_size=batch_size,
            callbacks=[callback])

CNN(cnn_train_x, np_indicator_train, cnn_test_x, np_indicator_test)
