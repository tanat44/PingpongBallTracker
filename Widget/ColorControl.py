from PyQt5.QtWidgets import (QSizePolicy, QWidget, QSlider, QVBoxLayout, QLabel, QPushButton)
from Widget.Slider import Slider

class ColorControl(QWidget):

    def __init__(self, videoThread):
        super().__init__()
        self.videoThread = videoThread
        colorThreshold = self.videoThread.imageProcessor.colorThreshold

        layout = QVBoxLayout()        

        self.hMinSlider = Slider("H Min", 0, 179, colorThreshold.h_min)
        self.hMinSlider.change_value_signal.connect(self.hMinSliderChange)
        layout.addWidget(self.hMinSlider)
        self.hMaxSlider = Slider("H Max", 0, 179, colorThreshold.h_max)
        self.hMaxSlider.change_value_signal.connect(self.hMaxSliderChange)
        layout.addWidget(self.hMaxSlider)

        self.sMinSlider = Slider("S Min", 0, 255, colorThreshold.s_min)
        self.sMinSlider.change_value_signal.connect(self.sMinSliderChange)
        layout.addWidget(self.sMinSlider)
        self.sMaxSlider = Slider("S Max", 0, 255, colorThreshold.s_max)
        self.sMaxSlider.change_value_signal.connect(self.sMaxSliderChange)
        layout.addWidget(self.sMaxSlider)

        self.vMinSlider = Slider("V Min", 0, 255, colorThreshold.v_min)
        self.vMinSlider.change_value_signal.connect(self.vMinSliderChange)
        layout.addWidget(self.vMinSlider)
        self.vMaxSlider = Slider("V Max", 0, 255, colorThreshold.v_max)
        self.vMaxSlider.change_value_signal.connect(self.vMaxSliderChange)
        layout.addWidget(self.vMaxSlider)

        self.setLayout(layout)

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