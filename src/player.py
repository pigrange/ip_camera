import sys
import cv2

from PyQt5 import QtGui
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QApplication, QMainWindow

from src.view import Ui_MainWindow


class MyWindow(QMainWindow, Ui_MainWindow):
    exit_flag = False

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.connect_btn.clicked.connect(self.onOkClick)
        self.cancel_btn.clicked.connect(self.onCancelClick)

    def loadImg(self, img):
        win_width = self.label.width()
        win_height = self.label.height()
        img = cv2.resize(img, (win_width, win_height))
        h, w, byte_per_line = img.shape
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
        res = QtGui.QImage(img.data, w, h, 3 * w, QImage.Format_RGB888)
        return res

    def setImg(self, raw):
        img = self.loadImg(raw)
        pix_map = QtGui.QPixmap.fromImage(img)
        self.label.setPixmap(pix_map)
        return self.exit_flag

    def onCancelClick(self):
        self.close()

    def onOkClick(self):
        self.close()

    def showEvent(self, a0: QtGui.QShowEvent):
        super().showEvent(a0)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        super().closeEvent(a0)
        self.exit_flag = True


def initPlayer():
    app = QApplication(sys.argv)
    my_win = MyWindow()
    my_win.show()
    return app, my_win
