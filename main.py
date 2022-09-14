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
# img_compared = crop(img_crop, *COORDINATES_AVATAR_RECOGNIZE_AREA)

test_db_heroes = {
    4710: "Lidia",
}


def split_name(str):
    return str.split('.')[0]


# blanked_img_1 = np.zeros([512,512,1],dtype=np.uint8)
# blanked_img_1.fill(255)
# blanked_img_2 = np.zeros([512,512,1],dtype=np.uint8)
# blanked_img_2.fill(130)
# blanked_img_3 = cv2.merge((blanked_img_1, blanked_img_2))

img_entry_1 = cv2.imread('images/screens/collection_1.png')
img_entry_2 = cv2.imread('images/screens/collection_2.png')

# img_entry = img_entry_1
img_entry = img_entry_2

img_entry_crop = crop(img_entry, *COORDINATES_PANEL_HEROES)

# Sliced: Aspect ratio: 1,264705
# Aspect ratio images from DB: 1,2987
matrix_heroes = crop_matrix(img_entry_crop, cols=3, rows=4)
img = matrix_heroes[2][0]
# p_coordinates = percentage_coordinates(img, *COORDINATES_AVATAR_RECOGNIZE_AREA)
# img_crop = crop(img, *COORDINATES_AVATAR_RECOGNIZE_AREA)
# detected_hero = detect_hero(img_crop, *p_coordinates)
# hero_title = split_name(detected_hero)
# print(hero_title)

# get_borders(cv2.imread('images/for_test/signature.jpg'))
# Detects heroes
detected_heroes = detect_heroes_from_matrix(matrix_heroes, *COORDINATES_AVATAR_RECOGNIZE_AREA)
heroes_list = list(map(split_name, detected_heroes.flatten()))
print(heroes_list)

# print(p_coordinates)

# p_coordinates = percentage_coordinates(img_crop, *COORDINATES_AVATAR_RECOGNIZE_AREA)
# detected_hero_id = detect_hero(img_crop, *p_coordinates)
# print(detected_hero_id)

# print(img.shape)
# cv2.imshow('Result 1', crop(img_entry_1, *COORDINATES_PANEL_HEROES))
# cv2.imshow('Result 2', crop(img_entry_2, *COORDINATES_PANEL_HEROES))
# cv2.imshow('Result 2', matrix_heroes[0][2])
cv2.waitKey(0)

# Should try 1: https://geekyhumans.com/compare-two-images-and-highlight-differences-using-python/

# img_1 = cv2.imread(os.path.join('images', 'for_test', 'test_1.png'))
# img_2 = cv2.imread(os.path.join('images', 'for_test', 'test_2.png'))

img_1 = cv2.imread(os.path.join('sliced', '0-0.jpg'))
# img_1 = cv2.imread(os.path.join('sliced', '1-0.jpg'))
# img_1 = cv2.imread(os.path.join('sliced', '2-0.jpg'))
# img_2 = cv2.imread(os.path.join('images', 'avatars', 'avatar_arbiter.jpg'))
# img_2 = cv2.imread(os.path.join('images', 'avatars', 'avatar_lydia.jpg'))
# img_2 = cv2.imread(os.path.join('images', 'avatars', 'avatar_lydia.png'))
# img_2 = cv2.imread(os.path.join('images', 'avatars', 'avatar_huntmaster.jpg'))
# img_2 = cv2.imread(os.path.join('images', 'avatars', 'avatar_arbiter2.png'))
# img_2 = cv2.imread(os.path.join('images', 'avatars', 'avatar_arbiter2.jpg'))
# img_2 = cv2.imread(os.path.join('images', 'avatars', 'avatar_arbiter2-1.jpg'))

# img_png = cv2.imread(os.path.join('images', 'avatars', 'avatar_lydia.png'))
# cv2.imwrite('avatar_lydia.jpg', img_png, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

# img_1_scaled = get_center_square(cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY), center_area_size)
# img_2_scaled = get_center_square(cv2.cvtColor(imutils.resize(img_2, height=img_1.shape[0], width=img_1.shape[1]), cv2.COLOR_BGR2GRAY), center_area_size)

# cv2.imshow('Result 1', img_1_scaled)
# cv2.imshow('Result 2', img_2_scaled)

# cv2.imshow('Compared image', img_crop)
# cv2.imshow('Compared image', img_compared)

# compared_metric = compare_images(img_1, img_2)
# print(compared_metric)

# Resize image
# img_2_resized = cv2.resize(img_2, (img_1.shape[1], img_1.shape[0]), interpolation=cv2.INTER_AREA)
# img_1_center = get_center_square(img_1, 25)
# img_2_center = get_center_square(img_2, 60)

# metric_val = compare_two_images(img_1, img_2)
# metric_val = compare_two_images(img_1_scaled, img_2_scaled)

# metric_val = compare_two_images(img_1, img_2_resized)
# metric_val = compare_two_images(img_1, img_2)

# 69,86
# cv2.imshow('Result 1', img_1_scaled)
# cv2.imshow('Result 2', img_2_scaled)

# cv2.imshow('Result 1', img_1)
# cv2.imshow('Result 2', img_2)

# assert(img_1_center.shape==img_1_center.shape)
# print(metric_val)

cv2.waitKey(0)
cv2.destroyAllWindows()
