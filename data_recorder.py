"""
    Records raw model training data
"""

from hook import KeyboardHook, MouseHook
from steering_controller import SteeringController
from screen_capturer import ScreenCapturer
from threading import Thread
import cv2
import time
import pickle
import os

class Recorder(Thread):
    def __init__(self, keyboardHook, steeringController, screenCapturer):
        Thread.__init__(self)
        self.alive = True

        self.steeringController = steeringController
        self.screenCapturer = screenCapturer
        keyboardHook.addTapListener(self.keyboardTap)

        self.recording = False
        self.frameIndex = 1 # next frame index

        # recorded steering data
        self.steeringData = []

        # check directory
        if not os.path.isdir("recording"):
            os.makedirs("recording")

        self.loadState()

    def stop(self):
        self.alive = False

        if self.recording:
            self.recording = False
            self.saveState()

    def loadState(self):
        if not os.path.isfile("recording/_steeringData.p") or not os.path.isfile("recording/_frameIndex.p"):
            return

        self.steeringData = pickle.load(open("recording/_steeringData.p", "rb"))
        self.frameIndex = pickle.load(open("recording/_frameIndex.p", "rb"))

    def saveState(self):
        pickle.dump(self.steeringData, open("recording/_steeringData.p", "wb"))
        pickle.dump(self.frameIndex, open("recording/_frameIndex.p", "wb"))

    def keyboardTap(self, keycode, character, press):
        if character == "F1" and press:
            self.recording = not self.recording
            print("Recording: " + str(self.recording))

            if not self.recording:
                self.saveState()

    def saveFrame(self):
        if not self.recording:
            return

        if self.frameIndex % 10 == 0:
            print("Saving frame " + str(self.frameIndex))

        cv2.imwrite(
            "recording/frame-" + str(self.frameIndex) + ".png",
            self.screenCapturer.capture()
        )
        self.steeringData.append([self.frameIndex, self.steeringController.xPos])
        
        self.frameIndex += 1

    def run(self):
        while self.alive:
            if not self.recording:
                time.sleep(0.1)
                continue

            self.saveFrame()
            time.sleep(1 / 24)

########
# MAIN #
########

# create hooks
keyboardHook = KeyboardHook()
mouseHook = MouseHook()

# create controllers
steeringController = SteeringController(keyboardHook, mouseHook)
screenCapturer = ScreenCapturer("Desktop-Win10")
recorder = Recorder(keyboardHook, steeringController, screenCapturer)

# program exit handling
def exitHandler(keycode, character, press):
    if character == "q" and press:
        recorder.stop()
        recorder.join()

        mouseHook.stop()
        mouseHook.join()

        exit() # keyboardHook.stop() not needed, runs synchronously

keyboardHook.addTapListener(exitHandler)

# start controllers
recorder.start()

# start hooks
mouseHook.start()
keyboardHook.run()