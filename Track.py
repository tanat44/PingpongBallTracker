import numpy as np
from enum import Enum

DOWN_VECTOR = np.array([0, 1])

class BallState(Enum):
    Unknown = 1
    Up = 2
    Down = 3

class Track():
    def __init__(self, pos, radius, speed=np.zeros(2), direction=DOWN_VECTOR):
        self.pos = np.array(pos)
        self.radius = radius
        self.speed = speed
        self.direction = direction

class Tracks():
    Y_DIRECTION_THRESHOLD = 10  # in pixel

    def __init__(self, maxLength=200):
        self.history = []
        self.maxLength = maxLength

    def append(self, newTrack):
        if len(self.history) > self.maxLength:
            self.history.pop(0)
        self.history.append(newTrack)

    def getTrackAt(self, index):
        if index < -1 or index >= len(self.history):
            return None

        return self.history[index]

    def getLastTrack(self):
        return self.getTrackAt(-1)

    def getBallState(self):
        if len(self.history) < 2:
            return BallState.Unknown

        t1 = self.history[-2].pos
        t2 = self.history[-1].pos
        return BallState.Down if t1[1] < t2[1] else BallState.Up

    def estimateCurrentSpeed(self):
        if len(self.history) < 2:
            return np.zeros(2)

        t1 = self.history[-2].pos
        t2 = self.history[-1].pos
        speed = np.subtract(t2, t1) 
        self.history[-1].speed = speed

        return speed
        
    def estimateBallDirection(self, numFrames):
        if len(self.history) < numFrames:
            self.history[-1].direction = np.zeros(2)
            return 

        d = np.zeros(2)
        for i in range(numFrames):
            n = self.history[-1-i].speed
            d += n 
        
        d_norm = np.linalg.norm(d)

        # Unstable result
        if d_norm < 0.5:
            self.history[-1].direction = np.copy(self.history[-2].direction)
            print("unstable")
            return
        
        d = d / d_norm
        diviation = np.dot(DOWN_VECTOR, d)

        # Up
        if diviation < 0:
            self.history[-1].direction = np.copy(self.history[-2].direction)

        # Down
        else:
            self.history[-1].direction = d
