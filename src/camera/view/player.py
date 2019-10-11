from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow

from camera.view.base.Ui_MainWindow import Ui_MainWindow

'''UI窗口'''


class MediaPlayer(QMainWindow, Ui_MainWindow):
    __TEXT_CONNECTED = "已连接"
    __TEXT_UNCONNECTED = "未连接"
    __TEXT_DISCONNECT = "断开连接"
    __TEXT_CONNECT = "连接"
    __TEXT_CONNECTING = "连接中"
    __TEXT_CONNECT_FAIL = "连接失败"

    def __init__(self, parent=None, callback=None):
        super(MediaPlayer, self).__init__(parent)
        self.callback = callback
        self.setupUi(self)
        self.bind_view()

    def bind_view(self):
        self.connect_btn.clicked.connect(self.on_connect_click)
        self.cancel_btn.clicked.connect(self.on_cancel_click)
        self.rotate_left_btn.clicked.connect(self.rotate_left)
        self.rotate_right_btn.clicked.connect(self.rotate_right)

    def get_expect_size(self):
        w = self.label.width()
        h = self.label.height()
        return w, h

    def on_frame(self, raw):
        pix_map = QtGui.QPixmap.fromImage(raw)
        self.label.setPixmap(pix_map)

    def on_cancel_click(self):
        self.callback.stop_process_frame()
        self.close()

    def on_connect_click(self):
        url = self.camera_url.text()
        self.callback.on_click(url)

    def rotate_left(self):
        self.callback.rotate(90)

    def rotate_right(self):
        self.callback.rotate(-90)

    def on_connecting(self):
        self.connect_state.setText(self.__TEXT_CONNECTING)
        self.camera_url.clear()

    def on_connect_fail(self):
        self.connect_state.setText(self.__TEXT_CONNECT_FAIL)

    def on_connected(self):
        self.connect_state.setText(self.__TEXT_CONNECTED)
        self.connect_btn.setText(self.__TEXT_DISCONNECT)

    def on_disconnect(self):
        self.label.clear()
        self.connect_btn.setText(self.__TEXT_CONNECT)
        self.connect_state.setText(self.__TEXT_UNCONNECTED)
