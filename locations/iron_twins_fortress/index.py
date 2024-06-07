from helpers.common import *
from classes.Location import Location

TWIN_KEYS_LIMIT = 6

# @TODO Refactor is needed
class IronTwins(Location):
    RESULT_DEFEAT = [450, 40, [178, 23, 38]]

    def __init__(self, app, props=None):
        Location.__init__(self, name='Iron Twins Fortress', app=app, report_predicate=self._report)

        self.results = []
        self.keys = TWIN_KEYS_LIMIT

        self._apply_props(props=props)

        self.event_dispatcher.subscribe('enter', self._enter)
        self.event_dispatcher.subscribe('run', self._run)

    def _report(self):
        res_list = []

        if len(self.results):
            res_list.append(f"Used: {str(self.results.count(True))} keys")
            res_list.append(f"Attempts: {str(len(self.results))} keys")

        return res_list

    def _enter(self):
        click_on_progress_info()
        # Fortress Keys
        click(600, 210)
        sleep(1)

        dungeons_scroll()

        # Enter the stage
        click(830, 460)
        sleep(.5)

    def _run(self, props=None):
        self._apply_props(props=props)
        self.attack()

    def _check_refill(self):
        sleep(1)
        ruby_button = find_needle_refill_ruby()

        if ruby_button is not None:
            # self.completed = True
            self.terminate = True
            self.completed = True
            close_popup()

    def _is_available(self):
        return self.results.count(True) < self.keys or dungeons_is_able()

    def _apply_props(self, props=None):
        if props:
            if 'keys' in props:
                self.keys = int(props['keys'])

    def attack(self):
        self._check_refill()
        if self.terminate:
            self.log('Terminated')
            return

        while self._is_available():
            dungeons_start_battle()

            self._check_refill()
            if self.terminate:
                self.log('Terminated')
                break

            self.waiting_battle_end_regular(self.NAME)

            res = not pixel_check_new(self.RESULT_DEFEAT, mistake=10)
            self.results.append(res)
            self.completed = self.results.count(True) >= self.keys

        # @TODO Test
        if not self.terminate:
            dungeons_click_stage_select()
