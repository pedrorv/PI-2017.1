import serial

def send_angle(x, y, serial_port):
    yAngle = y * 1000
    xAngle = x
    print 'x', x
    print 'y', y
    serial_port.write(str(yAngle + xAngle) + "x")