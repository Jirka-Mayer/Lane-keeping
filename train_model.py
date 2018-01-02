import numpy as np
import pickle
import sklearn.utils
import sklearn.model_selection

from keras.models import Sequential
from keras.layers import Activation, Dense, Flatten, Dropout
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization
#from keras.preprocessing.image import ImageDataGenerator
#from keras import regularizers

# load training data
training_X = pickle.load(open("training-data-4-input.p", "rb"))
training_Y = pickle.load(open("training-data-4-output.p", "rb"))

# shuffle data
training_X, training_Y = sklearn.utils.shuffle(training_X, training_Y)

# split into training and testing parts
training_X, validation_X, training_Y, validation_Y = sklearn.model_selection.train_test_split(
    training_X, training_Y, test_size=0.1
)

# parameters
batch_size = 128
epochs = 50
pool_size = (2, 2)
input_shape = training_X.shape[1:]

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

# compile the model
model.compile(optimizer='Adam', loss='mean_squared_error')

# train the model
model.fit(
    x=training_X,
    y=training_Y,
    batch_size=batch_size,
    epochs=epochs,
    verbose=1,
    validation_data=(validation_X, validation_Y)
)

# freeze layers
model.trainable = False
model.compile(optimizer='Adam', loss='mean_squared_error')

# save model
model.save('model.h5')

# show summary
model.summary()