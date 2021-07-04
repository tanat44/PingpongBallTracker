import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

LINK_LENGTH = 100
X_MOTION_RANGE = [-50, 55] # MAXIMUM X RANGE -50 55
Y_MOTION_RANGE = [-65, 0] # MAXIMUM Y RANGE -65 20
 
def degToRad(deg):
    return deg * math.pi / 180

def radToDeg(rad):
    return rad * 180 / math.pi

class Kinematic():
    def jacobianInv(q):
        a = q[0]
        b = q[1]
        j0 = np.array([-LINK_LENGTH*math.sin(a), -LINK_LENGTH*math.sin(b)])
        j1 = np.array([LINK_LENGTH*math.cos(a), LINK_LENGTH*math.cos(b)])
        j = np.array([j0, j1])
        
        return np.array([[j[1,1], -j[0,1]], [-j[1,0], j[0,0]]]) \
            / (j[1,1]*j[0,0] - j[0,1]*j[1,0])

    def forwardKinematic(q):
        x = [0]
        y = [0]
        for i in range(len(q)):
            x.append(x[-1] + LINK_LENGTH*math.cos(q[i]))
            y.append(y[-1] + LINK_LENGTH*math.sin(q[i]))
        return x, y

    def plot(q, ax):
        x,y = Kinematic.forwardKinematic(q)
        ax.plot(x, y)
        ax.plot(x, y, 'bo', color='green')

        # x, y = [],[]
        # for m in motion:
        #     x.append(m[0])
        #     y.append(m[1])

        # ax.plot(x, y, 'bo', color='red')



class MotionPlanner():

    def __init__(self, xRange = X_MOTION_RANGE, yRange = Y_MOTION_RANGE):
        # state variables
        self.q = degToRad(np.array([90, 0]))
        self.originalQ = self.q.copy()
        x, y = Kinematic.forwardKinematic(self.q)
        self.pos = np.array([x[-1], y[-1]])

        # parameters
        self.xRange = xRange
        self.yRange = yRange

        # motion
        self.motion = []
        self.jointMotion = []

    def moveToPos(self, endPos, steps = 20 ):
        endPos, endQ, newMotion, newJointMotion = self.planInverseKinematic(steps, self.pos, self.q, endPos)
        
        self.pos = endPos
        self.q = endQ
        self.motion += newMotion
        self.jointMotion += newJointMotion

    def planInverseKinematic(self, steps, startPos, startQ, endPos):
        motion = []
        jointMotion = []
        currentPos = startPos.copy()

        for i in range(steps):
            delta = endPos-currentPos
            dp = delta / (steps - i)
            dq = np.matmul(Kinematic.jacobianInv(startQ), dp[..., None])
            dq = np.transpose(dq)[0]
            jointMotion.append(radToDeg(dq))
            startQ += dq
            x, y = Kinematic.forwardKinematic(startQ)
            currentPos = [x[-1], y[-1]]
            motion.append(np.array([x[1], y[1]]))
            motion.append(np.array([x[2], y[2]]))
        
        endPos = currentPos
        endQ = startQ

        return endPos, endQ, motion, jointMotion

    def plot(self, showJointMotion = True, showKinematic = True):
        fig, ax = plt.subplots()
        ax.grid()
        ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')

        if showKinematic:
            Kinematic.plot(self.originalQ, ax)

        def animate(i):
            x, y = [],[]
            x.append(self.motion[i][0])
            y.append(self.motion[i][1])
            ax.plot(x, y, 'bo', color='red')

        anim = FuncAnimation(fig, animate, interval=50, frames=len(self.motion))
        plt.show()
    
    def saveJointMotion(self, outputFilePath = 'MotionData/motion.csv'):
        jointMotion = np.asarray(self.jointMotion)
        np.savetxt(outputFilePath, jointMotion, delimiter=',')


if __name__ == "__main__":
    motionPlanner = MotionPlanner()
    initialPos = motionPlanner.pos.copy()

    motionPlanner.moveToPos(initialPos + np.array([X_MOTION_RANGE[0], Y_MOTION_RANGE[1]]))
    motionPlanner.moveToPos(initialPos + np.array([X_MOTION_RANGE[0], Y_MOTION_RANGE[0]]))
    motionPlanner.moveToPos(initialPos + np.array([X_MOTION_RANGE[1], Y_MOTION_RANGE[0]]))
    motionPlanner.moveToPos(initialPos + np.array([X_MOTION_RANGE[1], Y_MOTION_RANGE[1]]))
    motionPlanner.moveToPos(initialPos)

    motionPlanner.plot()

    # # replay motion
    # q = np.array(originalQ)
    # motion = []
    # for j in jointMotion:
    #     q += degToRad(j)
    #     x, y = forwardKinematic(q)
    #     motion.append([x[-1], y[-1]])

