from MotionPlanner import RobotConfiguration
import numpy as np
import csv
from MotionPlanner import Kinematic
import cv2

MAX_ROBOT_SCALE = 10

class RobotParameter():
    def __init__(self, originX = -2, originY = -6, width = 31):
        self.originX = originX
        self.originY = originY
        self.width = width
        self.height = 100

class RobotController():
    def __init__(self, motionFilePath='MotionData/motion.csv'):
        self.robotParameter = RobotParameter()

        # map
        print("RobotController: Load motion data")
        self.map = np.zeros((120,120,2))        # map stores (x,y) to (q1,q2)
        with open(motionFilePath) as motionFile:
            reader = csv.reader(motionFile, delimiter=',')
            for row in reader:
                x, y, q1, q2 = row[0], row[1], row[2], row[3]
                self.map[int(x),int(y),:] = np.array([q1, q2])


    def lookUp(self, x, y):
        rangeX, rangeY = self.getMotionRange()
        q = np.zeros(2)
        if x < 0 or y < 0 or x > rangeX-1 or y > rangeY -1:
            return False, q

        q = self.map[x,y,:]
        if q[0] == 0 or q[1] == 0:
            return False, q

        return True, q

    def getMotionRange(self):
        shape = self.map.shape
        rangeX, rangeY = shape[0], shape[1]
        return rangeX, rangeY

    # x, y are float value 0.0-1.0
    # xOffset, yOffset are pixel absolute
    def drawKinematic(self, image, x, y, xOffset=0, yOffset=0, color=(0,255,255), scale=None, thickness=1):
        h, w, channel = image.shape

        # calculate
        rangeX, rangeY = self.getMotionRange()
        x = int(x*rangeX)
        y = int(y*rangeY)
        success, q = self.lookUp(x,y)
        if not success:
            return

        if scale is None:
            scale = 1.0 + self.robotParameter.width / 100.0 * MAX_ROBOT_SCALE
        p = Kinematic.forwardKinematic(q) * scale
        p = np.insert(p, 0, np.zeros(2), axis=0)
        p[:,1] = -yOffset + h - p[:,1]
        p[:,0] = xOffset + p[:,0]

        # draw
        p = p.astype(int)
        pts = p.reshape((-1,1,2))
        cv2.polylines(image,[pts],False, color, thickness=thickness)

if __name__ == "__main__":
    robotController = RobotController()
    image = np.zeros((200,800,3))
    for y in range(0, 100, 5):
        for x in range(1, 100, 5):
            robotController.drawKinematic(image, x, y, xOffset=50, scale=3, color=(100, int(x/100.0*255), int(y/100.0*255)))
    cv2.imwrite("test.jpg", image)

    