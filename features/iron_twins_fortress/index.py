from helpers.common import *

# twin fortress
TWIN_ATTACKS_LIMIT = 6

defeat = [443, 51, [229, 40, 104]]

# @TODO Checking first battle
class IronTwins:
    LOCATION_NAME = 'Iron Twins Fortress'

    def __init__(self):
        self.results = {
            'runs': TWIN_ATTACKS_LIMIT,
            'attempts': [],
        }

    def enter(self):
        go_index_page()

        click_on_progress_info()
        # Fortress Keys
        click(600, 210)
        sleep(1)

        dungeons_scroll()

    def attack(self):
        attack_limit = self.results['runs']
        click(830, 460)
        sleep(.5)

        while attack_limit > 0:
            if attack_limit == self.results['runs']:
                # starts first battle
                click(830, 460)
                sleep(.5)
            else:
                # repeat all subsequent battles
                dungeons_replay()

            waiting_battle_end_regular(self.LOCATION_NAME, x=28, y=88)

            res = not pixel_check_new(defeat)
            self.results['attempts'].append(res)
            if res:
                attack_limit -= 1

    def finish(self):
        dungeons_results_finish()
        go_index_page()
        log('DONE - ' + self.LOCATION_NAME)

    def report(self):
        attempts = self.results['attempts']
        s = None

        if len(attempts):
            s = self.LOCATION_NAME + ' | Completed ' + str(attempts.count(True)) + ' keys in ' + str(
                len(attempts)) + ' attempts '

        return s

    def run(self):
        self.enter()
        self.attack()
        self.finish()
