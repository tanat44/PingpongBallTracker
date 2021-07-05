from PyQt5.QtWidgets import (QSizePolicy, QWidget, QVBoxLayout, QSpacerItem)
from Widget.Slider import Slider

from RobotController import RobotParameter

class RobotControl(QWidget):

    def __init__(self, videoThread, robotParameter):
        super().__init__()
        self.videoThread = videoThread
        self.robotParameter = robotParameter

        layout = QVBoxLayout()
        self.originXSlider = Slider("Origin X", -50, 100, self.robotParameter.originX)
        self.originXSlider.change_value_signal.connect(self.originXSliderChange)
        layout.addWidget(self.originXSlider)

        self.originYSlider = Slider("Origin Y", -20, 100, self.robotParameter.originY)
        self.originYSlider.change_value_signal.connect(self.originYSliderChange)
        layout.addWidget(self.originYSlider)

        self.widthSlider = Slider("Width", 0, 100, self.robotParameter.width)
        self.widthSlider.change_value_signal.connect(self.widthSliderChange)
        layout.addWidget(self.widthSlider)

        layout.addItem(QSpacerItem(20,20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(layout)

    # SLOT
    def originXSliderChange(self, v):
        self.robotParameter.originX = v
        self.videoThread.reprocessFrame()

    def originYSliderChange(self, v):
        self.robotParameter.originY = v
        self.videoThread.reprocessFrame()

    def widthSliderChange(self, v):
        self.robotParameter.width = v
        self.videoThread.reprocessFrame()