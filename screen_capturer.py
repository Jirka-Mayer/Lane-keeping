import mss
import numpy as np
import cv2
import scipy.misc

CAPTURE_PROFILES = {
    "Desktop-Win10": {
        # fullscreen on the primary monitor
        "top": 0,
        "left": 0,
        "width": 1920,
        "height": 1080
    },
    "Laptop-Ubuntu": {
        # right-bottom corner - in a WineHQ window
        "top": 1080 / 2,
        "left": 1920 / 2,
        "width": 1920 / 2,
        "height": 1080 / 2
    }
}

class ScreenCapturer():
    def __init__(self, profileName="Desktop-Win10", invertColorOrder=True, prepareForModel=True):
        self.profile = CAPTURE_PROFILES[profileName]
        self.sct = mss.mss()

        # RGB to BGR
        self.invertColorOrder = invertColorOrder

        self.prepareForModel = prepareForModel

    def capture(self):
        shot = np.array(self.sct.grab(self.profile))
        
        if self.invertColorOrder:
            shot = cv2.cvtColor(shot, cv2.COLOR_BGR2RGB)

        if self.prepareForModel:
            shot = scipy.misc.imresize(shot, (80, 160, 3))
            shot = shot / 255

        return shot