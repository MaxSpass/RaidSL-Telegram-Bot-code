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
rgb_empty_slot = [49, 54, 49]
width_empty_slot = 48
height_empty_slot = 64
my_slots = [
    [226, 162, rgb_empty_slot],
    [184, 264, rgb_empty_slot],
    [146, 162, rgb_empty_slot],
    [105, 264, rgb_empty_slot],
    [64, 162, rgb_empty_slot],
]

enemy_slots = [
    [650, 198, rgb_empty_slot],
    [697, 289, rgb_empty_slot],
    [728, 199, rgb_empty_slot],
    [767, 292, rgb_empty_slot],
    [812, 201, rgb_empty_slot],
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
    E_CANT_FIND_OPPONENT = {
        "name": "Can't find an opponent",
        "expect": lambda: pixels_every(
            same_pixels_line(cant_find_opponent_button_cancel), lambda p: pixel_check_new(p, mistake=5)
        ),
        "interval": 3,
    }
    E_OPPONENT_LEFT = {
        "name": "Opponent left the battle",
        "expect": lambda: bool(find_victory_opponent_left()),
        "interval": .5,
    }
    E_PICK_FIRST = {
        "name": "Pick first",
        "expect": lambda: pixel_check_new(first, mistake=5),
    }
    E_PICK_SECOND = {
        "name": "Pick second",
        "expect": lambda: pixel_check_new(second, mistake=5),
    }
    E_VICTORY = {
        "name": "Victory",
        "expect": lambda: pixel_check_new(victory, mistake=30),
    }
    E_DEFEAT = {
        "name": "Defeat",
        "expect": lambda: pixel_check_new(defeat, mistake=30),
    }

    E_STAGE_1 = {
        "name": "Stage 1 | Picking characters",
        "expect": lambda: pixel_check_new(stage_1, mistake=10),
        "interval": 2,
    }
    E_PICKING_PROCESS = {
        "name": "Picking characters process",
        "expect": lambda: pixel_check_new(first, mistake=10),
        "interval": 2,
    }
    E_STAGE_2 = {
        "name": "Stage 2 | Ban hero",
        "expect": lambda: pixel_check_new(stage_2, mistake=10),
        "interval": 2,
    }
    E_STAGE_3 = {
        "name": "Stage 3 | Choosing leader",
        "expect": lambda: pixel_check_new(stage_3, mistake=10),
        "interval": 2,
    }
    E_CHOOSING_LEADER = {
        "name": "Choosing leader process",
        "expect": lambda: pixel_check_new(first, mistake=10),
        "interval": 2,
    }
    E_BATTLE_START_LIVE = {
        "name": "Battle start Live",
        "expect": lambda: pixel_check_new(battle_start_turn, mistake=20),
        "callback": enable_auto_play,
        "blocking": False,
        "limit": 1,
    }

    x_config = 600
    y_config = 175

    def __init__(self, app, props=None):
        Location.__init__(self, name='Arena Live', app=app, report_predicate=self._report)

        if self.results is None:
            self.results = []

        self.team = []
        self.pool = []
        self.leaders = []
        self.refill = PAID_REFILL_LIMIT
        self.idle_after_defeat = 0
        self.battles_counter = 0
        self.current_battle_time = None

        if props is not None:
            self._apply_props(props=props)

        self.event_dispatcher.subscribe('enter', self._enter)
        self.event_dispatcher.subscribe('run', self._run)

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
            self.terminate = True
            return

        click_on_progress_info()
        # live arena
        click(self.x_config, self.y_config)
        sleep(3)

    def _run(self, props=None):
        if props is not None:
            self._apply_props(props=props)

        if find_indicator_active() is not None:
            self.log('Active')
            has_pool = bool(len(self.pool))
            if has_pool:
                self.obtain()

                while self._is_available():
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
        else:
            self.log('NOT Active')
            close_popup_recursive()

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
            self.terminate = True

    def _is_available(self):
        if find_indicator_active() is None:
            self.terminate = True

        return not self.terminate

    def _save_result(self, result):
        self.results.append(result)
        s = ''

        if result:
            s += 'WIN'
        else:
            s += 'DEFEAT'

        self.log(s)

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
                self.terminate = True
        elif pixels_wait([refill_free], msg='Free refill sacs', mistake=10, timeout=1, wait_limit=2)[0]:
            self.log('Free coins are available')
            # wait and click on refill_free
            click(refill_free[0], refill_free[1], smart=True)
            self._click_on_find_opponent()

        return self.terminate

    def obtain(self):
        for i in range(len(rewards_pixels)):
            pixel = rewards_pixels[i]
            if pixel_check_new(pixel, mistake=30):
                x = pixel[0]
                y = pixel[1]
                click(x, y)
                sleep(.5)

    def attack(self):
        self.battles_counter += 1
        self.current_battle_time = get_time_for_log(s='_')
        self.stop = False
        sorted_pool = copy.deepcopy(self.pool)
        self.log('Attack | Pool Length: ' + str(len(sorted_pool)))
        team = []
        leaders = []
        slots_counter = 0

        def find_character(role=None):
            self.log(f'Current pool length: {len(sorted_pool)}')
            if role is None:
                role = sorted_pool[0]['role']

            next_char = None
            while next_char is None and not self.stop:
                i, char = find(sorted_pool, lambda x: x.get('role') == role)
                index_to_remove = 0

                if char and not self.stop:
                    hero_filter.choose(title=char['name'], wait_after=.5)

                    _slot = my_slots[slots_counter]
                    _region = [_slot[0], _slot[1], width_empty_slot, height_empty_slot]
                    # show_pyautogui_image(pyautogui.screenshot(region=_region))
                    _position_empty = find_hero_slot_active(region=_region)
                    if _position_empty is None and not self.stop:
                        next_char = char

                    # if not pixel_check_new(my_slots[slots_counter], mistake=10):
                    #     next_char = char

                    index_to_remove = i

                # @TODO Add checking
                del sorted_pool[index_to_remove]

            return next_char

        def find_leaders_indicis():
            res = []

            for i in range(len(self.leaders)):
                l = self.leaders[i]
                if l in team:
                    res.append(team.index(l))
                if len(res) == 2:
                    break

            res.reverse()

            return res

        def force_stop(*args):
            self.log("OPPONENT LEFT THE BATTLE")
            self.stop = True
            self._save_result(True)

        def apply_results(name):
            if self.E_VICTORY['name'] == name:
                self._save_result(True)
            elif self.E_DEFEAT['name'] == name:
                self._save_result(False)
                if self.idle_after_defeat:
                    sleep(self.idle_after_defeat)

        E_OPPONENT_LEFT_WITH_CALLBACK = prepare_event(self.E_OPPONENT_LEFT, {
            "callback": force_stop,
        })

        def await_start_events():
            return self.awaits(
                events=[self.E_PICK_FIRST, self.E_PICK_SECOND, self.E_CANT_FIND_OPPONENT],
                interval=.1
            )

        def await_stage_1():
            return self.awaits(events=[self.E_STAGE_1, E_OPPONENT_LEFT_WITH_CALLBACK])

        def await_pick():
            return self.awaits(events=[self.E_PICKING_PROCESS, E_OPPONENT_LEFT_WITH_CALLBACK])

        def await_stage_2():
            return self.awaits(events=[self.E_STAGE_2, E_OPPONENT_LEFT_WITH_CALLBACK])

        def await_stage_3():
            return self.awaits(events=[self.E_STAGE_3, E_OPPONENT_LEFT_WITH_CALLBACK])

        def await_choosing_leader():
            return self.awaits(events=[self.E_CHOOSING_LEADER, E_OPPONENT_LEFT_WITH_CALLBACK])

        def await_battle_results():
            return self.awaits(events=[self.E_BATTLE_START_LIVE, self.E_VICTORY, self.E_DEFEAT])

        start_events = await_start_events()
        opponent_found = False
        while not opponent_found and not self.terminate:
            # for "can't find opponent" cases
            if self.E_CANT_FIND_OPPONENT['name'] == start_events['name']:
                x_find = cant_find_opponent_button_cancel[0]
                y_find = cant_find_opponent_button_cancel[1]
                click(x_find, y_find)
                sleep(.5)
                self._click_on_find_opponent()
                start_events = await_start_events()
            else:
                self.log('Starts battle: ' + str(self.battles_counter))
                opponent_found = True

        self.log(start_events['name'])

        pattern = ARCHIVE_PATTERN_FIRST[:]
        if start_events['name'] == self.E_PICK_SECOND['name']:
            pattern.reverse()

        stage_1_events = await_stage_1()
        if self.E_STAGE_1['name'] == stage_1_events['name']:
            sleep(.5)
            for i in range(len(pattern)):
                if self.stop:
                    break

                pick_process_events = await_pick()
                if self.E_PICKING_PROCESS['name'] == pick_process_events['name']:
                    sleep(.2)

                    # picking heroes logic
                    for j in range(pattern[i]):
                        if self.stop:
                            break

                        unit = find_character()
                        if unit is not None:
                            team.append(unit['name'])
                            sleep(.1)
                            self.log(f"Picked: {unit['name']}")
                            slots_counter += 1

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
                leaders_indicis = find_leaders_indicis()

                for i in range(len(leaders_indicis)):
                    leader_index = leaders_indicis[i]
                    slot = my_slots[leader_index]
                    x = slot[0]
                    y = slot[1]
                    click(x, y)
                    sleep(.5)

                self._confirm()

        battle_start_events = await_battle_results()
        apply_results(battle_start_events['name'])

        tap_to_continue(wait_after=2)

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
