import math
import pyautogui
import time
import random
import os
import glob
import np
import cv2
import json
import re
# from text_recognition import *
from datetime import datetime
from constants.index import IS_DEV
from helpers.time_mgr import *
import pytesseract

time_mgr = TimeMgr()


def get_time_for_log():
    return '{}'.format(str(datetime.now().strftime("%H:%M:%S")))


def log_save(message):
    if not IS_DEV:
        time = get_time_for_log()

        current_date = time_mgr.timestamp_to_datetime()
        file_name = 'log-' + f'{current_date["day"]}-{current_date["month"]}-{current_date["year"]}' + '.txt'
        f = open(file_name, "a")
        f.write(time + ' | ' + message + '\n')
        f.close()


def log(message):
    time = get_time_for_log()

    if type(message) is dict:
        output = json.dumps(message, indent=2)
    elif type(message) is list:
        output = np.array(message)
    elif type(message) is str:
        output = message
    else:
        output = str(message)

    print(time + ' | ', output)
    log_save(str(message))


def sleep(duration):
    # seconds_str = 'seconds'
    # if duration == 1:
    #     seconds_str = 'second'
    # log('Sleeping ' + str(duration) + ' ' + seconds_str)
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


def click_alt(x, y, duration=1, moving=True):
    if moving:
        pyautogui.moveTo(x, y, duration)
    pyautogui.click(x, y)


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


def pixels_wait(pixels, msg=None, timeout=5, mistake=0, wait_limit=None):
    length = len(pixels)
    pixels_str = 'pixel'
    if length > 1:
        pixels_str = 'pixels'
    if msg is not None:
        log('Waiting some of ' + str(length) + ' ' + pixels_str + ': ' + msg)

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

    while checked_pixels.count(False) == length:
        sleep(timeout)
        counter += timeout
        checked_pixels = restart()
        log(str(counter) + ' seconds left')
        if type(wait_limit) is int and counter < wait_limit:
            break

    return checked_pixels


# @TODO Should implement based on 'pixels_wait' within one crucial difference
def pixels_wait_every():
    return 0


def await_click(pixels, msg=None, timeout=5, mistake=0, wait_limit=None):
    res = pixels_wait(pixels, msg=msg, timeout=timeout, mistake=mistake, wait_limit=wait_limit)

    for i in range(len(res)):
        el = res[i]
        if el:
            pixel = pixels[i]
            x = pixel[0]
            y = pixel[1]

            click(x, y)
            time.sleep(.3)

            break

    return res


def is_index_page():
    flag = False
    if find_needle_burger() is not None:
        flag = True
        log('Index Page detected')
    else:
        log('Index Page is not detected')
    return flag


def waiting_battle_end_regular(msg, timeout=5, x=20, y=46):
    return pixel_wait(msg, x, y, [255, 255, 255], timeout, mistake=10)


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


def axis_list_to_region(l):
    return l[0], l[1], l[2] - l[0], l[3] - l[1]


def clear_folder(path):
    files = glob.glob(path + '/*')
    for f in files:
        os.remove(f)


def show_pyautogui_image(pyautogui_screenshot):
    open_cv_image = np.array(pyautogui_screenshot)
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    cv2.imshow('Matches', open_cv_image)
    cv2.waitKey()


def show_image(path=None):
    if path is not None:
        image = cv2.imread(path)
        cv2.imshow('Matches', image)
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


# def recognize_text(region):
#     screenshot = pyautogui.screenshot(region=region)
#     screenshot.save(r"E:\Main\BACKEND\core\text.png")
#     img = cv2.imread(r"E:\Main\BACKEND\core\text.png", cv2.IMREAD_GRAYSCALE)
#
#     # img = cv2.resize(img, (0, 0), None, 4.0, 4.0)
#     # img = cv2.threshold(img, 160, 255, cv2.THRESH_BINARY)[1]
#     # config = '--psm 6 -c tessedit_char_whitelist="0123456789/"'
#     # config = '--oem 3 --psm 6 outputbase digits'
#     # text = pytesseract.image_to_string(img, config=config)
#
#     img = cv2.resize(img, (0, 0), fx=3.0, fy=3.0)
#     bin_inverted = ~cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
#     text = pytesseract.image_to_string(bin_inverted)
#     return text


def click_on_progress_info(delay=0.5):
    # keys/coins info
    click(760, 46)
    sleep(delay)


def make_lambda(predicate, *args):
    return lambda: predicate(*args)


def find_needle(image_name, region=None, confidence=.8):
    if region is None:
        region = [0, 0, 900, 530]

    path_image = os.path.join(os.getcwd(), 'images/needles/' + image_name)
    return capture_by_source(path_image, region,
                             confidence=confidence)


def find_needle_refill_ruby():
    return find_needle('refill_ruby.jpg', axis_to_region(320, 320, 640, 440))


def find_needle_refill_button(region):
    return find_needle('refill_button.jpg', region)


def find_needle_battles():
    return find_needle('battles.jpg', axis_to_region(730, 430, 900, 530))


def find_needle_close_popup():
    return find_needle('close.png')


def find_needle_burger():
    return find_needle('burger.jpg')


def battles_click():
    battle_button = find_needle_battles()
    if battle_button is not None:
        x = battle_button[0]
        y = battle_button[1]
        pyautogui.click(x, y)
    else:
        log('Battle button is not found')


def close_popup():
    close_popup_button = find_needle_close_popup()
    if close_popup_button is not None:
        x = close_popup_button[0]
        y = close_popup_button[1]
        click(x, y)
        log('Regular popup closed')

    # closes special offer popup when it appears
    sleep(0.3)
    special_offer_popup = [300, 370, [22, 124, 156], 5]
    if pixel_check_new(special_offer_popup):
        x = special_offer_popup[0]
        y = special_offer_popup[1]
        click(x, y)
        log('Special offer popup closed')


def go_index_page():
    log('Moving to the Index Page...')
    close_popup()
    sleep(1)
    is_index = is_index_page()
    if is_index is False:
        go_index_page()
    return is_index


def screenshot_to_image(screenshot):
    return np.array(screenshot)[:, :, ::-1].copy()


def flatten(xss):
    return [x for xs in xss for x in xs]


def find(arr, predicate):
    for i in range(len(arr)):
        el = arr[i]
        if predicate(el):
            return i, el
    return None, None


def image_to_text(image):
    # image = cv2.medianBlur(image, 5)

    return [
        pytesseract.image_to_string(image, config='--psm 1 --oem 3'),
        pytesseract.image_to_string(image, config='--psm 3 --oem 3'),
        pytesseract.image_to_string(image, config='--psm 4 --oem 3'),
        pytesseract.image_to_string(image, config='--psm 7 --oem 3'),
        pytesseract.image_to_string(image, config='--psm 8 --oem 3'),
        pytesseract.image_to_string(image, config='--psm 10 --oem 3'),
    ]

    # return pytesseract.image_to_string(image, config='--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789')


def archive_list(input_list, pattern):
    result = []
    index = 0

    for group_size in pattern:
        group = input_list[index:index + group_size]
        result.append(group)
        index += group_size

    return result


def pop_random_element(input_list):
    if not input_list:
        return None  # Return None if the list is empty

    random_index = random.randrange(len(input_list))  # Get a random index
    random_element = input_list.pop(random_index)  # Remove and get the element at that index
    return random_element

def to_int(s):
    return 1

def get_higher_occurrence(arr):
    if not len(arr):
        return None
    return max(arr, key=arr.count)


def parse_dealt_damage(variants):
    # only digits
    def _parse(s):
        arr = re.split(r'\D+', s)
        # removing empty lines
        arr = list(filter(bool, arr))
        # taking only first 2 elements
        arr = arr[0:2]
        # joining to the one string
        str_damage = '.'.join(arr)

        # avoid phantom bug for some cases
        if str_damage:
            int_damage = float(str_damage)
        else:
            int_damage = 0

        if s.count('K'):
            int_damage = int_damage / 1000

        return int_damage

    return list(map(lambda x: _parse(x), variants))

def parse_stage_energy_cost(variants):
    extract_numbers = lambda x: [float(match.group()) for match in re.finditer(r'\d+\.?\d*', str(x))]
    numbers_only = [num for x in variants for num in extract_numbers(x)]
    return numbers_only


def read_text(configs, region, timeout=0.1, parser=None):
    res = []

    for i in range(len(configs)):
        config = configs[i]
        screenshot = pyautogui.screenshot(region=region)
        image = screenshot_to_image(screenshot)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(image, config=config)
        res.append(text)
        sleep(timeout)

    if parser:
        res = parser(res)

    return get_higher_occurrence(res)


def read_dealt_damage():
    log('Computing dealt damage...')
    # returns the damage in millions
    region = [190, 156, 550, 50]
    configs = [
        '--psm 1 --oem 3',
        '--psm 3 --oem 3',
        '--psm 4 --oem 3',
        '--psm 7 --oem 3',
        '--psm 8 --oem 3',
        '--psm 10 --oem 3',
        '--psm 1 --oem 3',
        '--psm 3 --oem 3',
        '--psm 4 --oem 3',
        '--psm 7 --oem 3',
        '--psm 8 --oem 3',
        '--psm 10 --oem 3',
    ]

    return read_text(configs=configs, region=region, timeout=.5, parser=parse_dealt_damage)


def read_energy_cost():
    log('Computing energy cost...')
    # returns energy cost
    region = axis_to_region(720, 460, 860, 505)
    configs = [
        '--psm 1 --oem 3',
        '--psm 3 --oem 3',
        '--psm 4 --oem 3',
        '--psm 5 --oem 3',
        '--psm 6 --oem 3',
        '--psm 7 --oem 3',
        '--psm 8 --oem 3',
        '--psm 9 --oem 3',
        '--psm 10 --oem 3',
        '--psm 11 --oem 3',
        '--psm 12 --oem 3',
        '--psm 13 --oem 3',
    ]

    return read_text(configs=configs, region=region, parser=parse_stage_energy_cost)
