import os
import cv2
import pytesseract
import numpy as np
from helpers.screen import *
from constants.index import *
from classes.test import *

# from pytesseract import Output
# from classes.screen_manager import ScreenManagerPercentage

# @TODO Does not work
# base_path = os.getcwd()
# pytesseract.pytesseract.tesseract_cmd = os.path.join(base_path, "tesseract.exe")
# print('base_path', base_path)


# Get other running processes window sizes in Python
# https://stackoverflow.com/questions/151846/get-other-running-processes-window-sizes-in-python

# PyAutoGUI
# https://github.com/asweigart/pyautogui

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"


# screen_heroes_panel0 = ScreenManagerPercentage(**{
#     "width": 22.0556,
#     "height": 66.4107,
#     "offset_x": 1.4989,
#     "offset_y": 16.6986,
# })
# print(screen_heroes_panel0.x1, screen_heroes_panel0.x2)
# print(screen_heroes_panel0.y1, screen_heroes_panel0.y2)

# screen_heroes_panel = ScreenManager(*COORDINATES_PANEL_HEROES)
img = cv2.imread('images/screens/collection.png')
img_crop = crop(img, *COORDINATES_PANEL_HEROES)
#
# img = cv2.imread('images/screens/quests.png', cv2.IMREAD_UNCHANGED)
# img_quests = crop(img, *COORDINATES_QUESTS)
# img_quest_1 = crop(img_quests, *COORDINATES_QUESTS_1)

# img_in_work = img_quests
# img_in_work = img_quest_1

# img_prepared = apply_image_actions_before_determine_text(img_in_work, TYPE_QUESTS_ITEM)
# img_final = determine_text_blocks(img_in_work)

# text = get_text(img_prepared)
# text_occurrences = get_percentage_of_occurrences(text, TEXT_QUEST_CONDITION_FIGHT_5_TIMES)
# print(text_occurrences)

# cv2.imshow('Result 1', img_final)
# cv2.imshow('Result 2', img_prepared)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# img_crop_test = crop(img_crop, *(0, 0, 10, 20))

# crop_matrix(img_crop, cols=3, rows=4)

# Should try 1: https://geekyhumans.com/compare-two-images-and-highlight-differences-using-python/
# Should try 2: https://stackoverflow.com/questions/189943/how-can-i-quantify-difference-between-two-images

img_1 = cv2.imread(os.path.join('sliced', '1-0.jpg'))
# img_2 = cv2.imread(os.path.join('images', 'avatars', 'avatar_arbiter.jpg'))
# img_2 = cv2.imread(os.path.join('images', 'avatars', 'avatar_arbiter2.jpg'))
img_2 = cv2.imread(os.path.join('images', 'avatars', 'avatar_arbiter2.png'))

# Resize image
img_2_resized = cv2.resize(img_2, (img_1.shape[1], img_1.shape[0]), interpolation=cv2.INTER_AREA)
img_1_center = get_center_square(img_1)
img_2_center = get_center_square(img_2_resized)
metric_val = compare_two_images(img_1_center, img_2_center)

# metric_val = compare_two_images(img_1, img_2_resized)
# metric_val = compare_two_images(img_1, img_2)

cv2.imshow('Result 1', img_1_center)
cv2.imshow('Result 2', img_2_center)
# cv2.imshow('Result 2', img_2_resized)

print(metric_val)

cv2.waitKey(0)
cv2.destroyAllWindows()