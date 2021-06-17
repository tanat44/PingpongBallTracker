import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='COM17',
    baudrate=9600,
    timeout = 0.1
)

ser.isOpen()

value = 0
while value < 255:
    ser.write(f'{value}\n'.encode())
    value += 5
    print(value)
    time.sleep(0.2)