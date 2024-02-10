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
    '1': {'pixel': {'x': 223, 'y': 216}},
    '2': {'pixel': {'x': 297, 'y': 120}},
    '3': {'pixel': {'x': 291, 'y': 332}},
    '4': {'pixel': {'x': 419, 'y': 216}},
    '5': {'pixel': {'x': 531, 'y': 119}},
    '6': {'pixel': {'x': 633, 'y': 328}},
    '7': {'pixel': {'x': 701, 'y': 217}},
    '8': {'pixel': {'x': 767, 'y': 117}},
    '9': {'pixel': {'x': 22, 'y': 328}},
    '10': {'pixel': {'x': 213, 'y': 214}},
    '11': {'pixel': {'x': 295, 'y': 328}},
    '12': {'pixel': {'x': 391, 'y': 119}},
    '13': {'pixel': {'x': 481, 'y': 216}},
    '14': {'pixel': {'x': 622, 'y': 328}},
    '15': {'pixel': {'x': 726, 'y': 212}},
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
    SUPER_RAID = [653, 335, [108, 237, 255]]
    STAGE_ENTER = [850, 200, [93, 25, 27]]
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
            crypt['pixel'] = _position['pixel']
            return crypt

        return list(map(_prepare_item, FACTION_DATA))

    def _get_stage_by_id(self, uid=None):
        if uid and uid in self.stages:
            return str(self.stages[uid])
        else:
            return self.STAGE_DEFAULT

    def _prepare_run(self, name, stage_lvl):
        if name not in self.results:
            self.results[name] = {
                stage_lvl: 0,
            }

        return 1

    def _save_result(self, name, stage_lvl):
        if stage_lvl not in self.results[name]:
            self.results[name][stage_lvl] = 0
        else:
            self.results[name][stage_lvl] += 1

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

        if len(self.results):
            s = f"{self.LOCATION_NAME} | Completed: {str(self.results.keys())}"

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

                pixel = _crypt['pixel']
                x = pixel['x']
                y = pixel['y']

                is_new = _name not in self.results
                is_open = pixel_check_new([x, y, self.RGB_FREE_CRYPT], mistake=10)
                if is_new and is_open:
                    log(f"Crypt is available: {_name}")

                    await_click([[x, y, self.RGB_FREE_CRYPT]], mistake=10)
                    sleep(1)

                    stage_lvl = self._get_stage_by_id(_id)
                    stage = self.STAGES_POSITION[stage_lvl]

                    if pixel_check_new(stage, mistake=10):
                        # preparing results object
                        self._prepare_run(_name, stage_lvl)

                        x_stage = stage[0]
                        y_stage = stage[1]
                        click(x_stage, y_stage)
                        sleep(.5)

                        if pixel_check_new(self.STAGE_ENTER, mistake=10):
                            # enable "Super Raid Mode"
                            if not pixel_check_new(self.SUPER_RAID, mistake=10):
                                click(653, 335)
                                sleep(0.3)

                            # computing keys bank
                            keys = read_keys_bank()
                            log(f"keys: {str(keys)}")

                            # computing keys cost
                            cost = read_energy_cost()
                            log(f"cost: {str(cost)}")

                            if cost and keys:
                                if keys >= cost:
                                    log(f'Attacking: {_name}')
                                    runs = math.floor(keys / cost)
                                    log(f"runs: {str(runs)}")

                                    counter = 0
                                    while runs > 0:
                                        if counter == 0:
                                            # click 'Start' button
                                            dungeons_start()
                                        else:
                                            # click 'Replay' button
                                            dungeons_replay()

                                        counter += 1

                                        waiting_battle_end_regular(f"{self.LOCATION_NAME} | {_name}", x=28, y=88)
                                        sleep(1)

                                        # battle has been won
                                        if pixel_check_new(self.BATTLE_VICTORY, mistake=5):
                                            self._save_result(_name, stage_lvl)
                                            runs -= 1

                                    # click in the "Stage Selection"
                                    click(820, 50)
                                    sleep(2)

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
                            # save results for keeping it in memory
                            self._save_result(_name, stage_lvl)
                            log('Crypt is already attacked')

        self.finish()
        log(self.results)
