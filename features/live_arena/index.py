import pyautogui
import pause

from helpers.time_mgr import *
from features.hero_filter.index import *

time_mgr = TimeMgr()
hero_filter = HeroFilter()

first = [334, 209, [22, 51, 90]]
second = [899, 94, [90, 24, 24]]
cant_find_opponent = [590, 290, [187, 130, 5]]
rgb_empty_slot = [49, 54, 49]

my_slots = [
    [240, 170, rgb_empty_slot],
    [200, 270, rgb_empty_slot],
    [160, 170, rgb_empty_slot],
    [120, 270, rgb_empty_slot],
    [76, 170, rgb_empty_slot],
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
not_available = [321, 421, [167, 49, 56]]

# the white 'Clock' in the left-top corner
finish_battle = [21, 46, [255, 255, 255]]
# the yellow 'Line' in screen center
finish_arena = [452, 232, [16, 69, 96]]

victory = [451, 38, [23, 146, 218]]
defeat = [451, 38, [199, 26, 48]]

battle_start = [341, 74, [86, 191, 255]]
refill_free = [454, 373, [187, 130, 5]]
refill_paid = [444, 393, [195, 40, 66]]
claim_refill = [875, 173, [218, 0, 0]]
claim_chest = [534, 448, [233, 0, 0]]

auto_mode = [49, 486]
return_start_panel = [444, 490]

PAID_REFILL_LIMIT = 1
ARCHIVE_PATTERN_FIRST = [1, 2, 2]


# @TODO Issues: keyboard locale, enemy's leaving the battle
# Requires: checking amount of keys
class ArenaLive:
    x_config = 600
    y_config = 175
    x_find_opponent = 500
    y_find_opponent = 460

    def __init__(self, props=None):
        self.results = []
        self.team = []
        self.pool = []
        self.leaders = []
        self.terminate = False
        self.refill = PAID_REFILL_LIMIT
        self.battles_counter = 0

        if props is not None:
            self._apply_props(props)

    def _apply_props(self, props):
        if 'pool' in props:
            self.pool = sorted(props['pool'], key=lambda x: (-x.get('priority', 0), x.get('priority', 0)))
            if 'leaders' in props:
                self.leaders = props['leaders']
            # self.pool = props['pool']
            # random.shuffle(self.pool)
            # if 'leaders' in props:
            #     self.leaders = props['leaders']
            #     self.leaders.reverse()
            # else:
            #     self.leaders = self.pool[0:2]

        if 'refill' in props:
            self.refill = int(props['refill'])

    def _confirm(self):
        click(800, 490)
        sleep(.5)

    def _claim_chest(self):
        # the chest is available
        if pixel_check_new(claim_chest):
            x = claim_chest[0]
            y = claim_chest[1]
            click(x, y)
            sleep(1)
            # click on get rewards text
            click(450, 450)
            sleep(.5)

    def _claim_free_refill_coins(self):
        if pixel_check_new(claim_refill):
            x = claim_refill[0] - 5
            y = claim_refill[1] + 5
            click(x, y)
            sleep(2)

    def _click_on_find_opponent(self):
        # click(self.x_find_opponent, self.y_find_opponent)
        find_opponent = [self.x_find_opponent, self.y_find_opponent, [187, 130, 5]]
        await_click([find_opponent], mistake=10)
        sleep(1)

    def _is_available(self):
        if pixel_check_new(not_available):
            self.terminate = True

        return not self.terminate

    def _save_result(self, result):
        self.results.append(result)
        s = 'Live Arena | '

        if result:
            s += 'WIN'
        else:
            s += 'DEFEAT'

        log(s)

    def _refill(self):
        self._click_on_find_opponent()

        sleep(1)
        ruby_button = find_needle_refill_ruby()

        if ruby_button is not None:
            log('Free coins are NOT available')
            if self.refill > 0:
                # wait and click on refill_paid
                click(refill_paid[0], refill_paid[1])
                sleep(2)
                self.refill -= 1
                self._click_on_find_opponent()
            else:
                log('No more refill')
                self.terminate = True
        elif pixels_wait([refill_free], msg='Free refill sacs', mistake=10, timeout=1, wait_limit=2)[0]:
            log('Free coins are available')
            # wait and click on refill_free
            click(refill_free[0], refill_free[1])
            sleep(2)
            self._click_on_find_opponent()

        return self.terminate

    def enter(self):
        go_index_page()

        click_on_progress_info()
        # live arena
        click(self.x_config, self.y_config)
        sleep(3)

    def attack(self):
        log('Live Arena | Attack')
        sorted_pool = self.pool
        team = []
        leaders = []
        slots_counter = 0

        def pick(name):
            hero_filter.open(x2=450)
            hero_filter.input(name)
            hero_filter.pick()
            hero_filter.clear()
            hero_filter.reset()
            hero_filter.close()

        def find_character(role=None):
            if role is None:
                role = sorted_pool[0]['role']

            next_char = None
            while next_char is None:
                i, char = find(sorted_pool, lambda x: x.get('role') == role)

                if char:
                    pick(char['name'])

                    if not pixel_check_new(my_slots[slots_counter], mistake=0):
                        next_char = char

                    sorted_pool.pop(i)
                else:
                    sorted_pool.pop(0)

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

        def wait_start_pixels():
            return pixels_wait([cant_find_opponent, first, second], msg="Start screen 1", timeout=0.1, mistake=5)

        start_pixels = wait_start_pixels()
        opponent_found = False
        while not opponent_found:
            # for "can't find opponent" cases
            if start_pixels[0]:
                x_find = cant_find_opponent[0]
                y_find = cant_find_opponent[1]
                click(x_find, y_find)
                sleep(.5)
                self._click_on_find_opponent()
                start_pixels = wait_start_pixels()
            else:
                opponent_found = True

        log('Live Arena | Starts battle: ' + str(self.battles_counter))
        pattern = ARCHIVE_PATTERN_FIRST
        if start_pixels[1]:
            log("I'm first")
        elif start_pixels[2]:
            log("I'm second")
            pattern.reverse()

        if pixels_wait([stage_1], msg='Stage 1 | Picking characters', timeout=2, mistake=5)[0]:
            sleep(.5)

            for i in range(len(pattern)):
                if pixels_wait([first], msg='Picking characters', timeout=2, mistake=10)[0]:
                    sleep(.2)

                    # picking heroes logic
                    for j in range(pattern[i]):
                        unit = find_character()
                        team.append(unit['name'])
                        sleep(.1)
                        self._confirm()
                        slots_counter += 1

        if pixels_wait([stage_2], msg='Stage 2 | Ban hero', timeout=2, mistake=5)[0]:
            sleep(.5)
            # Banning random second slot
            random_slot = random.choice(enemy_slots)
            x = random_slot[0]
            y = random_slot[1]
            click(x, y)
            sleep(.5)
            self._confirm()

        if pixels_wait([stage_3], msg='Stage 3 | Choosing leader', timeout=2, mistake=5)[0]:
            sleep(.5)
            if pixels_wait([first], msg='Choosing leader', timeout=2, mistake=10)[0]:
                leaders_indicis = find_leaders_indicis()

                for i in range(len(leaders_indicis)):
                    leader_index = leaders_indicis[i]
                    slot = my_slots[leader_index]
                    x = slot[0]
                    y = slot[1]
                    click(x, y)
                    sleep(.5)
                self._confirm()

        my_turn_or_defeat = pixels_wait([battle_start, defeat], msg='My turn or Defeat', timeout=2, mistake=20)

        # Battle just started
        if my_turn_or_defeat[0]:
            click(auto_mode[0], auto_mode[1])
            battle_result = pixels_wait([victory, defeat], msg='Victory or Defeat', timeout=2, mistake=20)
            self._save_result(battle_result[0])
        else:
            self._save_result(False)

        click(return_start_panel[0], return_start_panel[1])
        sleep(3)

    def report(self):
        s = None
        if len(self.results):
            w = self.results.count(True)
            t = len(self.results)
            wr = w * 100 / t
            wr_str = str(round(wr)) + '%'
            s = 'Live Arena | Battles: ' + str(len(self.results)) + ' | ' + 'Win rate: ' + wr_str

        return s

    def finish(self):
        go_index_page()
        log('Live Arena | Finish')

    def check_availability(self):
        # @TODO Finish
        # res = {
        #     'is_active': False,
        #     'open_hour': None
        # }
        # live_arena_open_hours = [[6, 8], [14, 16], [20, 22]]
        # utc_timestamp = datetime.utcnow().timestamp()
        utc_datetime = datetime.fromtimestamp(utc_timestamp)
        parsed_time = time_mgr.timestamp_to_datetime(utc_datetime)
        # hour = parsed_time['hour']
        #
        # length = len(live_arena_open_hours)
        # for i in range(len(live_arena_open_hours)):
        #     arr = live_arena_open_hours[i]
        #     for j in range(len(arr)):
        #         if arr[0] < hour < arr[1]:
        #             res['is_active'] = True
        #             break
        #         elif arr[1] <= hour and i < length:
        #             res['open_hour'] = live_arena_open_hours[i + 1]

        year = parsed_time['year']
        month = parsed_time['month']
        day = parsed_time['day']
        # @TODO
        hour = parsed_time['hour']
        hour = 14
        pause.until(datetime(year, month, day, hour, 1, 0, tzinfo=timezone.utc))

    def run(self, props=None):
        # self.check_availability()

        if props is not None:
            self._apply_props(props)

        has_pool = bool(len(self.pool))
        is_active = pixel_check_new([822, 472, [41, 162, 33]], 10)

        if not has_pool:
            log('Live Arena is Terminated | The POOL is NOT specified')

        if not is_active:
            log('Live Arena | NOT Active')
            go_index_page()

        if has_pool and is_active:
            log('Live Arena | Active')
            self.enter()

            while self._is_available():
                self._claim_free_refill_coins()
                self._claim_chest()

                if self._refill():
                    break

                self.battles_counter += 1
                self.attack()

            self.finish()
