import numpy as np
from enum import Enum

class BallState(Enum):
    Unknown = 1
    Up = 2
    Down = 3

class Track():
    def __init__(self, pos, radius, speed=0, acceleration=0):
        self.pos = np.array(pos)
        self.radius = radius
        self.speed = speed
        self.acceleration = acceleration

class Tracks():
    Y_DIRECTION_THRESHOLD = 10  # in pixel

    def __init__(self, maxLength=200):
        self.history = []
        self.maxLength = maxLength

    def append(self, newTrack):
        if len(self.history) > self.maxLength:
            self.history.pop()
        self.history.append(newTrack)

    def getTrackAt(self, index):
        if index < 0 or index >= len(self.history):
            return None

        return self.history[index]

    def getLastTrack(self):
        return self.history[-1]

    def getBallState(self):
        if len(self.history) < 2:
            return BallState.Unknown

        t1 = self.history[-2].pos
        t2 = self.history[-1].pos
        return BallState.Down if t1[1] < t2[1] else BallState.Up

    def estimateSpeed(self):
        if len(self.history) < 4:
            return np.zeros(2)

        t1 = self.history[-2].pos
        t2 = self.history[-1].pos
        return np.subtract(t2, t1)
        