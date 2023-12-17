import os
import cv2
import numpy as np
import pytesseract
from classes.window_mgr import *
from constants.index import *
from skimage.metrics import structural_similarity as ssim
import numpy as np
import cv2

def prepare_window():
    w = WindowMgr()
    w.find_window_wildcard(".*%s*" % GAME_WINDOW)
    w.adjust_window()
    w.set_foreground()
    return w

def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


def crop(img, *coordinates):
    return img[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]]


def crop_percentage(img, *coordinates_percentage):
    w = img.shape[1]
    h = img.shape[0]

    coordinates = list(map(round, [
        coordinates_percentage[0] * w / 100,
        coordinates_percentage[1] * h / 100,
        coordinates_percentage[2] * w / 100,
        coordinates_percentage[3] * h / 100,
    ]))

    return img[
           coordinates[1]:coordinates[3],
           coordinates[0]:coordinates[2]
           ]


def percentage_coordinates(img, *coordinates):
    w = img.shape[1]
    h = img.shape[0]
    return list(map(round, [
        coordinates[0] * 100 / w,
        coordinates[1] * 100 / h,
        coordinates[2] * 100 / w,
        coordinates[3] * 100 / h
    ]))


def crop_matrix(img, cols, rows):
    width = round(img.shape[1] / cols)
    height = round(img.shape[0] / rows)
    # matrix = np.ones((rows, cols), dtype=np.int32)
    matrix = np.arange(cols * rows).reshape(rows, cols)
    res_1 = []
    # print(width, height)

    for index_row, row in enumerate(matrix):
        res_2 = []
        for index_col, col in enumerate(row):
            x1 = width * index_col
            y1 = height * index_row
            coordinates = (x1, y1, x1 + width, y1 + height)
            img_n = crop(img, *coordinates)
            res_2.append(img_n)

        res_1.append(res_2)

    return res_1


def compare_two_images(img_1, img_2):
    # Approach #1 | Calculate the histograms, set bin for (255, 255, 255) to 0, and normalize them
    hist_img1 = cv2.calcHist([img_1], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
    hist_img1[255, 255, 255] = 0
    cv2.normalize(hist_img1, hist_img1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    hist_img2 = cv2.calcHist([img_2], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
    hist_img2[255, 255, 255] = 0
    cv2.normalize(hist_img2, hist_img2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

    # Approach #2 | Calculate the histograms, and normalize them
    # hist_img1 = cv2.calcHist([img_1], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
    # cv2.normalize(hist_img1, hist_img1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    # hist_img2 = cv2.calcHist([img_2], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
    # cv2.normalize(hist_img2, hist_img2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

    # Find the metric value
    # metric_val = cv2.compareHist(hist_img1, hist_img2, cv2.HISTCMP_CORREL)
    metric_val = abs(round(cv2.compareHist(hist_img1, hist_img2, cv2.HISTCMP_CORREL) * 100))

    return metric_val

def cut_image_center(img, w, h):
    img_w = img.shape[1]
    img_h = img.shape[0]
    x1 = round(img_w / 2 - w / 2)
    y1 = round(img_h / 2 - h / 2)
    x2 = round(img_w / 2 + w / 2)
    y2 = round(img_h / 2 + h / 2)
    coordinates = (x1, y1, x2, y2)

    return crop(img, *coordinates)



def compare_images(img_1, img_2):
    # print(img_1.shape, img_2.shape)

    img_1_grey = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
    # img_2_resized = cv2.resize(img_2, (img_1.shape[1], img_1.shape[0]), interpolation=cv2.INTER_AREA)
    img_2_resized = image_resize(img_2, width=img_1.shape[1])

    # @TODO Should refactor
    if img_1.shape[0] < img_2_resized.shape[0]:
        diff = img_2_resized.shape[0] - img_1.shape[0]
        coordinates = (0, 0, img_2_resized.shape[1], img_2_resized.shape[0] - diff)
        img_2_resized = crop(img_2_resized, *coordinates)

    img_2_grey = cv2.cvtColor(img_2_resized, cv2.COLOR_BGR2GRAY)

    return round(ssim(img_1_grey, img_2_grey) * 100)


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized


def detect_hero(img_compared, *percentage_coordinates):
    dir = os.path.join('images', 'avatars')
    # dir = os.path.join('db', 'heroes')
    # dir = os.path.join('db', 'heroes_from_game')
    counter = 0
    name = ""
    for subdir, dirs, files in os.walk(dir):
        for file_name in files:
            frame = cv2.imread(os.path.join(subdir, file_name))
            frame_changed = crop_percentage(frame, *percentage_coordinates)
            metric_val = compare_images(img_compared, frame_changed)

            if counter < metric_val:
                counter = metric_val
                name = file_name

    return name


def detect_heroes_from_matrix(matrix, *coordinates):
    res_1 = []

    for index_row, row in enumerate(matrix):
        res_2 = []
        for index_col, col in enumerate(row):
            img = crop(matrix[index_row][index_col], *coordinates)
            p_coordinates = percentage_coordinates(matrix[index_row][index_col], *coordinates)
            hero = detect_hero(img, *p_coordinates)
            res_2.append(hero)

        res_1.append(res_2)

    return np.array(res_1)


def get_borders(image):
    img = image
    rsz_img = cv2.resize(img, None, fx=0.25, fy=0.25)  # resize since image is huge
    gray = cv2.cvtColor(rsz_img, cv2.COLOR_BGR2GRAY)  # convert to grayscale

    # threshold to get just the signature
    retval, thresh_gray = cv2.threshold(gray, thresh=100, maxval=255, type=cv2.THRESH_BINARY)

    # find where the signature is and make a cropped region
    points = np.argwhere(thresh_gray == 0)  # find where the black pixels are
    points = np.fliplr(points)  # store them in x,y coordinates instead of row,col indices
    x, y, w, h = cv2.boundingRect(points)  # create a rectangle around those points
    x, y, w, h = x - 10, y - 10, w + 20, h + 20  # make the box a little bigger
    crop = gray[y:y + h, x:x + w]  # create a cropped region of the gray image

    # get the thresholded crop
    retval, thresh_crop = cv2.threshold(crop, thresh=200, maxval=255, type=cv2.THRESH_BINARY)

    # display
    cv2.imshow("Cropped and thresholded image", thresh_crop)
    cv2.waitKey(0)


def get_center_square(img, size=40):
    width = img.shape[1]
    height = img.shape[0]
    size_half = size / 2
    x1 = int(round(width / 2) - size_half)
    y1 = int(round(height / 2) - size_half)
    x2 = int(x1 + size)
    y2 = int(y1 + size)

    return crop(img, *(x1, y1, x2, y2))


def apply_image_actions_before_determine_text(img, img_type):
    if img_type == TYPE_QUESTS_ITEM:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0, 0, 130])
        upper_red = np.array([255, 255, 255])
        mask = cv2.inRange(hsv, lower_red, upper_red)
        res = cv2.bitwise_and(img, img, mask=mask)

        return res
    else:
        return img


def get_text(img):
    text_extracted = pytesseract.image_to_string(img)

    return text_extracted.strip()


def determine_text_blocks(img):
    # Load image, grayscale, Otsu's threshold
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    return thresh


def get_percentage_of_occurrences(str, entry):
    arr = str.lower().split()
    counter = 0

    for item in arr:
        if entry.find(item) != -1:
            counter += 1

    return round(counter * 100 / len(arr))

def clear_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

# # get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#
#
# # noise removal
# def remove_noise(image):
#     return cv2.medianBlur(image, 2)
#
#
# # thresholding
# def thresholding(image):
#     return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
# # dilation
# def dilate(image):
#     kernel = np.ones((5, 5), np.uint8)
#     return cv2.dilate(image, kernel)
#
#
# # erosion
# def erode(image):
#     kernel = np.ones((5, 5), np.uint8)
#     return cv2.erode(image, kernel)
#
#
# # opening - erosion followed by dilation
# def opening(image):
#     kernel = np.ones((5, 5), np.uint8)
#     return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
#
#
# # canny edge detection
# def canny(image):
#     return cv2.Canny(image, 100, 200)
#
#
# # template matching
# def match_template(image, template):
#     return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
