import numpy as np
from enum import Enum
from Utils.RayIntersection import RayIntersection
import math

DOWN_VECTOR = np.array([0, 1])
SPEED_DIRECTION_THRESHOLD = 25

class BallState(Enum):
    Unknown = 1
    Up = 2
    Down = 3

class Track():
    def __init__(self, pos, radius, speed=np.zeros(2), direction=DOWN_VECTOR, hitPoint=np.zeros(2), ballState=BallState.Unknown):
        self.pos = np.array(pos)
        self.radius = radius
        self.speed = speed
        self.direction = direction
        self.hitPoint = hitPoint
        self.ballState = ballState

class Tracks():
    Y_DIRECTION_THRESHOLD = 10  # in pixel

    def __init__(self, gameParameter, maxLength=200):
        self.history = []
        self.maxLength = maxLength
        self.gameParameter = gameParameter

    def append(self, newTrack):
        if len(self.history) > self.maxLength:
            self.history.pop(0)
        self.history.append(newTrack)

        # CALCULATION
        self.calculateCurrentSpeed()
        self.calculateBallDirection(self.gameParameter.numPredictFrame)
        self.calculateBallState()
        self.calculateHitPoint()

    def getTrackAt(self, index):
        if index < -1 or index >= len(self.history):
            return None

        return self.history[index]

    def getLastTrack(self):
        return self.getTrackAt(-1)

    def isBallInGame(self, pos):
        yOpponent, yRobot = self.gameParameter.getPlayerZone()
        # ball in player zone
        if pos[1] < yOpponent or pos[1] > yRobot:
            return False

        # ball in game (table zone)
        # pos[1] >= yOpponent and y[1] <= yRobot
        return True

    def getBallState(self):
        if len(self.history) < 1:
            return BallState.Unknown

        return self.history[-1].ballState

    def getFrameToHit(self):
        if len(self.history) < 15:
            return -1

        pos = self.history[-1].pos

        # speed = latest known positive y speed
        speed = np.zeros(2)
        maxSeekFrame = 10
        foundPositiveYSpeed = False
        for i in range(maxSeekFrame):
            s = self.history[-1-i].speed
            if s[1] > 0:
                foundPositiveYSpeed = True
                speed = s.copy()
                break
        if not foundPositiveYSpeed:
            return -1        

        yOpponent, yRobot = self.gameParameter.getPlayerZone()
        time = (yRobot - pos[1]) / np.linalg.norm(speed)

        return time
    
    def getHitPoint(self):
        for i in range(len(self.history)-1, 0, -1):
            if self.history[i].hitPoint[0] != 0:
                return self.history[i].hitPoint

        return np.zeros(2)

    # CALCULATION
    def calculateBallState(self):
        if len(self.history) < 2:
            return 
        
        lastHistory = self.history[-1]
        isInGame = self.isBallInGame(lastHistory.pos)
        if not isInGame:
            return

        # ball is in-game, find the direction
        ballAtPlayerFrame = -1
        for i in range(len(self.history)-2, 0, -1):
            t = self.history[i]
            if t.ballState is BallState.Unknown:
                ballAtPlayerFrame = i
                break

        # cannot find when ball was at player
        if ballAtPlayerFrame == -1:
            return
        
        p0 = self.history[ballAtPlayerFrame].pos
        p = lastHistory.pos
        lastHistory.ballState = BallState.Down if p[1] > p0[1] else BallState.Up

    def calculateCurrentSpeed(self):
        if len(self.history) < 2:
            return np.zeros(2)

        t1 = self.history[-2].pos
        t2 = self.history[-1].pos
        speed = np.subtract(t2, t1) 
        self.history[-1].speed = speed

        return speed
        
    def calculateBallDirection(self, numFrames):
        if len(self.history) < numFrames:
            self.history[-1].direction = np.zeros(2)
            return 

        d = np.zeros(2)
        for i in range(numFrames):
            d += self.history[-1-i].speed
        
        # Unstable result when sum speed vector is smaller than threshold
        d_norm = np.linalg.norm(d)
        if d_norm < SPEED_DIRECTION_THRESHOLD*numFrames:
            self.history[-1].direction = np.copy(self.history[-2].direction)
            return
        
        d = d / d_norm
        diviation = np.dot(DOWN_VECTOR, d)

        # Up
        if diviation < 0:
            self.history[-1].direction = np.copy(self.history[-2].direction)

        # Down
        else:
            self.history[-1].direction = d

    def calculateHitPoint(self):
        lastTrack = self.getLastTrack()
        # ray1
        p = lastTrack.pos
        d = lastTrack.direction
        
        # ray2
        yOpponent, yRobot = self.gameParameter.getPlayerZone()
        yRobot = np.array([0, yRobot])

        hp = RayIntersection(p, p+d, yRobot, yRobot + np.array([1,0]))
        if math.isnan(hp[0]):
            return

        self.history[-1].hitPoint = hp.copy()

