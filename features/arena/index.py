from helpers.common import *
from constants.index import *
from classes.Feature import Feature

button_refresh = [817, 133, [22, 124, 156]]
refill_free = [455, 380, [187, 130, 5]]
refill_paid = [440, 376, [255, 33, 51]]
defeat = [443, 51, [229, 40, 104]]
tab_battle = [110, 115, [2, 93, 154]]

RGB_RED_DOT = [225, 0, 0]
PAID_REFILL_LIMIT = 0
OUTPUT_ITEMS_AMOUNT = 10


class ArenaFactory(Feature):
    name = None
    item_height = None
    button_locations = None
    item_locations = None
    x_axis_info = None

    max_swipe = None
    refill = None
    results = None
    terminate = None

    def __init__(
            self,
            app,
            name,
            x_axis_info,
            item_height,
            button_locations,
            item_locations,
            refill_coordinates,
            tiers_coordinates,
            props=None
    ):
        Feature.__init__(self, feature_name=name, app=app)

        self.name = name
        self.x_axis_info = x_axis_info
        self.item_height = item_height
        self.button_locations = button_locations
        self.item_locations = item_locations
        self.refill_coordinates = refill_coordinates
        self.tiers_coordinates = tiers_coordinates

        self.refill = PAID_REFILL_LIMIT
        self.initial_refresh = False
        self.max_swipe = 0
        self.results = []
        self.terminate = False

        self._apply_props(props=props)

        for i in range(len(self.item_locations)):
            item = self.item_locations[i]
            swipes = item['swipes']
            if swipes > self.max_swipe:
                self.max_swipe = swipes

        self.event_dispatcher.subscribe('enter', self._enter)
        self.event_dispatcher.subscribe('run', self._run)

    def _enter(self):
        click_on_progress_info()
        click(600, self.x_axis_info)
        sleep(1)

        self.obtain()

    def _run(self, props=None):
        if props is not None:
            self._apply_props(props=props)

        if self.initial_refresh:
            self._refresh_arena()
            # @TODO Test
            sleep(1)

        while self.terminate is False:
            self.attack()

            last_results = self._get_last_results()

            if self.terminate is False:
                # at least one 'Defeat' or continued battles - should refresh
                if last_results.count(False) > 0 or len(last_results) < OUTPUT_ITEMS_AMOUNT:
                    self._refresh_arena()

    def _apply_props(self, props=None):
        if props is not None:
            if 'refill' in props:
                self.refill = int(props['refill'])
            if 'initial_refresh' in props:
                self.initial_refresh = bool(props['initial_refresh'])

    def _refresh_arena(self):
        self.log('Refreshing...')
        await_click([button_refresh], msg='Refresh button', mistake=10)
        sleep(1)
        for index in range(2):
            pyautogui.moveTo(560, 185, .5, random_easying())
            pyautogui.dragTo(560, 510, duration=.4)
            sleep(1.5)
        sleep(3)

    def _refill(self):
        refilled = False

        def click_on_refill():
            click(439, 395)
            sleep(0.5)

        sleep(1)
        ruby_button = find_needle_refill_ruby()

        if ruby_button is not None:
            self.log('Free coins are NOT available')
            if self.refill > 0:
                self.refill -= 1
                click_on_refill()
                refilled = True
            else:
                self.log('No more refill')
                self.terminate = True
        elif pixels_wait([refill_free], msg='Free refill sacs', mistake=10, timeout=1, wait_limit=2)[0]:
            self.log('Free coins are available')
            click_on_refill()
            refilled = True

        sleep(0.5)

        return refilled

    def _get_last_results(self):
        length = len(self.results)
        if length:
            return [self.results[len(self.results) - 1]]
        else:
            return self.results

    def _show_results(self, results, is_detailed=False):
        s = None
        if len(results):
            flatten_list = flatten(results)
            w = flatten_list.count(True)
            l = flatten_list.count(False)

            if is_detailed:
                t = w + l
                wr = w * 100 / t
                wr_str = str(round(wr)) + '%'
                # lr = 100 - wr
                # lr_str = str(round(lr)) + '%'
                s = self.name + ' | ' + 'Battles: ' + str(len(flatten_list)) + ' | ' + 'Win rate: ' + wr_str
            else:
                s = 'Won: ' + str(w) + ' | Lost: ' + str(l)

        return s

    def obtain(self):
        x = self.tiers_coordinates[0]
        y = self.tiers_coordinates[1]
        tiers_pixel = [x, y, RGB_RED_DOT]
        if pixel_check_new(tiers_pixel, mistake=20):
            click(x, y)
            sleep(1)

            dot = find_needle_arena_reward()
            for i in range(3):
                swipe('right', 600, 350, 400, speed=.6, sleep_after_end=.2)
                dot = find_needle_arena_reward()
                if dot is not None:
                    x = dot[0]
                    y = dot[1]+20
                    # click on the chest
                    click(x, y)
                    sleep(1)
                    # click on the claim
                    click(455, 455)
                    sleep(1)
                    break

            click(tab_battle[0], tab_battle[1])
            sleep(.3)


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
                sleep(1.5)

            def click_on_start():
                click(860, 480)
                sleep(0.5)

            # checking - is an enemy already attacked
            is_not_attacked = len(results_local) - 1 < i
            if pixel_check_new([x, y, [187, 130, 5]]) and is_not_attacked:
                self.log(self.name + ' | Attack')
                # pyautogui.moveTo(x, y, 1)
                # self.log(pyautogui.pixel(x, y))
                # continue
                click_on_battle()

                if self._refill():
                    click_on_battle()

                if self.terminate:
                    self.log('Terminated')
                    break

                click_on_start()

                waiting_battle_end_regular(self.name + ' | Battle end')
                res = not pixel_check_new(defeat, 20)
                results_local.append(res)
                if res:
                    self.log('VICTORY')
                else:
                    self.log('DEFEAT')

                tap_to_continue()
                sleep(1)
                # tells to skip several teams by swiping
                should_use_multi_swipe = True

                # if i == 0:
                #     self.terminate = True
                #     break

        # appends result from attack series into the global results list
        if len(results_local):
            self.results.append(results_local)
        # return results_local

    def report(self):
        return self._show_results(self.results, is_detailed=True)


class ArenaClassic(ArenaFactory):
    def __init__(self, app, props=None):
        ArenaFactory.__init__(
            self,
            app=app,
            name='Classic Arena',
            x_axis_info=95,
            item_height=CLASSIC_ITEM_HEIGHT,
            button_locations=CLASSIC_BUTTON_LOCATIONS,
            item_locations=CLASSIC_ITEM_LOCATIONS,
            refill_coordinates=CLASSIC_COINS_REFILL,
            tiers_coordinates=CLASSIC_TIERS_COORDINATE,
            props=props
        )


class ArenaTag(ArenaFactory):
    def __init__(self, app, props=None):
        ArenaFactory.__init__(
            self,
            app=app,
            name='Tag Arena',
            x_axis_info=135,
            item_height=TAG_ITEM_HEIGHT,
            button_locations=TAG_BUTTON_LOCATIONS,
            item_locations=TAG_ITEM_LOCATIONS,
            refill_coordinates=TAG_COINS_REFILL,
            tiers_coordinates=TAG_TIERS_COORDINATE,
            props=props
        )
