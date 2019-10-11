from PyQt5.QtCore import QThread, pyqtSignal

'''连接摄像头的类 '''


class CameraConnector(QThread):
    signal = pyqtSignal(int)

    DISCONNECT = 0
    CONNECTING = 1
    CONNECTED = 2
    FAILED = 3

    def __init__(self, parent=None, url=None, cap=None):
        super(QThread, self).__init__(parent)
        self.url = url
        self.cap = cap

    # 0:disconnect
    # 1:connecting
    # 2:connected
    # 3:failed
    def run(self):
        self.signal.emit(self.CONNECTING)
        res = self.cap.open(self.url)
        if res:
            self.signal.emit(self.CONNECTED)
        else:
            self.signal.emit(self.FAILED)
