from threading import Lock, Timer

import cv2
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtGui

from camera.util.face_detector import FaceDetector
import camera.util.pic_mosaic as mosaic


class FrameProcessor(QThread):
    DEFAULT_DISPLAY_COUNT = 18

    # 同步锁
    lock = Lock()

    # 优化face_rect使用
    # 当某一帧face_Rect突然消失的时候，我们暂时认为是没有检测到人脸
    display_count = DEFAULT_DISPLAY_COUNT
    display_faces = []

    # 图像转码使用
    rgb = cv2.COLOR_BGR2RGB
    rgb888 = QtGui.QImage.Format_RGB888
    scale = 1.0

    signal = pyqtSignal(QtGui.QImage)
    finish = False

    def set_cap(self, cap):
        self.cap = cap

    def __init__(self, parent=None, size=None):
        super(FrameProcessor, self).__init__(parent)
        self.detector = FaceDetector()
        self.mosaic = mosaic
        self.size = size

    # 转化图像格式
    def compress_img(self, img):

        if self.size is not None:
            img = cv2.resize(img, self.size)

        raw = cv2.cvtColor(img, self.rgb)

        h, w, byte_per_line = raw.shape

        res = QtGui.QImage(raw.data, w, h, w * 3, self.rgb888)
        return res

    # 轮询
    def poll_frame(self):

        while True:
            res, raw = self.cap.read()
            img = self.rotate_img(raw, 90)

            if not res:
                return

            raw_faces = self.detector.detect_faces(img)
            faces = self.fill_missed_face(raw_faces)

            for face_rect in faces:
                x, y, w, h = face_rect
                self.mosaic.encrypt_face(img, (2 * x, 2 * y, 2 * h, 2 * w))

            display = self.compress_img(img)

            # 回调主线程显示
            self.signal.emit(display)

            # 加锁判断线程是否结束
            self.lock.acquire()
            if self.finish:
                self.lock.release()
                return

            # 立即释放锁
            self.lock.release()

        # # 使用timer重启
        # t = Timer(0.016, self.poll_frame)
        # t.start()

    def fill_missed_face(self, faces):
        if len(faces) != 0:
            self.display_count = self.DEFAULT_DISPLAY_COUNT
            self.display_faces = faces

        elif self.display_count != 0:
            self.display_count -= 1

        else:
            self.display_count = self.DEFAULT_DISPLAY_COUNT
            self.display_faces = faces

        return self.display_faces

    # 旋转图片
    def rotate_img(self, image, angle):
        # 获取图像尺寸
        (h, w) = image.shape[:2]
        # 若未指定旋转中心，则将图像中心设为旋转中心
        center = (w / 2, h / 2)
        pic = cv2.getRotationMatrix2D(center, angle, self.scale)
        rotated = cv2.warpAffine(image, pic, (w, h))
        # 返回旋转后的图像
        return rotated

    def run(self):
        # super().run()

        if self.cap is None:
            return
        else:
            self.poll_frame()

    # 获取锁，表示finish
    def stop(self):
        lock = self.lock
        lock.acquire()
        self.finish = True
        lock.release()
