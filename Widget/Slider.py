from PyQt5.QtWidgets import (QWidget, QSlider, QHBoxLayout,
                             QLabel, QApplication)
from PyQt5.QtCore import Qt


class Slider(QWidget):

    def __init__(self, name="Unknown", min=0, max=100, defaultValue = 50):
        super().__init__()
        hbox = QHBoxLayout()
        sld = QSlider(Qt.Horizontal, self)
        sld.setRange(min, max)
        sld.setValue(defaultValue)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setPageStep(1)
        sld.valueChanged.connect(self.updateLabel)
        
        
        self.nameLabel = QLabel(name, self)
        self.nameLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        

        self.valueLabel = QLabel(str(defaultValue), self)
        self.valueLabel.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.valueLabel.setMinimumWidth(80)
        
        hbox.addSpacing(15)
        hbox.addWidget(self.nameLabel)
        hbox.addWidget(sld)
        hbox.addWidget(self.valueLabel)

        self.setLayout(hbox)

    def updateLabel(self, value):
        self.valueLabel.setText(str(value))