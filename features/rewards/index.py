from helpers.common import *
from classes.Feature import Feature

red_dot_region = axis_to_region(170, 170, 790, 360)


def get_button_claim():
    return capture_by_source('images/needles/button_claim.jpg', axis_to_region(670, 150, 750, 520),
                             confidence=.8)


def get_red_dot():
    return find_needle_red_dot(region=red_dot_region, confidence=.7)


RGB_INDICATOR = [225, 0, 0]
# regular quests items pixel coordinates
QUESTS_TABS = [
    {'pixel': {'x': 24, 'y': 84}},
    {'pixel': {'x': 24, 'y': 161}},
    {'pixel': {'x': 24, 'y': 236}},
    {
        'pixel': {
            'x': 24, 'y': 316
        },
        'advanced': {
            'pixels': [
                {'x': 322, 'y': 81},
                {'x': 462, 'y': 81},
                {'x': 603, 'y': 81},
                {'x': 742, 'y': 81},
                {'x': 882, 'y': 81},
            ],
            'rgb': [231, 207, 97]
        }},
]


class Rewards(Feature):
    def __init__(self, app, props=None):
        Feature.__init__(self, name='Rewards', app=app, report_predicate=self._report)

        self.results = {
            'regular_quests': {
                'name': 'Regular Quests',
                'total': 0,
            },
            'play_time': {
                'name': 'Play-Time',
                'total': 0,
            }
        }

        self.event_dispatcher.subscribe('run', self._run)

    def _report(self):
        res_list = []
        t1 = self.results['regular_quests']['total']
        t2 = self.results['play_time']['total']
        total = t1 + t2

        if total > 0:
            res_list.append(f"Obtained: {str(total)}")

        return res_list

    def _run(self, props=None):
        self.quests_run()
        self.play_time_run()
        self.clan_war_rewards()
        self.clan_quests_rewards()

    def quests_obtain(self):
        for i in range(len(QUESTS_TABS)):
            tab = QUESTS_TABS[i]
            x = tab['pixel']['x']
            y = tab['pixel']['y']

            if pixel_check_new([x, y, RGB_INDICATOR], 20) is None:
                continue

            # Weekly quests tab (special case)
            if i == 1:
                # avoid left-panel notification
                y += 55

            click(x, y)
            sleep(0.5)

            button_position = get_button_claim()
            while button_position is not None:
                self.results['regular_quests']['total'] += 1
                x2 = button_position[0]
                y2 = button_position[1]
                pyautogui.moveTo(x2, y2, .5, random_easying())
                sleep(1)
                click(x2, y2)
                sleep(0.5)

                button_position = get_button_claim()

            # Daily, Weekly, Monthly
            all_quests_are_done = pixel_check_old(460, 120, [231, 206, 88], 5)
            can_claim_reward = pixel_check_old(856, 107, [184, 130, 7], 5)
            if all_quests_are_done and can_claim_reward:
                click(856, 107)
                sleep(0.5)

            # Advanced quests tab (special case)
            if i == 3:
                advanced_pixels = tab['advanced']['pixels']
                advanced_rgb = tab['advanced']['rgb']
                for j in range(len(advanced_pixels)):
                    advanced_pixel = advanced_pixels[j]
                    x2 = advanced_pixel['x']
                    y2 = advanced_pixel['y']
                    if pixel_check_old(x2, y2, advanced_rgb, 10):
                        self.results['regular_quests']['total'] += 1
                        # click on a reward
                        click(x2, y2 + 10)
                        sleep(1.5)

    def play_time_obtain(self):
        position = get_red_dot()
        while position is not None:
            self.results['play_time']['total'] += 1
            x = position[0]
            y = position[1]
            click(x, y)
            sleep(.5)
            position = get_red_dot()

    def quests_run(self):
        if is_index_page():
            if pixel_check_new([276, 480, RGB_INDICATOR], mistake=20):
                # enter
                click(276, 480)
                sleep(1)
                # obtain
                self.quests_obtain()
            else:
                self.log('Quests rewards are not available')
        else:
            self.log("Skipped! No Index Page found")

    def play_time_run(self):
        if is_index_page():
            x = 860
            y = 408
            if pixel_check_new([x, y, RGB_INDICATOR], mistake=20):
                # enter
                click(x, y)
                sleep(1)
                # obtain
                self.play_time_obtain()
            else:
                self.log('Play-Time rewards are not available')
        else:
            self.log("Skipped! No Index Page found")

    def clan_war_rewards(self):
        # grabs "clan war" related rewards
        CLAN_WAR_INDEX_DOT = [757, 122, RGB_INDICATOR]
        CLAN_WAR_REWARD_DOT = [402, 128, RGB_INDICATOR]

        close_popup_recursive()

        if await_click([CLAN_WAR_INDEX_DOT], mistake=30, wait_limit=2)[0]:
            await_click([CLAN_WAR_REWARD_DOT], mistake=30, wait_limit=3)

        close_popup_recursive()

    def clan_quests_rewards(self):
        # grabs "clan quests" related rewards
        CLAN_INDEX_DOT = [556, 479, RGB_INDICATOR]
        CLAN_REWARD_MENU_DOT = [152, 302, RGB_INDICATOR]
        CLAN_TABS = [
            [550, 80, RGB_INDICATOR],
            [422, 80, RGB_INDICATOR],
            [292, 80, RGB_INDICATOR],
        ]
        CLAN_BUTTON_COLLECT = [855, 192, [187, 130, 5]]

        close_popup_recursive()

        if await_click([CLAN_INDEX_DOT], mistake=30, wait_limit=2)[0]:
            if await_click([CLAN_REWARD_MENU_DOT], mistake=30, wait_limit=3)[0]:
                for i in range(len(CLAN_TABS)):
                    tab_pixel = CLAN_TABS[i]
                    if pixel_check_new(tab_pixel, mistake=30):
                        x = tab_pixel[0]
                        y = tab_pixel[1]
                        click(x, y)
                        sleep(.5)

                        while pixel_check_new(CLAN_BUTTON_COLLECT, mistake=30):
                            x_collect = CLAN_BUTTON_COLLECT[0]
                            y_collect = CLAN_BUTTON_COLLECT[1]
                            click(x_collect, y_collect)

        close_popup_recursive()
