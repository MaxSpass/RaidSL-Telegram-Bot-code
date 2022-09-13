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
# img = cv2.imread('images/screens/collection.png')
# img_crop = screen_heroes_panel.crop(img)

img = cv2.imread('images/screens/quests.png', cv2.IMREAD_UNCHANGED)
img_quests = crop(img, *COORDINATES_QUESTS)
img_quest_1 = crop(img_quests, *COORDINATES_QUESTS_1)

# img_in_work = img_quests
img_in_work = img_quest_1

img_prepared = apply_image_actions_before_determine_text(img_in_work, TYPE_QUESTS_ITEM)

img_final = determine_text_blocks(img_in_work)

text = get_text(img_prepared)
text_occurrences = get_percentage_of_occurrences(text, TEXT_QUEST_CONDITION_FIGHT_5_TIMES)
print(text_occurrences)

# cv2.imshow('Result 1', img_final)
# cv2.imshow('Result 2', img_prepared)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

cv2.waitKey(0)