from helpers.common import *
from classes.Feature import Feature

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
DOOM_TOWER_BOSS_ROOMS_REGION = [640, 70, 190, 460]


class DoomTower(Feature):
    RESULT_DEFEAT = [450, 40, [151, 21, 33]]
    # @TODO Duplication
    STAGE_ENTER = [890, 200, [93, 25, 27]]

    def __init__(self, app, props=None):
        Feature.__init__(self, feature_name='Doom Tower', app=app)
        self.bosses = []
        self.keys_golden = 0
        self.keys_silver = 0
        self.current = None
        self.results = {'bosses': 0}

        self.event_dispatcher.subscribe('enter', self._enter)
        self.event_dispatcher.subscribe('finish', self._finish)
        self.event_dispatcher.subscribe('run', self._run)

        self.apply_props(props=props)

    def _enter(self):
        click_on_progress_info()

        click(600, 420)
        sleep(1.5)

        # mistake=200 for ignoring different backgrounds
        dungeon_select_difficulty('hard', mistake=200)
        sleep(5)

        # go higher floor
        for i in range(15):
            swipe('top', 450, 80, 450, speed=.1, sleep_after_end=.2, instant_move=True)
        sleep(1)

    def _finish(self):
        dungeons_click_stage_select()

    def _run(self, *args, props=None):
        self._read_keys()

        # attack bosses
        position = self._find_boss_position()
        counter = 0

        while counter < 15 and position is None:
            for j in range(2):
                swipe('bottom', 450, 390, 250, speed=.5, sleep_after_end=.3, instant_move=True)
                position = self._find_boss_position()

            counter += 1

        if position:
            x = position[0]
            y = position[1]
            self.attack(x, y)

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
                position = find_needle(needle, confidence=.5, region=DOOM_TOWER_BOSS_ROOMS_REGION)
                if position:
                    break
        return position

    def report(self):
        res = None

        if self.results['bosses'] > 0:
            res = f"{self.FEATURE_NAME} | Commitment: {str(self.results['bosses'])}"

        return res

    def attack(self, x, y):
        log(f"{self.FEATURE_NAME} | Attacking")
        click(x, y)
        sleep(2)
        if pixel_check_new(self.STAGE_ENTER, mistake=10):
            enable_super_raid()
            cost = read_run_cost()
            log(f"Cost: {str(cost)}")
            if cost and self.keys_silver:
                while self.keys_silver >= cost:
                    dungeons_start_battle()
                    waiting_battle_end_regular(f"{self.FEATURE_NAME} | Battle end", x=28, y=88)
                    res = not pixel_check_new(self.RESULT_DEFEAT, mistake=30)
                    if res:
                        self.keys_silver -= cost
                        self.results['bosses'] += cost
