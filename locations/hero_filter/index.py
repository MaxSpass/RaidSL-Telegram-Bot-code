import random

import pyautogui
import pyperclip
import keyboard
from helpers.common import *

# def get_filter(x2, y2):
#     return capture_by_source('images/needles/filter.jpg', axis_to_region(0, 0, x2, y2),
#                              confidence=.8)


filter_button = [45, 269, [96, 209, 229]]
filter_reset = [450, 490, [118, 32, 30]]
filter_hide = [660, 490, [20, 123, 156]]
input_field = [653, 104, [239, 233, 211]]
input_clear = [653, 104, [255, 255, 255]]
include_vault = [287, 142, [16, 43, 64]]

BASIC_PARAMETERS = {
    'axis': {
        'rank': {
            '1-2': (338, 372),
            '3': (338, 340),
            '4': (338, 308),
            '5': (338, 280),
            '6': (338, 244),
        },
        'affinity': {
            'void': (536, 244),
            'force': (536, 276),
            'magic': (536, 308),
            'spirit': (536, 340),
        }
    }
}


class HeroFilter:
    FILTER_TYPE_DEFAULT = 'default'
    FILTER_TYPE_SMALL = 'small'

    PICK_SLOTS = {
        '1': [50, 400],
        '2': [50, 490],
    }

    def __init__(self, props=None):
        self.NAME = 'Hero filter'
        self.filter_props = None
        self.filter_needle_type = self.FILTER_TYPE_DEFAULT
        self.is_filter_opened = False
        self.is_input_focused = False

        if props is not None:
            if 'filter_props' in props:
                self.filter_props = props['filter_props']
            if 'filter_needle_type' in props and props['filter_needle_type'] in [self.FILTER_TYPE_SMALL]:
                self.filter_needle_type = props['filter_needle_type']

    def _find_filter(self, region=None, confidence=.7):
        if self.filter_needle_type == self.FILTER_TYPE_SMALL:
            return find_hero_filter_small(region=region, confidence=confidence, retries=5)
        else:
            return find_hero_filter_default(region=region, confidence=confidence, retries=5)

    def _apply_filter_option(self, type):
        option = self.filter_props['basic_parameters'][type]
        for i in range(len(option)):
            _rank_id = str(option[i])
            x, y = BASIC_PARAMETERS['axis'][type][_rank_id]
            click(x, y)
            sleep(.2)

    def filter(self):
        sleep(1)
        if 'basic_parameters' in self.filter_props:

            if 'rank' in self.filter_props['basic_parameters']:
                self._apply_filter_option(type='rank')

            if 'affinity' in self.filter_props['basic_parameters']:
                self._apply_filter_option(type='affinity')

    def open(self, x2=900, y2=520):
        region = axis_to_region(0, 0, x2, y2)

        filter_position = self._find_filter(region=region)
        if filter_position is not None:
            x = filter_position[0]
            y = filter_position[1]
            click(x, y)
            sleep(.3)
            move_out_cursor()
            self.is_filter_opened = True
        else:
            log('Have not found the filter button')

    def hide(self):
        if self.is_filter_opened:
            # click(filter_hide[0], filter_hide[1])
            if await_click([filter_hide], msg=f"{self.NAME} | hide", mistake=5, wait_limit=1)[0]:
                sleep(.3)
                self.is_filter_opened = False
        else:
            log('Filter is not opened')

    def input(self, title):
        if self.is_filter_opened:
            # click(input_field[0], input_field[1])
            if await_click([input_field], msg=f"{self.NAME} | input", mistake=5, wait_limit=1)[0]:
                sleep(.3)
                self.is_input_focused = True
                pyperclip.copy(title)
                keyboard.press_and_release('ctrl + v')
                sleep(.5)
        else:
            log('Filter is not opened')

    def clear(self):
        if self.is_filter_opened:
            # click(input_clear[0], input_clear[1])
            if await_click([input_clear], msg=f"{self.NAME} | clear", mistake=5, wait_limit=1)[0]:
                sleep(.3)
        else:
            log('Filter is not opened')

    def reset(self):
        if self.is_filter_opened:
            # click(filter_reset[0], filter_reset[1])
            if await_click([filter_reset], msg=f"{self.NAME} | reset", mistake=5, wait_limit=1)[0]:
                sleep(.3)
        else:
            log('Filter is not opened')

    def pick(self, slot='1'):
        # n=1 pick a hero from the first cell by default
        if self.is_filter_opened:
            pick_slot = self.PICK_SLOTS[str(slot)]
            click(pick_slot[0], pick_slot[1])
            sleep(.3)
        else:
            log('Filter is not opened')

    def choose(self, title, x2=900, slot='1', wait_after=.5):
        self.open(x2=x2)
        self.input(title=title)
        self.pick(slot=slot)
        self.clear()
        self.reset()
        self.hide()
        sleep(wait_after)
