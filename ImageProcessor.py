from abc import abstractmethod
import numpy as np
import cv2
import imutils

class ImageProcessor():
    @abstractmethod
    def calculate(self):
        pass

# PARAMETERS
RADIUS_MAX_SPEED = 5
PLANA_MAX_SPEED = 80
MAX_SKIP_FRAME = 10

class ColorThreshold():
    def __init__(self, h_min=14, h_max=30, s_min=14, s_max=255, v_min=243, v_max=255):
        self.h_min = h_min
        self.h_max = h_max
        self.s_min = s_min
        self.s_max = s_max
        self.v_min = v_min
        self.v_max = v_max

    def getMinValue(self):
        return (self.h_min, self.s_min, self.v_min)

    def getMaxValue(self):
        return (self.h_max, self.s_max, self.v_max)


class BallTracker(ImageProcessor):
    def __init__(self):
        self.skipFrames = 0 
        self.history = []
        self.roi = [0,0,1,1]
        self.colorThreshold = ColorThreshold()

    def setRoi(self, top, left, bottom, right):
        self.roi = [top, left, bottom, right]

    def setColorThreshold(self, h_min=None, h_max=None, s_min=None, s_max=None, v_min=None, v_max=None):
        if h_min is not None:
            self.colorThreshold.h_min = h_min
        if h_max is not None:
            self.colorThreshold.h_max = h_max
        if s_min is not None:
            self.colorThreshold.s_min = s_min
        if s_max is not None:
            self.colorThreshold.s_max = s_max
        if v_min is not None:
            self.colorThreshold.v_min = v_min
        if v_max is not None:
            self.colorThreshold.v_max = v_max

    def calculate(self, frame):
        blurred = cv2.GaussianBlur(frame, (13, 13), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.colorThreshold.getMinValue(), self.colorThreshold.getMaxValue())
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # self.history.append({
            #             "radius": radius,
            #             "center": center,
            #         })
            cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

            # if len(self.history) > 0:
            #     previousTrack = self.history[-1]
            #     radiusOk = previousTrack["radius"] - RADIUS_MAX_SPEED < radius < previousTrack["radius"] + RADIUS_MAX_SPEED
            #     speedXok = previousTrack["center"][0] - PLANA_MAX_SPEED < x < previousTrack["center"][0] + PLANA_MAX_SPEED 
            #     speedYok = previousTrack["center"][1] - PLANA_MAX_SPEED < y < previousTrack["center"][1] + PLANA_MAX_SPEED 
            #     if radiusOk and speedXok and speedYok:
                    
            #     else:
            #         self.skipFrames += 1
            #         if self.skipFrames > MAX_SKIP_FRAME:
            #             self.history.clear()
            # else:
            #     self.history.append({
            #         "radius": radius,
            #         "center": center,
            #     })

        # if len(self.history) < 2:
        #     return False, None, None

        # # loop over the set of tracked points
        # for i in range(1, len(self.history)):
        #     thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
        #     cv2.line(frame, self.history[i - 1]["center"], self.history[i]["center"], (0, 0, 255), thickness)

        # if len(self.history) > 64:
        #     self.history.pop(0)

        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

        # latestTrack = self.history[-1]

        return True, frame, mask