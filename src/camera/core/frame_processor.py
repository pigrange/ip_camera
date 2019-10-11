from threading import Lock

import cv2
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal

import camera.core.face_mosaic as mosaic
from camera.core.face_detector import FaceDetector

'''处理视频帧的类'''


class FrameProcessor(QThread):
    DEFAULT_DISPLAY_COUNT = 18

    # 同步锁
    lock = Lock()

    # 优化face_rect使用
    # 当某一帧face_Rect突然消失的时候，我们暂时认为是没有检测到人脸
    display_count = DEFAULT_DISPLAY_COUNT
    display_faces = []

    rotate_angle = 90

    # 图像转码使用
    rgb = cv2.COLOR_BGR2RGB
    rgb888 = QtGui.QImage.Format_RGB888
    scale = 1.0

    signal = pyqtSignal(QtGui.QImage)
    finish = False

    # 设置摄像头
    def set_cap(self, cap):
        self.cap = cap

    def __init__(self, parent=None, size=None):
        super(FrameProcessor, self).__init__(parent)
        self.detector = FaceDetector()
        self.mosaic = mosaic
        self.size = size
        self.cap = None

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

            if self.is_finish():
                self.cap.release()
                return

            res, raw = self.cap.read()
            img = self.rotate_img(raw, self.rotate_angle)

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

    # 判断事件循环是否结束
    def is_finish(self):
        self.lock.acquire()
        res = self.finish
        self.lock.release()
        return res

    # 用于某一次未检测到人脸时的判断
    # 如果上一次检测到了有效的人脸,但是这一次未检测到，这种情况
    # 我们认为是环境导致的摄像头失败判断，因为提供一个计数器
    # 让人脸未被探测到的时候face_rects仍然有效一段时间
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
    # 外部调用,实际是修改成员变量rotate_angle的值
    def rotate(self, angle):
        self.rotate_angle += angle
        if self.rotate_angle < 0:
            self.rotate_angle += 360
        self.rotate_angle %= 360

    # 旋转图片
    # 实际旋转图片的方法
    def rotate_img(self, image, angle):
        # 获取图像尺寸
        (h, w) = image.shape[:2]
        # 若未指定旋转中心，则将图像中心设为旋转中心
        center = (w / 2, h / 2)
        pic = cv2.getRotationMatrix2D(center, angle, self.scale)
        rotated = cv2.warpAffine(image, pic, (w, h))
        # 返回旋转后的图像
        return rotated

    # 线程执行时被调用
    def run(self):
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
