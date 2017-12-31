"""
    Makes the model drive the car
"""

from hook import KeyboardHook, MouseHook
from steering_controller import SteeringController
from screen_capturer import ScreenCapturer
from threading import Thread
import cv2
import time
import keras.models
import scipy.misc
import numpy as np

class Driver(Thread):
    def __init__(self, keyboardHook, steeringController, screenCapturer):
        Thread.__init__(self)
        self.alive = True

        self.steeringController = steeringController
        self.screenCapturer = screenCapturer
        keyboardHook.addTapListener(self.keyboardTap)

        self.driving = False

    def stop(self):
        self.alive = False

    def loadState(self):
        if not os.path.isfile("recording/_steeringData.p") or not os.path.isfile("recording/_frameIndex.p"):
            return

        self.steeringData = pickle.load(open("recording/_steeringData.p", "rb"))
        self.frameIndex = pickle.load(open("recording/_frameIndex.p", "rb"))

    def saveState(self):
        pickle.dump(self.steeringData, open("recording/_steeringData.p", "wb"))
        pickle.dump(self.frameIndex, open("recording/_frameIndex.p", "wb"))

    def keyboardTap(self, keycode, character, press):
        if character == "i" and press:
            self.driving = not self.driving
            print("Driving: " + str(self.driving))

    def run(self):
        model = keras.models.load_model("model.h5")

        print("Ready!")

        while self.alive:
            if not self.driving:
                time.sleep(0.1)
                continue

            # predict steering
            frame = self.screenCapturer.capture()
            frame = scipy.misc.imresize(frame, (80, 160, 3))
            frame = np.array(frame)
            frame = frame / 255 # normalize input
            frame = frame[None,:,:,:]

            prediction = model.predict(frame)
            prediction = prediction[0][0]
            steering = prediction * 0.1 # un-normalize

            self.steeringController.steerNetwork(steering)

########
# MAIN #
########

# create hooks
keyboardHook = KeyboardHook()
mouseHook = MouseHook()

# create controllers
steeringController = SteeringController(keyboardHook, mouseHook)
screenCapturer = ScreenCapturer("Desktop-Win10", True) # !!! TRUE !!!
driver = Driver(keyboardHook, steeringController, screenCapturer)

# program exit handling
def exitHandler(keycode, character, press):
    if character == "q" and press:
        driver.stop()
        driver.join()

        mouseHook.stop()
        mouseHook.join()

        exit() # keyboardHook.stop() not needed, runs synchronously

keyboardHook.addTapListener(exitHandler)

# start controllers
driver.start()

# start hooks
mouseHook.start()
keyboardHook.run()