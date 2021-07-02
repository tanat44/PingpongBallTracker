from PyQt5.QtWidgets import (QSizePolicy, QSpacerItem, QWidget, QSlider, QVBoxLayout, QLabel, QPushButton)
from Widget.Slider import Slider

class RoiControl(QWidget):

    def __init__(self, videoThread):
        super().__init__()
        self.videoThread = videoThread

        layout = QVBoxLayout()
        self.topSlider = Slider("Top", 0, 100, 2)
        self.topSlider.change_value_signal.connect(self.topSliderChange)
        layout.addWidget(self.topSlider)

        self.leftSlider = Slider("Left", 0, 100, 27)
        self.leftSlider.change_value_signal.connect(self.leftSliderChange)
        layout.addWidget(self.leftSlider)

        self.bottomSlider = Slider("Bottom", 0, 100, 3)
        self.bottomSlider.change_value_signal.connect(self.bottomSliderChange)
        layout.addWidget(self.bottomSlider)

        self.rightSlider = Slider("Right", 0, 100, 30)
        self.rightSlider.change_value_signal.connect(self.rightSliderChange)
        layout.addWidget(self.rightSlider)

        layout.addItem(QSpacerItem(20,20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(layout)

        # INIT VALUE
        self.videoThread.setRoi(top=self.topSlider.value(), left=self.leftSlider.value(), bottom=self.bottomSlider.value(), right=self.rightSlider.value())

    # SLOT
    def topSliderChange(self, v):
        self.videoThread.setRoi(top=v)

    def leftSliderChange(self, v):
        self.videoThread.setRoi(left=v)

    def bottomSliderChange(self, v):
        self.videoThread.setRoi(bottom=v)

    def rightSliderChange(self, v):
        self.videoThread.setRoi(right=v)