import pyautogui

from helpers.common import *

# clan boss
# PRESET_POSITIONS = {
#     '1': {'x': 44, 'y': 132},
#     '2': {'x': 44, 'y': 252},
#     '3': {'x': 44, 'y': 374},
#     '4': {'x': 44, 'y': 494},
# }

# hydra
PRESET_POSITIONS = {
    # '1': {'x': 46, 'y': 136},
    # '2': {'x': 46, 'y': 257},
    '1': {'x': 46, 'y': 134},
    '2': {'x': 46, 'y': 254},
    '3': {'x': 46, 'y': 374},
    '4': {'x': 46, 'y': 494},
}

PRESET_ACTIVE_TEAM_RGB = [71, 223, 255]
# check dominant color: \images\docs\hero_preset.jpg
PRESET_CHECKBOX_LOCKED_HUE = 71
PRESET_CHECKBOX_CHECKED_HUE = 72
PRESET_CHECKBOX_UNCHECKED_HUE = 73
PRESET_CHECKBOX_LOCKED_SIZE = 28
PRESET_CHECKBOX_OFFSET = PRESET_CHECKBOX_LOCKED_SIZE / 2


def get_presets(region=None):
    if not region:
        region = [0, 32, 906, 501]

    return capture_by_source('images/needles/presets.jpg', region, confidence=.7, grayscale=True)


class HeroPreset():
    def __init__(self):
        self.is_presets_opened = False

    def _get_hue_by_preset(self, preset_position):
        x = preset_position['x']
        y = preset_position['y']
        region = [
            int(x - PRESET_CHECKBOX_OFFSET),
            int(y - PRESET_CHECKBOX_OFFSET),
            PRESET_CHECKBOX_LOCKED_SIZE,
            PRESET_CHECKBOX_LOCKED_SIZE
        ]

        # checks is already blocked
        if not find_team_preset_locked(region=region):
            return dominant_color_hue(region=region, rank=1)

        log('Team Preset is already locked')
        return False

    def open(self):
        # avoid sudden notification in this area
        sleep(7)
        # clan boss = x2:150, y2:350
        presets_position = get_presets()
        if presets_position is not None:
            # Offset is needed for avoiding calculating hue color bug
            offset = 6
            x = presets_position[0] + offset
            y = presets_position[1] + offset
            click(x, y)
            sleep(1)
            self.is_presets_opened = True
        else:
            log('Have not found the presets button')

    def close(self):
        if self.is_presets_opened:
            # close presets
            # @TODO Test
            close_popup()
            sleep(1)
        else:
            log('Presets is not opened')

    def pick(self, preset_index):
        index = str(preset_index)
        is_checked = False

        # @TODO Does not support scrolling
        if index in PRESET_POSITIONS:
            p = PRESET_POSITIONS[index]
            x = p['x']
            y = p['y']
            checkbox_hue = self._get_hue_by_preset(p)
            if checkbox_hue == PRESET_CHECKBOX_UNCHECKED_HUE:
                click(x, y)
                is_checked = True
                log(f'Presets | The team #{index} just picked')
            elif checkbox_hue == PRESET_CHECKBOX_CHECKED_HUE:
                is_checked = True
                log(f'Presets | The team #{index} is already picked')
            elif checkbox_hue == PRESET_CHECKBOX_LOCKED_HUE:
                log(f'Presets | The team #{index} has been locked')

            # if not pixel_check_new([x, y, PRESET_ACTIVE_TEAM_RGB], mistake=5):
            #     click(x, y)
        else:
            log('Presets | No preset_index found')

        return is_checked

    def choose(self, preset_index=1):
        res = None
        self.open()
        if self.is_presets_opened:
            res = self.pick(preset_index)
            self.close()
        sleep(.5)
        return res
