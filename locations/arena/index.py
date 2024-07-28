from helpers.common import *
from constants.index import *
from classes.Location import Location

button_refresh = [817, 133, [22, 124, 156]]
refill_free = [455, 380, [187, 130, 5]]
refill_paid = [440, 376, [255, 33, 51]]
defeat = [443, 51, [229, 40, 104]]
tab_battle = [110, 115, [2, 93, 154]]

RGB_RED_DOT = [225, 0, 0]
PAID_REFILL_LIMIT = 0
OUTPUT_ITEMS_AMOUNT = 10


def callback_refresh(*args):
    click(button_refresh[0], button_refresh[1])
    sleep(3)
    for index in range(2):
        swipe_new('top', 560, 200, 300, speed=.2, instant_move=True)
    sleep(2)


class ArenaFactory(Location):
    E_BUTTON_REFRESH = {
        "name": "Refresh button",
        "expect": lambda: pixel_check_new(button_refresh, mistake=5),
        "callback": callback_refresh,
        "interval": 5,
    }

    name = None
    item_height = None
    button_locations = None
    item_locations = None
    x_axis_info = None
    read_coins_predicate = None

    max_swipe = None
    refill = None
    results = None

    def __init__(
            self,
            app,
            name,
            x_axis_info,
            read_coins_predicate,
            item_height,
            button_locations,
            item_locations,
            refill_coordinates,
            tiers_coordinates,
            props=None
    ):
        Location.__init__(self, name=name, app=app, report_predicate=self._report)

        if self.results is None:
            self.results = []

        self.name = name
        self.x_axis_info = x_axis_info
        self.read_coins_predicate = read_coins_predicate
        self.item_height = item_height
        self.button_locations = button_locations
        self.item_locations = item_locations
        self.refill_coordinates = refill_coordinates
        self.tiers_coordinates = tiers_coordinates

        self.refill = PAID_REFILL_LIMIT
        self.initial_refresh = False
        self.battle_time_limit = True
        self.max_swipe = 0

        self._apply_props(props=props)

        self.E_BATTLE_END = prepare_event(self.E_BATTLE_END, {
            "expect": lambda: pixel_check_new([20, 46, [255, 255, 255]], mistake=3)
        })

        for i in range(len(self.item_locations)):
            item = self.item_locations[i]
            swipes = item['swipes']
            if swipes > self.max_swipe:
                self.max_swipe = swipes

        self.event_dispatcher.subscribe('enter', self._enter)
        self.event_dispatcher.subscribe('run', self._run)

    def _report(self):
        res_list = []
        if len(self.results):
            flatten_list = flatten(self.results)
            w = flatten_list.count(True)
            l = flatten_list.count(False)
            str_battles = f"Battles: {str(len(flatten_list))}"
            str_wr = f"(WR: {calculate_win_rate(w, l)})"
            res_list.append(f"{str_battles} {str_wr}")

        return res_list

    def _enter(self):
        click_on_progress_info()
        click(600, self.x_axis_info, smart=True)
        sleep(1)

        self.obtain()

    def _run(self, props=None):
        # for i in range(2):
        #     sleep(1)
        # return
        if props is not None:
            self._apply_props(props=props)

        if self.initial_refresh:
            self._refresh_arena()
            # @TODO Test
            sleep(1)

        while self.terminated is False:
            self.attack()

            last_results = self._get_last_results()

            if self.terminated is False:
                # at least one 'Defeat' or continued battles - should refresh
                if last_results.count(False) > 0 or len(last_results) < OUTPUT_ITEMS_AMOUNT:
                    self._refresh_arena()

    def _apply_props(self, props=None):
        if props is not None:
            if 'refill' in props:
                self.refill = int(props['refill'])
            if 'initial_refresh' in props:
                self.initial_refresh = bool(props['initial_refresh'])
            if 'battle_time_limit' in props:
                self.battle_time_limit = int(props['battle_time_limit'])

    def _refresh_arena(self):
        _coins, _region = self.read_coins_predicate()
        if _coins == 0:
            _x = _region[0] - 5
            _y = _region[1] + 5
            click(_x, _y)
            self._refill()

        self.awaits([self.E_BUTTON_REFRESH, self.E_TERMINATE])

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
                self.terminated = True
        elif pixels_wait([refill_free], msg='Free refill sacs', mistake=10, timeout=1, wait_limit=2)[0]:
            self.log('Free coins are available')
            click_on_refill()
            refilled = True

        sleep(0.5)

        return refilled

    def _get_last_results(self):
        length = len(self.results)
        if length:
            return self.results[len(self.results) - 1]
        else:
            return self.results

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
                    y = dot[1] + 20
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
                    swipe_new('bottom', 580, 254, self.item_height, speed=.5)
            # @TODO Tag-arena does not work well because of 'max_swipe' value
            elif 0 < i <= self.max_swipe:
                swipe_new('bottom', 580, 254, self.item_height, speed=.5)

        for i in range(len(self.item_locations)):
            if self.terminated:
                break

            el = self.item_locations[i]
            swipes = el['swipes']
            position = el['position']
            inner_swipe(swipes)
            pos = self.button_locations[position]
            x = pos[0]
            y = pos[1]

            def click_on_battle():
                click(x, y, smart=True)
                sleep(1.5)

            def click_on_start():
                click(860, 480, smart=True)
                sleep(0.5)

            # checking - is an enemy already attacked
            is_not_attacked = len(results_local) - 1 < i
            if pixel_check_new([x, y, [187, 130, 5]]) and is_not_attacked:
                self.log(self.name + ' | Attack')
                click_on_battle()

                if self._refill():
                    click_on_battle()

                if self.terminated:
                    self.log('Terminated')
                    break

                # Enables AutoPlay if it's disabled
                enable_start_on_auto()

                click_on_start()

                self.waiting_battle_end_regular(self.name, battle_time_limit=self.battle_time_limit)
                res = not pixel_check_new(defeat, 20)
                results_local.append(res)
                result_name = 'VICTORY' if res else 'DEFEAT'
                self.log(result_name)

                tap_to_continue(times=2)
                sleep(1)
                # tells to skip several teams by swiping
                should_use_multi_swipe = True

        # appends result from attack series into the global results list
        if len(results_local):
            self.results.append(results_local)
            # @TODO Temp commented
            # self.event_dispatcher.publish('update_results')


class ArenaClassic(ArenaFactory):
    def __init__(self, app, props=None):
        ArenaFactory.__init__(
            self,
            app=app,
            name='Arena Classic',
            x_axis_info=95,
            read_coins_predicate=read_bank_arena_classic,
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
            name='Arena Tag',
            x_axis_info=135,
            read_coins_predicate=read_bank_arena_tag,
            item_height=TAG_ITEM_HEIGHT,
            button_locations=TAG_BUTTON_LOCATIONS,
            item_locations=TAG_ITEM_LOCATIONS,
            refill_coordinates=TAG_COINS_REFILL,
            tiers_coordinates=TAG_TIERS_COORDINATE,
            props=props
        )
