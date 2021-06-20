import numpy as np
import cv2
import time
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import time
import imutils

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray, np.ndarray)

    def __init__(self, imageProcessor):
        super().__init__()
        self.running = True
        self.vs = cv2.VideoCapture(1)
        time.sleep(2.0)
        self.imageProcessor = imageProcessor
    def run(self):
        
        while self.running:
            ret, frame  = self.vs.read()
            if ret:
                success, newFrame, pos = self.imageProcessor.calculate(frame)
                print(pos)
                if success:
                    self.change_pixmap_signal.emit(newFrame, pos)

            # latestTrack = self.history[-1]
            # writeServo(latestTrack["center"][0])

        self.vs.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self.running = False
        self.wait()
