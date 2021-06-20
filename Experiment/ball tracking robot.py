# import the necessary packages
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
myserial = serial.Serial(
    port='COM17',
    baudrate=9600,
    timeout = 0.1
)
myserial.isOpen()



def writeServo(x):
    setPoint = 300
    delta = x-setPoint
    inRange = [-300,300]
    outRange = [0,255]
    outMid = (float(outRange[0]) + outRange[1]) / 2

    out = float(delta) / (inRange[1] - inRange[0]) * (outRange[1] - outRange[0]) + outRange[0] + outMid
    myserial.write(f'{out}\n'.encode())
    


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
args = vars(ap.parse_args())

# PARAMETERS
RADIUS_MAX_SPEED = 5
PLANA_MAX_SPEED = 80
MAX_SKIP_FRAME = 10
greenLower = (15, 70, 220)
greenUpper = (30, 190, 255)

skipFrames = 0 
history = []

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    vs = VideoStream(src=1).start()

# otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(args["video"])

# allow the camera or video file to warm up
time.sleep(2.0)

# keep looping
while True:
    # grab the current frame
    frame = vs.read()

    # handle the frame from VideoCapture or VideoStream
    frame = frame[1] if args.get("video", False) else frame

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break

    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    frame = cv2.flip(frame,1)
    blurred = cv2.GaussianBlur(frame, (13, 13), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))


        
        if len(history) > 0:
            previousTrack = history[-1]
            radiusOk = previousTrack["radius"] - RADIUS_MAX_SPEED < radius < previousTrack["radius"] + RADIUS_MAX_SPEED
            speedXok = previousTrack["center"][0] - PLANA_MAX_SPEED < x < previousTrack["center"][0] + PLANA_MAX_SPEED 
            speedYok = previousTrack["center"][1] - PLANA_MAX_SPEED < y < previousTrack["center"][1] + PLANA_MAX_SPEED 
            if radiusOk and speedXok and speedYok:
                history.append({
                    "radius": radius,
                    "center": center,
                })
                cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
            else:
                skipFrames += 1
                if skipFrames > MAX_SKIP_FRAME:
                    history.clear()
        else:
            history.append({
                "radius": radius,
                "center": center,
            })

    if len(history) < 2:
        continue

    # loop over the set of tracked points
    for i in range(1, len(history)):
        thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
        cv2.line(frame, history[i - 1]["center"], history[i]["center"], (0, 0, 255), thickness)

    if len(history) > 64:
        history.pop(0)

    # show the frame to our screen
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    frame = cv2.hconcat([frame, mask])
    cv2.imshow("Frame", frame)


    latestTrack = history[-1]
    writeServo(latestTrack["center"][0])

    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
    vs.stop()

# otherwise, release the camera
else:
    vs.release()

# close all windows
cv2.destroyAllWindows()