from helpers.common import *
from more_itertools import first_true

DUNGEON_MINOTAUR = "Minotaur's Labyrinth"
DUNGEON_GOLEM = "Ice Golem's Peak"
DUNGEON_SPIDER = "Spider's Den"
DUNGEON_DRAGON = "Dragon's Lair"
DUNGEON_FIRE = "Fire Knight's Castle"
DUNGEON_SAND_DEVIL = "Sand Devil's Necropolis"
DUNGEON_PHANTOM = "Phantom Shogun's Grove"
# TODO is not considered here
DUNGEON_IRON_TWINS = "Iron Twins Fortress"

# DUNGEON_POSITION_PRESETS = {
#     'primary': {
#         {'stage': 1, 'swipes': 0, 'x': 0, 'y': 0},
#         {'stage': 2, 'swipes': 0, 'x': 0, 'y': 0},
#         {'stage': 3, 'swipes': 0, 'x': 0, 'y': 0},
#         {'stage': 4, 'swipes': 0, 'x': 0, 'y': 0},
#         {'stage': 5, 'swipes': 0, 'x': 0, 'y': 0},
#         {'stage': 6, 'swipes': 0, 'x': 0, 'y': 0},
#         {'stage': 7, 'swipes': 0, 'x': 0, 'y': 0},
#         {'stage': 8, 'swipes': 0, 'x': 0, 'y': 0},
#         {'stage': 9, 'swipes': 0, 'x': 0, 'y': 0},
#         {'stage': 10, 'swipes': 0, 'x': 0, 'y': 0},
#         {'stage': 11, 'swipes': 0, 'x': 0, 'y': 0},
#         {'stage': 12, 'swipes': 0, 'x': 0, 'y': 0},
#         {'stage': 13, 'swipes': 0, 'x': 0, 'y': 0},
#         {'stage': 14, 'swipes': 0, 'x': 0, 'y': 0},
#         {'stage': 15, 'swipes': 0, 'x': 0, 'y': 0},
#         {'stage': 16, 'swipes': 0, 'x': 0, 'y': 0},
#         {'stage': 17, 'swipes': 0, 'x': 0, 'y': 0},
#         {'stage': 18, 'swipes': 0, 'x': 0, 'y': 0},
#         {'stage': 19, 'swipes': 0, 'x': 0, 'y': 0},
#         {'stage': 20, 'swipes': 0, 'x': 0, 'y': 0},
#         {'stage': 21, 'swipes': 0, 'x': 0, 'y': 0},
#         {'stage': 22, 'swipes': 0, 'x': 0, 'y': 0},
#         {'stage': 23, 'swipes': 0, 'x': 0, 'y': 0},
#         {'stage': 24, 'swipes': 0, 'x': 0, 'y': 0},
#         {'stage': 25, 'swipes': 0, 'x': 0, 'y': 0},
#     }
# }

DUNGEON_DATA = [
    {'id': '1', 'name': DUNGEON_MINOTAUR},
    {'id': '2', 'name': DUNGEON_GOLEM},
    {'id': '3', 'name': DUNGEON_SPIDER},
    {'id': '4', 'name': DUNGEON_DRAGON},
    {'id': '5', 'name': DUNGEON_FIRE},
    {'id': '6', 'name': DUNGEON_SAND_DEVIL},
    {'id': '7', 'name': DUNGEON_PHANTOM},
]

DUNGEON_NO_DIFFICULTIES = ['1', '6', '7']

DUNGEON_LOCATIONS = {
    '1': {
        'swipe': 1,
        'click': {'x': 420, 'y': 300},
    },
    '2': {
        'swipe': 1,
        'click': {'x': 540, 'y': 160},
    },
    '3': {
        'swipe': 1,
        'click': {'x': 680, 'y': 300},
    },
    '4': {
        'swipe': 1,
        'click': {'x': 775, 'y': 175},
    },
    '5': {
        'swipe': 2,
        'click': {'x': 490, 'y': 300},
    },
    '6': {
        'swipe': 2,
        'click': {'x': 650, 'y': 170},
    },
    '7': {
        'swipe': 2,
        'click': {'x': 810, 'y': 340},
    },
}


# props
# { 'String', [ Int, 'battle' | 'energy' ], {
# refill_force: Boolean,
# refill_max: Int,
# difficulty: 'normal' | 'hard'
# enable_super_raid: Boolean
# }}

# @TODO
# - passing 'difficulty' and 'enable_super_raid'
# - choosing certain lvl/stage for each dungeon
class Dungeons:
    LOCATION_NAME = 'Dungeon'
    BUTTON_START = [850, 475, [187, 130, 5]]
    CHECKBOX_SUPER_RAID = [655, 336, [108, 237, 255]]
    REFILL_PAID = [440, 376, [255, 33, 51]]
    DEFEAT = [443, 51, [229, 40, 104]]
    DIFFICULTY_SELECT = [144, 490, [13, 35, 45]]
    RGB_DIFFICULTY = [34, 47, 60]
    DIFFICULTY_NORMAL = [144, 394, RGB_DIFFICULTY]
    DIFFICULTY_HARD = [144, 450, RGB_DIFFICULTY]

    DUNGEON_DIFFICULTY_NORMAL = 'normal'
    DUNGEON_DIFFICULTY_HARD = 'hard'
    DUNGEON_DIFFICULTY_DEFAULT = DUNGEON_DIFFICULTY_HARD
    DUNGEON_SUPER_RAID_DEFAULT = False
    DIFFICULTIES = {
        DUNGEON_DIFFICULTY_NORMAL: DIFFICULTY_NORMAL,
        DUNGEON_DIFFICULTY_HARD: DIFFICULTY_HARD,
    }

    def __init__(self, props=None):
        self.dungeons = []
        self.results = {}
        self.current = None

        self._apply_props(props)

        # for i in range(len(self.dungeons)):
        #     print(self.dungeons[i])

    def _apply_props(self, props=None):
        # # @TODO it starts working from Index Page only
        # go_index_page()

        if props is not None:
            length = len(props['locations'])

            self.bank = int(props['bank']) if 'bank' in props and not bool(props['bank']) else read_energy_bank()
            self.refill = bool(props['refill']) if 'refill' and bool(props['refill']) in props else False
            self.super_raid = bool(props['super_raid']) \
                if 'super_raid' and bool(props['super_raid']) in props\
                else self.DUNGEON_SUPER_RAID_DEFAULT

            self._log(f'Bank: {self.bank}')

            available_energy = self.bank

            if 'locations' in props and length:
                for i in range(length):
                    _dungeon = None
                    _location = props['locations'][i]
                    if 'id' in _location:
                        _id = str(_location['id'])
                        j, dungeon = find(DUNGEON_DATA, lambda x: x['id'] == _id)

                        if dungeon:
                            _dungeon = dungeon

                            if _id not in DUNGEON_NO_DIFFICULTIES:
                                _dungeon['difficulty'] = _location['difficulty'] \
                                    if 'difficulty' in _location \
                                    else self.DUNGEON_DIFFICULTY_DEFAULT

                            if 'energy' in _location:
                                _e = int(_location['energy'])
                                if _e <= available_energy:
                                    _dungeon['energy'] = _e
                                    if available_energy >= _e:
                                        available_energy -= _e

                    if _dungeon:
                        self.dungeons.append(_dungeon)

                if available_energy > 0:
                    # calculating energy for 'not defined energy' locations
                    no_energy_quantity = len(list(filter(lambda x: 'energy' not in x, self.dungeons)))
                    if no_energy_quantity > 0:
                        energy_for_each = round(available_energy / no_energy_quantity)
                        for i in range(len(self.dungeons)):
                            _d = self.dungeons[i]
                            if 'energy' not in self.dungeons[i]:
                                self.dungeons[i]['energy'] = energy_for_each

        for i in range(len(self.dungeons)):
            print(self.dungeons[i])

    def _initialize(self, dungeon):
        self.current = dungeon
        if dungeon['id'] not in self.results:
            self.results[dungeon['id']] = {
                'victory': 0,
                'defeat': 0,
            }

    def _is_first_battle(self):
        _id = self.current['id']
        return (self.results[_id]['victory'] + self.results[_id]['defeat']) == 0

    def _able_attacking(self, cost):
        return self.current['energy'] >= cost or self.refill

    def _save_result(self, condition):
        _id = self.current['id']
        if condition:
            self.results[_id]['victory'] += 1
        else:
            self.results[_id]['defeat'] += 1

    def _select_difficulty(self, difficulty):
        if difficulty in self.DIFFICULTIES:
            await_click([self.DIFFICULTY_SELECT], mistake=5)
            await_click([self.DIFFICULTIES[difficulty]], mistake=5)

    def _exit_location(self):
        # click on the "Stage selection"
        dungeons_results_finish()
        # moving to the Index Page for starting new Dungeon location
        go_index_page()

    def _start_battle(self):
        sleep(1)
        if self._is_first_battle():
            # click on 'Start'
            await_click([self.BUTTON_START], msg='await button start', timeout=1, mistake=10)
        else:
            # click on 'Replay'
            dungeons_replay()
        sleep(1)

    def _click_on_super_raid(self):
        x = self.CHECKBOX_SUPER_RAID[0]
        y = self.CHECKBOX_SUPER_RAID[1]
        click(x, y)
        sleep(.3)

    def _log(self, message):
        log(f"{self.LOCATION_NAME} | {message}")

    def enter(self):
        go_index_page()
        sleep(1)
        go_index_page()

        location = DUNGEON_LOCATIONS[str(self.current['id'])]

        battles_click()
        sleep(1)

        # enter all dungeons
        click(300, 300)

        length = location['swipe']
        for i in range(length):
            # moving to the certain dungeon
            swipe('right', 850, 400, 800, speed=.5)
            x = location['click']['x']
            y = location['click']['y']
            # click on dungeon icon
            click(x, y)
            sleep(1)

        # swiping bottom
        swipe('bottom', 500, 450, 400, speed=.5)

        if 'difficulty' in self.current:
            self._select_difficulty(self.current['difficulty'])

        # @TODO Works with the last stage/floor only
        # click last floor
        click(850, 475)
        sleep(.5)

        # @TODO validate
        if self.super_raid:
            if not pixel_check_new(self.CHECKBOX_SUPER_RAID, mistake=10):
                self._click_on_super_raid()
        else:
            if pixel_check_new(self.CHECKBOX_SUPER_RAID, mistake=10):
                self._click_on_super_raid()

    def attack(self):
        skip = False

        self._start_battle()

        sleep(1)
        ruby_button = find_needle_refill_ruby()

        if ruby_button is not None:
            self._log('Free coins are NOT available')
            if self.refill:
                await_click([self.REFILL_PAID], mistake=10)
                self._start_battle()
            else:
                self._log('No more refill')
                skip = True

        if not skip:
            _name = self.current['name']
            waiting_battle_end_regular(f'{_name} battle end', x=28, y=88)
            sleep(1)

            result = not pixel_check_new(self.DEFEAT)
            self._save_result(result)

    def finish(self):
        go_index_page()
        log('DONE - ' + self.LOCATION_NAME)

    def report(self):
        res = None

        for _id, value in self.results.items():
            j, dungeon = find(DUNGEON_DATA, lambda x: x['id'] == _id)
            key = dungeon['name'] if dungeon else _id
            has_battles = value['victory'] + value['defeat'] > 0

            if has_battles:
                if not res:
                    res = f'{self.LOCATION_NAME} Report\n'

                win_rate = calculate_win_rate(value['victory'], value['defeat'])
                line = f"{key} | Battles: {value['victory'] + value['defeat']}, Win rate: {win_rate}"
                res += f"{line}\n"

        return res


    def run(self, props=None):
        if props is not None:
            self._apply_props(props)

        # return

        for i in range(len(self.dungeons)):
            self._initialize(self.dungeons[i])
            self._log(f"Starting {self.current['name']}")
            self.enter()

            cost = read_energy_cost()
            self._log(f'Energy cost: {cost}')

            while self._able_attacking(cost):
                self._log('Start battle')
                self.attack()
                # @TODO Validate
                # decreasing energy of the certain Dungeon
                self.current['energy'] -= cost

            self._exit_location()

        self.finish()
