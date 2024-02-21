import math
from helpers.common import *

FACTION_LIZARDMEN = 'Lizardmen'
FACTION_SKINWALKER = 'Skinwalker'
FACTION_KNIGHTS_REVENANT = 'Knights Revenant'
FACTION_UNDEAD_HORDE = 'Undead Horde'
FACTION_DEMONSPAWN = 'Demonspawn'
FACTION_OGRYN_TRIBE = 'Ogryn Tribe'
FACTION_ORC = 'Orc'
FACTION_HIGH_ELF = 'High Elf'
FACTION_DARK_ELF = 'Dark Elf'
FACTION_SACRED_ORDER = 'Sacred Order'
FACTION_BANNER_LORD = 'Banner Lord'
FACTION_BARBARIAN = 'Barbarian'
FACTION_DWARF = 'Dwarf'
FACTION_SHADOWKIN = 'Shadowkin'
FACTION_SYLVAN_WATCHER = 'Sylvan Watcher'

FACTION_POSITION = {
    '1': {'axis': {'x': 223, 'y': 216}},
    '2': {'axis': {'x': 297, 'y': 120}},
    '3': {'axis': {'x': 291, 'y': 332}},
    '4': {'axis': {'x': 419, 'y': 216}},
    '5': {'axis': {'x': 531, 'y': 119}},
    '6': {'axis': {'x': 633, 'y': 328}},
    '7': {'axis': {'x': 701, 'y': 217}},
    '8': {'axis': {'x': 767, 'y': 117}},
    '9': {'axis': {'x': 22, 'y': 328}},
    '10': {'axis': {'x': 213, 'y': 214}},
    '11': {'axis': {'x': 295, 'y': 328}},
    '12': {'axis': {'x': 391, 'y': 119}},
    '13': {'axis': {'x': 481, 'y': 216}},
    '14': {'axis': {'x': 622, 'y': 328}},
    '15': {'axis': {'x': 726, 'y': 212}},
}

FACTION_DATA = [
    {'id': '1', 'name': FACTION_LIZARDMEN},
    {'id': '2', 'name': FACTION_SKINWALKER},
    {'id': '3', 'name': FACTION_KNIGHTS_REVENANT},
    {'id': '4', 'name': FACTION_UNDEAD_HORDE},
    {'id': '5', 'name': FACTION_DEMONSPAWN},
    {'id': '6', 'name': FACTION_OGRYN_TRIBE},
    {'id': '7', 'name': FACTION_ORC},
    {'id': '8', 'name': FACTION_HIGH_ELF},
    {'id': '9', 'name': FACTION_DARK_ELF},
    {'id': '10', 'name': FACTION_SACRED_ORDER},
    {'id': '11', 'name': FACTION_BANNER_LORD},
    {'id': '12', 'name': FACTION_BARBARIAN},
    {'id': '13', 'name': FACTION_DWARF},
    {'id': '14', 'name': FACTION_SHADOWKIN},
    {'id': '15', 'name': FACTION_SYLVAN_WATCHER},
]


# @TODO Must be reworked by following new standard and refactor 'attack' method
# @TODO Requires: keyboard locale, enemy's leaving the battle
class FactionWars():
    LOCATION_NAME = 'Faction Wars'
    RGB_FREE_CRYPT = [30, 36, 49]
    RGB_FREE_STAGE = [187, 130, 5]
    BATTLE_VICTORY = [452, 42, [30, 186, 239]]
    STAGE_DEFAULT = '21'
    STAGES_POSITION = {
        '21': [860, 479, RGB_FREE_STAGE],
        '20': [860, 393, RGB_FREE_STAGE],
        '19': [860, 308, RGB_FREE_STAGE],
        '18': [860, 221, RGB_FREE_STAGE],
        '17': [860, 134, RGB_FREE_STAGE],
    }

    def __init__(self, props=None):
        self.results = {}
        self.crypts = self._prepare_crypts()
        self.slides = [
            np.array(self.crypts)[:8],
            np.array(self.crypts)[8:]
        ]

        self._apply_props(props)

    def _apply_props(self, props=None):
        if props is not None:
            if 'stages' in props:
                self.stages = props['stages']

    def _prepare_crypts(self):
        def _prepare_item(crypt):
            _position = FACTION_POSITION[crypt['id']]
            crypt['axis'] = _position['axis']
            return crypt

        return list(map(_prepare_item, FACTION_DATA))

    def _get_stage_by_id(self, uid=None):
        if uid and uid in self.stages:
            return str(self.stages[uid])
        else:
            return self.STAGE_DEFAULT

    def _prepare_run(self, name, expect=16):
        if name not in self.results:
            self.results[name] = {
                "commitment": 0,
                "completed": False,
                "expect": expect
            }
            log(f"Prepare run: {str(self.results[name])}")

    def _save_result(self, name, commitment=None, completed=None):
        if name in self.results:
            crypt = self.results[name]
            if commitment:
                crypt["commitment"] = crypt["commitment"] + commitment
            if completed:
                crypt["completed"] = completed
            else:
                crypt["completed"] = crypt["commitment"] >= crypt["expect"]

            log('Save crypt result: ' + str(crypt))
    def _get_result_by_name(self, name):
        return self.results[name]

    def _is_available(self, name, pixel):
        is_not_completed = name not in self.results or (name in self.results and not self.results[name]["completed"])
        is_open = pixel_check_new(pixel, mistake=10)

        return is_not_completed and is_open

    def _swipe_left_border(self, times=2):
        for i in range(times):
            swipe('left', 50, 400, 800, speed=0.3)

    def _swipe_right_border(self, times=2):
        for k in range(times):
            swipe('right', 850, 200, 690, speed=1)

    def enter(self):
        # @TODO Test
        close_popup_recursive()
        click_on_progress_info()

        # Faction Keys
        click(600, 260)
        sleep(1)

    def finish(self):
        close_popup_recursive()
        log('DONE - ' + self.LOCATION_NAME)

    def report(self):
        s = None

        items = self.results.items()
        if len(items):
            progress = ', '.join(list(map(lambda arr: f"{arr[0]}: {str(arr[1]['commitment'])}keys", items)))
            s = f"{self.LOCATION_NAME} | {progress}"

        return s

    def run(self, props=None):
        self._apply_props(props)

        close_popup_recursive()

        self.enter()
        self._swipe_left_border()

        for i in range(len(self.slides)):
            slide = self.slides[i]

            if i > 0:
                self._swipe_right_border()

            for j in range(len(slide)):
                _crypt = slide[j]
                _name = _crypt['name']
                _id = _crypt['id']
                pixel = [_crypt['axis']['x'], _crypt['axis']['y']] + [self.RGB_FREE_CRYPT]

                available = self._is_available(_name, pixel=pixel)
                if available:
                    log(f"Crypt is available: {_name}")

                    await_click([pixel], mistake=10)
                    sleep(1)

                    stage_lvl = self._get_stage_by_id(_id)
                    stage = self.STAGES_POSITION[stage_lvl]

                    if pixel_check_new(stage, mistake=10):

                        x_stage = stage[0]
                        y_stage = stage[1]
                        click(x_stage, y_stage)
                        sleep(.5)

                        if dungeons_is_able():
                            # enable "Super Raid Mode"
                            enable_super_raid()

                            # computing keys bank
                            keys = read_keys_bank()
                            log(f"keys: {str(keys)}")

                            # computing keys cost
                            cost = read_run_cost(scale=8)
                            log(f"cost: {str(cost)}")

                            if cost and keys:
                                if keys >= cost:
                                    log(f'Attacking: {_name}')
                                    runs = math.floor(keys / cost)
                                    log(f"runs: {str(runs)}")
                                    expect = runs*cost

                                    self._prepare_run(_name, expect=expect)

                                    while not self._get_result_by_name(_name)["completed"]:
                                        dungeons_start_battle()

                                        waiting_battle_end_regular(f"{self.LOCATION_NAME} | {_name}", x=28, y=88)
                                        sleep(1)

                                        # battle has been won
                                        if pixel_check_new(self.BATTLE_VICTORY, mistake=5):
                                            self._save_result(name=_name, commitment=cost)

                                    # click in the "Stage Selection"
                                    dungeons_click_stage_select()

                                    # going to the index page and enter to the factions again
                                    self.enter()
                                    self._swipe_left_border()
                                    if i > 0:
                                        self._swipe_right_border()
                                else:
                                    log(f"Stage is not available (name: {_name}, stage: {stage_lvl})")
                            else:
                                log("Cost or Keys are not calculated well")
                        else:
                            # going back one lvl upper
                            close_popup()
                            # fake preparation the crypt
                            self._prepare_run(_name, expect=0)
                            # save results for keeping it in memory
                            self._save_result(name=_name, completed=True)
                            log('Crypt is already attacked')

        self.finish()
        log(self.results)
