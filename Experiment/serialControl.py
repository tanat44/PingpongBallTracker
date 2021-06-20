import time
import serial
import numpy as np

ser = serial.Serial(
    port='COM17',
    baudrate=9600,
    timeout = 0.1
)

ser.isOpen()

class Servo:
    index = 0

    def __init__(self, step, maxAngle = 90.0, offsetAngle = 0.0):
        self.value = 0
        self.forward = True
        self.step = step
        self.valueToAngle = maxAngle/255
        self.offsetAngle = offsetAngle
        self.index = Servo.index
        Servo.index += 1

    
    def setAngle(self, angle):
        newValue = (angle + self.offsetAngle) / self.valueToAngle
        if newValue < 0:
            newValue = 0
            print("LOWER LIMIT", self.index)
        elif newValue > 255:
            newValue = 255
            print("UPPER LIMIT", self.index)

        self.value = newValue

    def getAngle(self):
        return self.value * self.valueToAngle - self.offsetAngle

    # def move(self):
    #     if self.forward:
    #         self.value += self.step
    #         if self.value > 255:
    #             self.value = 255
    #             self.forward = False
    #     else:
    #         self.value -= self.step
    #         if self.value < 0:
    #             self.value = 00
    #             self.forward = True
    #     self.updateAngle()

# move servo to zero pos
s1 = Servo(2, maxAngle = 92.9, offsetAngle=60.0) # 92.9 60.0
s2 = Servo(10, maxAngle = 81.6, offsetAngle=42.0) # 81.6 42.0
s1.setAngle(0)
s2.setAngle(0)
ser.write(f'{s1.value}-{s2.value}\n'.encode())
time.sleep(1)


def manualControl():
    cycle = 0
    while cycle < 10:  
        
        d = input("Please enter delta: ")
        d = int(d)
        s1.setAngle(s1.getAngle() + d)
        s2.setAngle(s2.getAngle() + d)
        ser.write(f'{int(s1.value)}-{int(s2.value)}\n'.encode())

        print(f'New Value is {s1.getAngle()}')

        cycle += 1
        time.sleep(1)

def loadMotion():
    # read motion data and replay
    motion = np.loadtxt('MotionData/motion.csv',delimiter=',')
    for m in motion:
        s1.setAngle(s1.getAngle() + m[0])
        s2.setAngle(s2.getAngle() + m[1])
        ser.write(f'{int(s1.value)}-{int(s2.value)}\n'.encode())
        time.sleep(0.05)

# manualControl()
while True:
    loadMotion()

ser.close()