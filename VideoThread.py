import numpy as np
import cv2
import time
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import time
import imutils

class Roi():
    # values stored are percentage from each side of the image
    def __init__(self, top, left, bottom, right):
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right

    def getAbsoluteValue(self, width, height):
        t = height * self.top / 100
        b = height * (1- float(self.bottom/ 100) )
        l = width * self.left / 100
        r = width * (1- float(self.right/ 100) )
        return int(t), int(l), int(b), int(r)

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, imageProcessor, file = None):
        super().__init__()

        # FLAGS
        self.running = True
        self.playing = False
        self.playOneFrame = False

        # IMAGE PROCESSING
        self.file = file
        if file is None:
            self.vs = cv2.VideoCapture(1)
        else:    
            self.vs = cv2.VideoCapture(file)
        time.sleep(2.0)
        self.imageProcessor = imageProcessor
        self.roi = Roi(0,0,0,0)
        self.currentFrame = None
        
    def run(self):        
        reloadingVideo = False
        while self.running:
            ret, frame  = self.vs.read()

            if frame is None:
                if reloadingVideo:
                    break
                else:
                    self.vs = cv2.VideoCapture(self.file)
                    reloadingVideo = True
                    continue
            else:
                if reloadingVideo:
                    reloadingVideo = False

                self.currentFrame = frame.copy()
                self.processFrame(frame)

            if self.playOneFrame:
                self.playOneFrame = False
                self.playing = False

            while not self.playing:
                time.sleep(0.5)
            time.sleep(0.03)
            # latestTrack = self.history[-1]
            # writeServo(latestTrack["center"][0])

    def stop(self):
        self.running = False
        self.playing = True
        self.wait()

    # PLAY API
    def togglePlay(self):
        self.playing = not self.playing

    def resetPlay(self):
        if self.file is not None:
            self.vs = cv2.VideoCapture(self.file)
    
    def nextFrame(self):
        self.playOneFrame = True
        self.playing = True
    
    def previousFrame(self):
        pass

    # IMAGE PROCESSING API
    def processFrame(self, frame):
        if frame is None:
            return None

        height, width, channels = frame.shape
        

        t, l, b, r = self.roi.getAbsoluteValue(width, height)
        cropFrame = frame[t:b, l:r]
        success, newFrame, mask = self.imageProcessor.calculate(cropFrame.copy())
        processImage = np.zeros((height,width,3), np.uint8)
        if success:
            processImage = cv2.hconcat([newFrame, mask])
            processImage = self.resizeToFit(width, height, processImage)

        self.drawRoi(frame, width, height)
        outputFrame = cv2.vconcat([frame, processImage])
        self.change_pixmap_signal.emit(outputFrame)
        
        return outputFrame                      
        
    def reprocessFrame(self):
        if self.currentFrame is None:
            return
        self.processFrame(self.currentFrame.copy())

    def resizeToFit(self, targetWidth, targetHeight, image):
        h, w, c = image.shape
        wRatio = targetWidth / w
        hRatio = targetHeight / h
        ratio = 1
        if wRatio < hRatio:
            ratio = wRatio
        else:
            ratio = hRatio
        image = cv2.resize(image, (int(ratio*w), int(ratio*h)), interpolation=cv2.INTER_AREA)
        h, w, c = image.shape
        vPad = targetHeight - h
        hPad = targetWidth - w
        return cv2.copyMakeBorder(image, 0, vPad, 0, hPad, borderType=cv2.BORDER_CONSTANT, value=[0,0,0])


    def drawRoi(self, image, width, height):
        t, l, b, r = self.roi.getAbsoluteValue(width, height)
        pts = np.array([[l, t],\
            [r, t], \
            [r, b], \
            [l, b], \
            ], np.int32)

        pts = pts.reshape((-1,1,2))

        cv2.polylines(image,[pts],True,(0,255,255), thickness=5)
        return image

    def setRoi(self, top=None, left=None, bottom=None, right=None):
        if top is not None:
            self.roi.top = top
        if left is not None:
            self.roi.left = left
        if bottom is not None:
            self.roi.bottom = bottom
        if right is not None:
            self.roi.right = right

        self.reprocessFrame()


