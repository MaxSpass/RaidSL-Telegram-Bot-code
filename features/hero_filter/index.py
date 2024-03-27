import random

import pyautogui
import pyperclip
import keyboard
from helpers.common import *


# def get_filter(x2, y2):
#     return capture_by_source('images/needles/filter.jpg', axis_to_region(0, 0, x2, y2),
#                              confidence=.8)


filter_button = [45, 269, [96, 209, 229]]
filter_reset = [377, 491, [66, 68, 70]]
filter_close = [570, 493, [217, 211, 194]]
input_field = [442, 99, [230, 224, 203]]
input_clear = [656, 102, [24, 47, 56]]
include_vault = [287, 142, [16, 43, 64]]

BASIC_PARAMETERS = {
    'axis': {
        'rank': {
            '1-2': (338, 372),
            '3': (338, 340),
            '4': (338, 308),
            '5': (338, 280),
            '6': (338, 244),
        }
    }
}

class HeroFilter:
    PICK_SLOTS = {
        '1': [50, 400],
        '2': [50, 490],
    }

    is_filter_opened = False
    is_input_focused = False

    def __init__(self, props=None):
        self.filter_props = None
        self.needle_image = 'filter.jpg'

        if props is not None:
            if 'filter_props' in props:
                self.filter_props = props['filter_props']
            if 'needle_image' in props:
                self.needle_image = props['needle_image']
            if 'needle_region' in props:
                self.needle_region = props['needle_region']


    def _get_filter(self, x2, y2, region=None, confidence=.8):
        if region is None:
            region = axis_to_region(0, 0, x2, y2)

        return capture_by_source(f'images/needles/{self.needle_image}', region, confidence=confidence)

    def filter(self):
        sleep(1)
        if 'basic_parameters' in self.filter_props:
            if 'rank' in self.filter_props['basic_parameters']:
                rank = self.filter_props['basic_parameters']['rank']
                for i in range(len(rank)):
                    _rank_id = str(rank[i])
                    x, y = BASIC_PARAMETERS['axis']['rank'][_rank_id]
                    click(x, y)
                    sleep(.2)


    def open(self, x2=900, y2=520):
        filter_position = self._get_filter(x2, y2)
        if filter_position is not None:
            x = filter_position[0]
            y = filter_position[1]
            click(x, y)
            sleep(.3)
            move_out_cursor()
            self.is_filter_opened = True
        else:
            log('Have not found the filter button')

    def close(self):
        if self.is_filter_opened:
            # close hero_filter
            click(filter_close[0], filter_close[1])
            sleep(.3)
            self.is_filter_opened = False
        else:
            log('Filter is not opened')

    def input(self, name):
        if self.is_filter_opened:
            # focus input_field
            click(input_field[0], input_field[1])
            sleep(.5)
            self.is_input_focused = True
            # interval = random.randint(2, 5) / 10

            pyperclip.copy(name)
            keyboard.press_and_release('ctrl + v')
            sleep(.5)
        else:
            log('Filter is not opened')

    def clear(self):
        if self.is_filter_opened:
            # reset hero_filter
            click(input_clear[0], input_clear[1])
            sleep(.3)
        else:
            log('Filter is not opened')

    def reset(self):
        if self.is_filter_opened:
            # reset hero_filter
            click(filter_reset[0], filter_reset[1])
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
