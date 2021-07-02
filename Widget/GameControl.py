from PyQt5.QtWidgets import (QSizePolicy, QWidget, QVBoxLayout, QSpacerItem)
from Widget.Slider import Slider

from ImageProcessor import GameParameter

class GameControl(QWidget):

    def __init__(self, videoThread):
        super().__init__()
        self.videoThread = videoThread
        self.imageProcessor = self.videoThread.imageProcessor
        self.gameParameter = self.imageProcessor.gameParameter

        layout = QVBoxLayout()
        self.opponentZoneSlider = Slider("Opponent Zone", 0, 100, self.gameParameter.opponentZone)
        self.opponentZoneSlider.change_value_signal.connect(self.opponentZoneSliderChange)
        layout.addWidget(self.opponentZoneSlider)

        self.robotZoneSlider = Slider("Robot Zone", 0, 100, self.gameParameter.robotZone)
        self.robotZoneSlider.change_value_signal.connect(self.robotZoneChange)
        layout.addWidget(self.robotZoneSlider)

        self.numPredictFrameSlider = Slider("Predict Frame", 0, 10, self.gameParameter.numPredictFrame)
        self.numPredictFrameSlider.change_value_signal.connect(self.numPredictFrameChange)
        layout.addWidget(self.numPredictFrameSlider)

        self.perspectiveSlider = Slider("Perspective Correct", 0, 200, self.gameParameter.perspective)
        self.perspectiveSlider.change_value_signal.connect(self.perspectiveSliderChange)
        layout.addWidget(self.perspectiveSlider)

        layout.addItem(QSpacerItem(20,20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(layout)

    # SLOT
    def opponentZoneSliderChange(self, v):
        self.gameParameter.opponentZone = v
        self.videoThread.reprocessFrame()

    def robotZoneChange(self, v):
        self.gameParameter.robotZone = v
        self.videoThread.reprocessFrame()

    def numPredictFrameChange(self, v):
        self.gameParameter.numPredictFrame = v
        self.videoThread.reprocessFrame()

    def perspectiveSliderChange(self, v):
        self.gameParameter.perspective = v
        self.imageProcessor.updatePerspectiveCorrection()
        self.videoThread.reprocessFrame()