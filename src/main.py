import sys

import cv2
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal

from camera.core.frame_processor import FrameProcessor
from camera.core.camera_connector import CameraConnector
from camera.view.player import MediaPlayer
from threading import Thread

BASE_URL = 'http://admin:admin@'

STATE_UNCONNECTED = 0
STATE_CONNECTING = 1
STATE_CONNECTED = 2


class IPCamera:
    # 0:unconnected
    # 1:connecting
    # 2:connected
    camera_state = 0

    def __init__(self):
        self.cap = cv2.VideoCapture()
        self.player = MediaPlayer(callback=self)
        self.expect_screen_size = self.player.get_expect_size()
        self.producer = None
        self.connector = None

    def init_frame_processor(self):
        self.producer = FrameProcessor(size=self.expect_screen_size)
        self.producer.signal.connect(self.display_frame)
        self.producer.set_cap(self.cap)

    def on_click(self, url):
        # 0:unconnected
        if self.camera_state == STATE_UNCONNECTED:
            self.connect_camera(url)
        # 1:connecting
        elif self.camera_state == STATE_CONNECTING:
            return
        # 2:connected
        elif self.camera_state == STATE_CONNECTED:
            self.stop_process_frame()

    def connect_camera(self, url):
        if len(url) == 0:
            self.on_connect_event(CameraConnector.FAILED)
            return
        cam_url = 0 if url == '0' else BASE_URL + url
        self.connector = CameraConnector(url=cam_url, cap=self.cap)
        self.connector.signal.connect(self.on_connect_event)
        self.connector.start()

    def on_connect_event(self, res):
        # 1:connecting
        if res == CameraConnector.CONNECTING:
            self.camera_state = STATE_CONNECTING
            self.player.on_connecting()
        # 2:connected
        elif res == CameraConnector.CONNECTED:
            self.camera_state = STATE_CONNECTED
            self.player.on_connected()
            self.start_process_frame()
        # 3:failed
        elif res == CameraConnector.FAILED:
            self.camera_state = STATE_UNCONNECTED
            self.player.on_connect_fail()
        # 4:disconnect
        elif res == CameraConnector.DISCONNECT:
            self.camera_state = STATE_UNCONNECTED
            self.player.on_disconnect()

    def start_process_frame(self):
        self.init_frame_processor()
        self.producer.start()

    # 停止线程的执行
    def stop_process_frame(self):
        if self.producer is not None:
            self.producer.stop()
        # self.producer = None
        self.on_connect_event(CameraConnector.DISCONNECT)

    def show_player(self):
        self.player.show()

    def rotate(self, angle):
        if self.producer is not None:
            self.producer.rotate(angle)

    # QThread处理完图片后回调此方法
    def display_frame(self, raw):
        if self.camera_state == STATE_CONNECTED:
            self.player.on_frame(raw)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    camera = IPCamera()
    camera.show_player()
    sys.exit(app.exec_())
