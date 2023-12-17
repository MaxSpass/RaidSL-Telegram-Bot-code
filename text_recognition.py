import pytesseract
import cv2
import pyautogui
from helpers.screen import *
import uuid
import os
from pathlib import Path
from helpers.common import *

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

root_dir = 'E:/Main/BACKEND/core'
dir = 'demon-lord'
path = os.path.join(root_dir, dir)


def make_uniq_screenshot():
    if os.path.isdir(path) is False:
        os.mkdir(path)

    image_id = str(uuid.uuid4())
    image_output = os.path.join(path, "result-" + image_id + ".png")
    screenshot = pyautogui.screenshot(region=axis_to_region(184, 150, 687, 202))

    print(image_output)
    screenshot.save(image_output)


def check_results():
    files = os.listdir(path)
    # files = os.listdir(path)[slice(5)]
    results = []
    for i in range(len(files)):
        img_name = files[i]
        img_path = os.path.join(path, img_name)
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        threshold_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        text = pytesseract.image_to_string(threshold_img)
        results.append(text)

    for i in range(len(results)):
        print(results[i])


def capture_demon_lord_result():
    return read_text_in_region(axis_to_region(184, 150, 687, 202))


def read_text_in_region(region):
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save(r"E:\Main\BACKEND\core\text.png")
    img = cv2.imread(r"E:\Main\BACKEND\core\text.png")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    threshold_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_string(threshold_img)
    return text


# check_results()
