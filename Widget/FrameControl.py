from PyQt5.QtWidgets import (QSizePolicy, QWidget, QSlider, QHBoxLayout, QLabel, QPushButton)
from PyQt5.QtCore import Qt, pyqtSignal


class FrameControl(QWidget):

    def __init__(self, videoThread):
        super().__init__()
        self.videoThread = videoThread
        
        layout = QHBoxLayout()
        self.startButton = QPushButton("Play")
        self.startButton.clicked.connect(self.togglePlayClick)
        layout.addWidget(self.startButton)

        self.previousFrameButton = QPushButton("<<")
        self.previousFrameButton.clicked.connect(self.previousFrameClick)
        layout.addWidget(self.previousFrameButton)
        
        self.nextFrameButton = QPushButton(">>")
        self.nextFrameButton.clicked.connect(self.nextFrameClick)
        layout.addWidget(self.nextFrameButton)

        self.resetButton = QPushButton("Reset")
        self.resetButton.clicked.connect(self.resetClick)
        layout.addWidget(self.resetButton)
        
        self.setLayout(layout)
        self.setFixedHeight(50)

    # SLOT
    def togglePlayClick(self):
        self.videoThread.togglePlay()

    def resetClick(self):
        self.videoThread.resetPlay()

    def nextFrameClick(self):
        self.videoThread.nextFrame()
    
    def previousFrameClick(self):
        self.videoThread.previousFrame()