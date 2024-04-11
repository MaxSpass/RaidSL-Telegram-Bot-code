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

# Quest 1 Start
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
# Quest 1 End

# Quest 2 Start
ARTIFACT_STORAGE_SLOT_WIDTH = 66
ARTIFACT_STORAGE_SLOT_HEIGHT = 66
ARTIFACT_STORAGE_OFFSET = {'x': 258, 'y': 164}
ARTIFACT_STORAGE_SLOTS_MATRIX = [
    # (0, 0), (0, 2), (0, 2), (3, 0), (4, 0), (5, 0),
    (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0),
    (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1),
    (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2),
    (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3),
    (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4),
]
# Quest 2 End

# Quest 6 Start
MARKET_SHARDS_REGION = [35, 80, 650, 450]
# Quest 6 End

hero_filter = HeroFilter({
    'needle_image': 'filter_small.png',
    'needle_region': REGION_TOP_LEFT,
    'filter_props': {
        'basic_parameters': {
            'rank': ['1-2'],
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

    def _attack_campaign(self, quest_id, stage, times):
        x = 755
        y = 480
        counter = 0

        if stage == 7:
            y = 480
        elif stage == 6:
            y = 390

        battles_click()

        # Campaign
        if await_click(
                [[30, 122, [5, 37, 58]]],
                msg='Campaign',
                mistake=10,
                timeout=2,
                wait_limit=30
        )[0]:
            sleep(1)

            # Swipe to the needed campaign location
            for i in range(5):
                swipe('right', 875, 435, 700, speed=.1, sleep_after_end=.2, instant_move=True)

            # Choose Brimstone Path
            click(650, 150)

            if pixels_wait(
                    [[220, 90, [7, 21, 37]]],
                    msg='Stage sidebar',
                    mistake=10,
                    timeout=2,
                    wait_limit=30
            ):
                # Specify 'normal' difficulty
                click(180, 490)
                sleep(.5)
                click(120, 290)
                sleep(.5)

                msg_stage = f"Stage '{str(stage)}'"
                if await_click(
                        [[x, y, [187, 130, 5]]],
                        msg=msg_stage,
                        mistake=10,
                        timeout=2,
                        wait_limit=30
                )[0]:

                    sleep(2)
                    if dungeons_is_able():
                        for k in range(times):
                            dungeons_start_battle()
                            waiting_battle_end_regular(f'{msg_stage} | Battle end', x=28, y=88)
                            counter += 1

                        # click in the "Stage Selection"
                        dungeons_click_stage_select()

                        if counter == times:
                            self.results.append(quest_id)

                else:
                    print(f"Can't reach '{msg_stage}'")
            else:
                print("Can't reach 'Stage sidebar'")
        else:
            print("Can't reach 'Campaign'")

        return 1

    def daily_quest_1(self, quest_id='1'):
        global LEVELS
        global MAX_LEVEL_LIMIT

        levels = LEVELS
        max_levels_limit = MAX_LEVEL_LIMIT

        close_popup_recursive()

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
                        self.results.append(quest_id)
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

                    else:
                        self._log('Hero is NOT active, breaking the loop')
                        break

                if levels > 0:
                    swipes += 1
                    self._log(f'Swipe has been increased: {swipes}')

            if levels > 0:
                self._log(f'Cannot increase {levels} levels')

        close_popup_recursive()

    def daily_quest_2(self, quest_id='2'):
        upgrade_attempts = 4

        close_popup_recursive()

        # Await click on a 'Champions' icon
        await_click([[690, 500, [28, 49, 61]]], msg='Champions icon', mistake=10)

        if await_needle('close.png', region=[820, 24, 80, 80]):
            # Click on a boots artifact
            click(856, 226)

            # Await click on a small 'Filter' button
            await_click([[555, 88, [19, 48, 67]]], msg='Filter button', mistake=10)

            # Wait expanded 'Artifacts sidebar'
            if pixels_wait(
                    [[215, 78, [0, 15, 33]]],
                    msg='Artifacts sidebar',
                    mistake=10,
                    timeout=1,
                    wait_limit=60
            )[0]:

                # Swipe 'Artifacts sidebar' 60px down
                swipe('bottom', 110, 490, 60, speed=.5, instant_move=True)

                # Checked -> 'Hide Set Filters'
                click(190, 498)
                sleep(2)

                running = True
                swipes = 0

                while running:

                    for i in range(swipes):
                        swipe('bottom', 450, 490, 340, speed=3)

                    # All artifact
                    for i in range(len(ARTIFACT_STORAGE_SLOTS_MATRIX)):
                        if upgrade_attempts <= 0:
                            self._log('Upgrade attempts reached')
                            self.results.append(quest_id)
                            running = False
                            break
                        else:
                            x_steps, y_steps = ARTIFACT_STORAGE_SLOTS_MATRIX[i]
                            x_initial = x_steps * ARTIFACT_STORAGE_SLOT_WIDTH + ARTIFACT_STORAGE_OFFSET['x']
                            y_initial = y_steps * ARTIFACT_STORAGE_SLOT_HEIGHT + ARTIFACT_STORAGE_OFFSET['y']

                            x = int(x_initial + ARTIFACT_STORAGE_SLOT_WIDTH / 2)
                            y = int(y_initial + ARTIFACT_STORAGE_SLOT_HEIGHT / 2)
                            pixel_empty_artifact = [x, y, [15, 44, 68]]

                            # if an empty slot
                            if pixel_check_new(pixel_empty_artifact):
                                running = False
                                self._log('Found an empty slot - breaks the loop')
                                break
                            else:

                                click(x, y)
                                # sleep(1)

                                if pixels_wait(
                                        [[240, 325, [16, 78, 110]]],
                                        msg='Artifact info popover',
                                        mistake=10,
                                        timeout=1
                                )[0]:
                                    # Await click
                                    await_click(
                                        [[108, 500, [20, 123, 156]]],
                                        msg='Upgrade button in popover', timeout=1, mistake=10
                                    )

                                    # Check pixel on the top of the frame. Full-screen artifact screen
                                    if pixels_wait(
                                            [[444, 77, [5, 32, 47]]],
                                            msg='Top frame in full-screen',
                                            timeout=1,
                                            wait_limit=2
                                    ):
                                        # if the main 'Upgrade' button is active
                                        if pixel_check_new([430, 466, [187, 130, 5]], mistake=10):
                                            self._log('Able to upgrade')

                                            # Disable 'Instant Upgrade'
                                            if pixel_check_new([264, 435, [108, 237, 255]], mistake=10):
                                                click(264, 435)
                                                sleep(.3)

                                            while upgrade_attempts > 0 and pixels_wait(
                                                    [[430, 466, [187, 130, 5]]],
                                                    msg="Upgrade button in full-screen",
                                                    mistake=10,
                                                    timeout=1,
                                                    wait_limit=5,
                                            )[0]:
                                                # Click on 'Upgrade' button
                                                await_click(
                                                    [[430, 466, [187, 130, 5]]],
                                                    msg='Upgrade button',
                                                    mistake=10, timeout=1, wait_limit=3
                                                )
                                                upgrade_attempts -= 1
                                                self._log(f'Upgrade attempts left: {upgrade_attempts}')

                                            # Delay is needed for properly closing the popup
                                            sleep(5)
                                        else:
                                            self._log('Unable to upgrade')

                                    close_popup()
                                    # Waiting popover right after pop-up closed
                                    pixels_wait(
                                        [[240, 325, [16, 78, 110]]],
                                        msg='Artifact info popover',
                                        mistake=10,
                                        timeout=1
                                    )

                                else:
                                    self._log("Have not found 'Artifact info popover'")

                    if upgrade_attempts > 0:
                        swipes += 1


            else:
                self._log("Have not found 'Artifacts sidebar'")

        close_popup_recursive()

    def daily_quest_3(self, quest_id='3'):
        NUMBER_TO_SUMMON = 3

        close_popup_recursive()

        # Click on the Portal
        click(275, 195)

        # Checking for a Mystery Shard
        if pixels_wait(
                pixels=[[50, 110, [33, 229, 49]]],
                msg='Mystery Shard',
                mistake=10,
                timeout=1,
                wait_limit=3
        )[0]:

            counter = 0
            for i in range(NUMBER_TO_SUMMON):
                # Coordinates depending on the index
                x = 460 if i == 0 else 195
                y = 475 if i == 0 else 465
                if await_click(
                        [[x, y, [187, 130, 5]]],
                        msg='Summon button',
                        mistake=10,
                        timeout=3,
                        wait_limit=30
                )[0]:
                    counter += 1
                    self._log(f'Summoned {counter} heroes from Mystery shards')
                    sleep(1)
                else:
                    print("Can't reach 'Summon button'")

            if counter == NUMBER_TO_SUMMON:
                self.results.append(quest_id)

        else:
            self._log('Have not found the Mystery Shard')

        # Wait until there is no screen lock
        sleep(5)

        close_popup_recursive()

    def daily_quest_6(self, quest_id='6'):
        global MARKET_SHARDS_REGION
        counter = 0

        close_popup_recursive()

        # Click on the Market
        click(315, 360)
        sleep(3)

        def _find_shards():
            return list(filter(lambda x: x is not None, [
                find_needle('market_ancient_shard.jpg', region=MARKET_SHARDS_REGION),
                find_needle('market_mystery_shard.jpg', region=MARKET_SHARDS_REGION)
            ]))

        frame_index = 0
        shards = _find_shards()
        while len(shards) or frame_index == 0:
            for k in range(len(shards)):
                print('Found shard in the frame')
                position = shards[k]
                x = position[0]
                y = position[1]
                click(x, y)

                if await_click(
                        [[630, 340, [187, 130, 5]]],
                        msg='Shard purchase button in dialog',
                        mistake=10,
                        timeout=2
                )[0]:
                    sleep(1)
                    counter += 1
                else:
                    print("Can't reach 'Shard purchase button in dialog'")

            shards = _find_shards()

            if not len(shards) and frame_index == 0:
                swipe('bottom', 362, 500, 300, speed=.2, sleep_after_end=.5, instant_move=True)
                shards = _find_shards()
                frame_index += 1

        if counter > 0:
            self.results.append(quest_id)

        close_popup_recursive()

    def daily_quest_7(self, quest_id='7', stage=7, times=3):
        close_popup_recursive()
        # Brimstone Path Stage: 7, Times: 3
        self._attack_campaign(quest_id, stage=stage, times=times)
        close_popup_recursive()

    def daily_quest_8(self, quest_id='8', stage=6, times=7):
        # Brimstone Path Stage: 6, Times: 7
        self._attack_campaign(quest_id, stage=stage, times=times)

    def handle_quest(self, quest_id):
        _qid = str(quest_id)

        if _qid == '1':
            # Increase Champion's Level in Tavern 3 times
            self.daily_quest_1(_qid)
        elif _qid == '2':
            # Make 4 Artifact/Accessory upgrade attempts
            self.daily_quest_2(_qid)
        elif _qid == '3':
            # Summon 3 Champions
            self.daily_quest_3(_qid)
        elif _qid == '6':
            # Purchase an item at the Market
            self.daily_quest_6(_qid)
        elif _qid == '7':
            # Beat a Campaign Boss 3 times
            # @TODO Temp decision | Default: times=3
            self.daily_quest_7(_qid, times=7)
        elif _qid == '8':
            # Win Campaign Battles 7 times
            self.daily_quest_8(_qid)

    def enter(self):
        close_popup_recursive()

    def report(self):
        res = None

        if len(self.results):
            res = f'{self.LOCATION_NAME} | Completed Daily quest IDs: {str(np.array(self.results, dtype=object))}'

        return res

    def finish(self):
        close_popup_recursive()
        self._log('Done')

    def run(self, *args, props=None):
        HARDCODE_QUEST_IDS = ['1', '2', '3', '6', '7']

        self.enter()

        for quest_id in HARDCODE_QUEST_IDS:
            self.handle_quest(quest_id)

        self.finish()
