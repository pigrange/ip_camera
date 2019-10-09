import sys

import cv2
from PyQt5.QtWidgets import QApplication

from camera.util.frame_processor import FrameProcessor
from camera.view.player import MediaPlayer

BASE_URL = 'http://admin:admin@'


class IPCamera:

    def __init__(self):
        self.cap = cv2.VideoCapture()
        self.player = MediaPlayer(callback=self)
        size = self.player.get_expect_size()
        self.producer = FrameProcessor(size=size)
        self.producer.signal.connect(self.display_frame)

    def connect_camera(self, url):
        print(url)
        cam_url = 0 if url == '0' else BASE_URL + url
        # test_url = 'http://admin:admin@113.54.207.47:8081'
        res = self.cap.open(cam_url)

        # 成功打开
        if res:
            print('连接成功')
            self.producer.set_cap(self.cap)
            self.producer.start()
        else:
            print('连接失败')

    def show(self):
        self.player.show()

    # QThread处理完图片后回调此方法
    # running on main thread
    def display_frame(self, raw):
        self.player.set_frame(raw)

    # 停止线程的执行
    def stop(self):
        self.producer.stop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    camera = IPCamera()
    camera.show()
    sys.exit(app.exec_())
