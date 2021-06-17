import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def degToRad(deg):
    return deg * math.pi / 180

def radToDef(rad):
    return rad * 180 / math.pi

def jacobian(q):
    return np.array([[-math.sin(q[0]), -math.sin(q[1])], [math.cos(q[0]), math.cos(q[1])]])

def jacobianInv(q):
    a = q[0]
    b = q[0] + q[1]
    j0 = np.array([-math.sin(a)-math.sin(b), -math.sin(b)])
    j1 = np.array([math.cos(a)+math.cos(b), math.cos(b)])
    j = np.array([j0, j1])
    
    return np.array([[j[1,1], -j[0,1]], [-j[1,0], j[0,0]]]) \
        / (j[1,1]*j[0,1] - j[1,0]*j[0,0])

def forwardKinematic(q):
    x = [0]
    y = [0]
    sumAngle = 0
    for i in range(len(q)):
        print(q[i])
        sumAngle += q[i]
        x.append(x[-1] + math.cos(sumAngle))
        y.append(y[-1] + math.sin(sumAngle))
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

q = np.array([30,30])
q  = degToRad(q)
originalQ = np.array(q)
x, y = forwardKinematic(q)
startingPos = np.array([x[-1], y[-1]])
delta = np.array([0, -1.5])

motion = []

# ik interpolation
steps = 100
dp = delta / steps
currentPos = np.array(startingPos)
for i in range(steps):
    dq = np.matmul(jacobianInv(q), dp[..., None])
    q += np.transpose(dq)[0]
    x, y = forwardKinematic(q)
    motion.append(np.array([x[1], y[1]]))
    motion.append(np.array([x[2], y[2]]))

fig, ax = plt.subplots()
ax.grid()
ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
plotKinematic(originalQ, ax)

def animate(i):
    x, y = [],[]
    x.append(motion[i][0])
    y.append(motion[i][1])

    ax.plot(x, y, 'bo', color='red')

anim = FuncAnimation(fig, animate, interval=100)

plt.show()