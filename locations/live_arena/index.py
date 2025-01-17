import pyautogui
import pause
import copy

from helpers.time_mgr import *
from locations.hero_filter.index import *
from classes.Location import Location

time_mgr = TimeMgr()
hero_filter = HeroFilter()

first = [334, 209, [22, 51, 90]]
second = [899, 94, [90, 24, 24]]
cant_find_opponent_button_find = [590, 290, [187, 130, 5]]
cant_find_opponent_button_cancel = [280, 290, [22, 124, 156]]

RGB_EMPTY_SLOT = [49, 54, 49]
EMPTY_SLOT_WIDTH = 48
EMPTY_SLOT_HEIGHT = 64
LIVE_ARENA_HERO_SLOTS = [
    [226, 162, RGB_EMPTY_SLOT],
    [184, 264, RGB_EMPTY_SLOT],
    [146, 162, RGB_EMPTY_SLOT],
    [105, 264, RGB_EMPTY_SLOT],
    [64, 162, RGB_EMPTY_SLOT],
]

enemy_slots = [
    [650, 198, RGB_EMPTY_SLOT],
    [697, 289, RGB_EMPTY_SLOT],
    [728, 199, RGB_EMPTY_SLOT],
    [767, 292, RGB_EMPTY_SLOT],
    [812, 201, RGB_EMPTY_SLOT],
]

# picking heroes
stage_1 = [460, 330, [36, 88, 110]]
# ban hero
stage_2 = [460, 330, [72, 60, 77]]
# choose leader
stage_3 = [460, 330, [72, 87, 77]]

turn_to_pick = [461, 245, [149, 242, 255]]

# Statuses are not working properly (en localization only)
# status_active = [320, 420, [50, 165, 42]]
# status_not_active = [320, 420, [165, 45, 52]]

# index page
index_indicator_active = [822, 474, [62, 170, 53]]

# the white 'Clock' in the left-top corner
finish_battle = [21, 46, [255, 255, 255]]

victory = [451, 38, [23, 146, 218]]
defeat = [451, 38, [199, 26, 48]]

find_opponent = [500, 460, [187, 130, 5]]
battle_start_turn = [341, 74, [86, 191, 255]]
refill_free = [454, 373, [187, 130, 5]]
refill_paid = [444, 393, [195, 40, 66]]
claim_refill = [875, 173, [218, 0, 0]]
claim_chest = [534, 448, [233, 0, 0]]

# return_start_panel = [444, 490]

PAID_REFILL_LIMIT = 1
ARCHIVE_PATTERN_FIRST = [1, 2, 2]

# @TODO Can be useful
error_dialog_button_left = [357, 287, [22, 124, 156]]
error_dialog_button_right = [550, 291, [22, 124, 156]]

# RGB
# arena_classic victory: [59, 37, 11]
# arena_classic defeat: [27, 19, 131]
# arena_live victory: [77, 53, 10]
rgb_victory = [77, 53, 10]
rgb_defeat = [27, 19, 131]

rgb_reward = [220, 0, 0]
rewards_pixels = [
    [875, 118, rgb_reward],
    [875, 472, rgb_reward],
    [875, 422, rgb_reward],
    [875, 372, rgb_reward],
    [875, 322, rgb_reward],
    [875, 272, rgb_reward],
]


class ArenaLive(Location):
    def __init__(self, app, props=None):
        Location.__init__(self, name='Arena Live', app=app, report_predicate=self._report)

        if self.results is None:
            self.results = []

        self.pool = []
        self.leaders = []
        self.refill = PAID_REFILL_LIMIT
        self.idle_after_defeat = 0

        # The variable resets each battle start
        self.current = {
            'counter': 0,
            'slots_counter': 0,
            'battle_time': None,
            'sorted_pool': [],
            'team': [],
            'next_char': None,
            'current_char': None,
        }

        # Applying properties
        if props is not None:
            self._apply_props(props=props)

        # LiveArena related events
        self.E_CANT_FIND_OPPONENT = {
            "name": "CantFindAnOpponent",
            "expect": lambda: pixels_every(
                same_pixels_line(cant_find_opponent_button_cancel), lambda p: pixel_check_new(p, mistake=5)
            ),
            "callback": self._cb_cant_find_opponent,
            "blocking": False,
            "interval": 3,
        }
        self.E_OPPONENT_LEFT = {
            "name": "OpponentLeft",
            "expect": find_victory_opponent_left,
            "callback": lambda *args: self.terminate(terminated=False, predicate=lambda: self.handle_result(True)),
            "interval": .5,
        }
        self.E_PICK_FIRST = {
            "name": "PickFirst",
            "expect": lambda: pixel_check_new(first, mistake=5),
        }
        self.E_PICK_SECOND = {
            "name": "PickSecond",
            "expect": lambda: pixel_check_new(second, mistake=5),
        }
        self.E_VICTORY = {
            "name": "Victory",
            "expect": lambda: pixel_check_new(victory, mistake=30),
            "callback": lambda *args: self.handle_result(True),
        }
        self.E_DEFEAT = {
            "name": "Defeat",
            "expect": lambda: pixel_check_new(defeat, mistake=30),
            "callback": lambda *args: self.handle_result(False),
        }

        self.E_STAGE_1 = {
            "name": "Stage 1 | PickingCharacters",
            "expect": lambda: pixel_check_new(stage_1, mistake=10),
            "interval": 2,
        }
        self.E_PICKING_PROCESS = {
            "name": "PickingCharactersProcess",
            "expect": lambda: pixel_check_new(first, mistake=10),
            "interval": 2,
        }
        self.E_STAGE_2 = {
            "name": "Stage 2 | BanHero",
            "expect": lambda: pixel_check_new(stage_2, mistake=10),
            "interval": 2,
        }
        self.E_STAGE_3 = {
            "name": "Stage 3 | ChoosingLeader",
            "expect": lambda: pixel_check_new(stage_3, mistake=10),
            "interval": 2,
        }
        self.E_CHOOSING_LEADER = {
            "name": "ChoosingLeaderProcess",
            "expect": lambda: pixel_check_new(first, mistake=10),
            "interval": 2,
        }
        self.E_BATTLE_START_LIVE = {
            "name": "BattleStartLive",
            "expect": lambda: pixel_check_new(battle_start_turn, mistake=20),
            "callback": enable_auto_play,
            "blocking": False,
            "limit": 1,
        }
        self.E_INDICATOR_ACTIVE = {
            "name": "IndicatorActive",
            "expect": find_indicator_active,
            "limit": 1,
            "wait_limit": 15,
        }
        self.E_INDICATOR_INACTIVE = {
            "name": "IndicatorInactive",
            "expect": find_indicator_inactive,
            "limit": 1,
            "interval": 10,
            "callback": self.terminate,
        }
        # @TODO Not implemented yet (see index_new_2.py)
        self.E_FILLED_HERO_SLOT = {
            'name': 'FilledHeroSlot',
            'expect': lambda: find_hero_slot_empty(region=[
                LIVE_ARENA_HERO_SLOTS[self.current['slots_counter']][0],
                LIVE_ARENA_HERO_SLOTS[self.current['slots_counter']][1],
                EMPTY_SLOT_WIDTH,
                EMPTY_SLOT_HEIGHT
            ]) is None,
            'limit': 1,
            'interval': 1,
            'wait_limit': 30,
            'callback': self._cb_active_hero_slot,
        }

        # PubSub
        self.event_dispatcher.subscribe('enter', self._enter)
        self.event_dispatcher.subscribe('run', self._run)

    def _cb_active_hero_slot(self, *args):
        print('next_char', self.current['next_char'])
        print('current_char', self.current['current_char'])
        self.current['next_char'] = self.current['current_char']

    def _cb_cant_find_opponent(self, *args):
        _x = cant_find_opponent_button_cancel[0]
        _y = cant_find_opponent_button_cancel[1]
        click(_x, _y)
        sleep(1)
        self._click_on_find_opponent()

    def _report(self):
        res_list = []
        t = len(self.results)
        if t:
            v = self.results.count(True)
            d = t - v
            str_battles = f"Battles: {str(t)}"
            str_wr = f"(WR: {calculate_win_rate(v, d)})"
            res_list.append(f"{str_battles} {str_wr}")

        return res_list

    def _enter(self):
        # Additional check for avoiding further proceeding
        if not pixel_check_new(index_indicator_active, mistake=10):
            self.log("IndexPage indicator is NOT active")
            self.terminate()
            return

        click_on_progress_info()
        # live arena
        click(600, 175)
        sleep(3)

    def _run(self, props=None):
        if props is not None:
            self._apply_props(props=props)

        def cb_starting(*args):
            self.log('Active')
            has_pool = bool(len(self.pool))
            if has_pool:
                self.obtain()

                while self._is_available():
                    self.break_loops = False

                    self._claim_free_refill_coins()
                    self._claim_chest()

                    if self._refill():
                        break

                    self.attack()

                self.obtain()
                # @TODO Temp commented
                # self.event_dispatcher.publish('update_results')

            else:
                self.log("Terminated | The 'pool' property is NOT specified")

        E_INDICATOR_ACTIVE_WITH_CALLBACK = prepare_event(self.E_INDICATOR_ACTIVE, {
            "callback": cb_starting
        })

        if self.awaits([E_INDICATOR_ACTIVE_WITH_CALLBACK])['name'] == self.EVENT_NOT_FOUND:
            self.log('NOT Active')

    def _apply_props(self, props):
        if 'pool' in props:
            pool_copy = copy.deepcopy(props['pool'])
            self.pool = sorted(pool_copy, key=lambda x: (-x.get('priority', 0), x.get('priority', 0)))
            if 'leaders' in props:
                self.leaders = props['leaders']

        if 'refill' in props:
            self.refill = int(props['refill'])

        if 'idle_after_defeat' in props:
            self.idle_after_defeat = int(props['idle_after_defeat'])

    def _confirm(self):
        click(870, 465)
        sleep(.5)

    def _claim_chest(self):
        # the chest is available
        if pixel_check_new(claim_chest):
            x = claim_chest[0]
            y = claim_chest[1]
            claim_rewards(x, y)

    def _claim_free_refill_coins(self):
        if pixel_check_new(claim_refill):
            x = claim_refill[0] - 5
            y = claim_refill[1] + 5
            click(x, y)
            sleep(2)

    def _click_on_find_opponent(self):
        if not await_click([find_opponent], msg="Click on find opponent", mistake=20, wait_limit=65)[0]:
            self.terminate()

    def _is_available(self):
        if not find_indicator_active():
            self.terminate()

        return not self.terminated

    def _save_result(self, result):
        self.results.append(result)
        result_msg = 'WIN' if result else 'DEFEAT'
        self.log(result_msg)

    def _refill(self):
        self._click_on_find_opponent()

        sleep(1)
        ruby_button = find_needle_refill_ruby()

        if ruby_button is not None:
            self.log('Free coins are NOT available')
            if self.refill > 0:
                # wait and click on refill_paid
                click(refill_paid[0], refill_paid[1], smart=True)
                self.refill -= 1
                self._click_on_find_opponent()
            else:
                self.log('No more refill')
                self.terminate()
        elif pixels_wait([refill_free], msg='Free refill sacs', mistake=10, timeout=1, wait_limit=2)[0]:
            self.log('Free coins are available')
            # wait and click on refill_free
            click(refill_free[0], refill_free[1], smart=True)
            self._click_on_find_opponent()

        return self.terminated

    def obtain(self):
        for i in range(len(rewards_pixels)):
            if self.terminated:
                break

            pixel = rewards_pixels[i]
            if pixel_check_new(pixel, mistake=30):
                x = pixel[0]
                y = pixel[1]
                click(x, y)
                sleep(.5)

    def handle_result(self, result):
        self._save_result(bool(result))
        if not result and self.idle_after_defeat:
            sleep(self.idle_after_defeat)

        tap_to_continue(wait_after=2)

    def find_leaders_indicis(self):
        res = []

        for i in range(len(self.leaders)):
            l = self.leaders[i]
            if l in self.current['team']:
                res.append(self.current['team'].index(l))
            if len(res) == 2:
                break

        res.reverse()

        return res

    def attack(self):
        self.current['counter'] += 1
        self.current['battle_time'] = get_time_for_log(s='_')
        self.current['sorted_pool'] = copy.deepcopy(self.pool)
        self.current['team'] = []
        self.current['slots_counter'] = 0

        self.log('Attack | Pool Length: ' + str(len(self.current['sorted_pool'])))

        def find_character(role=None):
            self.log(f"Current pool length: {len(self.current['sorted_pool'])}")

            # @TODO Not implemented yet
            self.current['next_char'] = None
            self.current['current_char'] = None

            if role is None:
                role = self.current['sorted_pool'][0]['role']

            while self.current['next_char'] is None and not self.break_loops:
                # Opponent leaves the battle while picking the character
                if self.E_OPPONENT_LEFT['expect']():
                    self.E_OPPONENT_LEFT['callback']()
                    debug_save_screenshot(suffix_name='left while picking')
                    break

                i, char = find(self.current['sorted_pool'], lambda x: x.get('role') == role)
                index_to_remove = 0

                if char and not self.break_loops:
                    hero_filter.choose(title=char['name'], wait_after=.5)

                    _slot = LIVE_ARENA_HERO_SLOTS[self.current['slots_counter']]
                    _region = [_slot[0], _slot[1], EMPTY_SLOT_WIDTH, EMPTY_SLOT_HEIGHT]
                    # show_pyautogui_image(pyautogui.screenshot(region=_region))
                    _position_empty = find_hero_slot_empty(region=_region)
                    if _position_empty is None and not self.break_loops:
                        self.current['next_char'] = char

                    # if not pixel_check_new(LIVE_ARENA_HERO_SLOTS[self.current['slots_counter']], mistake=10):
                    #     next_char = char

                    index_to_remove = i

                # @TODO Add checking
                del self.current['sorted_pool'][index_to_remove]

            return self.current['next_char']

        def await_start_events():
            return self.awaits(
                events=[self.E_PICK_FIRST, self.E_PICK_SECOND, self.E_CANT_FIND_OPPONENT, self.E_INDICATOR_INACTIVE],
                interval=.1
            )

        def await_stage_1():
            return self.awaits(events=[self.E_STAGE_1, self.E_OPPONENT_LEFT])

        def await_pick():
            return self.awaits(events=[self.E_PICKING_PROCESS, self.E_OPPONENT_LEFT])

        def await_stage_2():
            return self.awaits(events=[self.E_STAGE_2, self.E_OPPONENT_LEFT])

        def await_stage_3():
            return self.awaits(events=[self.E_STAGE_3, self.E_OPPONENT_LEFT])

        def await_choosing_leader():
            return self.awaits(events=[self.E_CHOOSING_LEADER, self.E_OPPONENT_LEFT])

        start_events = await_start_events()
        self.log(start_events['name'])

        pattern = ARCHIVE_PATTERN_FIRST[:]
        if self.E_PICK_SECOND['name'] == start_events['name']:
            pattern.reverse()

        stage_1_events = await_stage_1()
        if self.E_STAGE_1['name'] == stage_1_events['name']:
            sleep(.5)
            for i in range(len(pattern)):
                if self.break_loops:
                    break

                pick_process_events = await_pick()
                if self.E_PICKING_PROCESS['name'] == pick_process_events['name']:
                    sleep(.2)

                    # picking heroes logic
                    for j in range(pattern[i]):
                        if self.break_loops:
                            break

                        unit = find_character()
                        if unit is not None:
                            self.current['team'].append(unit['name'])
                            sleep(.1)
                            self.log(f"Picked: {unit['name']}")
                            self.current['slots_counter'] += 1

                    self._confirm()

        stage_2_events = await_stage_2()
        if self.E_STAGE_2['name'] == stage_2_events['name']:
            sleep(.5)
            # Banning random second slot
            random_slot = random.choice(enemy_slots)
            x = random_slot[0]
            y = random_slot[1]
            click(x, y)
            sleep(.5)

            self._confirm()

        stage_3_events = await_stage_3()
        if self.E_STAGE_3['name'] == stage_3_events['name']:
            sleep(.5)

            choosing_leader_events = await_choosing_leader()
            if self.E_CHOOSING_LEADER['name'] == choosing_leader_events['name']:
                leaders_indicis = self.find_leaders_indicis()

                for i in range(len(leaders_indicis)):
                    leader_index = leaders_indicis[i]
                    slot = LIVE_ARENA_HERO_SLOTS[leader_index]
                    x = slot[0]
                    y = slot[1]
                    click(x, y)
                    sleep(.5)

                self._confirm()

        # Test
        self.awaits(events=[self.E_BATTLE_START_LIVE, self.E_VICTORY, self.E_DEFEAT])

    def check_availability(self):
        # @TODO Finish
        # res = {
        #     'is_active': False,
        #     'open_hour': None
        # }
        # live_arena_open_hours = [[6, 8], [14, 16], [20, 22]]
        utc_timestamp = datetime.utcnow().timestamp()
        utc_datetime = datetime.fromtimestamp(utc_timestamp)
        parsed_time = time_mgr.timestamp_to_datetime(utc_datetime)

        year = parsed_time['year']
        month = parsed_time['month']
        day = parsed_time['day']
        # @TODO
        hour = parsed_time['hour']
        hour = 14
        pause.until(datetime(year, month, day, hour, 1, 0, tzinfo=timezone.utc))
