import cv2

FRONT_fACE_PATH = 'Cascades/haarcascade_frontalface_alt2.xml'
PROFILE_FACE_PATH = 'Cascades/haarcascade_profileface.xml'

'''人脸检测的相关类'''


class FaceDetector:
    detect_count = 0
    __cascades = []
    __last_detect_faces = []

    # 初始化
    def __init__(self):
        self.__cascades.append(cv2.CascadeClassifier(FRONT_fACE_PATH))
        self.__cascades.append(cv2.CascadeClassifier(PROFILE_FACE_PATH))

    # 合并重叠人脸
    def __merge_faces(self, front_faces, profile_faces):
        if len(front_faces) == 0:
            return profile_faces

        if len(profile_faces) == 0:
            return front_faces

        res = front_faces.copy().tolist()

        for profile in profile_faces:
            overlap = False

            for front in front_faces:
                # 如果和其中一个矩形有重叠，就continue
                if self.__is_overlap(front, profile):
                    overlap = True
                    break

            # 如果没有重叠，就把这个前脸加入
            if not overlap:
                res.append(profile)

        return res

        # 判断是否重叠

    # 判断是否重叠
    def __is_overlap(self, rect1, rect2):
        l1, t1, w1, h1 = rect1
        l2, t2, w2, h2 = rect2
        (l1, t1, w1, h1) = (l1 * 2, t1 * 2, w1 * 2, h1 * 2)
        (l2, t2, w2, h2) = (l2 * 2, t2 * 2, w2 * 2, h2 * 2)

        r1 = l1 + w1
        b1 = t1 + h1

        r2 = l2 + w2
        b2 = t2 + h2

        res = False

        res = res | (b1 < t2 & r1 < l2)
        res = res | (b1 < t2 & l1 > r2)
        res = res | (t1 > b2 & r1 < l2)
        res = res | (t1 > b2 & l1 > r2)

        res = not res
        return res

    # 获取人脸坐标
    def detect_faces(self, raw_img):
        self.detect_count = (self.detect_count + 1) % 4
        count = self.detect_count

        if count != 0:
            return self.__last_detect_faces

        gray = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)
        frame = cv2.resize(gray, (0, 0), fx=0.5, fy=0.5)

        faces = []
        cascades = self.__cascades

        faces_1 = cascades[0].detectMultiScale(frame, scaleFactor=1.2, minNeighbors=2, minSize=(16, 16))
        faces_2 = cascades[1].detectMultiScale(frame, scaleFactor=1.2, minNeighbors=3, minSize=(16, 16))

        faces = self.__merge_faces(faces_1, faces_2)
        self.__last_detect_faces = faces
        return faces
