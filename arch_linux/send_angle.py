import serial
from math import degrees

def send_angle(x, y, serial_port):
    yAngle = (int((y)) + 75) * 1000
    xAngle = (int((x)) + 93)
    #print 'x', int((x)) + 93
    #print 'y', int((y)) + 75
    serial_port.write(str(yAngle + xAngle) + "x")
