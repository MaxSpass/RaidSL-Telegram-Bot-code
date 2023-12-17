import math
import pyautogui
import time
import random
import os
import glob
import np
import cv2
import json
from text_recognition import *
from datetime import datetime


def log(message):
    time = '{}'.format(str(datetime.now().strftime("%H:%M:%S")))
    output = message

    if type(message) is not str:
        output = json.dumps(message)

    print(time + ' | ' + output)

def sleep(duration):
    time.sleep(duration)


def test_screenshot(region):
    iml = pyautogui.screenshot(region=region)
    if iml is not None:
        iml.save(r"D:\ComputerVision\bot\test_screenshot.png")
        log('test_screenshot.png has been updated')


def track_mouse_position():
    try:
        while True:
            sleep(2)
            x, y = pyautogui.position()
            r, g, b = pyautogui.pixel(x, y)
            positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
            print(positionStr + ' | RGB(' + str(r) + ', ' + str(g) + ', ' + str(b) + ')')
    except KeyboardInterrupt:
        print('\n')


def capture_by_source(src, region, confidence=.9, grayscale=False):
    return pyautogui.locateCenterOnScreen(src, region=region, confidence=confidence, grayscale=grayscale)


def click(x, y):
    pyautogui.click(x, y)
    # win32api.SetCursorPos((x, y))
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    # sleep(0.1)
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def click_alt(x, y, duration=1):
    pyautogui.moveTo(x, y, duration)
    pyautogui.click()


def random_easying():
    return random.choice([
        pyautogui.easeInQuad,
        pyautogui.easeOutQuad,
        pyautogui.easeInOutQuad,
        pyautogui.easeInBounce,
        pyautogui.easeInElastic
    ])


def pixel_check_old(x, y, rgb, mistake=0):
    pixel = pyautogui.pixel(x, y)
    if mistake == 0:
        return pixel[0] == rgb[0] and pixel[1] == rgb[1] and pixel[2] == rgb[2]
    else:
        return rgb[0] - mistake < pixel[0] < rgb[0] + mistake and rgb[1] - mistake < pixel[1] < rgb[1] + mistake and \
               rgb[2] - mistake < pixel[2] < rgb[2] + mistake


def pixel_check_new(pixel, mistake=10):
    x = pixel[0]
    y = pixel[1]
    rgb = pixel[2]
    p = pyautogui.pixel(x, y)
    if mistake == 0:
        return p[0] == rgb[0] and p[1] == rgb[1] and p[2] == rgb[2]
    else:
        return rgb[0] - mistake < p[0] < rgb[0] + mistake and rgb[1] - mistake < p[1] < rgb[1] + mistake and \
               rgb[2] - mistake < p[2] < rgb[2] + mistake


def pixels_check(msg, pixels, mistake=0):
    length = len(pixels)
    log('Checking some of ' + str(length) + ' pixels: ' + msg)
    res = []

    for i in range(len(pixels)):
        res.append(pixel_check_new(pixels[i], mistake=mistake))

    return res


def pixel_wait(msg, x, y, rgb, timeout=5, mistake=0):
    log('Waiting pixel: ' + msg)
    while pixel_check_new([x, y, rgb], mistake=mistake) is False:
        sleep(timeout)
    log('Found  pixel: ' + msg)
    return True


def pixels_wait(msg, pixels, timeout=5, mistake=0, wait_limit=120):
    length = len(pixels)
    log('Waiting some of ' + str(length) + ' pixels: ' + msg)

    def restart():
        res = []
        for i in range(len(pixels)):
            x = pixels[i][0]
            y = pixels[i][1]
            rgb = pixels[i][2]
            res.append(pixel_check_old(x, y, rgb, mistake=mistake))
        return res

    checked_pixels = restart()
    counter = 0

    while checked_pixels.count(False) == length and counter < wait_limit:
        sleep(timeout)
        counter += timeout
        checked_pixels = restart()
        log(str(counter) + ' seconds left')

    return checked_pixels


def is_index_page():
    flag = False
    if pixel_check_old(756, 39, [179, 111, 26], 5):
        flag = True
        log('Index Page detected')
    else:
        log('Index Page is not detected')
    return flag


def close_popup():
    # closes regular offer popup when it appears
    position = pyautogui.locateCenterOnScreen('images/needles/close.png', confidence=.8)
    if position is None:
        log('Regular popup was not found')
    else:
        x = position[0]
        y = position[1]
        pyautogui.moveTo(x, y, 1)
        pyautogui.click()

    # closes special offer popup when it appears
    sleep(0.3)
    x = 300
    y = 370
    if pixel_check_old(x, y, [22, 124, 156]):
        click(x, y)
    else:
        log('Special offer popup was not found')

    return position


def go_index_page():
    log('Moving to the Index Page...')
    click_alt(5, 5)
    sleep(1)
    # pyautogui.press('esc')
    close_popup()
    sleep(1)
    is_index = is_index_page()
    if is_index is False:
        go_index_page()
    return is_index


def battles_click():
    position = pyautogui.locateCenterOnScreen('images/needles/battles.jpg', confidence=.9)
    if position is None:
        log('Battles needle is not found')
    else:
        x = position[0]
        y = position[1]
        pyautogui.moveTo(x, y, 1)
        pyautogui.click()
    return position


def waiting_battle_end_regular(msg, timeout=5, x=20, y=46):
    return pixel_wait(msg, x, y, [255, 255, 255], timeout)


def tap_to_continue():
    sleep(1)
    for i in range(2):
        click(420, 490)
        sleep(1)


def dungeons_scroll(direction='bottom', times=2):
    x = 500
    y_axis = [510, 90]

    if direction == 'top':
        y_axis.reverse()

    for index in range(times):
        pyautogui.moveTo(x, y_axis[0], .5, random_easying())
        pyautogui.dragTo(x, y_axis[1], duration=.4)
        sleep(1.5)

    sleep(2)


def dungeons_replay():
    click(500, 480)
    sleep(0.3)


def dungeons_results_finish():
    # click on the "Stage selection"
    sleep(1)
    click(820, 53)
    sleep(0.5)


# @TODO Should be fixed ASAP
def swipe(direction, x1, y1, distance, sleep_after_end=1.5, speed=2):
    # @TODO It does not work perfect
    sleep(1)
    click(x1, y1)
    sleep(0.5)

    pyautogui.mouseDown()

    if direction == 'bottom':
        pyautogui.moveTo(x1, y1 - distance, speed)
    elif direction == 'right':
        pyautogui.moveTo(x1 - distance, y1, speed)
    elif direction == 'left':
        pyautogui.moveTo(x1 + distance, y1, speed)

    sleep(1)
    pyautogui.mouseUp()
    # pyautogui.moveTo(x1, y1, 1)
    # x2 = x1
    # y2 = y1
    #
    # if direction == 'bottom':
    #     y2 = y1 - distance
    #
    # pyautogui.drag(45, 180, 1)
    sleep(sleep_after_end)


# @TODO It's in used in outdated features only (classic_arena, tag_arena)
def refresh_arena():
    if pixel_wait('Refresh button', 817, 133, [22, 124, 156], 10):
        log('Refreshing...')
        click(817, 133)
        sleep(1)
        for index in range(2):
            pyautogui.moveTo(560, 185, .5, random_easying())
            pyautogui.dragTo(560, 510, duration=.4)
            sleep(1.5)
        sleep(3)


def axis_to_region(x1, y1, x2, y2):
    return x1, y1, x2 - x1, y2 - y1


def clear_folder(path):
    files = glob.glob(path + '/*')
    for f in files:
        os.remove(f)


def show_pyautogui_image(pyautogui_screenshot):
    open_cv_image = np.array(pyautogui_screenshot)
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    cv2.imshow('Matches', open_cv_image)
    cv2.waitKey()


# run only in case when you are aware of the action
def find_perfect_pixel():
    tracker = []
    for x in range(913):
        for y in range(540):
            log('X: ' + str(x) + ' Y: ' + str(y))
            if pixel_check_old(x, y, [222, 0, 0]):
                log("Found")
                tracker.append([x, y])
    log(tracker)


def recognize_text(region):
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save(r"E:\Main\BACKEND\core\text.png")
    img = cv2.imread(r"E:\Main\BACKEND\core\text.png", cv2.IMREAD_GRAYSCALE)

    # img = cv2.resize(img, (0, 0), None, 4.0, 4.0)
    # img = cv2.threshold(img, 160, 255, cv2.THRESH_BINARY)[1]
    # config = '--psm 6 -c tessedit_char_whitelist="0123456789/"'
    # config = '--oem 3 --psm 6 outputbase digits'
    # text = pytesseract.image_to_string(img, config=config)

    img = cv2.resize(img, (0, 0), fx=3.0, fy=3.0)
    bin_inverted = ~cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_string(bin_inverted)
    return text


def click_on_progress_info(delay=0.5):
    # keys/coins info
    click(760, 46)
    sleep(delay)


def make_lambda(predicate, *args):
    return lambda: predicate(*args)


def get_progress():
    ITEM_HEIGHT = 40

    x1 = 585
    y1 = 72
    x2 = 744
    y2 = 112

    # x1 = x1 + 70
    # x2 = x2 - 70
    # y1 += ITEM_HEIGHT + ITEM_HEIGHT / 2
    # y2 += ITEM_HEIGHT

    if is_index_page():
        click(760, 46)
        sleep(0.5)

        for i in range(9):
            # show_pyautogui_image(pyautogui.screenshot(region=axis_to_region(x1, y1, x2, y2)))
            text = recognize_text(axis_to_region(x1, y1, x2, y2))
            log(text)
            y1 += ITEM_HEIGHT
            y2 += ITEM_HEIGHT

    else:
        log("Stopped! It's not an Index Page")


def find_needle(image_name, region=None, confidence=.8):
    if region is None:
        region = [0, 0, 900, 530]

    # @TODO Make it generic
    path_root = 'E:/Main/BACKEND/core'
    path_image = os.path.join(path_root, 'images/needles/' + image_name)
    return capture_by_source(path_image, region,
                             confidence=confidence)


def find_needle_refill_ruby():
    return find_needle('refill_ruby.jpg', axis_to_region(320, 320, 640, 440))
