from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy, QWidget, QApplication, QLabel, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np

# MY LIB
from VideoThread import VideoThread
from ImageProcessor import BallTracker
from Widget.Slider import Slider

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pingpong Robot Manager")
        self.setFixedSize(1200,800)
        mainLayout = QHBoxLayout()

        # VIDEO DISPLAY
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(640,480)
        mainLayout.addWidget(self.image_label)
        self.imageProcessor = {
            "ballTracker": BallTracker()
        }
        self.videoThread = VideoThread(self.imageProcessor["ballTracker"], file = "Video/test.mp4")
        self.videoThread.change_pixmap_signal.connect(self.update_image)
        self.videoThread.start()

        # FRAME CONTROL
        frameControlLayout = QHBoxLayout()
        self.startButton = QPushButton("Play")
        self.startButton.clicked.connect(self.toggleVideoPlay)
        frameControlLayout.addWidget(self.startButton)
        self.previousButton = QPushButton("-1")
        frameControlLayout.addWidget(self.previousButton)
        self.nextButton = QPushButton("+1")
        frameControlLayout.addWidget(self.nextButton)
        self.resetButton = QPushButton("Reset")
        frameControlLayout.addWidget(self.resetButton)
        self.resetButton.clicked.connect(self.resetVideo)


        # MASK CONTROL
        maskControlLayout = QVBoxLayout()
        self.topSlider = Slider("Top", 0, 100, 50)
        maskControlLayout.addWidget(self.topSlider)
        self.bottomSlider = Slider("Bottom", 0, 100, 50)
        maskControlLayout.addWidget(self.bottomSlider)
        self.leftSlider = Slider("Left", 0, 100, 50)
        maskControlLayout.addWidget(self.leftSlider)
        self.rightSlider = Slider("Right", 0, 100, 50)
        maskControlLayout.addWidget(self.rightSlider)


        # CONTROL PANEL
        controlPanelLayout = QVBoxLayout()
        controlPanelLayout.addLayout(frameControlLayout)
        controlPanelLayout.addLayout(maskControlLayout)
        controlPanelLayout.addWidget(QWidget())

        self.controlPanel = QWidget()
        self.controlPanel.setLayout(controlPanelLayout)
        mainLayout.addWidget(self.controlPanel)

        self.setLayout(mainLayout)

    def closeEvent(self, event):
        self.videoThread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    def toggleVideoPlay(self):
        self.videoThread.togglePlay()

    def resetVideo(self):
        self.videoThread.resetPlay()
    
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