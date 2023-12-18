import math
from helpers.common import *
from text_recognition import *

CRYPT_SLIDES = [
    {
        'title': 'Lizardmen',
        'pixel': {
            'x': 223, 'y': 216
        }
    },
    {
        'title': 'Skinwalker',
        'pixel': {
            'x': 297, 'y': 120
        }
    },
    {
        'title': 'Knights Revenant',
        'pixel': {
            'x': 291, 'y': 332
        }
    },
    {
        'title': 'Undead Horde',
        'pixel': {
            'x': 419, 'y': 216
        }
    },
    {
        'title': 'Demonspawn',
        'pixel': {
            'x': 531, 'y': 119
        }
    },
    {
        'title': 'Ogryn Tribe',
        'pixel': {
            'x': 633, 'y': 328
        }
    },
    {
        'title': 'Orc',
        'pixel': {
            'x': 701, 'y': 217
        }
    },
    {
        'title': 'High Elf',
        'pixel': {
            'x': 767, 'y': 117
        }
    },
    {
        'title': 'Dark Elf',
        'pixel': {
            'x': 22, 'y': 328
        }
    },
    {
        'title': 'Sacred Order',
        'pixel': {
            'x': 213, 'y': 214
        }
    },
    {
        'title': 'Banner Lord',
        'pixel': {
            'x': 295, 'y': 328
        }
    },
    {
        'title': 'Barbarian',
        'pixel': {
            'x': 391, 'y': 119
        }
    },
    {
        'title': 'Dwarf',
        'pixel': {
            'x': 481, 'y': 216
        }
    },
    {
        'title': 'Shadowkin',
        'pixel': {
            'x': 622, 'y': 328
        }
    },
    {
        'title': 'Sylvan Watcher',
        'pixel': {
            'x': 726, 'y': 212
        }
    },
]


# @TODO Must be reworked by following new standard and refactor 'attack' method
def faction_wars():
    tracker = []
    slide_first = np.array(CRYPT_SLIDES)[:8]
    slide_second = np.array(CRYPT_SLIDES)[8:]

    def _swipe_left_border(times=2):
        for i in range(times):
            swipe('left', 50, 400, 800, speed=0.3)

    def _detect(x, y):
        return bool(pixel_check_old(x, y, [30, 36, 49], 3))

    def _attack_item(x, y, title):
        log('Entering ' + title + ' Crypt...')
        # @TODO Should be calculated
        runs = 2
        key_cost = 8

        click(x, y)
        sleep(0.5)

        # @TODO Blindly moves to the bottom (no open floors checking)
        for i in range(2):
            swipe('bottom', 500, 500, 400, speed=0.3)

        # @TODO Custom | visits Knights Revenant 20 floor only
        if title == 'Knights Revenant':
            # click 'Battle' button 20 floor
            click(815, 385)
        else:
            # click 'Battle' button 21 floor
            click(815, 465)

        sleep(0.5)

        # enable "Super Raid Mode"
        if pixel_check_old(653, 335, [108, 237, 255], 3) is False:
            click(653, 335)
            sleep(0.3)

        while runs > 0:
            if runs == 2:
                # click 'Start' button
                click(815, 465)
            else:
                # click 'Replay' button
                dungeons_replay()

            sleep(1)
            waiting_battle_end_regular(title + ' Crypt Battle', x=28, y=88)
            sleep(1)

            # battle has been won
            if pixel_check_old(452, 42, [30, 186, 239], 5):
                runs -= 1

        # going back to all Factions
        for i in range(2):
            pyautogui.press('esc')
            sleep(0.5)

    def enter():
        click_on_progress_info()
        # faction
        click(600, 260)
        sleep(1)

    def attack():

        should_swipe_left = True
        for i in range(len(slide_first)):
            el = slide_first[i]
            title = el['title']

            if bool(tracker.count(title)):
                break

            x = el['pixel']['x']
            y = el['pixel']['y']

            if should_swipe_left:
                _swipe_left_border()

            if _detect(x, y):
                _attack_item(x, y, title)
                tracker.append(title)
                should_swipe_left = True
            else:
                should_swipe_left = False

        should_swipe_left = False
        should_swipe_right = True
        for i in range(len(slide_second)):
            el = slide_second[i]
            title = el['title']

            if bool(tracker.count(title)):
                break

            x = el['pixel']['x']
            y = el['pixel']['y']

            if should_swipe_left:
                _swipe_left_border()

            if should_swipe_right:
                for k in range(2):
                    swipe('right', 850, 200, 690, speed=1)

            if _detect(x, y):
                _attack_item(x, y, title)
                tracker.append(title)
                should_swipe_left = True
                should_swipe_right = True
            else:
                should_swipe_left = False
                should_swipe_right = False

    def finish():
        go_index_page()
        log('DONE - Faction Wars')
        log(tracker)

    enter()
    attack()
    finish()
