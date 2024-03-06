from helpers.common import *
# from features.hero_preset.index import *

DOOM_TOWER_DATA = [
    {'id': '1', 'name': 'Dark Fae', 'needle': 'doom_tower/boss_dark_fae.jpg'},
    {'id': '2', 'name': 'Celestian Griffin', 'needle': 'doom_tower/boss_celestian_griffin.jpg'},
    {'id': '3', 'name': 'Dreadhorn', 'needle': 'doom_tower/boss_dreadhorn.jpg'},
    {'id': '4', 'name': 'Scarab King', 'needle': 'doom_tower/boss_scarab_king.jpg'},
]

# @TODO
DOOM_TOWER_LOCATIONS = {}

# hero_preset = HeroPreset()


class DoomTower:
    LOCATION_NAME = 'Doom Tower'
    RESULT_DEFEAT = [450, 40, [178, 23, 38]]
    # @TODO Duplication
    STAGE_ENTER = [890, 200, [93, 25, 27]]

    def __init__(self, props=None):
        self.bosses = []
        self.keys_golden = 0
        self.keys_silver = 0
        self.current = None
        self.results = {'bosses': 0}

        self.apply_props(props)

    def apply_props(self, props=None):
        if props:
            if 'bosses' in props:
                self.bosses = list(map(lambda x: str(x), props['bosses']))

            if 'keys_golden' in props:
                self.keys_golden = int(props['keys_golden'])

            if 'keys_silver' in props:
                self.keys_silver = int(props['keys_silver'])

    def _read_keys(self):
        self.keys_golden = read_doom_tower_keys('golden')
        self.keys_silver = read_doom_tower_keys('silver')
        log(f"Golden keys: {str(self.keys_golden)}")
        log(f"Silver keys: {str(self.keys_silver)}")

    def _find_boss_position(self):
        position = None
        for i in range(len(self.bosses)):
            id_boss = self.bosses[i]
            i, boss = find(DOOM_TOWER_DATA, lambda x: x['id'] == id_boss)
            if boss:
                needle = boss['needle']
                position = find_needle(needle, confidence=.5)
                if position:
                    break
        return position

    def report(self):
        res = None

        if self.results['bosses'] > 0:
            res = f"{self.LOCATION_NAME} | Commitment: {str(self.results['bosses'])}"

        return res


    def finish(self):
        dungeons_click_stage_select()
        close_popup_recursive()
        log(f"DONE - {self.LOCATION_NAME}")

    def enter(self):
        close_popup_recursive()
        click_on_progress_info()
        click(600, 420)
        sleep(2)
        dungeon_select_difficulty('hard')
        sleep(5)

    def attack(self, x, y):
        log(f"{self.LOCATION_NAME} | Attacking")
        click(x, y)
        sleep(2)
        if pixel_check_new(self.STAGE_ENTER, mistake=10):
            enable_super_raid()
            cost = read_run_cost()
            log(f"Cost: {str(cost)}")
            if cost:
                while self.keys_silver >= cost:
                    dungeons_start_battle()
                    waiting_battle_end_regular(f"{self.LOCATION_NAME} | Waiting battle end", x=28, y=88)
                    res = not pixel_check_new(self.RESULT_DEFEAT, mistake=20)
                    if res:
                        self.keys_silver -= cost
                        self.results['bosses'] += cost

    def run(self):
        self.enter()

        self._read_keys()
        # attack bosses
        position = self._find_boss_position()
        if position:
            x = position[0]
            y = position[1]
            self.attack(x, y)

        self.finish()