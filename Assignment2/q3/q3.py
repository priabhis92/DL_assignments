from __future__ import print_function
import numpy as np

import keras
from keras.models import Model,Sequential
from keras.layers import Lambda, Dense, Dropout, Flatten, Conv2D, MaxPool2D, BatchNormalization, GaussianNoise, Input, Dropout, concatenate
from keras import optimizers
from keras.preprocessing.image import img_to_array
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import keras.backend as K
from keras.backend import tf as ktf


weight_dir = "../q2/weight/"

def inception_block(x, filters):
#     last = x

    net1 = Conv2D(filters = filters, kernel_size=(1,1), padding='Same', activation = 'relu')(x)

    net2 = Conv2D(filters = filters, kernel_size=(1,1), padding='Same', activation = 'relu')(x)
    net2 = Conv2D(filters = filters, kernel_size=(3,3), padding='Same', activation = 'relu')(net2)

    net3 = Conv2D(filters = filters, kernel_size=(1,1), padding='Same', activation = 'relu')(x)
    net3 = Conv2D(filters = filters, kernel_size=(3,3), padding='Same', activation = 'relu')(net3)
    net3 = Conv2D(filters = filters, kernel_size=(3,3), padding='Same', activation = 'relu')(net3)

    output = concatenate([net1, net2, net3], axis=3)
    return output

input_tensor = Input(shape=(28, 28, 3))

x = Conv2D(filters = 32, kernel_size=(3,3), padding='Same', activation = 'relu')(input_tensor)
x = Conv2D(filters = 32, kernel_size=(3,3), padding='Same', activation = 'relu')(x)
x = BatchNormalization()(x)
x = MaxPool2D(pool_size=(5, 5), strides=(2,2))(x)

x = inception_block(x,32)
x = MaxPool2D(pool_size=(3, 3), strides=(1,1),padding='Same')(x)
x = Flatten()(x)

length = Dense(128, activation = 'sigmoid')(x)
length = Dropout(0.25)(length)
length = Dense(1, activation = 'sigmoid',name = 'length')(length)

width = Dense(1, activation = 'sigmoid',name = 'width')(x)

color = Dense(1, activation = 'sigmoid',name = 'color')(x)

angle = Dense(256, activation = 'softmax',name = 'angle')(x)
angle = Dropout(0.5)(x)
angle = Dense(12, activation = 'softmax',name = 'angle')(angle)

model = Model(input_tensor,[length, width, color, angle] )
model.summary()



loss = ['binary_crossentropy', 'binary_crossentropy', 'binary_crossentropy', 'sparse_categorical_crossentropy']
loss_weights = [0.1, 0.1, 0.1, 2.0]
model.compile(optimizer='adam',
              loss=loss,
              loss_weights = loss_weights,
              metrics=['accuracy'])

# history = model.fit(x_train, [y_train_length, y_train_width, y_train_color, y_train_angle], epochs=epochs, batch_size=batch_size, shuffle=True,verbose=1)
model.load_weights(weight_dir + "line_2_final.h5")