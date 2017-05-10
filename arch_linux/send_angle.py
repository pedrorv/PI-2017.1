import serial
from math import degrees

def send_angle(x, y, serial_port):
    yAngle = (int(degrees(y)) + 93) * 1000
    xAngle = (int(degrees(x)) + 93)
    print 'x', int(degrees(x)) + 93
    print 'y', int(degrees(y)) + 93
    serial_port.write(str(yAngle + xAngle) + "x")
