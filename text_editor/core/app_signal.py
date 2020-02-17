from PyQt5.QtCore import QObject, pyqtSignal


class AppSignal(QObject):
    SIGNAL = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)

    def connect(self, slot):
        self.SIGNAL.connect(slot)

    def emit(self):
        self.SIGNAL.emit()