import pyautogui

from helpers.common import *
from features.hero_filter.index import *

CHAMPIONS = [690, 500, [28, 49, 61]]
REGION_TOP_LEFT = axis_to_region(0, 35, 210, 115)
QUESTS_BUTTON_UPGRADE = [866, 474, [187, 130, 5]]
QUESTS_POSITIONS = {
    'daily': {
        'quests': [
            {'position': 1, 'swipes': 0},
            {'position': 2, 'swipes': 0},
            {'position': 3, 'swipes': 0},
            {'position': 4, 'swipes': 0},

            {'position': 4, 'swipes': 3},
            {'position': 4, 'swipes': 3},
            {'position': 4, 'swipes': 3},
        ]
    }
}

# @TODO Common
SIDEBAR_SLOT_WIDTH = 66
SIDEBAR_SLOT_HEIGHT = 84
SIDEBAR_SLOT_GUTTER = 8
SIDEBAR_SLOTS_OFFSET = {'x': 16, 'y': 118}
SIDEBAR_SLOTS_MATRIX = [
    (0, 0), (1, 0), (2, 0),
    (0, 1), (1, 1), (2, 1),
    (0, 2), (1, 2), (2, 2),
    (0, 3), (1, 3), (2, 3)
]
SIDEBAR_SLOT_ACTIVE_RGB = [6, 255, 0]
SIDEBAR_REGION_AREA = axis_to_region(14, 106, 212, 532)
XP_BAR_REGION = [322, 394, 328, 62]
XP_BAR_REGION_CURRENT_LVL_CHAMPIONS_SCREEN = [514, 482, 90, 15]
XP_BAR_REGION_CURRENT_LVL_TAVERN_SCREEN = [560, 437, 88, 16]
XP_BAR_REGION_END = [511, 483, 3, 14]
XP_BAR_DOMINANT_RGB_NOT_FULL = [0, 0, 0]
# @TODO Extend
AFFINITIES = [
    {'name': 'spirit', 'needle': 'affinity/beer_spirit.png'},
    {'name': 'force', 'needle': 'affinity/beer_force.png'},
    {'name': 'magic', 'needle': 'affinity/beer_magic.png'},
    {'name': 'void', 'needle': 'affinity/beer_void.png'},
]
TAVERN_AFFINITY_REGIONS = {
    'magic': [164, 38, 52, 18],
    'spirit': [250, 38, 52, 18],
    'force': [340, 38, 52, 18],
    'void': [428, 38, 52, 18],
}
BEER_SCALE_FACTOR = .55
BEER_CONFIDENCE = .7
MAX_LEVEL_LIMIT = 10
LEVELS = 3

hero_filter = HeroFilter({
    'needle_image': 'filter_small.png',
    'needle_region': REGION_TOP_LEFT,
    'filter_props': {
        'basic_parameters': {
            'rank': ['1-2', 4],
        }
    }
})


class Quests:
    LOCATION_NAME = 'Quests'

    def __init__(self, props=None):
        self.results = []

    def _log(self, msg):
        print(f'{self.LOCATION_NAME} | {msg}')

    def _get_level_tavern_screen(self):
        return read_text(
            region=XP_BAR_REGION_CURRENT_LVL_TAVERN_SCREEN,
            parser=parse_levels,
            scale=4
        )

    def handle_quest(self, quest_id):
        global LEVELS
        global MAX_LEVEL_LIMIT
        # for affinity, region in TAVERN_AFFINITY_REGIONS.items():
        #     amount_str = read_text(region=region, scale=4, parser=parse_energy_cost)
        #     print(type(amount_str))
        #     print(f"{affinity}: {amount_str}")

        # swipe('bottom', 112, 442, 343, speed=3)
        # return

        close_popup_recursive()

        if str(quest_id) == '1':
            levels = LEVELS
            max_levels_limit = MAX_LEVEL_LIMIT

            await_click([CHAMPIONS], mistake=20)
            columns_mode = await_needle('heroes_sidebar_columns_mode.png', confidence=.7, region=REGION_TOP_LEFT)
            if columns_mode is not None:
                should_filter = True
                running = True
                swipes = 0

                while running:
                    for s in range(swipes):
                        swipe('bottom', 112, 442, 343, speed=3)

                    for i in range(len(SIDEBAR_SLOTS_MATRIX)):
                        if levels <= 0:
                            break
                        else:
                            self._log(f'Levels needs to be up: {str(levels)}')

                        if should_filter:
                            hero_filter.open()
                            hero_filter.filter()
                            hero_filter.close()

                        x_steps, y_steps = SIDEBAR_SLOTS_MATRIX[i]
                        x_initial = x_steps * SIDEBAR_SLOT_WIDTH + SIDEBAR_SLOTS_OFFSET['x']
                        y_initial = y_steps * SIDEBAR_SLOT_HEIGHT + SIDEBAR_SLOTS_OFFSET['y']

                        x = x_initial + SIDEBAR_SLOT_WIDTH / 2
                        y = y_initial + SIDEBAR_SLOT_HEIGHT / 2

                        click(x, y)
                        sleep(.5)

                        # Detecting the fact of choosing a hero
                        region_slot = (
                            x_initial,
                            y_initial,
                            3,
                            SIDEBAR_SLOT_HEIGHT,
                        )

                        color_dominant_active = dominant_color_rgb(region=region_slot)
                        running = rgb_check(color_dominant_active, SIDEBAR_SLOT_ACTIVE_RGB, mistake=10)
                        # show_pyautogui_image(pyautogui.screenshot(region=region_slot))
                        print('color_dominant_active', color_dominant_active)
                        if running:
                            self._log('Hero is active')

                            color_dominant_lvl_bar_end = dominant_color_rgb(region=XP_BAR_REGION_END)
                            if rgb_check(color_dominant_lvl_bar_end, XP_BAR_DOMINANT_RGB_NOT_FULL):
                                self._log('Hero is ready for lvl-up')

                                # @TODO Checking lvl before up
                                lvl_current_info = read_text(
                                    region=XP_BAR_REGION_CURRENT_LVL_CHAMPIONS_SCREEN,
                                    parser=parse_levels
                                )
                                if lvl_current_info is not None:
                                    lvl_current_info_split = lvl_current_info.split('/')
                                    lvl_initial = int(lvl_current_info_split[0])
                                    lvl_max = int(lvl_current_info_split[1])
                                    self._log(f"Initial lvl: {lvl_initial} | Max lvl: {lvl_max}")

                                    # @TODO Take from props (does not work)
                                    if lvl_initial >= max_levels_limit:
                                        self._log(f"Skip | Exceeds the permissible level: {max_levels_limit}")
                                        should_filter = False
                                        continue

                                    # Taverna
                                    click(592, 436)
                                    sleep(1)

                                    move_out_cursor()

                                    position_sort_order = find_needle(
                                        'sort_order.png',
                                        region=REGION_TOP_LEFT,
                                        confidence=.7
                                    )
                                    if position_sort_order is not None:
                                        # Sort order
                                        click(172, 92)
                                        sleep(1)

                                    beer_points = []
                                    for k in range(len(AFFINITIES)):
                                        path_image = os.path.normpath(
                                            os.path.join(os.getcwd(), 'images/needles/' + AFFINITIES[k]['needle'])
                                        )

                                        physical_image = cv2.imread(path_image)

                                        scaled_image = scale_up(image=physical_image, factor=BEER_SCALE_FACTOR)

                                        cropped_image = crop(scaled_image, region=(28, 30, 25, 25))

                                        _beer = pyautogui.locateCenterOnScreen(
                                            cropped_image,
                                            region=SIDEBAR_REGION_AREA,
                                            confidence=BEER_CONFIDENCE
                                        )

                                        if _beer is not None:
                                            beer_points.append({
                                                'name': AFFINITIES[k]['name'],
                                                'x': _beer[0],
                                                'y': _beer[1],
                                            })

                                    if len(beer_points):
                                        sorted_beers = sort_by_closer_axis(beer_points)
                                        lvl_desired = None

                                        for l in range(len(sorted_beers)):
                                            if lvl_desired == lvl_max:
                                                break

                                            beer = sorted_beers[l]
                                            self._log(f"Beer: {beer}")

                                            beer_region = TAVERN_AFFINITY_REGIONS[beer['name']]

                                            # @TODO Parser 'parse_energy_cost' is not intended to be used here
                                            beer_total_float = read_text(
                                                region=beer_region,
                                                scale=4,
                                                parser=parse_energy_cost
                                            )
                                            if type(beer_total_float) is float:
                                                self._log(f"Beer {beer['name']}: {str(beer_total_float)}")
                                                beer_total = int(beer_total_float)

                                                # @TODO Total beer amount calculation

                                                x_beer = beer['x']
                                                y_beer = beer['y']
                                                click(x_beer, y_beer)
                                                sleep(5)
                                                beer_total -= 1
                                                lvl_desired = int(self._get_level_tavern_screen())

                                                # @TODO Up the lvl | Calculating beer amount is required

                                                while beer_total > 0 \
                                                        and levels > 0 \
                                                        and lvl_desired < lvl_max \
                                                        and not (lvl_desired - lvl_initial) >= levels:

                                                    self._log(f"Initial Lvl: {lvl_initial} "
                                                              f"| Desired Lvl: {str(lvl_desired)}")

                                                    position_button_plus_beer = find_needle(
                                                        'bar_plus.png',
                                                        region=XP_BAR_REGION
                                                    )

                                                    x_plus = position_button_plus_beer[0]
                                                    y_plus = position_button_plus_beer[1]
                                                    click(x_plus, y_plus)
                                                    sleep(5)
                                                    beer_total -= 1
                                                    lvl_desired = int(self._get_level_tavern_screen())

                                                await_click([QUESTS_BUTTON_UPGRADE], mistake=10)
                                                sleep(3)
                                                self._log(f"Increased levels by {LEVELS}")
                                                levels -= lvl_desired - lvl_initial
                                                if levels <= 0:
                                                    break

                                # Champions
                                click(688, 104)
                                sleep(1)

                            else:
                                self._log('Hero is NOT ready for lvl-up')

                            running = False
                            self._log(f'Swipe has been increased: {swipes}')

                        else:
                            self._log('Hero is NOT active, breaking the loop')
                            break

                    if levels > 0:
                        swipes += 1

                if levels > 0:
                    self._log(f'Cannot increase {levels} levels')

        close_popup_recursive()


    def enter(self):
        close_popup_recursive()
        return 1

    def report(self):
        return 1

    def finish(self):
        close_popup_recursive()
        return 1

    def run(self):
        return 1
