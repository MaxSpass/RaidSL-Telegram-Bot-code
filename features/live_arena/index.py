import pyautogui

from helpers.common import *
from features.hero_filter.index import *

hero_filter = HeroFilter()

first = [334, 209, [22, 51, 90]]
second = [899, 94, [90, 24, 24]]

my_slots = [
    [253, 188],
    [202, 293],
    [170, 202],
    [122, 295],
    [91, 194]
]

enemy_slots = [
    [650, 198],
    [697, 289],
    [728, 199],
    [767, 292],
    [812, 201]
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

MAX_DEFAULT_PAID_REFILL = 1


# @TODO Needs to be refactor in order to fix phantom bug
class ArenaLive:
    x_config = 600
    y_config = 175
    pool = []
    team = []
    leaders = []
    refill = MAX_DEFAULT_PAID_REFILL

    x_find_opponent = 461
    y_find_opponent = 468

    results = []
    terminate = False

    def __init__(self, pool, leaders, refill=MAX_DEFAULT_PAID_REFILL):
        self.pool = pool
        self.leaders = leaders
        self.refill = refill

        self.leaders.reverse()
        random.shuffle(self.pool)

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
        click(self.x_find_opponent, self.y_find_opponent)
        sleep(2)

    def _is_available(self):
        if pixel_check_new(not_available):
            self.terminate = True

        return not self.terminate

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
        click_on_progress_info()
        # live arena
        click(self.x_config, self.y_config)
        sleep(3)

    def attack(self):
        log('Live Arena | Attack')
        states = ['first', 'second', 'stage_1', 'stage_2', 'stage_3', 'battle_start']
        states_done = []

        # len(states) > len(states_done) and
        # # @TODO Something here
        # while True:
        #     state_results = pixels_wait(
        #         [first, second, stage_1, stage_2, stage_3, battle_start],
        #         msg='Determining the state...',
        #         timeout=0.1,
        #         mistake=5
        #     )
        #     is_first = state_results[0] and states[0] not in states_done
        #     is_second = state_results[1] and states[1] not in states_done
        #     is_stage_1 = state_results[2] and states[2] not in states_done
        #     is_stage_2 = state_results[3] and states[3] not in states_done
        #     is_stage_3 = state_results[4] and states[4] not in states_done
        #     is_started_battle = state_results[5] and states[5] not in states_done
        #
        #
        #     log('Stages pixel')
        #     log(pyautogui.pixel(stage_1[0], stage_1[1]))
        #
        #     log('First and second')
        #     log(pyautogui.pixel(first[0], first[1]))
        #     log(pyautogui.pixel(second[0], second[1]))
        #
        #     log('Started battle')
        #     log(pyautogui.pixel(battle_start[0], battle_start[1]))
        #
        #     # waiting for start panel (picking logic)
        #     if is_first or is_second:
        #         states_done.append(states[0])
        #         states_done.append(states[1])
        #         if is_first:
        #             # first
        #             log("I'm first")
        #             self.team = [
        #                 self.pool[0:1],
        #                 self.pool[1:3],
        #                 self.pool[3:5]
        #             ]
        #         elif is_second:
        #             # second
        #             log("I'm second")
        #             self.team = [
        #                 self.pool[0:2],
        #                 self.pool[2:4],
        #                 self.pool[4:5]
        #             ]
        #
        #     if is_stage_1:
        #         log('Stage 1 | Picking characters')
        #         states_done.append(states[2])
        #         sleep(.5)
        #         slots_counter = 0
        #         print(self.team)
        #         for i in range(len(self.team)):
        #             if pixels_wait([first], msg='Picking characters', timeout=2, mistake=10, wait_limit=65)[0]:
        #                 log('picked')
        #                 sleep(.2)
        #                 hero_filter.open(x2=450)
        #
        #                 # picking heroes logic
        #                 for j in range(len(self.team[i])):
        #                     hero_name = self.team[i][j]
        #                     hero_filter.input(hero_name)
        #                     hero_filter.pick()
        #                     hero_filter.clear()
        #                     slots_counter += 1
        #
        #                 hero_filter.reset()
        #                 hero_filter.close()
        #                 sleep(.1)
        #
        #                 self._confirm()
        #
        #     if is_stage_2:
        #         log('Stage 2 | Ban second hero')
        #         states_done.append(states[3])
        #         sleep(.5)
        #         # @TODO Banning random second slot
        #         random_slot = random.choice(enemy_slots)
        #         x = random_slot[0]
        #         y = random_slot[1]
        #         click(x, y)
        #         sleep(.5)
        #         self._confirm()
        #
        #     if is_stage_3:
        #         log('Stage 3 | Choosing leader')
        #         states_done.append(states[4])
        #         sleep(.5)
        #         if pixels_wait([first], msg='Choosing leader', timeout=2, mistake=10)[0]:
        #             for i in range(len(self.leaders)):
        #                 leader = self.leaders[i]
        #                 team_index = self.pool.index(leader)
        #                 slot = my_slots[team_index]
        #                 x = slot[0]
        #                 y = slot[1]
        #                 click(x, y)
        #                 sleep(.5)
        #             self._confirm()
        #
        #     if is_started_battle:
        #         log('Battle start')
        #         states_done.append(states[5])
        #         click(auto_mode[0], auto_mode[1])
        #
        #         battle_result = pixels_wait([victory, defeat], msg='End of the battle', timeout=2, mistake=20)
        #
        #         if battle_result[0]:
        #             log("Live Arena | WIN")
        #             self.results.append(True)
        #         elif battle_result[1]:
        #             log('Live Arena | DEFEAT')
        #             self.results.append(False)
        #
        #     # @TODO
        #     if state_results.count(True) == 0:
        #         sleep(10)
        #
        #     # battle_start
        #     if states[5] in states_done:
        #         break

        start_pixels = pixels_wait([first, second], msg="Start screen", timeout=0.1)
        if start_pixels[0]:
            # first
            log("I'm first")
            self.team = [
                self.pool[0:1],
                self.pool[1:3],
                self.pool[3:5]
            ]
        elif start_pixels[1]:
            # second
            log("I'm second")
            self.team = [
                self.pool[0:2],
                self.pool[2:4],
                self.pool[4:5]
            ]

        if pixels_wait([stage_1], msg='Stage 1 | Picking characters', timeout=2, mistake=5)[0]:
            sleep(.5)
            slots_counter = 0
            print(self.team)
            for i in range(len(self.team)):
                if pixels_wait([first], msg='Picking characters', timeout=2, mistake=10)[0]:
                    sleep(.2)
                    hero_filter.open(x2=450)

                    # picking heroes logic
                    for j in range(len(self.team[i])):
                        hero_name = self.team[i][j]
                        hero_filter.input(hero_name)
                        hero_filter.pick()
                        hero_filter.clear()
                        slots_counter += 1

                    hero_filter.reset()
                    hero_filter.close()
                    sleep(.1)

                    self._confirm()

        if pixels_wait([stage_2], msg='Stage 2 | Ban second hero', timeout=2, mistake=5)[0]:
            sleep(.5)
            # Banning random second slot
            random_slot = random.choice(enemy_slots)
            x = random_slot[0]
            y = random_slot[1]
            click(x, y)
            sleep(.5)
            self._confirm()

        if pixels_wait([stage_3], msg='Stage 3 | Choosing leader',  timeout=2, mistake=5)[0]:
            sleep(.5)
            if pixels_wait([first], msg='Choosing leader', timeout=2, mistake=10)[0]:
                for i in range(len(self.leaders)):
                    leader = self.leaders[i]
                    team_index = self.pool.index(leader)
                    slot = my_slots[team_index]
                    x = slot[0]
                    y = slot[1]
                    click(x, y)
                    sleep(.5)
                self._confirm()

        if pixels_wait([battle_start], msg='Start battle', timeout=2, mistake=5)[0]:
            click(auto_mode[0], auto_mode[1])

            battle_result = pixels_wait([victory, defeat], msg='End of the battle', timeout=2, mistake=20)

            if battle_result[0]:
                log("Live Arena | WIN")
                self.results.append(True)
            elif battle_result[1]:
                log('Live Arena | DEFEAT')
                self.results.append(False)

        click(return_start_panel[0], return_start_panel[1])
        sleep(3)

    def report(self):
        s = None
        if len(self.results):
            w = self.results.count(True)
            l = self.results.count(False)
            t = w + l
            wr = w * 100 / t
            wr_str = str(round(wr)) + '%'
            # lr = 100 - wr
            # lr_str = str(round(lr)) + '%'
            s = 'Live Arena | Battles: ' + str(len(self.results)) + ' | ' + 'Win rate: ' + wr_str

        return s

    def finish(self):
        go_index_page()
        log('Live Arena | Finish')

    def run(self):
        if pixel_check_old(822, 472, [41, 162, 33], 10):
            log('Live Arena | Active')
            self.enter()

            battles_counter = 1
            while self._is_available():
                log('Live Arena | Starts battle: ' + str(battles_counter))
                self._claim_free_refill_coins()
                self._claim_chest()

                if self._refill():
                    break

                self.attack()
                battles_counter += 1

            self.finish()
        else:
            log('Live Arena | NOT Active')
            go_index_page()
