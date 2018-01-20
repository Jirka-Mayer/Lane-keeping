import numpy as np
import pickle
import sklearn.utils
import sklearn.model_selection
import scipy.misc

import keras.optimizers
import os
import random

# parameters
BATCH_SIZE = 64
EPOCHS = 100

# load model
model = keras.models.load_model("model.h5")

optimizer = "Adam" # original
#optimizer = keras.optimizers.SGD(lr=0.001, momentum=0.0, decay=0.0, nesterov=False)

# compile the model
model.compile(optimizer=optimizer, loss='mean_squared_error')

# batch generator
def trainingDataGenerator():
    items = os.listdir("recording")
    for item in items:
        if not os.path.isfile("recording/" + item):
            items.remove(item)

    random.shuffle(items)

    while True:
        batch = np.random.choice(items, BATCH_SIZE)
        dataX = np.empty((BATCH_SIZE, 80, 160, 3))
        dataY = np.empty((BATCH_SIZE, 1))

        for i in range(BATCH_SIZE):
            item = np.random.choice(items)
            dataX[i] = scipy.misc.imread("recording/" + item) / 255
            dataY[i] = (dataX[i][0, 0, 0] - 0.5) * 2
        
        yield (dataX, dataY)

model.fit_generator(trainingDataGenerator(), steps_per_epoch=BATCH_SIZE, epochs=EPOCHS)

# save model
model.save('model.h5')

# show summary
#model.summary()