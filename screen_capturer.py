import mss
import numpy as np
import cv2

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
    def __init__(self, profileName, invertColorOrder=False):
        self.profile = CAPTURE_PROFILES[profileName]
        self.sct = mss.mss()

        # RGB to BGR
        self.invertColorOrder = invertColorOrder

    def capture(self):
        shot = np.array(self.sct.grab(self.profile))
        
        if self.invertColorOrder:
            shot = cv2.cvtColor(shot, cv2.COLOR_BGR2RGB)

        return shot