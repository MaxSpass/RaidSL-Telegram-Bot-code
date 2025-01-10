from helpers.common import *
from classes.Location import Location
from classes.Foundation import RGB_PRIMARY

# when fake battle is needed
FAKE_BATTLE = False
# FAKE_BATTLE = True

DUNGEON_MINOTAUR = "Minotaur's Labyrinth"
DUNGEON_GOLEM = "Ice Golem's Peak"
DUNGEON_SPIDER = "Spider's Den"
DUNGEON_DRAGON = "Dragon's Lair"
DUNGEON_FIRE = "Fire Knight's Castle"
DUNGEON_SAND_DEVIL = "Sand Devil's Necropolis"
DUNGEON_PHANTOM = "Phantom Shogun's Grove"
DUNGEON_SECRET = "Secret Dungeon"

DUNGEON_NO_DIFFICULTIES = ['1', '6', '7', '8']
DUNGEON_NO_SUPER_RAID = ['1']

DUNGEON_DATA = [
    {'id': '1', 'name': DUNGEON_MINOTAUR},
    {'id': '2', 'name': DUNGEON_GOLEM},
    {'id': '3', 'name': DUNGEON_SPIDER},
    {'id': '4', 'name': DUNGEON_DRAGON},
    {'id': '5', 'name': DUNGEON_FIRE},
    {'id': '6', 'name': DUNGEON_SAND_DEVIL},
    {'id': '7', 'name': DUNGEON_PHANTOM},
    {'id': '8', 'name': DUNGEON_SECRET},
]

# These values are calculated based on swipe arguments: x=500, y=450, distance=400, speed=0.25, instant_move=True
DUNGEON_SWIPES_TO_BOTTOM = {
    '1': {'normal': 3},
    '2': {'normal': 6, 'hard': 2},
    '3': {'normal': 6, 'hard': 2},
    '4': {'normal': 6, 'hard': 2},
    '5': {'normal': 6, 'hard': 2},
    '6': {'normal': 6},
    '7': {'normal': 6},
    '8': {'normal': 7},
}

DUNGEON_LOCATIONS = {
    '1': {'swipe': 1, 'click': {'x': 420, 'y': 300}},
    '2': {'swipe': 1, 'click': {'x': 540, 'y': 160}},
    '3': {'swipe': 1, 'click': {'x': 680, 'y': 300}},
    '4': {'swipe': 1, 'click': {'x': 775, 'y': 175}},
    '5': {'swipe': 2, 'click': {'x': 490, 'y': 300}},
    '6': {'swipe': 2, 'click': {'x': 650, 'y': 170}},
    '7': {'swipe': 2, 'click': {'x': 810, 'y': 340}},
    '8': {'swipe': 1, 'click': {'x': 575, 'y': 370}},
}

DUNGEON_STAGES = {
    'n': {'x': 860, 'y': 475},
    'n-1': {'x': 860, 'y': 386},
    'n-2': {'x': 860, 'y': 300},
    'n-3': {'x': 860, 'y': 214},
    'n-4': {'x': 860, 'y': 124},
}

class Dungeons(Location):
    REFILL_PAID = [440, 376, [255, 33, 51]]

    RESULT_VICTORY = [450, 40, [15, 121, 182]]
    RESULT_DEFEAT = [450, 40, [178, 23, 38]]

    # @TODO Rework
    DUNGEON_BANK_MIN_LIMIT = 20
    DUNGEON_DIFFICULTY_DEFAULT = 'hard'

    def __init__(self, app, props=None):
        Location.__init__(self, name='Dungeon', app=app, report_predicate=self._report)

        self.dungeons = []
        self.results = {}
        self.current = None

        self.bank = 0
        self.refill = 0
        self.locations = []

        # @TODO Temp dirty fix
        # self.props = props
        self.apply_props(props)
        # self._distribute_energy()

        self.event_dispatcher.subscribe('run', self._run)

    def _report(self):
        res_list = []
        for _id, value in self.results.items():
            j, dungeon = find(DUNGEON_DATA, lambda x: x['id'] == _id)
            key = dungeon['name'] if dungeon else _id
            has_battles = bool(value['victory'] + value['defeat'])

            if has_battles:
                res_list.append(f"Location: {key}")
                str_battles = f"Battles: {value['victory'] + value['defeat']}"
                str_wr = f"(WR: {calculate_win_rate(value['victory'], value['defeat'])})"
                res_list.append(f"{str_battles} {str_wr}")

        return res_list

    def _enter(self):
        _difficulty = 'normal'
        _id = str(self.current['id'])
        _stage = DUNGEON_STAGES[self.current['stage']]
        location = DUNGEON_LOCATIONS[_id]

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

        if 'difficulty' in self.current:
            _difficulty = self.current['difficulty']
            dungeon_select_difficulty(self.current['difficulty'])

        # swiping bottom
        swipes_to_bottom = DUNGEON_SWIPES_TO_BOTTOM[_id][_difficulty]
        for j in range(swipes_to_bottom):
            swipe('bottom', 280, 450, distance=400, speed=0.25, instant_move=True)

        await_click(
            [[_stage['x'], _stage['y'], RGB_PRIMARY]],
            mistake=20,
            msg=f"Choosing Stage: {self.current['stage']}",
            timeout=1,
        )
        sleep(1)

        if self.current['id'] not in DUNGEON_NO_SUPER_RAID:
            # enable "Super Raid Mode"
            enable_super_raid()

    def _run(self, props=None):
        self.apply_props(props=props)

        # if props is not None:
        #     self.apply_props(props=props)
        # else:
        #     self.apply_props(props=self.props)
        # self.bank = self._get_available_energy()

        self._distribute_energy()
        # self.log(f'Bank: {self.bank}')

        for i in range(len(self.dungeons)):
            if self.terminated:
                break

            self._initialize(self.dungeons[i])
            self.log(f"Starting {self.current['name']}")
            self._enter()

            cost = read_run_cost()
            self.log(f'Energy cost: {cost}')

            while self._able_attacking(cost):
                self.log('Start battle')
                self.attack()
                self.current['energy'] -= cost

            if not FAKE_BATTLE:
                self._exit_location()

    # @TODO These responsibility must be on the different scope
    def _get_available_energy(self):
        # @TODO These responsibility must be on the different scope
        close_popup_recursive()
        return read_available_energy()

    def _distribute_energy(self):
        # @TODO Refactor
        available_energy = self.bank if bool(self.bank) else self._get_available_energy()
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

                        _dungeon['stage'] = _location['stage'] \
                            if 'stage' in _location and _location['stage'] in DUNGEON_STAGES \
                            else 'n'

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

    def apply_props(self, props=None):
        # if props is None:
        #     props = self.props

        if props is not None:
            # self.bank = int(props['bank']) if 'bank' in props and bool(props['bank']) else self._get_available_energy()
            self.bank = int(props['bank']) if 'bank' in props and bool(props['bank']) else None

            # if self.bank is None:
            #     self.bank = 0

            if self.bank and self.bank < self.DUNGEON_BANK_MIN_LIMIT:
                self.terminated = True
                self.log(f"Bank is critically low")
                return

            if 'refill' in props:
                self.refill = int(props['refill'])

            if 'locations' in props:
                self.locations = props['locations']

    def _initialize(self, dungeon):
        self.current = dungeon
        if dungeon['id'] not in self.results:
            self.results[dungeon['id']] = {
                'victory': 0,
                'defeat': 0,
            }

    def _able_attacking(self, cost):
        return bool(cost) and self.current['energy'] >= cost and not self.terminated

    def _save_result(self, condition):
        _id = self.current['id']
        if condition:
            self.results[_id]['victory'] += 1
        else:
            self.results[_id]['defeat'] += 1

    def _exit_location(self):
        # click on the "Stage selection"
        dungeons_click_stage_select()
        # moving to the Index Page for starting new Dungeon location
        close_popup_recursive()

    def _start_battle(self):
        if FAKE_BATTLE:
            return
        self.dungeons_continue_battle()

    def attack(self):
        skip = False

        self._start_battle()

        sleep(1)
        ruby_button = find_needle_refill_ruby()

        if ruby_button is not None:
            self.log('Free coins are NOT available')
            if self.refill < 0:
                await_click([self.REFILL_PAID], mistake=10)
                self.refill -= 1
                self._start_battle()
            else:
                self.log('No more refill')
                skip = True

        if not skip:
            if not FAKE_BATTLE:
                self.waiting_battle_end_regular(msg=self.current['name'])
                sleep(.5)

            result = not pixel_check_new(self.RESULT_DEFEAT, mistake=10)
            self._save_result(result)
