import cv2
import numpy as np
import pytesseract
from constants.index import *

def crop(img, *coordinates):
    return img[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]]

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
# def get_grayscale(image):
#     return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
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
