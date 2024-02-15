from helpers.common import *

TWIN_ATTACKS_LIMIT = 6

# @TODO Refactor is needed
class IronTwins:
    LOCATION_NAME = 'Iron Twins Fortress'
    RESULT_DEFEAT = [450, 40, [178, 23, 38]]

    def __init__(self, props=None):
        self.results = []
        self.completed = False

    def _check_refill(self):
        sleep(1)
        ruby_button = find_needle_refill_ruby()

        if ruby_button is not None:
            self.completed = True

    def _enter_stage(self):
        click(830, 460)
        sleep(.5)

    def enter(self):
        close_popup_recursive()
        sleep(1)

        click_on_progress_info()
        # Fortress Keys
        click(600, 210)
        sleep(1)

        dungeons_scroll()

    def attack(self):
        self._enter_stage()
        self._check_refill()

        self.completed = not dungeons_is_able()

        if not self.completed:

            while self.results.count(True) < TWIN_ATTACKS_LIMIT and not self.completed:
                dungeons_start_battle()

                self._check_refill()
                if self.completed:
                    log('Terminated')
                    break

                waiting_battle_end_regular(self.LOCATION_NAME + ' battle end', x=28, y=88)

                res = not pixel_check_new(self.RESULT_DEFEAT, mistake=10)
                self.results.append(res)

            dungeons_click_stage_select()

    def finish(self):
        dungeons_click_stage_select()
        close_popup_recursive()
        log('DONE - ' + self.LOCATION_NAME)

    def report(self):
        s = None

        if len(self.results):
            s = self.LOCATION_NAME + ' | Completed ' + str(self.results.count(True)) + ' keys in ' + str(
                len(self.results)) + ' attempts '

        return s

    def run(self, props=None):
        if not self.completed:
            self.enter()
            self.attack()
            self.finish()
        else:
            close_popup_recursive()
            log(f'{self.LOCATION_NAME} is Done')
