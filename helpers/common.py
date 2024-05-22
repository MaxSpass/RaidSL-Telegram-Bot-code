import math
import pyautogui
import time
import random
import os
import glob
import np
import json
import re
import cv2
from datetime import datetime
from constants.index import IS_DEV
from helpers.time_mgr import *
from constants.index import *
import pytesseract
from PIL import Image
import PIL
import sys
import copy
import traceback

time_mgr = TimeMgr()

special_offer_popup = [300, 370, [22, 124, 156]]


def get_date_for_log():
    return datetime.now().strftime('%Y_%m_%d')


def get_time_for_log(s=':'):
    return '{}'.format(str(datetime.now().strftime(f"%H{s}%M{s}%S")))


def format_string_for_log(input_string):
    # Remove special characters and convert to lowercase
    clean_string = re.sub(r'[^a-zA-Z0-9-\-\s]', '', input_string).lower()
    # Replace spaces with underscores
    formatted_string = clean_string.replace(' ', '_')
    return formatted_string


def log_save(message):
    if not IS_DEV:
        time = get_time_for_log()
        current_date = time_mgr.timestamp_to_datetime()
        file_name = 'log-' + f'{current_date["day"]}-{current_date["month"]}-{current_date["year"]}' + '.txt'
        f = open(file_name, "a")
        string = str(f"{time} | {message} | \n".encode('utf-8'))
        f.write(string)
        f.close()


def log(message):
    time = get_time_for_log()

    if type(message) is dict:
        output = json.dumps(message, indent=2)
    elif type(message) is list:
        output = np.array(message, dtype=object)
    elif type(message) is str:
        output = message
    else:
        output = str(message)

    print(time + ' | ', output)
    log_save(str(message))


def folder_ensure(folder_path):
    # Check if the folder exists
    if not os.path.exists(os.path.normpath(folder_path)):
        # If the folder doesn't exist, create it
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")


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


def click(x, y, smart=False, timeout=0.5, interval=2):
    rgb = pyautogui.pixel(x, y) if smart else None

    pyautogui.click(x, y)

    if smart and rgb:
        counter = 0
        while pixel_check_new([x, y, rgb]) and counter < 3:
            if counter == 0:
                sleep(timeout)
            log('Delay occurred, re-trying to click again')
            click(x, y)
            sleep(interval)
            counter += 1


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


def debug_save_screenshot(region=None, suffix_name=None, output=None, quality=75, ext='jpg'):
    if not region:
        region = [0, 0, 906, 533]
    output_debug = 'debug'
    if output is not None:
        output_debug = os.path.normpath(f"{output_debug}/{output}")

    time = get_time_for_log(s='-')
    folder_ensure(output_debug)
    file_name = format_string_for_log(f"{time}-{str(suffix_name).lower()}" if suffix_name else time)
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save(os.path.join(output_debug, f"{file_name}.{ext}"), quality=quality)


def pixel_check_new(pixel, mistake=10):
    x = pixel[0]
    y = pixel[1]
    rgb = pixel[2]
    p = pyautogui.pixel(x, y)

    return rgb_check(p, rgb, mistake=mistake)


def rgb_check(rgb_1, rgb_2, mistake=0):
    if all(abs(rgb_1[i] - rgb_2[i]) <= mistake for i in range(3)):
        return True
    return False


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


def pixels_wait(pixels, msg=None, timeout=5, mistake=0, wait_limit=None, debug=False):
    length = len(pixels)
    pixels_str = 'pixel'
    if length > 1:
        pixels_str = 'pixels'
    if msg is not None:
        log(f"Waiting {pixels_str}: {msg}")

    def restart():
        res = []
        for i in range(len(pixels)):
            res.append(pixel_check_new(pixels[i], mistake=mistake))
        return res

    checked_pixels = restart()
    counter = 0
    has_wait_limit = type(wait_limit) is int or type(wait_limit) is float

    while checked_pixels.count(False) == length:
        counter += timeout
        checked_pixels = restart()
        if has_wait_limit and counter >= wait_limit:
            break

        log(str(counter) + ' seconds left')
        sleep(timeout)

    if debug and has_wait_limit and counter >= wait_limit:
        # debug
        debug_save_screenshot(suffix_name=msg)

    return checked_pixels


# @TODO Should implement based on 'pixels_wait' within one crucial difference
def pixels_wait_every():
    return 0


def await_click(pixels, msg=None, timeout=5, mistake=0, wait_limit=None, smart=False):
    res = pixels_wait(pixels, msg=msg, timeout=timeout, mistake=mistake, wait_limit=wait_limit)

    for i in range(len(res)):
        el = res[i]
        if el:
            pixel = pixels[i]
            x = pixel[0]
            y = pixel[1]

            click(x, y, smart=smart)
            time.sleep(.3)

            break

    return res


def await_needle(image_name, region=None, confidence=None, scale=None, timeout=.5, wait_limit=30):
    counter = 0
    needle_image = find_needle(image_name, region=region, confidence=confidence, scale=scale)
    while needle_image is None and counter < wait_limit:
        needle_image = find_needle(image_name, region=region, confidence=confidence, scale=scale)
        sleep(timeout)
        counter += timeout
    return needle_image


def is_index_page(logger=True):
    flag = False
    message = None
    if find_needle_burger() is not None:
        flag = True
        message = 'Index Page detected'
    else:
        message = 'Index Page is not detected'

    if logger and message:
        log(message)
    return flag


def get_closer_axis(arr):
    # Initialize the smallest_point with the first point in the array
    smallest_point = arr[0]

    # Iterate through the rest of the points to find the smallest 'x' and 'y' values
    for point in arr[1:]:
        if point.x < smallest_point.x:
            smallest_point = point
        elif point.x == smallest_point.x and point.y < smallest_point.y:
            smallest_point = point

    return smallest_point


def sort_by_closer_axis(arr):
    # Define a custom sorting key function
    def custom_sort(item):
        # Sort first by 'y', then by 'x'
        return item['y'], item['x']

    # Sort the data using the custom sorting key
    sorted_data = sorted(arr, key=custom_sort)

    return sorted_data


def move_out_cursor():
    # @TODO Refactor
    pyautogui.moveTo(1000, 1000)


def waiting_battle_end_regular(msg, timeout=5, x=20, y=46):
    return pixel_wait(msg, x, y, [255, 255, 255], timeout, mistake=10)


def tap_to_continue(times=1, wait_after=None):
    sleep(2)
    for i in range(times):
        click(420, 490)
        sleep(1)

    if type(wait_after) is int:
        sleep(wait_after)


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
    sleep(0.5)
    click(500, 480, smart=True)
    sleep(0.3)


def dungeons_start():
    BUTTON_START = [850, 475, [187, 130, 5]]
    await_click([BUTTON_START], msg="await 'Button Start'", timeout=1, mistake=10)


def dungeons_click_stage_select():
    # click on the "Stage selection"
    sleep(2)
    click(820, 55)
    sleep(2)


def dungeons_start_battle():
    log('Function: dungeons_start_battle')
    # @TODO Duplication
    STAGE_ENTER = [890, 200, [93, 25, 27]]
    if pixels_wait([STAGE_ENTER], msg="await 'Stage enter'", mistake=10, wait_limit=2)[0]:
        # click on 'Start'
        dungeons_start()
    else:
        # click on 'Replay'
        dungeons_replay()
    sleep(1)


def dungeons_is_able():
    log('Function: dungeons_is_able')
    # @TODO Duplication
    STAGE_ENTER = [890, 200, [93, 25, 27]]
    return pixel_check_new(STAGE_ENTER, mistake=10)


def dungeon_select_difficulty(difficulty, mistake=5):
    # rgb background exists in dungeon related locations only
    DIFFICULTY_SELECT = [144, 490, [13, 35, 45]]
    RGB_DIFFICULTY = [34, 47, 60]
    DIFFICULTY_NORMAL = [144, 394, RGB_DIFFICULTY]
    DIFFICULTY_HARD = [144, 450, RGB_DIFFICULTY]
    DUNGEON_DIFFICULTY_NORMAL = 'normal'
    DUNGEON_DIFFICULTY_HARD = 'hard'
    DIFFICULTIES = {
        DUNGEON_DIFFICULTY_NORMAL: DIFFICULTY_NORMAL,
        DUNGEON_DIFFICULTY_HARD: DIFFICULTY_HARD,
    }

    if difficulty in DIFFICULTIES:
        await_click([DIFFICULTY_SELECT], mistake=mistake)
        await_click([DIFFICULTIES[difficulty]], mistake=mistake)


def enable_super_raid(pixel=None):
    log('Function: enable_super_raid')
    # @TODO Duplication
    STAGE_ENTER = [890, 200, [93, 25, 27]]
    SUPER_RAID_PIXEL = [655, 336, [108, 237, 255]]

    if not pixel:
        pixel = SUPER_RAID_PIXEL

    if pixels_wait([STAGE_ENTER], msg="Waiting for entering the stage", mistake=10)[0]:
        if not pixel_check_new(pixel, mistake=10):
            x = pixel[0]
            y = pixel[1]
            click(x, y)
            sleep(.3)


def enable_auto_play(*args):
    AUTO_PLAY_BUTTON = [49, 486]
    sleep(2)
    click(AUTO_PLAY_BUTTON[0], AUTO_PLAY_BUTTON[1])


def detect_pause_button():
    BUTTON_PAUSE = [866, 66, [216, 206, 156]]
    return pixel_check_new(BUTTON_PAUSE, mistake=10)

def calculate_win_rate(w, l):
    t = w + l
    wr = w * 100 / t
    wr_str = str(round(wr)) + '%'
    return wr_str


# @TODO Should be fixed ASAP
def swipe(direction, x1, y1, distance, speed=2, sleep_after_end=1.5, instant_move=False):
    # @TODO The function does not work perfect
    if instant_move:
        pyautogui.moveTo(x1, y1)
    else:
        sleep(1)
        click(x1, y1)
        sleep(0.5)

    pyautogui.mouseDown()

    if direction == 'top':
        pyautogui.moveTo(x1, y1 + distance, speed)
    elif direction == 'bottom':
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


def show_pyautogui_image(pyautogui_screenshot, title='match'):
    open_cv_image = np.array(pyautogui_screenshot)
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    cv2.imshow(title, open_cv_image)
    cv2.moveWindow(title, 1000, 1000)
    cv2.waitKey()


def show_image(path=None, image=None, title='Image'):
    if path:
        image = cv2.imread(path)

    cv2.imshow(title, image)
    cv2.moveWindow(title, 1000, 1000)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def click_on_progress_info(delay=0.5):
    # keys/coins info
    click(760, 46)
    sleep(delay)


def make_lambda(predicate, *args):
    return lambda: predicate(*args)


def image_path(image):
    # @TODO Does not work as expected
    return os.path.join(os.getcwd(), 'image', image)


def find_needle(
        image_name,
        region=None,
        confidence=None,
        scale=None,
        retries=0,
        retry_interval=1,
        return_dimensions=True
):
    if region is None:
        region = [0, 0, 900, 530]
    if confidence is None:
        confidence = .8

    path_image = os.path.join(os.getcwd(), 'images/needles/' + image_name)
    # width = None
    # height = None

    if scale:
        physical_image = cv2.imread(path_image)
        _height, _width = physical_image.shape
        # Scale the physical image to match the screen size
        # Calculate the new dimensions
        width = _width * scale
        height = _height * scale
        # Resize the image with Lanczos interpolation
        # scaled_image = image.resize((new_width, new_height), Image.LANCZOS)
        scaled_image = cv2.resize(physical_image, (width, height))

        path_image = scaled_image

        # show_pyautogui_image(path_image)

    position = capture_by_source(path_image, region, confidence=confidence)
    while retries > 0 and position is None:
        position = capture_by_source(path_image, region, confidence=confidence)
        retries -= 1
        sleep(retry_interval)

    # if return_dimensions:
    #     if width and height:
    #         return position, width, height
    #     else:
    #         _height, _width = cv2.imread(path_image).shape
    #         return position + (_width, _height)

    return position


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


def find_needle_energy_bank(region=None):
    if not region:
        region = axis_to_region(220, 32, 790, 68)

    return find_needle('bank_energy.jpg', region)


def find_faction_keys_bank(region=None):
    if not region:
        region = [0, 32, 900, 50]

    return find_needle('bank_faction_keys.jpg', region, confidence=.6)


def find_needle_refill_plus(region):
    return find_needle('refill_plus.jpg', region=region)


def find_needle_energy_cost(region=None):
    if not region:
        region = axis_to_region(720, 460, 860, 505)

    return find_needle('energy_cost.jpg', region)


def find_needle_red_dot(region=None, confidence=None):
    return find_needle('red_dot.jpg', region=region, confidence=confidence)


def find_needle_arena_reward(region=None):
    if not region:
        region = axis_to_region(177, 424, 880, 450)

    return find_needle('arena_reward.jpg', region=region, confidence=.6)


def find_guardian_ring():
    return find_needle('guardian_ring_2.jpg', confidence=.4)


def find_doom_tower_golden_keys():
    return find_needle('bank_keys_golden.jpg', confidence=.65)


def find_doom_tower_silver_keys():
    return find_needle('bank_keys_silver.jpg', confidence=.65)


def find_hero_filter_default(region=None, confidence=.7, retries=None):
    return find_needle('filter.jpg', region=region, confidence=confidence, retries=retries)


def find_hero_filter_small(region=None, confidence=.7, retries=None):
    return find_needle('filter_small.png', region=region, confidence=confidence, retries=retries)


def find_hero_slot_active(region):
    return find_needle('hero_slot_active.jpg', region=region, confidence=.65, retries=2)


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
    special_offer_button = pixel_check_new(special_offer_popup, mistake=5)
    if special_offer_button:
        x = special_offer_popup[0]
        y = special_offer_popup[1]
        click(x, y)
        sleep(3)
        log('Special offer popup closed')

    return [close_popup_button, special_offer_button]


def close_popup_recursive(timeout=2, delay=1):
    def _check():
        res = close_popup()
        return res[0] is not None or res[1]

    while _check():
        sleep(timeout)

    sleep(delay)


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


def check_image(region):
    screenshot = pyautogui.screenshot(region=region)
    show_pyautogui_image(screenshot)


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
        int_damage = 0

        try:
            last_char = str_damage[len(str_damage) - 1]
            multiplier = s[s.index(last_char) + 1].upper()

            if str_damage:
                int_damage = float(str_damage)

            if multiplier in ['K', 'M', 'B']:
                if multiplier == 'K':
                    int_damage = int_damage / 1000
                elif multiplier == 'B':
                    int_damage = int_damage * 1000
        except Exception:
            error = traceback.format_exc()
            log_save(error)

        return int_damage

    return list(map(lambda x: _parse(x), variants))


def parse_energy_cost(variants):
    extract_numbers = lambda x: [float(match.group()) for match in re.finditer(r'\d+\.?\d*', str(x))]
    res = [num for x in variants for num in extract_numbers(x)]
    return res


def parse_energy_bank(variants):
    # works with examples: 1234/130, 18/12 and etc
    extract_first_number = lambda x: int(re.search(r'(?<!\d)\d+(?=/\d+)', x.replace(',', '')).group()) if re.search(
        r'(?<!\d)\d+/\d+', x) else None

    # extracting Number elements
    res = list(map(extract_first_number, variants))
    # removing None elements
    res = list(filter(lambda x: x is not None, res))
    return res


def parse_levels(data):
    levels = []

    for item in data:
        # Extract numeric values from the item
        numbers = ''.join(filter(lambda x: x.isdigit() or x == '/', item))

        # Check if there are any numeric values extracted
        if numbers:
            levels.append(numbers)

    return levels


def scale_up(screenshot=None, image=None, factor=1):
    if screenshot is not None:
        image = Image.frombytes("RGB", screenshot.size, screenshot.tobytes())

        # Calculate the new dimensions
        new_width = image.width * factor
        new_height = image.height * factor

        # Resize the image with Lanczos interpolation
        scaled_image = image.resize((new_width, new_height), Image.LANCZOS)

        return np.array(scaled_image)

    if image is not None:
        # Get the dimensions of the original image
        height, width, _ = image.shape

        # Calculate the new dimensions based on the scaling factor
        new_width = int(width * factor)
        new_height = int(height * factor)

        # Resize the image to the new dimensions
        scaled_image = cv2.resize(image, (new_width, new_height))

        return scaled_image


def crop(image=None, region=None):
    if image is not None and region is not None:
        return image[region[1]:region[1] + region[3], region[0]:region[0] + region[2]]


def read_text(
        region,
        configs=None,
        timeout=0.1,
        parser=None,
        update_screenshot=False,
        scale=2,
        debug=False,
        title='match'
):
    # debug = True
    res = []
    screenshot = None

    if configs is None:
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

    if not update_screenshot:
        screenshot = pyautogui.screenshot(region=region)

    for i in range(len(configs)):
        if update_screenshot:
            screenshot = pyautogui.screenshot(region=region)

        config = configs[i]
        # image = scale_up(screenshot=screenshot, factor=scale)

        # @TODO Should be well tested
        img = screenshot_to_image(screenshot)
        image = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_LANCZOS4)
        # thresh = cv2.threshold(image, 175, 255, cv2.THRESH_BINARY_INV)[1]
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        # opening = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        # greyscale
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # @TODO Debug
        if debug and i == 0:
            cv2.imshow(title, image)
            cv2.waitKey()

        text = pytesseract.image_to_string(image, config=config)
        res.append(text.strip())
        sleep(timeout)

    # log(res)
    if parser:
        res = parser(res)
    # log(res)

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

    move_out_cursor()
    return read_text(configs=configs, region=region, timeout=.5, update_screenshot=True, parser=parse_dealt_damage)


def read_run_cost(region=None, scale=4):
    log('Computing run cost...')

    # x1 = 820
    x1 = 740
    y1 = 477
    x2 = 852
    y2 = 494

    if not region:
        # index page
        region = axis_to_region(x1, y1, x2, y2)
        # show_pyautogui_image(pyautogui.screenshot(region=region))

    # region = axis_to_region(720, 460, 860, 505)
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

    return read_text(configs=configs, region=region, parser=parse_energy_cost, scale=scale)


def get_resource_region(needle_predicate, needle_width, predicted_offset_x=150):
    region = None
    IMG_REFILL_SIDE = 12

    position_energy = needle_predicate()
    if position_energy:
        x1_refill_button = position_energy[0] - predicted_offset_x + needle_width
        region_refill_button = [x1_refill_button, 38, 100, 18]
        position_refill_button = find_needle_refill_plus(region=region_refill_button)
        if position_refill_button:
            x1 = position_refill_button[0] + IMG_REFILL_SIDE
            x2 = position_energy[0] - needle_width / 2
            region = axis_to_region(x1, 38, x2, 56)

    return region


def read_available_energy(region=None):
    log('Computing available energy...')
    if not region:
        region = get_resource_region(needle_predicate=find_needle_energy_bank, needle_width=17)
        # show_pyautogui_image(pyautogui.screenshot(region=region))

    configs = [
        '--psm 1 --oem 3',
        '--psm 3 --oem 3',
        '--psm 4 --oem 3',
        '--psm 6 --oem 3',
        '--psm 7 --oem 3',
        '--psm 8 --oem 3',
        '--psm 9 --oem 3',
        '--psm 10 --oem 3',
        '--psm 11 --oem 3',
        '--psm 12 --oem 3',
    ]

    return read_text(configs=configs, region=region, parser=parse_energy_bank, scale=4)


def read_keys_bank(region=None, scale=8, key=None):
    log(f"Computing{' ' + key if bool(key) else ''} keys bank...")

    if not region:
        region = get_resource_region(needle_predicate=find_faction_keys_bank, needle_width=24)
        # show_pyautogui_image(pyautogui.screenshot(region=region))

    configs = [
        '--psm 1 --oem 3',
        '--psm 3 --oem 3',
        '--psm 4 --oem 3',
        '--psm 6 --oem 3',
        '--psm 7 --oem 3',
        '--psm 8 --oem 3',
        '--psm 9 --oem 3',
        '--psm 10 --oem 3',
        '--psm 11 --oem 3',
        '--psm 12 --oem 3',
    ]

    return read_text(configs=configs, region=region, parser=parse_energy_bank, scale=scale, debug=False)


def read_doom_tower_keys(key_type='golden'):
    position = None
    x1 = 0
    x2 = 0

    if key_type == 'golden':
        position = find_doom_tower_golden_keys()
        x1 = 618
    elif key_type == 'silver':
        position = find_doom_tower_silver_keys()
        x1 = 730

    if position:
        x1 = position[0] - 68
        x2 = position[0] - 12

    region = axis_to_region(x1, 38, x2, 56)

    # screenshot = pyautogui.screenshot(region=region)
    # show_pyautogui_image(screenshot)

    return read_keys_bank(region=region, scale=4, key=key_type)


def dominant_color_hue(region, rank=1):
    screenshot = pyautogui.screenshot(region=region)
    image = screenshot_to_image(screenshot)

    # Convert the image to the HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Calculate the histogram of the image in the Hue channel
    histogram = cv2.calcHist([hsv_image], [0], None, [180], [0, 180])

    # Find the rank-th dominant color bin
    dominant_color_bin = np.argsort(histogram.flatten())[-rank]

    # Convert the bin index to the corresponding hue value
    dominant_color_hue = int(dominant_color_bin * 180 / 256)

    return dominant_color_hue


# @TODO Remove 'reverse' property
def dominant_color_rgb(region, rank=1, reverse=True):
    screenshot = pyautogui.screenshot(region=region)
    image = screenshot_to_image(screenshot)

    # Reshape the image into a 2D array of pixels
    pixels = image.reshape((-1, 3))

    # Calculate the histogram of pixel values
    histogram = np.zeros((256, 256, 256))
    for pixel in pixels:
        r, g, b = pixel
        histogram[r, g, b] += 1

    # Find the rank-th dominant color (index) in the flattened histogram
    dominant_color_index = np.argsort(histogram.flatten())[-rank]

    # Convert the index to RGB values
    r, g, b = np.unravel_index(dominant_color_index, (256, 256, 256))

    res = [r, g, b]

    # Making right format here
    if not reverse:
        res.reverse()

    return res


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_logged_out():
    _is_logged_out = True

    rgb = [16, 126, 158]
    pixels = [
        # Re-log In button
        [350, 294, rgb],
        # Support button
        [550, 294, rgb],
    ]

    for i in range(len(pixels)):
        if not pixel_check_new(pixels[i], mistake=10):
            _is_logged_out = False
            break

    return _is_logged_out


def is_production():
    return getattr(sys, 'frozen', False)


def merge_dicts(dict1, dict2):
    """
    Merge two dictionaries deeply.
    """
    merged_dict = copy.deepcopy(dict1)

    for key, value in dict2.items():
        if key in merged_dict and isinstance(merged_dict[key], dict) and isinstance(value, dict):
            # If both values are dictionaries, merge them recursively
            merged_dict[key] = merge_dicts(merged_dict[key], value)
        else:
            # Otherwise, update the value in merged_dict with the value from dict2
            merged_dict[key] = value

    return merged_dict


def prepare_event(event, props):
    event_copy = copy.copy(event)
    return merge_dicts(event_copy, props)

def get_result(rgb):
    REGION_BATTLE_RESULT = [
        WINDOW_SIZE[0] / 2 - BORDER_WIDTH - 25,
        BORDER_WIDTH + WINDOW_TOP_BAR_HEIGHT,
        50,
        10
    ]
    dominant_rgb = dominant_color_rgb(region=REGION_BATTLE_RESULT)
    # print(f"Dominant rgb: {dominant_rgb}")

    # high mistake is needed,
    # because, dominant_color_rgb returns not accurate result
    return rgb_check(rgb, dominant_rgb, mistake=50)


def pixels_some(pixels, predicate):
    res = False
    for i in range(len(pixels)):
        _p = pixels[i]
        if predicate(_p):
            res = True
            break
    return res


def pixels_every(pixels, predicate):
    res = True
    for i in range(len(pixels)):
        _p = pixels[i]
        if not predicate(_p):
            res = False
            break
    return res


def same_pixels_line(pixel, long=3, axis='x'):
    _el = copy.copy(pixel)
    acc = []
    for i in range(long):
        acc.append(copy.copy(_el))
        if axis == 'x':
            _el[0] += 1
        elif axis == 'y':
            _el[1] += 1
    return acc
