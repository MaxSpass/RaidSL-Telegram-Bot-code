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
    '1': {'x': 44, 'y': 136},
    '2': {'x': 44, 'y': 257},
    '3': {'x': 44, 'y': 378},
    '4': {'x': 44, 'y': 498},
}

rgb_active_team = [71, 223, 255]

def get_presets(x2, y2):
    return capture_by_source('images/needles/presets.jpg', axis_to_region(0, 0, x2, y2),
                             confidence=.8)

class HeroPreset():
    def __init__(self):
        self.is_presets_opened = False

    def open(self, x2=900, y2=520):
        # clan boss = x2:150, y2:350
        presets_position = get_presets(x2, y2)
        if presets_position is not None:
            x = presets_position[0]
            y = presets_position[1]
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

        # @TODO Does not support scrolling
        if index in PRESET_POSITIONS:
            p = PRESET_POSITIONS[index]
            x = p['x']
            y = p['y']
            if not pixel_check_new([x, y, rgb_active_team], mistake=5):
                click(x, y)
        else:
            log('Presets | No preset_index found')

    def choose(self, preset_index=1):
        self.open()
        if self.is_presets_opened:
            self.pick(preset_index)
            self.close()
        sleep(.5)

