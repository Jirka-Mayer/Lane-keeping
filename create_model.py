import numpy as np
import pickle
import sklearn.utils
import sklearn.model_selection

import keras.optimizers
from keras.models import Sequential
from keras.layers import Activation, Dense, Flatten, Dropout
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization

# parameters
pool_size = (2, 2)
input_shape = (80, 160, 3)

#########################
# Neural net definition #
#########################

model = Sequential()

model.add(BatchNormalization(input_shape=input_shape))

model.add(Conv2D(8, (3, 3), padding='valid', strides=(1,1), activation = 'relu', name = 'Conv1'))
model.add(Conv2D(16, (3, 3), padding='valid', strides=(1,1), activation = 'relu', name = 'Conv2'))

model.add(MaxPooling2D(pool_size=pool_size))

model.add(Conv2D(16, (3, 3), padding='valid', strides=(1,1), activation = 'relu', name = 'Conv3'))
model.add(Dropout(0.2))

model.add(Conv2D(32, (3, 3), padding='valid', strides=(1,1), activation = 'relu', name = 'Conv4'))
model.add(Dropout(0.2))

model.add(Conv2D(32, (3, 3), padding='valid', strides=(1,1), activation = 'relu', name = 'Conv5'))
model.add(Dropout(0.2))

model.add(MaxPooling2D(pool_size=pool_size))

model.add(Conv2D(64, (3, 3), padding='valid', strides=(1,1), activation = 'relu', name = 'Conv6'))
model.add(Dropout(0.2))

model.add(Conv2D(64, (3, 3), padding='valid', strides=(1,1), activation = 'relu', name = 'Conv7'))
model.add(Dropout(0.2))

model.add(MaxPooling2D(pool_size=pool_size))

# my custom layers

model.add(Flatten())

model.add(Dense(16*6))
model.add(Dense(1))

model.add(Activation("tanh"))

#############################
# Neural net definition end #
#############################

# save model
model.save('model.h5')