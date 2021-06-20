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
greenLower = (15, 70, 220)
greenUpper = (30, 190, 255)


class BallTracker(ImageProcessor):
    def __init__(self):
        self.skipFrames = 0 
        self.history = []

    def calculate(self, frame):
        if frame is None:
            return False, None, None

        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (13, 13), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, greenLower, greenUpper)
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

            if len(self.history) > 0:
                previousTrack = self.history[-1]
                radiusOk = previousTrack["radius"] - RADIUS_MAX_SPEED < radius < previousTrack["radius"] + RADIUS_MAX_SPEED
                speedXok = previousTrack["center"][0] - PLANA_MAX_SPEED < x < previousTrack["center"][0] + PLANA_MAX_SPEED 
                speedYok = previousTrack["center"][1] - PLANA_MAX_SPEED < y < previousTrack["center"][1] + PLANA_MAX_SPEED 
                if radiusOk and speedXok and speedYok:
                    self.history.append({
                        "radius": radius,
                        "center": center,
                    })
                    cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)
                else:
                    self.skipFrames += 1
                    if self.skipFrames > MAX_SKIP_FRAME:
                        self.history.clear()
            else:
                self.history.append({
                    "radius": radius,
                    "center": center,
                })

        if len(self.history) < 2:
            return False, None, None

        # loop over the set of tracked points
        for i in range(1, len(self.history)):
            thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
            cv2.line(frame, self.history[i - 1]["center"], self.history[i]["center"], (0, 0, 255), thickness)

        if len(self.history) > 64:
            self.history.pop(0)

        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
        frame = cv2.vconcat([frame, mask])

        latestTrack = self.history[-1]

        return True, frame, latestTrack["center"]