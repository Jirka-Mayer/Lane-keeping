#from vjoy import vj, setJoy
import serial
import time
from threading import Thread

PWM_CENTER = 1487 # PWM center time
PWM_SCALE = 420.0 # PWM time range

EASE = 0.3 # Range limit for finer control

class ArduinoController(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.alive = True
        
        self.serial = None
        try:
            self.serial = serial.Serial("COM3")
        except serial.serialutil.SerialException:
            print("Arduino not found!")
            self.alive = False

        # publicly accessible steering value
        self.steering = 0.0

    def stop(self):
        self.alive = False

    def run(self):
        while self.alive:
            pwm = int(self.serial.readline().decode("ansi"))
            self.steering = ((PWM_CENTER - pwm) / PWM_SCALE) * EASE
