from helpers.common import *

# when fake battle is needed
FAKE_BATTLE = False

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
    '1': {'swipe': 1, 'click': {'x': 420, 'y': 300}},
    '2': {'swipe': 1, 'click': {'x': 540, 'y': 160}},
    '3': {'swipe': 1, 'click': {'x': 680, 'y': 300}},
    '4': {'swipe': 1, 'click': {'x': 775, 'y': 175}},
    '5': {'swipe': 2, 'click': {'x': 490, 'y': 300}},
    '6': {'swipe': 2, 'click': {'x': 650, 'y': 170}},
    '7': {'swipe': 2, 'click': {'x': 810, 'y': 340}},
}


class Dungeons:
    LOCATION_NAME = 'Dungeon'
    BUTTON_START = [850, 475, [187, 130, 5]]
    # @TODO Duplication
    STAGE_ENTER = [850, 200, [93, 25, 27]]
    # @TODO Duplication
    SUPER_RAID = [655, 336, [108, 237, 255]]
    REFILL_PAID = [440, 376, [255, 33, 51]]
    DEFEAT = [443, 51, [229, 40, 104]]
    DIFFICULTY_SELECT = [144, 490, [13, 35, 45]]
    RGB_DIFFICULTY = [34, 47, 60]
    DIFFICULTY_NORMAL = [144, 394, RGB_DIFFICULTY]
    DIFFICULTY_HARD = [144, 450, RGB_DIFFICULTY]

    DUNGEON_DIFFICULTY_NORMAL = 'normal'
    DUNGEON_DIFFICULTY_HARD = 'hard'
    DUNGEON_BANK_MIN_LIMIT = 8
    DUNGEON_DIFFICULTY_DEFAULT = DUNGEON_DIFFICULTY_HARD
    DUNGEON_SUPER_RAID_DEFAULT = True
    DIFFICULTIES = {
        DUNGEON_DIFFICULTY_NORMAL: DIFFICULTY_NORMAL,
        DUNGEON_DIFFICULTY_HARD: DIFFICULTY_HARD,
    }

    def __init__(self, props=None):
        self.dungeons = []
        self.results = {}
        self.current = None
        self.terminate = False

        self.bank = 0
        self.refill = 0
        self.locations = []
        self.super_raid = self.DUNGEON_SUPER_RAID_DEFAULT

        # @TODO Temp dirty fix
        self.props = props
        # self._apply_props(props)
        # self._distribute_energy()

    # @TODO These responsibility must be on the different scope
    def _get_available_energy(self):
        # @TODO These responsibility must be on the different scope
        close_popup_recursive()
        return read_available_energy()

    def _distribute_energy(self):
        available_energy = self.bank
        length = len(self.locations)
        if len(self.locations):
            new_dungeon = []
            for i in range(length):
                _dungeon = None
                _location = self.locations[i]
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
                    # self.dungeons.append(_dungeon)
                    new_dungeon.append(_dungeon)

            self.dungeons = new_dungeon

            if available_energy > 0:
                # @TODO REFACTOR !!!
                # calculating energy for 'not defined energy' locations
                # no_energy_quantity = len(list(filter(lambda x: 'energy' not in x, self.dungeons)))
                no_energy_quantity = len(self.dungeons)
                if no_energy_quantity:
                    energy_for_each = round(available_energy / no_energy_quantity) if available_energy > 0 else 0
                    for i in range(len(self.dungeons)):
                        _d = self.dungeons[i]
                        # if 'energy' not in self.dungeons[i]:
                        self.dungeons[i]['energy'] = energy_for_each

        for i in range(len(self.dungeons)):
            print(self.dungeons[i])
    def _apply_props(self, props=None):
        if props is None:
            props = self.props

        if props is not None:
            self.bank = int(props['bank']) if 'bank' in props and bool(props['bank']) else self._get_available_energy()

            if self.bank is None:
                self.bank = 0

            if self.bank < self.DUNGEON_BANK_MIN_LIMIT:
                self.terminate = True
                self._log(f"Bank is critically low")
                return

            if 'refill' in props:
                self.refill = int(props['refill'])

            if 'locations' in props:
                self.locations = props['locations']

            # @TODO Consider to remove
            if 'super_raid' in props:
                self.super_raid = bool(props['super_raid'])

    def _initialize(self, dungeon):
        self.current = dungeon
        if dungeon['id'] not in self.results:
            self.results[dungeon['id']] = {
                'victory': 0,
                'defeat': 0,
            }

    def _able_attacking(self, cost):
        return self.current['energy'] >= cost

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
        close_popup_recursive()

    def _start_battle(self):
        if FAKE_BATTLE:
            return

        if pixels_wait([self.STAGE_ENTER], msg="await 'Stage enter'", mistake=10, wait_limit=2)[0]:
            # click on 'Start'
            log('Start')
            await_click([self.BUTTON_START], msg="await 'Button Start'", timeout=1, mistake=10)
        else:
            # click on 'Replay'
            log('Replay')
            dungeons_replay()
        sleep(1)

    def _click_on_super_raid(self):
        x = self.SUPER_RAID[0]
        y = self.SUPER_RAID[1]
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
        # click last floor @TODO Temp commented
        click(850, 475)

        # click(850, 375)
        sleep(.5)

        if not pixel_check_new(self.SUPER_RAID, mistake=10):
            self._click_on_super_raid()

    def attack(self):
        skip = False

        self._start_battle()

        sleep(1)
        ruby_button = find_needle_refill_ruby()

        if ruby_button is not None:
            self._log('Free coins are NOT available')
            if self.refill < 0:
                await_click([self.REFILL_PAID], mistake=10)
                self.refill -= 1
                self._start_battle()
            else:
                self._log('No more refill')
                skip = True

        if not skip:
            if not FAKE_BATTLE:
                _name = self.current['name']
                waiting_battle_end_regular(f'{_name} battle end', x=28, y=88)
                sleep(.5)

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
                    res = f'{self.LOCATION_NAME} Report'

                win_rate = calculate_win_rate(value['victory'], value['defeat'])
                line = f"\n{key} | Battles: {value['victory'] + value['defeat']}, Win rate: {win_rate}"
                res += f"{line}"

        return res

    def run(self, props=None):
        self.terminate = False

        if props is not None:
            self._apply_props(props)
        else:
            self._apply_props(self.props)
            # self.bank = self._get_available_energy()

        self._distribute_energy()
        self._log(f'Bank: {self.bank}')

        if not self.terminate:
            for i in range(len(self.dungeons)):
                self._initialize(self.dungeons[i])
                self._log(f"Starting {self.current['name']}")
                self.enter()

                cost = read_energy_cost()
                self._log(f'Energy cost: {cost}')

                counter = 0
                while self._able_attacking(cost):
                    self._log('Start battle')
                    self.attack()
                    self.current['energy'] -= cost

                if not FAKE_BATTLE:
                    self._exit_location()

        self.finish()