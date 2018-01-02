import pickle
import numpy as np
import cv2
import os
import scipy.misc
import matplotlib.pyplot as plt

# source data folders and their properties
SOURCES = [

    # some old recorded data
    ["recording-1-filtered", 0.0],

    # car is in the center of lane facing forward (correct car position)
    ["recording-centered", 0.0],

    # these steering weights are important to tweak well:

    # car facing forward, but shifted to a side close to a lane
    ["recording-shifted-left", 0.08],
    ["recording-shifted-right", -0.08],

    # car rotated, facing a lane
    ["recording-rotated-left", 0.08],
    ["recording-rotated-right", -0.08],
]
TRAINING_DATA_NAME = "training-data-3"

# training dataset image dimensions
TRAINING_WIDTH = 160
TRAINING_HEIGHT = 80

# model I/O normalization
STEERING_NORMALIZATION = 0.1
IMAGE_NORMALIZATION = 255

# method that does the conversion
def prepareFrame(training_X, training_Y, framePath, steering):
    """Inserts single frame into the training dataset"""

    # read file
    frame = cv2.imread(framePath)

    # correct color channel order for scipy & numpy
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # convert to numpy array
    frame = np.array(frame)

    # resize to correct dimensions
    frame = scipy.misc.imresize(frame, (TRAINING_HEIGHT, TRAINING_WIDTH, 3))

    # insert into the training set
    training_X.append(frame / IMAGE_NORMALIZATION)
    training_Y.append(steering / STEERING_NORMALIZATION)


def processFolder(training_X, training_Y, folderName, steeringOffset=0.0):
    """Inserts entire folder into the training dataset"""
    
    # print some info
    print("================================")
    print("Folder: " + folderName)
    
    # load steering data
    steeringData = pickle.load(open(folderName + "/_steeringData.p", "rb"))

    # go through all frames
    i = 0
    for item in steeringData:
        framePath = folderName + "/frame-" + str(item[0]) + ".png"
        
        # check frame existence, if the frame doesn't exist, skip it
        if not os.path.isfile(framePath):
            continue

        # add frame to the dataset
        prepareFrame(
            training_X,
            training_Y,
            framePath,
            item[1] + steeringOffset
        )

        # increment frame counter
        i += 1

        # print info
        if i % 50 == 0:
            print("Frame: " + str(i))

    # print final info
    print(str(i) + " frames total.")


########
# Main #
########

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