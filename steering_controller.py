from vjoy import vj, setJoy
import time

SCALE = 16000.0
TRIMMER = 0.025

print("Openning vJoy...")
vj.open()
time.sleep(1)

class SteeringController():
    def __init__(self, keyboardHook, mouseHook):
        # joystick axis position
        self.xPos = 0.0
        self.yPos = 0.0

        # mouse control properties
        self.neutralPosition = 1920 / 2
        self.sensitivity = 800
        self.currentPosition = 0

        # bind listeners
        keyboardHook.addTapListener(self.keyboardTap)
        mouseHook.addMoveListener(self.mouseMove)

    def updateJoystick(self):
        print("Steering: " + str(self.xPos))
        setJoy(self.xPos + TRIMMER, self.yPos, SCALE)

    def keyboardTap(self, keycode, character, press):
        if character == "d":
            if press:
                self.xPos = 1.0
                self.neutralPosition = self.currentPosition
            else:
                self.xPos = 0.0
            self.updateJoystick()

        if character == "a":
            if press:
                self.xPos = -1.0
                self.neutralPosition = self.currentPosition
            else:
                self.xPos = 0.0
            self.updateJoystick()

    def mouseMove(self, x, y):
        # get pos
        self.currentPosition = x
        self.xPos = (x - self.neutralPosition) / self.sensitivity

        # clamp
        if self.xPos > 1:
            self.xPos = 1
        elif self.xPos < -1:
            self.xPos = -1

        # update joystick
        self.updateJoystick()