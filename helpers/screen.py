import os
import cv2
import numpy as np
import pytesseract
from constants.index import *

def crop(img, *coordinates):
    return img[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]]


def crop_matrix(img, cols, rows):
    width = round(img.shape[1] / cols)
    height = round(img.shape[0] / rows)
    # matrix = np.ones((rows, cols), dtype=np.int32)
    matrix = np.arange(cols * rows).reshape(rows, cols)

    # print(width, height)

    # Temp
    dirname = 'sliced'
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    for index_row, row in enumerate(matrix):
        for index_col, col in enumerate(row):
            # print(index_row, index_col)
            x1 = width * index_col
            y1 = height * index_row
            # coordinates = (x1, y1, x1 + width, y1 + height)
            coordinates = (x1, y1, x1 + width, y1 + height)

            # Temp
            file_name = f'{index_row}-{index_col}.jpg'
            img_n = crop(img, *coordinates)
            img_output = os.path.join(dirname, file_name)
            cv2.imwrite(img_output, img_n)

            # cv2.imshow('Result 2', img_n)
            # cv2.waitKey(0)

            # matrix[index_row][index_col] = coordinates
            # matrix[index_row][index_col] = coordinates
            # print(matrix[index_row][index_col])

        # for y in x:
        #     print(y)

    # print(width, height)




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
