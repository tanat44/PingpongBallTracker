import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

LENGTH = 100

def degToRad(deg):
    return deg * math.pi / 180

def radToDeg(rad):
    return rad * 180 / math.pi

def jacobianInv(q):
    a = q[0]
    b = q[1]
    j0 = np.array([-LENGTH*math.sin(a), -LENGTH*math.sin(b)])
    j1 = np.array([LENGTH*math.cos(a), LENGTH*math.cos(b)])
    j = np.array([j0, j1])
    
    return np.array([[j[1,1], -j[0,1]], [-j[1,0], j[0,0]]]) \
        / (j[1,1]*j[0,0] - j[0,1]*j[1,0])

def forwardKinematic(q):
    x = [0]
    y = [0]
    for i in range(len(q)):
        x.append(x[-1] + LENGTH*math.cos(q[i]))
        y.append(y[-1] + LENGTH*math.sin(q[i]))
    return x, y

def plotKinematic(q, ax, motion = []):
    x,y = forwardKinematic(q)
    ax.plot(x, y)
    ax.plot(x, y, 'bo', color='green')

    x, y = [],[]
    for m in motion:
        x.append(m[0])
        y.append(m[1])

    ax.plot(x, y, 'bo', color='red')

# INITIAL CONFIGURATION
q = np.array([90, 0])
q  = degToRad(q)
originalQ = np.array(q)
x, y = forwardKinematic(q)
startingPos = np.array([x[-1], y[-1]])
currentPos = np.array(startingPos)

motion = []
jointMotion = []

def inverseKinematic(steps, startPos, endPos, q):
    motion = []
    currentPos = np.array(startPos)

    for i in range(steps):
        delta = endPos-currentPos
        dp = delta / (steps - i)
        dq = np.matmul(jacobianInv(q), dp[..., None])
        dq = np.transpose(dq)[0]
        jointMotion.append(radToDeg(dq))
        q += dq
        x, y = forwardKinematic(q)
        currentPos = [x[-1], y[-1]]
        motion.append(np.array([x[1], y[1]]))
        motion.append(np.array([x[2], y[2]]))
    
    return currentPos, motion

# IK PLANNER

xRange = [-50, 55] # MAXIMUM X RANGE -50 55
yRange = [-65, 0] # MAXIMUM Y RANGE -65 20

steps = 20
center = np.array(currentPos)
currentPos, newMotion = inverseKinematic(steps, currentPos, center + np.array([xRange[0], yRange[1]]), q)
motion += newMotion
currentPos, newMotion = inverseKinematic(steps, currentPos, center + np.array([xRange[0], yRange[0]]), q)
motion += newMotion
currentPos, newMotion = inverseKinematic(steps, currentPos, center + np.array([xRange[1], yRange[0]]), q)
motion += newMotion
currentPos, newMotion = inverseKinematic(steps, currentPos, center + np.array([xRange[1], yRange[1]]), q)
motion += newMotion
currentPos, newMotion = inverseKinematic(steps, currentPos, center, q)
motion += newMotion


# SAVE PLANNING
jointMotion = np.asarray(jointMotion)
np.savetxt('MotionData/motion.csv', jointMotion, delimiter=',')

# # replay motion
# q = np.array(originalQ)
# motion = []
# for j in jointMotion:
#     q += degToRad(j)
#     x, y = forwardKinematic(q)
#     motion.append([x[-1], y[-1]])

# PLOT
fig, ax = plt.subplots()
ax.grid()
ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
plotKinematic(originalQ, ax)

def animate(i):
    x, y = [],[]
    x.append(motion[i][0])
    y.append(motion[i][1])

    ax.plot(x, y, 'bo', color='red')

anim = FuncAnimation(fig, animate, interval=50, frames=len(motion))

plt.show()