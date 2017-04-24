import serial
from random import randrange
import time

ser = serial.Serial('/dev/ttyUSB0', 9600)

def sendAngle():
    yAngle = randrange(0, 181, 1) * 1000
    xAngle = randrange(0, 181, 1)
    print 'x', xAngle
    print 'y', yAngle
    ser.write(str(yAngle + xAngle) + "x")

while (1 == 1):
    sendAngle()
    time.sleep(5)