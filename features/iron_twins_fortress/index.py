from helpers.common import *

# twin fortress
TWIN_ATTACKS_LIMIT = 6

defeat = [443, 51, [229, 40, 104]]

# @TODO Checking first battle
class IronTwins:
    LOCATION_NAME = 'Iron Twins Fortress'

    def __init__(self, props=None):
        self.results = {
            'runs': TWIN_ATTACKS_LIMIT,
            'attempts': [],
        }
        self.completed = False

    def _check_refill(self):
        sleep(1)
        ruby_button = find_needle_refill_ruby()

        if ruby_button is not None:
            self.completed = True


    def enter(self):
        go_index_page()
        sleep(1)
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

        self._check_refill()

        while attack_limit > 0 and not self.completed:
            if attack_limit == self.results['runs']:
                # starts first battle
                click(830, 460)
                sleep(.5)
            else:
                # repeat all subsequent battles
                dungeons_replay()

            self._check_refill()

            if self.completed:
                log('terminate')
                break

            waiting_battle_end_regular(self.LOCATION_NAME + ' battle end', x=28, y=88)

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

    def run(self, props=None):
        if not self.completed:
            self.enter()
            self.attack()
            self.finish()
        else:
            go_index_page()
            log(f'{self.LOCATION_NAME} is Done')
