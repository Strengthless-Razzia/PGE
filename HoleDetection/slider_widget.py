from PyQt5.QtWidgets import QWidget, QSlider, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal


class CustomSlider(QWidget):

    valueChangedSignal = pyqtSignal(float)

    def __init__(self, init_value = 0.0 , min = 0, max = 1, name = ""):
        super().__init__()
        self.min = min
        self.max = max
        self.name = name
        self.init_value = init_value
        self.sld = QSlider(Qt.Horizontal, self)

        self.initUI()

    def initUI(self):

        hbox = QHBoxLayout()

        self.sld.setRange(0, 100)
        self.sld.setFocusPolicy(Qt.NoFocus)
        self.sld.setPageStep(5)

        self.sld.valueChanged.connect(self.valueChanged)
        self.valueChangedSignal.connect(self.updateLabel)

        self.label = QLabel('', self)
        self.updateLabel(self.init_value)
        self.sld.setValue(int((self.init_value) / (self.max - self.min) *100))

        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label.setMinimumWidth(80)

        hbox.addWidget(QLabel(self.name))
        hbox.addWidget(self.sld)
        hbox.addSpacing(15)
        hbox.addWidget(self.label)
        self.setLayout(hbox)

        #self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('QSlider')
        self.show()

    def updateLabel(self, value):

        self.label.setText("{:.2f}".format(value))
    
    def valueChanged(self, value):
        self.valueChangedSignal.emit((self.max - self.min)*(value/100) + abs(self.min))
        