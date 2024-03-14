from PyQt6 import QtWidgets
import sys
import serial
from pathlib import Path


class ZPLWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("ZPL demonstration")
        self.resize(300, 100)

        self.combobox = QtWidgets.QComboBox(self)
        self.combobox.addItems(["console", "COM1"])

        self.buttom = QtWidgets.QPushButton("Send", self)
        self.buttom.clicked.connect(self.on_clicked)

        vbox = QtWidgets.QVBoxLayout(self)
        vbox.addWidget(self.combobox)
        vbox.addWidget(self.buttom)

        self.port = serial.Serial()

        file = Path('label.zpl')
        self.label = file.read_bytes() 

    def on_clicked(self):
        if self.combobox.currentIndex() == 0:
            print(self.label.decode("utf8"))
        elif self.combobox.currentIndex() == 1:
            if self.port.is_open:
                self.port.close()
            self.port.port = self.combobox.currentText()
            self.port.baudrate = 9600
            self.port.open()
            self.port.write(self.label)
            self.port.flush()
            self.port.close()            

def Main(args):
    app = QtWidgets.QApplication(args)
    form = ZPLWidget()
    form.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    Main(sys.argv)