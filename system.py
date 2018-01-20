"""
    Makes the model drive the car
"""

from hook import KeyboardHook
from steering_controller import SteeringController
from screen_capturer import ScreenCapturer
from threading import Thread
import cv2
import time
import keras
import scipy.misc
import numpy as np
from arduino import ArduinoController

"""
    Controls:
    Q - quit
    I - enable driver
    A, D - full control of steering
"""

INTERVENTION_THRESHOLD = 0.005

# handles all the tasks
class SystemManager(Thread):
    def __init__(self, keyboardHook, steeringController, screenCapturer, arduinoController):
        Thread.__init__(self)
        self.alive = True

        self.arduinoController = arduinoController
        self.steeringController = steeringController
        self.screenCapturer = screenCapturer
        keyboardHook.addTapListener(self.keyboardTap)

        # state of the system
        self.state = "cruise"

    def stop(self):
        self.alive = False

    def keyboardTap(self, keycode, character, press):
        if character == "i" and press:
            if self.state == "cruise":
                self.state = "model"
                print("Model takes the control")
            elif self.state == "model":
                self.state = "cruise"
                print("It's yours now")

        if character == "F1" and press:
            if self.state == "cruise":
                self.state = "recording"
                print("Recording now")
            elif self.state == "recording":
                self.state = "cruise"
                print("Recording done")

    def run(self):
        model = keras.models.load_model("model.h5")

        print("Ready!")

        while self.alive:

            # when cruising
            if self.state == "cruise":
                self.steeringController.updateSteering(self.arduinoController.steering)
                time.sleep(0.1)
                continue

            # when recording data
            if self.state == "recording":
                self.steeringController.updateSteering(self.arduinoController.steering)
                frame = self.screenCapturer.capture()
                frame[0, 0, 0] = 0.5 + (self.arduinoController.steering / 2)
                scipy.misc.toimage(frame, cmin=0.0, cmax=1.0, channel_axis=2).save("recording/" + str(time.time()) + ".png")
                time.sleep(0.1)
                continue

            # when the model drives
            if self.state == "model":
                # predict steering
                frame = self.screenCapturer.capture()
                steering = model.predict(frame[None,:,:,:])[0][0]

                self.steeringController.updateSteering(
                    steering + self.arduinoController.steering
                )

                if abs(self.arduinoController.steering) > INTERVENTION_THRESHOLD:
                    frame[0, 0, 0] = 0.5 + (steering + self.arduinoController.steering) / 2
                    scipy.misc.toimage(frame, cmin=0.0, cmax=1.0, channel_axis=2).save("recording/" + str(time.time()) + ".png")
                    print("Intervention, " + str(time.time()))

                time.sleep(0.1)

########
# MAIN #
########

# create hooks
keyboardHook = KeyboardHook()

# create controllers
arduinoController = ArduinoController()
steeringController = SteeringController(keyboardHook)
screenCapturer = ScreenCapturer("Desktop-Win10", True) # !!! TRUE !!!
systemManager = SystemManager(keyboardHook, steeringController, screenCapturer, arduinoController)

# program exit handling
def exitHandler(keycode, character, press):
    if character == "q" and press:
        systemManager.stop()
        systemManager.join()

        arduinoController.stop()
        arduinoController.join()

        exit() # keyboardHook.stop() not needed, runs synchronously

keyboardHook.addTapListener(exitHandler)

# start controllers
arduinoController.start()
systemManager.start()

# start hooks
keyboardHook.run()