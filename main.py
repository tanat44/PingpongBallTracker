from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy, QWidget, QApplication, QLabel, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np

# MY LIB
from VideoThread import VideoThread
from ImageProcessor import BallTracker, ImageProcessor
from Widget.Slider import Slider

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pingpong Robot Manager")
        self.setFixedSize(1000,800)
        

        # VIDEO DISPLAY
        self.image_label = QLabel(self)
        # self.image_label.setFixedSize(640,480)
        self.imageProcessor = {
            "ballTracker": BallTracker()
        }
        self.videoThread = VideoThread(self.imageProcessor["ballTracker"], file = "Video/test.mp4")
        self.videoThread.change_pixmap_signal.connect(self.update_image)
        self.videoThread.start()

        # FRAME CONTROL
        frameControlLayout = QHBoxLayout()
        self.startButton = QPushButton("Play")
        self.startButton.clicked.connect(self.togglePlayClick)
        frameControlLayout.addWidget(self.startButton)

        self.previousFrameButton = QPushButton("<<")
        self.previousFrameButton.clicked.connect(self.previousFrameClick)
        frameControlLayout.addWidget(self.previousFrameButton)
        
        self.nextFrameButton = QPushButton(">>")
        self.nextFrameButton.clicked.connect(self.nextFrameClick)
        frameControlLayout.addWidget(self.nextFrameButton)

        self.resetButton = QPushButton("Reset")
        self.resetButton.clicked.connect(self.resetClick)
        frameControlLayout.addWidget(self.resetButton)

        # MASK CONTROL
        maskControlLayout = QVBoxLayout()
        self.topSlider = Slider("Top", 0, 100, 2)
        self.topSlider.change_value_signal.connect(self.topSliderChange)
        maskControlLayout.addWidget(self.topSlider)

        self.leftSlider = Slider("Left", 0, 100, 27)
        self.leftSlider.change_value_signal.connect(self.leftSliderChange)
        maskControlLayout.addWidget(self.leftSlider)

        self.bottomSlider = Slider("Bottom", 0, 100, 3)
        self.bottomSlider.change_value_signal.connect(self.bottomSliderChange)
        maskControlLayout.addWidget(self.bottomSlider)

        self.rightSlider = Slider("Right", 0, 100, 30)
        self.rightSlider.change_value_signal.connect(self.rightSliderChange)
        maskControlLayout.addWidget(self.rightSlider)

        # COLOR CONTROL
        colorControlLayout = QVBoxLayout()
        colorThreshold = self.videoThread.imageProcessor.colorThreshold

        self.hMinSlider = Slider("H Min", 0, 179, colorThreshold.h_min)
        self.hMinSlider.change_value_signal.connect(self.hMinSliderChange)
        colorControlLayout.addWidget(self.hMinSlider)
        self.hMaxSlider = Slider("H Max", 0, 179, colorThreshold.h_max)
        self.hMaxSlider.change_value_signal.connect(self.hMaxSliderChange)
        colorControlLayout.addWidget(self.hMaxSlider)

        self.sMinSlider = Slider("S Min", 0, 255, colorThreshold.s_min)
        self.sMinSlider.change_value_signal.connect(self.sMinSliderChange)
        colorControlLayout.addWidget(self.sMinSlider)
        self.sMaxSlider = Slider("S Max", 0, 255, colorThreshold.s_max)
        self.sMaxSlider.change_value_signal.connect(self.sMaxSliderChange)
        colorControlLayout.addWidget(self.sMaxSlider)

        self.vMinSlider = Slider("V Min", 0, 255, colorThreshold.v_min)
        self.vMinSlider.change_value_signal.connect(self.vMinSliderChange)
        colorControlLayout.addWidget(self.vMinSlider)
        self.vMaxSlider = Slider("V Max", 0, 255, colorThreshold.v_max)
        self.vMaxSlider.change_value_signal.connect(self.vMaxSliderChange)
        colorControlLayout.addWidget(self.vMaxSlider)

        # CONTROL PANEL
        controlPanelLayout = QVBoxLayout()
        controlPanelLayout.addLayout(frameControlLayout)
        controlPanelLayout.addLayout(maskControlLayout)
        controlPanelLayout.addLayout(colorControlLayout)
        controlPanelLayout.addWidget(QWidget())

        self.controlPanel = QWidget()
        self.controlPanel.setLayout(controlPanelLayout)
        self.controlPanel.setFixedWidth(300)

        # MAIN LAYOUT
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.image_label)
        mainLayout.addWidget(self.controlPanel)

        self.setLayout(mainLayout)

        # INIT VALUE
        self.videoThread.setRoi(top=self.topSlider.value(), left=self.leftSlider.value(), bottom=self.bottomSlider.value(), right=self.rightSlider.value())

    def closeEvent(self, event):
        self.videoThread.stop()
        event.accept()

    # SLOT

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    def topSliderChange(self, v):
        self.videoThread.setRoi(top=v)

    def leftSliderChange(self, v):
        self.videoThread.setRoi(left=v)

    def bottomSliderChange(self, v):
        self.videoThread.setRoi(bottom=v)

    def rightSliderChange(self, v):
        self.videoThread.setRoi(right=v)

    def hMinSliderChange(self, v):
        self.videoThread.imageProcessor.setColorThreshold(h_min = v)
        self.videoThread.reprocessFrame()
    
    def hMaxSliderChange(self, v):
        self.videoThread.imageProcessor.setColorThreshold(h_max = v)
        self.videoThread.reprocessFrame()

    def sMinSliderChange(self, v):
        self.videoThread.imageProcessor.setColorThreshold(s_min = v)
        self.videoThread.reprocessFrame()
    
    def sMaxSliderChange(self, v):
        self.videoThread.imageProcessor.setColorThreshold(s_max = v)
        self.videoThread.reprocessFrame()

    def vMinSliderChange(self, v):
        self.videoThread.imageProcessor.setColorThreshold(v_min = v)
        self.videoThread.reprocessFrame()
    
    def vMaxSliderChange(self, v):
        self.videoThread.imageProcessor.setColorThreshold(v_max = v)
        self.videoThread.reprocessFrame()

    def togglePlayClick(self):
        self.videoThread.togglePlay()

    def resetClick(self):
        self.videoThread.resetPlay()

    def nextFrameClick(self):
        self.videoThread.nextFrame()
    
    def previousFrameClick(self):
        self.videoThread.previousFrame()
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        # print(self.image_label.width(), self.image_label.height)
        p = convert_to_Qt_format.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())