from helpers.common import *
from classes.Location import Location

DOOM_TOWER_DATA = [
    {'id': '1', 'name': 'Dark Fae', 'needle': 'doom_tower/boss_dark_fae.jpg'},
    {'id': '2', 'name': 'Celestian Griffin', 'needle': 'doom_tower/boss_celestian_griffin.jpg'},
    {'id': '3', 'name': 'Dreadhorn', 'needle': 'doom_tower/boss_dreadhorn.jpg'},
    {'id': '4', 'name': 'Scarab King', 'needle': 'doom_tower/boss_scarab_king.jpg'},
    {'id': '5', 'name': 'Magma Dragon', 'needle': 'doom_tower/boss_magma_dragon.jpg'},
    {'id': '6', 'name': 'Nether Spider', 'needle': 'doom_tower/boss_nether_spider.jpg'},
    {'id': '7', 'name': 'Frost Spider', 'needle': 'doom_tower/boss_frost_spider.jpg'},
]

# @TODO
DOOM_TOWER_LOCATIONS = {}
DOOM_TOWER_BOSS_ROOMS_REGION = [420, 70, 400, 460]
DOOM_TOWER_DIFFICULTIES = ['hard', 'normal']


class DoomTower(Location):
    RESULT_DEFEAT = [450, 40, [151, 21, 33]]
    # @TODO Duplication
    STAGE_ENTER = [890, 200, [93, 25, 27]]
    # For test purpose
    FAKE_BATTLE = False

    def __init__(self, app, props=None):
        Location.__init__(self, name='Doom Tower', app=app, report_predicate=self._report)

        self.bosses = []
        self.keys_golden = 0
        self.keys_silver = 0
        self.current = None
        self.results = {'bosses': 0, 'floors': 0}

        self.event_dispatcher.subscribe('enter', self._enter)
        self.event_dispatcher.subscribe('run', self._run)

        self.apply_props(props=props)

    def _report(self):
        res_list = []

        if self.results['bosses'] > 0:
            res_list.append(f"Boss commitment: {str(self.results['bosses'])}")
        if self.results['floors'] > 0:
            res_list.append(f"Floors passed: {str(self.results['floors'])}")

        return res_list

    def _enter(self):
        click_on_progress_info()

        click(600, 420)
        sleep(1.5)

    def _run(self, props=None):
        self.read_keys()

        for d in range(len(DOOM_TOWER_DIFFICULTIES)):
            if self._can_continue():
                # mistake=200 for ignoring different backgrounds
                dungeon_select_difficulty(DOOM_TOWER_DIFFICULTIES[d], mistake=200)
                sleep(5)
                self.attack()

    def _can_continue(self):
        return self.keys_golden > 0 or self.keys_silver > 1

    def _wait_stage_enter(self):
        return pixels_wait([self.STAGE_ENTER], msg='Stage enter', timeout=1, mistake=10, wait_limit=3)[0]

    def swipe_top(self, limit=15, long=450, needle_predicate=None):
        counter = 0
        needle_position = None
        sleep(1.5)
        while counter < limit:
            if find_doom_tower_edge_top():
                break
            elif needle_predicate:
                needle_position = needle_predicate()
                if needle_position:
                    break
            swipe('top', 820, 80, long, speed=.1, sleep_after_end=.7, instant_move=True)
            counter += 1

        sleep(1)
        return needle_position

    def swipe_bottom(self, limit=30, long=250, needle_predicate=None):
        counter = 0
        needle_position = None
        sleep(1.5)
        while counter < limit:
            if find_doom_tower_edge_bottom():
                break
            elif needle_predicate:
                needle_position = needle_predicate()
                if needle_position:
                    break
            swipe('bottom', 820, 390, long, speed=.1, sleep_after_end=.7, instant_move=True)
            counter += 1

        sleep(1)
        return needle_position

    def apply_props(self, props=None):
        if props:
            if 'bosses' in props:
                self.bosses = list(map(lambda x: str(x), props['bosses']))

    def read_keys(self):
        # self.keys_golden = 10
        self.keys_golden = read_doom_tower_keys('golden')
        self.keys_silver = read_doom_tower_keys('silver')
        self.log(f"Golden keys: {str(self.keys_golden)}")
        self.log(f"Silver keys: {str(self.keys_silver)}")

    def find_all_bosses(self):
        position = None
        for i in range(len(DOOM_TOWER_DATA)):
            boss_needle = DOOM_TOWER_DATA[i]['needle']
            position = find_needle(boss_needle, confidence=.5, region=DOOM_TOWER_BOSS_ROOMS_REGION)
            if position:
                break
        return position

    def find_boss_position(self):
        position = None
        for i in range(len(self.bosses)):
            id_boss = self.bosses[i]
            i, boss = find(DOOM_TOWER_DATA, lambda x: x['id'] == id_boss)
            if boss:
                needle = boss['needle']
                position = find_needle(needle, confidence=.5, region=DOOM_TOWER_BOSS_ROOMS_REGION)
                if position:
                    break
        return position

    def find_boss_position_by_id(self, id_boss):
        position = None
        i, boss = find(DOOM_TOWER_DATA, lambda x: x['id'] == id_boss)
        if boss:
            needle = boss['needle']
            position = find_needle(needle, confidence=.5, region=DOOM_TOWER_BOSS_ROOMS_REGION)
        return position

    def use_golden_keys(self, position=None, deny_predicate=None):
        if position:
            self.log("Attacking Regular Floor")
            click(position[0], position[1])

            if self._wait_stage_enter():
                if deny_predicate and deny_predicate():
                    close_popup()
                    return

                disable_auto_climb()
                cost = read_run_cost()
                counter = 1

                if cost and self.keys_golden:
                    while self.keys_golden >= cost:
                        if not self.FAKE_BATTLE:
                            dungeons_start()
                            self.waiting_battle_end_regular(f"Regular Floor Battle: {str(counter)}")

                            # Victory
                            if not pixel_check_new(DoomTower.RESULT_DEFEAT, mistake=30):
                                dungeons_start()
                                self.keys_golden -= cost
                                self.results['floors'] += cost
                                counter += 1
                            else:
                                # Defeat
                                dungeons_continue_battle()

                        else:
                            self.log(f"Fake battle: {str(counter)}")
                            self.keys_golden -= cost
                            self.results['floors'] += cost
                            counter += 1

                    if not self.FAKE_BATTLE:
                        dungeons_click_stage_select()
                else:
                    close_popup()

                if self.FAKE_BATTLE:
                    close_popup()

    def use_silver_keys(self, position=None):
        if position:
            self.log("Attacking Boss Floor")
            click(position[0], position[1])

            if self._wait_stage_enter():
                enable_super_raid()
                cost = read_run_cost()
                counter = 1

                self.log(f"Cost: {str(cost)}")
                if cost and self.keys_silver:
                    while self.keys_silver >= cost:
                        if not self.FAKE_BATTLE:
                            dungeons_continue_battle()
                            self.waiting_battle_end_regular(f"Boss Floor Battle: {str(counter)}")

                            # Victory
                            if not pixel_check_new(self.RESULT_DEFEAT, mistake=30):
                                self.keys_silver -= cost
                                self.results['bosses'] += cost
                                counter += 1
                        else:
                            self.log(f"Fake Battle: {str(counter)}")
                            self.keys_silver -= cost
                            self.results['bosses'] += cost
                            counter += 1

                    if not self.FAKE_BATTLE:
                        dungeons_click_stage_select()
                else:
                    close_popup()

                if self.FAKE_BATTLE:
                    close_popup()

    def attack(self):
        iterations_data = [
            # Search for a regular floor
            {'needle_predicate': find_doom_tower_next_floor_regular, 'deny_predicate': None},
            # Search for a boss
            {'needle_predicate': self.find_all_bosses, 'deny_predicate': lambda: not find_checkbox_locked()},
        ]

        # Using Golden Keys
        for j in range(len(iterations_data)):
            if self.keys_golden > 0:
                needle_predicate = iterations_data[j]['needle_predicate']
                deny_predicate = iterations_data[j]['deny_predicate']
                self.swipe_top(needle_predicate=find_doom_tower_locked_floor)
                position_regular = self.swipe_bottom(limit=60, long=125, needle_predicate=needle_predicate)
                print('Position Regular Floor:', position_regular)
                self.use_golden_keys(position_regular, deny_predicate=deny_predicate)

        # Using Silver Keys
        if self.keys_silver > 0:
            self.swipe_top(needle_predicate=find_doom_tower_locked_floor)
            position_boss = None
            for i in range(len(self.bosses)):
                id_boss = self.bosses[i]
                if i == 0:
                    position_boss = self.find_boss_position_by_id(id_boss)

                if position_boss is None:
                    self.swipe_top(needle_predicate=find_doom_tower_locked_floor)
                    position_boss = self.swipe_bottom(needle_predicate=lambda: self.find_boss_position_by_id(id_boss))
                    print('Position Boss:', position_boss)
                    self.use_silver_keys(position_boss)

                    if position_boss or not self._can_continue():
                        break
