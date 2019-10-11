import cv2
from camera.util import pic_mosaic

DEFAULT_DISPLAY_COUNT = 6


# 旋转视频
def rotate(image, angle, center=None, scale=1.0):
    # 获取图像尺寸
    (h, w) = image.shape[:2]
    # 若未指定旋转中心，则将图像中心设为旋转中心
    if center is None:
        center = (w / 2, h / 2)
    pic = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, pic, (w, h))
    # 返回旋转后的图像
    return rotated


# 合并重叠人脸
def merge_faces(front_faces, profile_faces):
    if len(front_faces) == 0:
        return profile_faces

    if len(profile_faces) == 0:
        return front_faces

    res = front_faces.copy().tolist()

    for profile in profile_faces:
        overlap = False

        for front in front_faces:
            # 如果和其中一个矩形有重叠，就continue
            if is_overlap(front, profile):
                # print('has overlap')
                overlap = True
                break

        # 如果没有重叠，就把这个前脸加入
        if not overlap:
            res.append(profile)

    # print("face size", len(res))
    return res


# 人脸打码
def encrypt_face(img, rect):
    x, y, w, h = rect
    pic = img[y:y + h, x: x + w]
    pic_mosaic.encrypt_face(pic, rect)
    pass

    # 判断人脸是否重叠


def is_overlap(rect1, rect2):
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


def main(widow):
    face_cascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_alt2.xml')
    profile_cascade = cv2.CascadeClassifier('Cascades/haarcascade_profileface.xml')
    cam_url = 'http://admin:admin@10.252.252.13:8081/'
    cap = cv2.VideoCapture(cam_url)
    print(cap.isOpened())

    count = 0
    display_count = DEFAULT_DISPLAY_COUNT
    display_faces = []
    faces = []

    while True:
        ret, img = cap.read()
        img = rotate(img, 90)

        if count == 0:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转换灰色
            # 调用识别人脸
            small_frame = cv2.resize(gray, (0, 0), fx=0.5, fy=0.5)
            front_faces = face_cascade.detectMultiScale(small_frame, scaleFactor=1.2, minNeighbors=2, minSize=(16, 16))
            profile_faces = profile_cascade.detectMultiScale(small_frame, scaleFactor=1.2, minNeighbors=3,
                                                             minSize=(16, 16))
            faces = merge_faces(front_faces, profile_faces)

        if len(faces) != 0:
            display_count = DEFAULT_DISPLAY_COUNT
            display_faces = faces
        # 此次没有检测到人脸
        elif display_count != 0:
            display_count -= 1
        else:
            display_count = DEFAULT_DISPLAY_COUNT
            display_faces = faces

        for faceRect in display_faces:
            x, y, w, h = faceRect
            encrypt_face(img, (2 * x, 2 * y, 2 * h, 2 * w))

        count = (count + 1) % 3

        flag = widow.set_frame(img)
        if flag:
            break

        cv2.waitKey()

    cap.release()
    cv2.destroyAllWindows()

#
# def start():
#     app, win = player.initPlayer()
#     main(win)
#     sys.exit(app.exec_())
