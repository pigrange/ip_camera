from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow

from camera.view.base.Ui_MainWindow import Ui_MainWindow


class MediaPlayer(QMainWindow, Ui_MainWindow):
    exit_flag = False

    def __init__(self, parent=None, callback=None):
        super(MediaPlayer, self).__init__(parent)
        self.callback = callback
        self.setupUi(self)
        self.connect_btn.clicked.connect(self.on_connect_click)
        self.cancel_btn.clicked.connect(self.on_cancel_click)

    def get_expect_size(self):
        w = self.label.width()
        h = self.label.height()
        return w, h

    def set_frame(self, raw):
        pix_map = QtGui.QPixmap.fromImage(raw)
        self.label.setPixmap(pix_map)

    def on_cancel_click(self):
        self.callback.stop()
        self.close()

    def on_connect_click(self):
        url = self.camera_url.text()
        self.callback.connect_camera(url)

    def showEvent(self, a0: QtGui.QShowEvent):
        super().showEvent(a0)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        super().closeEvent(a0)
        self.exit_flag = True
