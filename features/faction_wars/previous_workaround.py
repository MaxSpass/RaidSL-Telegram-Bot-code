import pyautogui
import os
import np
import cv2
import uuid
import math
from helpers.common import *

SLICE_WITH = 50

# @TODO Should taken from global varibales
SCREENSHOT_WIDTH = 900
SCREENSHOT_HEIGHT = 530

root_dir = 'E:/Main/BACKEND/core'
dir = 'test'
path = os.path.join(root_dir, dir)

# 58x28
CRYPTS_NEEDLE_WIDTH = 58
CRYPTS_NEEDLE_HEIGHT = 28
CRYPTS_SLIDES = [
    [
        # 'images/needles/crypt_lizardmen.png',
        # 'images/needles/crypt_knight_revenant.png',
        'images/needles/crypt_skinwalker.png',
        'images/needles/crypt_undead.png',
        # 'images/needles/crypt_demonspawn.png',
        # 'images/needles/crypt_ogryn_tribe.png',
        # 'images/needles/crypt_orc.png',
        # 'images/needles/crypt_high_elf.png',
    ],
    [
        # 'images/needles/crypt_dark_elf.png',
        # 'images/needles/crypt_sacred_order.png',
        # 'images/needles/crypt_barbarian.png',
        # 'images/needles/crypt_banner_lord.png',
        # 'images/needles/crypt_dwarf.png',
        'images/needles/crypt_shadowkin.png',
        # 'images/needles/crypt_sylvan_watcher.png',
    ]
]

# @TODO
def slice():
    len = math.ceil(SCREENSHOT_WIDTH / SLICE_WITH)
    clear_folder(path)
    for i in range(len):
        slice_index = i
        log(slice_index)
        # (0, 20, 0, 530)
        x1 = slice_index * SLICE_WITH
        y1 = 0
        x2 = x1 + SLICE_WITH
        y2 = SCREENSHOT_HEIGHT
        region = axis_to_region(x1, y1, x2, y2)

        image_id = str(uuid.uuid4())
        image_output = os.path.join(path, "index-" + str(slice_index) + "-" + image_id + ".jpg")
        screenshot = pyautogui.screenshot(region=region)
        screenshot.save(image_output)

        # needle = os.path.join(root_dir, 'images/needles/faction_key.jpg')
        # needle = os.path.join(root_dir, 'images/needles/faction_item_top_border.jpg')
        needle = os.path.join(root_dir, 'images/needles/faction_clock.jpg')
        images = list(pyautogui.locateAllOnScreen(needle, confidence=.6, grayscale=True, region=axis_to_region(0, 0, SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT)))
        log(images)

# @TODO Playing with OpenCV
def test():
    w = SCREENSHOT_WIDTH
    h = SCREENSHOT_HEIGHT
    screenshot = pyautogui.screenshot(region=(0, 0, w, h))
    open_cv_image = np.array(screenshot)
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    # cv2.imshow('Matches', open_cv_image)
    # cv2.waitKey()

    # needle_image = cv2.imread(os.path.join(root_dir, 'images/needles/faction_key.jpg'))
    # needle_image = cv2.imread(os.path.join(root_dir, 'images/needles/faction_item_top_border.jpg'))
    needle_image = cv2.imread(os.path.join(root_dir, 'images/needles/faction_clock.jpg'))
    result = cv2.matchTemplate(open_cv_image, needle_image, cv2.TM_CCOEFF_NORMED)

    log(len(result))

    threshold = 0.8
    yloc, xloc = np.where(result >= threshold)
    for (x, y) in zip(xloc, yloc):
        cv2.rectangle(open_cv_image, (x, y), (x + w, y + h), (0, 255, 255), 2)

    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.6)
    # There is a bug here | Found elements overlaps each other
    # print(locations, len(locations))

    log(rectangles)