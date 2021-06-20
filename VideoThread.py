import numpy as np
import cv2
import time
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import time
import imutils

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, imageProcessor, file = None):
        super().__init__()
        self.running = True
        if file is None:
            self.vs = cv2.VideoCapture(1)
        else:    
            self.vs = cv2.VideoCapture(file)
        time.sleep(2.0)
        self.imageProcessor = imageProcessor
        self.playing = False

    def run(self):        
        while self.running:
            ret, frame  = self.vs.read()
            if ret:
                success, newFrame, pos = self.imageProcessor.calculate(frame)
                print(pos)
                if success:
                    self.change_pixmap_signal.emit(newFrame)
            while not self.playing:
                time.sleep(0.5)
            time.sleep(0.33)
            # latestTrack = self.history[-1]
            # writeServo(latestTrack["center"][0])

        self.vs.release()

    def togglePlay(self):
        self.playing = not self.playing

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self.running = False
        self.wait()
