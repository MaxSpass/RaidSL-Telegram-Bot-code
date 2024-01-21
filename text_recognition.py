from helpers.screen import *
from helpers.common import *
from pathlib import Path
import pytesseract
import cv2
import pyautogui
import uuid
import os

def get_demon_lord_path():
    root_dir = os.getcwd()
    dir = 'demon-lord'
    path = os.path.join(root_dir, dir)

    return path


def make_uniq_screenshot():
    path = get_demon_lord_path()
    if os.path.isdir(path) is False:
        os.mkdir(path)

    image_id = str(uuid.uuid4())
    image_output = os.path.join(path, "result-" + image_id + ".png")
    screenshot = pyautogui.screenshot(region=axis_to_region(184, 150, 687, 202))
    screenshot.save(image_output)


def check_results():
    path = get_demon_lord_path()
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
