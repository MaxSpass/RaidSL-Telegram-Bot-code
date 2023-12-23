from helpers.common import *


def get_button_claim():
    return capture_by_source('images/needles/button_claim.jpg', axis_to_region(670, 150, 750, 520),
                             confidence=.8)


def get_red_dot():
    return capture_by_source('images/needles/red_dot.jpg', axis_to_region(170, 170, 790, 360),
                             confidence=.7)


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


class Rewards:
    cache = {
        'regular_quests': {
            'name': 'Regular Quests',
            'total': 0,
        },
        'play_time': {
            'name': 'Play-Time',
            'total': 0,
        }
    }

    def finish(self, quest_type):
        go_index_page()
        name = self.cache[quest_type]['name']
        total = self.cache[quest_type]['total']
        log('DONE - ' + name + ' rewards')
        log('Total ' + name + ' rewards obtained: ' + str(total))

    def quests_obtain(self):
        for i in range(len(QUESTS_TABS)):
            # log(i)
            # continue
            tab = QUESTS_TABS[i]
            x = tab['pixel']['x']
            y = tab['pixel']['y']

            if pixel_check_old(x, y, [225, 0, 0], 10) is None:
                continue

            # Weekly quests tab (special case)
            if i == 1:
                # avoid left-panel notification
                y += 55

            click(x, y)
            sleep(0.5)

            button_position = get_button_claim()
            while button_position is not None:
                self.cache['regular_quests']['total'] += 1
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
                        self.cache['regular_quests']['total'] += 1
                        # click on a reward
                        click(x2, y2 + 10)
                        sleep(1.5)

    def play_time_obtain(self):
        position = get_red_dot()
        while position is not None:
            self.cache['play_time']['total'] += 1
            x = position[0]
            y = position[1]
            click(x, y)
            sleep(.5)
            position = get_red_dot()

    def quests_run(self):
        if is_index_page():
            if pixel_check_old(276, 480, [225, 0, 0], 5):
                # enter
                click(276, 480)
                sleep(1)
                # obtain
                self.quests_obtain()
                # finish and log output
                self.finish('regular_quests')
            else:
                log('Quests rewards are not available')
        else:
            log("Skipped! No Index Page found")

    def play_time_run(self):
        if is_index_page():
            x = 860
            y = 408
            # @TODO Needs to be tested
            if pixel_check_old(x, y, [225, 0, 0], 20):
                # enter
                click(x, y)
                sleep(1)
                # obtain
                self.play_time_obtain()
                # finish and log output
                self.finish('play_time')
            else:
                log('Play-Time rewards are not available')
        else:
            log("Skipped! No Index Page found")
