import pickle
import numpy as np
import cv2
import os
import scipy.misc
import matplotlib.pyplot as plt

SOURCES = [
    ["recording-1-filtered", 0.0],
    ["recording-center", 0.0],
    ["recording-left", 0.04],
    ["recording-flat-left", 0.04],
    ["recording-right", -0.04],
    ["recording-flat-right", -0.04],
]
TRAINING_DATA_NAME = "training-data-3"

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


def processFolder(training_X, training_Y, folderName, steeringOffset=0.0):
    print("================================")
    print("Folder: " + folderName)
    
    # load recording
    steeringData = pickle.load(open(folderName + "/_steeringData.p", "rb"))

    # go through all frames
    i = 0
    for item in steeringData:
        framePath = folderName + "/frame-" + str(item[0]) + ".png"
        
        # check frame existence
        if not os.path.isfile(framePath):
            continue

        # convert
        prepareFrame(
            training_X,
            training_Y,
            framePath,
            item[1] + steeringOffset
        )

        i += 1

        if i % 50 == 0:
            print("Frame: " + str(i))

    print(str(i) + " frames total.")


# prepare training data variables
training_X = []
training_Y = []

# go over all folders and prepare them
for item in SOURCES:
    processFolder(training_X, training_Y, item[0], item[1])

print("Ending...")

# convert training vars to np array
training_X = np.array(training_X)
training_Y = np.array(training_Y)

# save training data
pickle.dump(training_X, open(TRAINING_DATA_NAME + "-input.p", "wb"))
pickle.dump(training_Y, open(TRAINING_DATA_NAME + "-output.p", "wb"))

print("Done!")