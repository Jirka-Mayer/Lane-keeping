from vjoy import vj, setJoy
import time

SCALE = 16000.0
TRIMMER = 0.025

print("Openning vJoy...")
vj.open()
time.sleep(1)

class SteeringController():
    def __init__(self, keyboardHook):
        # joystick axis position
        self.xPos = 0.0
        self.yPos = 0.0

        # mouse control properties
        self.neutralPosition = 1920 / 2
        self.sensitivity = 800
        self.currentPosition = 0

        # if the keyboard overrides the network
        self.keyboardActive = False

        # bind listener to keyboard
        keyboardHook.addTapListener(self.keyboardTap)

    def updateJoystick(self):
        #print("Steering: " + str(self.xPos))
        setJoy(self.xPos + TRIMMER, self.yPos, SCALE)

    def keyboardTap(self, keycode, character, press):
        if character == "d":
            if press:
                self.keyboardActive = True
                self.xPos = 1.0
                self.neutralPosition = self.currentPosition
            else:
                self.keyboardActive = False
                self.xPos = 0.0
            self.updateJoystick()

        if character == "a":
            if press:
                self.keyboardActive = True
                self.xPos = -1.0
                self.neutralPosition = self.currentPosition
            else:
                self.keyboardActive = False
                self.xPos = 0.0
            self.updateJoystick()

    def updateSteering(self, steering):
        if self.keyboardActive:
            return
        
        self.xPos = steering
        self.neutralPosition = self.currentPosition
        self.updateJoystick()