import time
import win32gui
import win32api, win32con
from classes.window_mgr import *
from debug.functions import *
from helpers.screen import *
import pyautogui
import random

# demon lord | levels for attack
DEMON_LORD_LEVELS_FOR_ATTACK = [6, 5]
# demon lord | clicking areas for obtaining rewards
DEMON_LORD_REWARD_COORDINATES = {
    3: (580, 120),
    4: (580, 200),
    5: (580, 300),
    6: (580, 380),
}
# tag arena | refilling number
TAG_ARENA_MAX_REFILL = 2


def log(message):
    print(message)


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
            # px = pyautogui.pixel((x, y))
            print(positionStr + "\n", end='')
            print('RGB(' + str(r) + ', ' + str(g) + ', ' + str(b) + ')')
    except KeyboardInterrupt:
        print('\n')


def capture_by_source(src, region, confidence=.9):
    return pyautogui.locateCenterOnScreen(src, region=region, confidence=confidence)


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


def pixel_check(x, y, rgb):
    pixel = pyautogui.pixel(x, y)
    return pixel[0] == rgb[0] and pixel[1] == rgb[1] and pixel[2] == rgb[2]


def pixel_wait(msg, x, y, rgb, timeout=5):
    while pixel_check(x, y, rgb) is False:
        log('Waiting pixel: ' + msg)
        sleep(timeout)
    log(msg + ' just found requested pixel')
    return True


def is_index_page():
    flag = False
    if pixel_check(756, 39, [179, 111, 26]):
        flag = True
        log('Index Page detected')
    else:
        log('Index Page is not detected')
    return flag


def close_popup():
    position = pyautogui.locateCenterOnScreen('dataset/test/close.png', confidence=.8)
    if position is None:
        log('Popup close needle not found')
    else:
        x = position[0]
        y = position[1]
        pyautogui.moveTo(x, y, 1)
        pyautogui.click()
    return position


def go_index_page():
    log('Moving to the Index Page...')
    click_alt(1, 1)
    pyautogui.press('esc')
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


def waiting_battle_end_regular(msg, timeout=5):
    return pixel_wait(msg, 20, 46, [255, 255, 255], timeout)


def tap_to_continue():
    sleep(1)
    for i in range(2):
        click(420, 490)
        sleep(1)


def swipe(direction, x1, y1, distance, sleep_after_end=1.5):
    # @TODO It does not work perfect
    sleep(1)
    click(x1, y1)
    sleep(0.2)
    pyautogui.mouseDown()
    pyautogui.moveTo(x1, y1 - distance, 2)
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


def demon_lord():
    def enter():
        # moving to the Demon Lord
        # click on the red button "Battles"
        battles_click()
        sleep(1)
        # click on the clan boss
        click(890, 300)
        sleep(1)
        # click on the Demon Lord
        click(320, 290)
        sleep(1)

        # swapping to the bottom @TODO
        pyautogui.moveTo(580, 400, 1)
        pyautogui.dragTo(580, 120, duration=1)
        sleep(2)

    def obtain():
        global DEMON_LORD_LEVELS_FOR_ATTACK
        global DEMON_LORD_REWARD_COORDINATES
        # obtain rewards
        for lvl in DEMON_LORD_REWARD_COORDINATES:
            x = DEMON_LORD_REWARD_COORDINATES[lvl][0]
            y = DEMON_LORD_REWARD_COORDINATES[lvl][1]
            click(x, y)
            sleep(0.5)
            str_lvl = str(lvl)
            if pixel_check(870, 457, [246, 0, 0]):
                # click on the "Claim reward button"
                click(870, 457)
                sleep(1)
                # click on the "Obtain reward button"
                click(460, 444)
                sleep(1)
                # click on the "Obtain reward button"
                click(460, 444)
                log('Obtained reward from Demon Lord ' + str_lvl)
            else:
                log('No reward found from Demon Lord ' + str_lvl)
            sleep(2)

    def attack():
        global DEMON_LORD_LEVELS_FOR_ATTACK
        global DEMON_LORD_REWARD_COORDINATES
        # attack
        for i in range(len(DEMON_LORD_LEVELS_FOR_ATTACK)):
            # zero-indexed Demon Lord level is always next
            lvl = DEMON_LORD_LEVELS_FOR_ATTACK[0]
            x = DEMON_LORD_REWARD_COORDINATES[lvl][0]
            y = DEMON_LORD_REWARD_COORDINATES[lvl][1]
            # click on the certain demon lord
            click(x, y)
            # pyautogui.moveTo(x, y, 1)
            # DEMON_LORD_LEVELS_FOR_ATTACK.remove(lvl)
            sleep(.5)
            # prepare to battle
            click(860, 480)
            sleep(.5)
            # start battle
            click(860, 480)
            if pixel_wait('End of the battle with Demon Lord: ' + str(lvl) + ' level', 20, 112, [255, 255, 255], 3):
                # return to the demon lord menu
                click(420, 490)
                close_popup()
                sleep(2)
                # removing already attacked Demon Lord from the array
                DEMON_LORD_LEVELS_FOR_ATTACK.remove(lvl)

    enter()
    obtain()
    attack()


def tag_arena():
    # @TODO Should add moving to the Tag arena page, called "enter"
    sleep(2)

    def get_canvas():
        return capture_by_source('images/needles/tag_arena_weak_team.jpg', axis_to_region(425, 175, 882, 521),
                                 confidence=.9)

    def enter():
        # click on the red button "Battles"
        battles_click()
        sleep(1)
        # click on arenas
        click(700, 280)
        sleep(1)
        # click on the Tag Arena
        click(710, 250)
        sleep(1)

    def attack():
        global TAG_ARENA_MAX_REFILL
        # @TODO Can be moved to the global scope
        item_height = 100
        for i in range(7):
            team_for_attack = get_canvas()

            # @TODO
            # sleep(.5)
            # click(team_for_attack[0] + 135, team_for_attack[1])
            # break

            while team_for_attack is not None:
                log('Found a team')
                # The battle button is positioned at 135 pixels with an offset to the right
                x = team_for_attack[0] + 135
                y = team_for_attack[1]
                # pyautogui.moveTo(team_for_attack[0] + 135, team_for_attack[1], 1, random_easying())
                click(x, y)
                sleep(0.5)

                should_refill_by_coins = pixel_check(439, 395, [255, 38, 46]) and TAG_ARENA_MAX_REFILL > 0
                should_refill_for_free = pixel_check(455, 374, [187, 130, 5])
                should_refill = should_refill_by_coins or should_refill_for_free
                if should_refill:
                    click(439, 395)
                    sleep(0.5)
                    if should_refill_by_coins:
                        TAG_ARENA_MAX_REFILL = TAG_ARENA_MAX_REFILL - 1

                # @TODO Might be in the "if" condition same nesting, above
                click(x, y)
                sleep(1)

                click(860, 480)
                waiting_battle_end_regular('Tag Arena Battle end')
                tap_to_continue()
                sleep(2)
                team_for_attack = get_canvas()

            log('No team found in this frame')
            swipe('bottom', 580, 254, item_height)

    def refresh():
        if pixel_wait('Refresh button', 817, 133, [22, 124, 156], 10):
            log('Refreshing...')
            click(817, 133)
            sleep(1)
            for index in range(2):
                pyautogui.moveTo(560, 185, .5, random_easying())
                pyautogui.dragTo(560, 510, duration=.4)
                sleep(1.5)
            sleep(3)

    enter()
    attack()
    log('No more teams for fighting...')
    refresh()
    # @TODO Should check TAG_ARENA_MAX_REFILL and actual amount of available battles
    tag_arena()

    return 0


def classic_arena():
    def enter():
        # click on the red button "Battles"
        battles_click()
        sleep(1)
        # click on arenas
        click(700, 280)
        sleep(1)
        # click on the Classic Arena
        click(200, 250)
        sleep(1)

    def attack():
        # @TODO Can be moved to the global scope
        item_height = 92

        positions = {
            1: (855, 200),
            2: (855, 295),
            3: (855, 380),
            4: (855, 465),
        }

        # all swipes calculated based on item height: 92
        dictionary_map = [
            {
                'swipes': 0,
                'position': 1,
            },
            {
                'swipes': 1,
                'position': 1,
            },
            {
                'swipes': 2,
                'position': 1,
            },
            {
                'swipes': 3,
                'position': 1,
            },
            {
                'swipes': 4,
                'position': 1,
            },
            {
                'swipes': 5,
                'position': 1,
            },
            {
                'swipes': 6,
                'position': 1,
            },
            {
                'swipes': 6,
                'position': 2,
            },
            {
                'swipes': 6,
                'position': 3,
            },
            {
                'swipes': 6,
                'position': 4,
            },
        ]

        tracker = []
        should_use_multi_swipe = False

        for i in range(len(dictionary_map)):
            el = dictionary_map[i]
            swipes = el['swipes']
            position = el['position']

            if should_use_multi_swipe:
                for j in range(swipes):
                    swipe('bottom', 580, 254, item_height)
            elif 0 < i < 7:
                swipe('bottom', 580, 254, item_height)

            # pyautogui.moveTo(x, y, 1)

            pos = positions[position]
            x = pos[0]
            y = pos[1]

            # checking - is an enemy already attacked
            is_not_attacked = len(tracker) - 1 < i
            if pixel_check(x, y, [187, 130, 5]) and is_not_attacked:
                print('Attacking Classic Arena battle')
                # pyautogui.moveTo(x, y, 1)
                # continue
                click(x, y)
                sleep(0.5)

                # @TODO Should add should_refill_by_coins
                should_refill_for_free = pixel_check(455, 380, [187, 130, 5])
                should_refill = should_refill_for_free
                if should_refill:
                    click(439, 395)
                    sleep(0.5)
                    click(x, y)
                    sleep(0.5)
                    # if should_refill_by_coins:
                    #     TAG_ARENA_MAX_REFILL = TAG_ARENA_MAX_REFILL - 1

                click(860, 480)
                sleep(0.5)
                waiting_battle_end_regular('Classic Arena battle end')

                # battle has been failed
                if pixel_check(443, 51, [229, 40, 104]):
                    log('Failed Classic Arena battle')
                    tracker.append(False)
                # battle has been won
                else:
                    log('Won  Classic Arena battle')
                    tracker.append(True)

                tap_to_continue()
                sleep(1)
                # tells to skip several teams by swiping
                should_use_multi_swipe = True

        log(tracker)

    enter()
    attack()


def prepare():
    prepare_window()
    sleep(1)


def start():
    log('START')
    demon_lord()
    go_index_page()
    tag_arena()
    log('END')



def main():
    pyautogui.FAILSAFE = True

    track_mouse_position()
    return 0

    # tag_arena()
    # prepare()
    # demon_lord()

    # classic_arena()
    # return 0

    # prepare()
    # demon_lord()

    return 0

    if is_index_page() is True:
        start()
    else:
        go_index_page()
        start()


if __name__ == "__main__":
    main()
