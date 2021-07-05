import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

LINK_LENGTH = 100
X_MOTION_RANGE = [-40, 70] # MAXIMUM X RANGE -50 55
Y_MOTION_RANGE = [-65, 25] # MAXIMUM Y RANGE -65 20
POSITION_ACCURACY = 0.3
 
def degToRad(deg):
    return deg * math.pi / 180

def radToDeg(rad):
    return rad * 180 / math.pi

class RobotConfiguration():
    def __init__(self, pos = np.zeros((2,2)), q = np.zeros(2), accurate=False):
        self.pos = pos.copy()
        self.q = q.copy()
        self.accurate = accurate
    
    def getEndEffectorPos(self):
        return self.pos[-1,:]

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
        pos = np.zeros((2,2))
        for i in range(len(q)):
            x, y = 0,0
            if i != 0:
                x, y = pos[i-1, 0], pos[i-1, 1]
            pos[i, 0] = x + LINK_LENGTH*math.cos(q[i])
            pos[i, 1] = y + LINK_LENGTH*math.sin(q[i])
        return pos

    def plot(q, ax):
        pos = Kinematic.forwardKinematic(q)
        x, y = [0],[0]
        for p in pos:
            x.append(p[0])
            y.append(p[1])
        ax.plot(x, y, color='black', linestyle='-')

class MotionPlanner():

    def __init__(self, xRange = X_MOTION_RANGE, yRange = Y_MOTION_RANGE):
        # state variables
        self.q = degToRad(np.array([90, 0]))
        self.originalQ = self.q.copy()
        temp = Kinematic.forwardKinematic(self.q)
        temp = temp[-1,:]
        self.origin = temp.copy()
        self.pos = temp.copy()

        # parameters
        self.xRange = xRange
        self.yRange = yRange

        # motion
        self.motion = []

    def clearMotion(self):
        self.motion.clear()
        self.originalQ = self.q.copy()
        p = Kinematic.forwardKinematic(self.originalQ)
        self.motion.append(RobotConfiguration(p, self.originalQ))

    def moveToPos(self, endPos, steps = 20 ):
        endPos, endQ, newMotion = self.planInverseKinematic(steps, self.pos, self.q, endPos)
        
        self.pos = endPos
        self.q = endQ
        self.motion += newMotion

    def planInverseKinematic(self, steps, startPos, startQ, endPos):
        motion = []
        currentPos = startPos.copy()

        for i in range(steps):
            delta = endPos-currentPos
            dp = delta / (steps - i)
            target = currentPos + dp
            dq = np.matmul(Kinematic.jacobianInv(startQ), dp[..., None])
            dq = np.transpose(dq)[0]
            startQ += dq            
            newPos = Kinematic.forwardKinematic(startQ)

            error = newPos[-1] - target
            isAccurate = np.linalg.norm(error) < POSITION_ACCURACY
            motion.append(RobotConfiguration(newPos, startQ, isAccurate))
            currentPos = newPos[-1]
        
        endPos = currentPos
        endQ = startQ

        return endPos, endQ, motion

    def plot(self, animate = True, showKinematic = True, showKinematicAnimation = False):
        fig, ax = plt.subplots()
        ax.grid()
        ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')

        if showKinematic:
            Kinematic.plot(self.originalQ, ax)


        if animate:
            def animate(i):
                p = self.motion[i].getEndEffectorPos()
                x, y = [p[0]],[p[1]]
                color = 'green' if self.motion[i].accurate else 'red'
                ax.plot(x, y, color=color, marker='o')
                if showKinematicAnimation:
                    Kinematic.plot(self.motion[i].q, ax)

            anim = FuncAnimation(fig, animate, interval=50, frames=len(self.motion))
        else:
            for m in self.motion:
                p = m.getEndEffectorPos()
                color = 'green' if m.accurate else 'red'
                ax.plot([p[0]], [p[1]], color=color, marker='o')

        plt.show()

    def generateIkMap(self, stepSize=5):
        # move to world origin
        worldOrigin = self.origin + np.array([self.xRange[0], self.yRange[0]])
        self.moveToPos(worldOrigin)
        self.clearMotion()

        firstPos = True
        c = self.motion[-1]    
        for j in range(self.yRange[0], self.yRange[1], stepSize):           
            self.q = c.q
            self.pos = c.getEndEffectorPos()
            
            for i in range(self.xRange[0], self.xRange[1], stepSize):
                self.moveToPos(self.origin + np.array([i, j]), steps = 1)
                if firstPos:
                    c = self.motion[-1]
                    firstPos = False 

            firstPos = True

    
    # def saveJointMotion(self, outputFilePath = 'MotionData/motion.csv'):
    #     jointMotion = np.asarray(self.jointMotion)
    #     np.savetxt(outputFilePath, jointMotion, delimiter=',')


if __name__ == "__main__":
    motionPlanner = MotionPlanner()
    motionPlanner.generateIkMap(stepSize=5)
    motionPlanner.plot(animate = False)

    # # replay motion
    # q = np.array(originalQ)
    # motion = []
    # for j in jointMotion:
    #     q += degToRad(j)
    #     x, y = forwardKinematic(q)
    #     motion.append([x[-1], y[-1]])

