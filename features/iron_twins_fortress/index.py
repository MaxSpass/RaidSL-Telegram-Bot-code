from helpers.common import *

TWIN_KEYS_LIMIT = 6

# @TODO Refactor is needed
class IronTwins:
    LOCATION_NAME = 'Iron Twins Fortress'
    RESULT_DEFEAT = [450, 40, [178, 23, 38]]

    def __init__(self, props=None):
        self.results = []
        self.terminate = False
        self.completed = False

        self.keys = TWIN_KEYS_LIMIT

        self._apply_props(props=props)

    def _check_refill(self):
        sleep(1)
        ruby_button = find_needle_refill_ruby()

        if ruby_button is not None:
            # self.completed = True
            self.terminate = True
            close_popup()

    def _enter_stage(self):
        click(830, 460)
        sleep(.5)

    def _is_available(self):
        return self.results.count(True) < self.keys or dungeons_is_able()

    def _apply_props(self, props=None):
        if props:
            if 'keys' in props:
                self.keys = int(props['keys'])


    def enter(self):
        close_popup_recursive()
        sleep(1)

        click_on_progress_info()
        # Fortress Keys
        click(600, 210)
        sleep(1)

        dungeons_scroll()
        self._enter_stage()

    def attack(self):
        self._check_refill()
        if self.terminate:
            log('Terminated')
            return

        while self._is_available():
            dungeons_start_battle()

            self._check_refill()
            if self.terminate:
                log('Terminated')
                break

            waiting_battle_end_regular(self.LOCATION_NAME + ' battle end', x=28, y=88)

            res = not pixel_check_new(self.RESULT_DEFEAT, mistake=10)
            self.results.append(res)
            self.completed = self.results.count(True) >= self.keys

        # @TODO Test
        # if not self.terminate:
        #     dungeons_click_stage_select()

    def finish(self):
        dungeons_click_stage_select()
        close_popup_recursive()

        if self.completed:
            log(f"{self.LOCATION_NAME} | Done")
        elif self.terminate:
            log(f"{self.LOCATION_NAME} | Terminated")

    def report(self):
        s = None

        if len(self.results):
            s = self.LOCATION_NAME + ' | Completed ' + str(self.results.count(True)) + ' keys in ' + str(
                len(self.results)) + ' attempts '

        return s

    def run(self, *args, props=None):
        self.terminate = False

        self._apply_props(props=props)

        if not self.completed:
            self.enter()
            self.attack()
            self.finish()
        else:
            close_popup_recursive()
            log(f'{self.LOCATION_NAME} is already completed')
