from helpers.common import *
from constants.index import *

button_refresh = [817, 133, [22, 124, 156]]
refill_free = [455, 380, [187, 130, 5]]
refill_paid = [440, 376, [255, 33, 51]]
defeat = [443, 51, [229, 40, 104]]

DEFAULT_STRIKES_LIMIT = 1
PAID_REFILL = 0

class ArenaFactory:
    name = None
    item_height = None
    button_locations = None
    item_locations = None
    # classic: 95 | tag: 135
    x_axis_info = None

    strikes = DEFAULT_STRIKES_LIMIT
    max_swipe = 0
    refill = 0
    tracker = []
    terminate = False

    def __init__(
            self,
            name,
            x_axis_info,
            item_height,
            button_locations,
            item_locations,
            refill=PAID_REFILL
    ):
        self.name = name
        self.x_axis_info = x_axis_info
        self.item_height = item_height
        self.button_locations = button_locations
        self.item_locations = item_locations
        self.refill = refill

        for i in range(len(self.item_locations)):
            item = self.item_locations[i]
            swipes = item['swipes']
            if swipes > self.max_swipe:
                self.max_swipe = swipes

    def _refresh_arena(self):
        # if pixels_wait('Refresh button', [[817, 133, [22, 124, 156]]], timeout=10, mistake=10, wait_limit=5)[0]:
        if pixels_wait('Refresh button', [button_refresh], 10)[0]:
            log('Refreshing...')
            click(817, 133)
            sleep(1)
            for index in range(2):
                pyautogui.moveTo(560, 185, .5, random_easying())
                pyautogui.dragTo(560, 510, duration=.4)
                sleep(1.5)
            sleep(3)

    def enter(self):
        click_on_progress_info()
        # classic arena
        click(600, self.x_axis_info)
        sleep(1)

    def _refill(self):
        refilled = False

        def click_on_refill():
            click(439, 395)
            sleep(0.5)

        sleep(1)
        ruby_button = find_needle_refill_ruby()

        if ruby_button is not None:
            log('No more free sacs')
            if self.refill > 0:
                self.refill -= 1
                click_on_refill()
                refilled = True
            else:
                log('Refill value is 0')
                self.terminate = True
        elif pixel_check_new(refill_free, mistake=10):
            log('Has free sacs')
            click_on_refill()
            refilled = True

        return refilled

    def attack(self):
        results_local = []
        should_use_multi_swipe = False

        def inner_swipe(swipes_amount):
            if should_use_multi_swipe:
                for j in range(swipes_amount):
                    sleep(1)
                    swipe('bottom', 580, 254, self.item_height)
            # @TODO Tag-arena does not work well because of 'max_swipe' value
            elif 0 < i <= self.max_swipe:
                swipe('bottom', 580, 254, self.item_height)

        for i in range(len(self.item_locations)):
            el = self.item_locations[i]
            swipes = el['swipes']
            position = el['position']
            inner_swipe(swipes)
            pos = self.button_locations[position]
            x = pos[0]
            y = pos[1]

            def click_on_battle():
                click(x, y)
                sleep(.5)

            def click_on_start():
                click(860, 480)
                sleep(0.5)

            # checking - is an enemy already attacked
            is_not_attacked = len(results_local) - 1 < i
            if pixel_check_old(x, y, [187, 130, 5]) and is_not_attacked:
                log(self.name + ' | Attack')
                # pyautogui.moveTo(x, y, 1)
                # log(pyautogui.pixel(x, y))
                # continue
                click_on_battle()

                if self._refill():
                    click_on_battle()

                if self.terminate:
                    break

                click_on_start()

                waiting_battle_end_regular(self.name + ' battle end')
                res = not pixel_check_new(defeat, 5)
                results_local.append(res)
                if res:
                    log('VICTORY')
                else:
                    log('DEFEAT')

                tap_to_continue()
                sleep(1)
                # tells to skip several teams by swiping
                should_use_multi_swipe = True

        return results_local

    def finish(self):
        go_index_page()
        log('DONE - ' + self.name)
        log('Won: ' + str(self.tracker.count(True)) + ' | Lost: ' + str(self.tracker.count(False)))

    def run(self, strikes=DEFAULT_STRIKES_LIMIT):
        # @TODO strikes ???
        self.strikes = strikes
        self.enter()
        # and self.strikes > 0
        while self.refill > 0 or self.terminate is False:
            results = self.attack()
            self.strikes -= 1

            # joins each attack results into the global tracker
            for j in range(len(results)):
                self.tracker.append(results[j])

            # at least one 'Defeat' - should refresh
            if results.count(False) > 0:
                self._refresh_arena()

        self.finish()


arena_classic = ArenaFactory(
    name='Classic Arena',
    x_axis_info=95,
    item_height=CLASSIC_ITEM_HEIGHT,
    button_locations=CLASSIC_BUTTON_LOCATIONS,
    item_locations=CLASSIC_ITEM_LOCATIONS,
)

arena_tag = ArenaFactory(
    name='Tag Arena',
    x_axis_info=135,
    item_height=TAG_ITEM_HEIGHT,
    button_locations=TAG_BUTTON_LOCATIONS,
    item_locations=TAG_ITEM_LOCATIONS,
)
