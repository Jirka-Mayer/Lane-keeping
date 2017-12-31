import pickle
import numpy as np
import cv2
import os
import scipy.misc
import matplotlib.pyplot as plt

RECORDING_NAME = "recording-1"
TRAINING_DATA_NAME = "training-data-1"

TRAINING_WIDTH = 160
TRAINING_HEIGHT = 80

# this value will become 1.0 after normalization
STEERING_NORMALIZATION = 0.1
IMAGE_NORMALIZATION = 255

# method that does the conversion
def prepareFrame(training_X, training_Y, framePath, steering):
    frame = cv2.imread(framePath)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.array(frame)
    frame = scipy.misc.imresize(frame, (TRAINING_HEIGHT, TRAINING_WIDTH, 3))

    training_X.append(frame / IMAGE_NORMALIZATION)
    training_Y.append(steering / STEERING_NORMALIZATION)


# load recording
steeringData = pickle.load(open(RECORDING_NAME + "/_steeringData.p", "rb"))

# prepare training data variables
training_X = []
training_Y = []

# go over all frames and prepare them
i = 0
for item in steeringData:
    framePath = RECORDING_NAME + "/frame-" + str(item[0]) + ".png"
    
    # check frame existence
    if not os.path.isfile(framePath):
        continue

    # convert
    prepareFrame(training_X, training_Y, framePath, item[1])

    i += 1

    if i % 100 == 0:
        print("Frame: " + str(i))

# convert training vars to np array
training_X = np.array(training_X)
training_Y = np.array(training_Y)

# save training data
pickle.dump(training_X, open(TRAINING_DATA_NAME + "-input.p", "wb"))
pickle.dump(training_Y, open(TRAINING_DATA_NAME + "-output.p", "wb"))

print(str(i) + " frames total.")