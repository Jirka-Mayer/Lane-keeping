from vjoy import vj, setJoy
import serial
import time

SCALE = 16000.0
TRIMMER = 0.025
print("Openning vJoy...")
vj.open()
time.sleep(1)

ser = serial.Serial("COM3")
PWM_CENTER = 1487
PWM_SCALE = 420.0

EASE = 0.3

while True:
    pwm = int(ser.readline().decode("ansi"))
    steer = ((PWM_CENTER - pwm) / PWM_SCALE) * EASE
    print("Steer: ", steer)
    setJoy(steer + TRIMMER, 0.0, SCALE)