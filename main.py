from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy, QWidget, QApplication, QLabel, QVBoxLayout, QGridLayout, QTabWidget
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np

# MY LIB
from VideoThread import VideoThread
from ImageProcessor import BallTracker, ImageProcessor
from Track import BallState

# MY WIDGET
from Widget.Slider import Slider
from Widget.FrameControl import FrameControl
from Widget.RoiControl import RoiControl
from Widget.BallControl import BallControl
from Widget.GameControl import GameControl

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pingpong Robot Manager")
        self.setFixedSize(1000,800)

        # VIDEO DISPLAY
        self.image_label = QLabel(self)
        self.imageProcessor = BallTracker()
        self.videoThread = VideoThread(self.imageProcessor, file = "Video/test.mp4")
        self.videoThread.change_pixmap_signal.connect(self.update_image)
        self.videoThread.start()

        # FRAME CONTROL
        self.frameControl = FrameControl(self.videoThread)

        # SETTING TAB
        self.roiControl = RoiControl(self.videoThread)
        self.ballControl = BallControl(self.videoThread)
        self.gameControl = GameControl(self.videoThread)

        self.settingTab = QTabWidget()
        self.settingTab.addTab(self.gameControl, "Game")
        self.settingTab.addTab(self.roiControl, "Roi")
        self.settingTab.addTab(self.ballControl, "Ball")
        # self.settingTab.setCurrentWidget(self.roiControl)

        # RESULT
        resultLayout = QVBoxLayout()

        resultLayout.addWidget(QLabel("Ball Direction"))
        self.ballStateLabel = QLabel("")
        self.ballStateLabel.setAlignment(Qt.AlignCenter)
        self.ballStateLabel.setFixedHeight(80)
        self.updateBallState()
        resultLayout.addWidget(self.ballStateLabel)

        resultLayout.addWidget(QLabel("Frames to hit"))
        self.frameToHitLabel = QLabel("-")
        self.frameToHitLabel.setAlignment(Qt.AlignCenter)
        self.frameToHitLabel.setStyleSheet("font-weight: bold; font-size: 20px;")
        self.frameToHitLabel.setFixedHeight(80)
        resultLayout.addWidget(self.frameToHitLabel)

        # CONTROL PANEL
        controlPanelLayout = QVBoxLayout()
        controlPanelLayout.addWidget(self.frameControl)
        controlPanelLayout.addWidget(self.settingTab)
        controlPanelLayout.addLayout(resultLayout)
        controlPanelLayout.addWidget(QWidget())

        self.controlPanel = QWidget()
        self.controlPanel.setLayout(controlPanelLayout)
        self.controlPanel.setFixedWidth(300)

        # MAIN LAYOUT
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.image_label)
        mainLayout.addWidget(self.controlPanel)

        self.setLayout(mainLayout)


    def closeEvent(self, event):
        self.videoThread.stop()
        event.accept()

    # FUNCTION
    def updateBallState(self):
        s = self.imageProcessor.tracks.getBallState()
        color = "transparent"
        if s == BallState.Up:
            self.ballStateLabel.setText("UP")
            color = "green"
        elif s == BallState.Down:
            self.ballStateLabel.setText("DOWN")
            color = "red"
        else:
            self.ballStateLabel.setText("Unknown")
        self.ballStateLabel.setStyleSheet(f'background-color: {color}')
    
    def updateFrameToHit(self):
        v = self.imageProcessor.tracks.getFrameToHit()
        if v < 0:
            self.frameToHitLabel.setText("-")
        else:
            v = int(v)
            self.frameToHitLabel.setText(str(v))

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        # print(self.image_label.width(), self.image_label.height)
        p = convert_to_Qt_format.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


    # SLOT
    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

        self.updateBallState()
        self.updateFrameToHit()
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())