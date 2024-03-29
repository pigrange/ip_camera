import copy

_SPLIT_NUM = 20
_MAP = [17, 19, 10, 15, 18, 14, 11, 13, 16, 12]


# 外部调用的打码人脸的方法
def encrypt_face(img, rect):
    x, y, w, h = rect
    pic = img[y:y + h, x: x + w]
    __encrypt(pic)
    pass


# 实际的打码图片的方法
def __encrypt(pic):
    shape = pic.shape
    height = shape[0]
    width = shape[1]
    width_base = int(width / _SPLIT_NUM)
    height_base = int(height / _SPLIT_NUM)
    count = int(_SPLIT_NUM / 2)

    for i in range(0, count):
        j = _MAP[i]
        row1 = copy.copy(pic[0:height, i * width_base:(i + 1) * width_base])
        row2 = copy.copy(pic[0:height, j * width_base:(j + 1) * width_base])
        pic[0:height, j * width_base:(j + 1) * width_base] = row1
        pic[0:height, i * width_base:(i + 1) * width_base] = row2
        col1 = copy.copy(pic[i * height_base:(i + 1) * height_base, 0:width])
        col2 = copy.copy(pic[j * height_base: (j + 1) * height_base, 0:width])
        pic[j * height_base: (j + 1) * height_base, 0:width] = col1
        pic[i * height_base:(i + 1) * height_base, 0:width] = col2

    return pic


# 解除打码人脸的方法
def __decrypt(pic):
    shape = pic.shape
    height = shape[0]
    width = shape[1]
    width_base = int(width / _SPLIT_NUM)
    height_base = int(height / _SPLIT_NUM)
    count = int(_SPLIT_NUM / 2)

    for i in range(0, count):
        j = _MAP[i]
        col1 = copy.copy(pic[i * height_base:(i + 1) * height_base, 0:width])
        col2 = copy.copy(pic[j * height_base: (j + 1) * height_base, 0:width])
        pic[i * height_base:(i + 1) * height_base, 0:width] = col2
        pic[j * height_base: (j + 1) * height_base, 0:width] = col1
        row1 = copy.copy(pic[0:height, i * width_base:(i + 1) * width_base])
        row2 = copy.copy(pic[0:height, j * width_base:(j + 1) * width_base])
        pic[0:height, i * width_base:(i + 1) * width_base] = row2
        pic[0:height, j * width_base:(j + 1) * width_base] = row1

    return pic
