from helpers.common import *

# demon lord | levels for attack
DEFAULT_STAGES = [6, 5]
# demon lord | clicking areas for obtaining rewards
DEMON_LORD_REWARD_COORDINATES = {
    3: (580, 120),
    4: (580, 200),
    5: (580, 300),
    6: (580, 380),
}

# @TODO Refactor
class DemonLord:
    def __init__(self, props=None):
        self.results = {
            'obtained': [],
            'attacked': []
        }
        self.stages = DEFAULT_STAGES
        self.terminate = False
        self.completed = False

        if props is not None:
            if 'stages' in props:
                self.stages = props['stages']

    def _check_refill(self):
        sleep(1)
        ruby_button = find_needle_refill_ruby()

        if ruby_button is not None:
            self.terminate = True

    def enter(self):
        go_index_page()
        sleep(1)
        go_index_page()

        # moving to the Demon Lord
        # click on the red button "Battles"
        battles_click()
        sleep(1)
        # click on the clan boss
        click(890, 300)
        sleep(1)
        # click on the Demon Lord
        click(320, 290)
        sleep(1)

        # swapping to the bottom @TODO
        pyautogui.moveTo(580, 400, 1)
        pyautogui.dragTo(580, 120, duration=1)
        sleep(2)

    def obtain(self):
        global DEFAULT_STAGES
        global DEMON_LORD_REWARD_COORDINATES
        # obtain rewards
        for lvl in DEMON_LORD_REWARD_COORDINATES:
            x = DEMON_LORD_REWARD_COORDINATES[lvl][0]
            y = DEMON_LORD_REWARD_COORDINATES[lvl][1]
            click(x, y)
            sleep(0.5)
            stage = str(lvl)
            if pixel_check_new([870, 457, [246, 2, 0]], mistake=10):
                # click on the "Claim reward button"
                click(870, 457)

                # click on the "Obtain reward button" twice
                for i in range(2):
                    sleep(5)
                    click(460, 444)
                    sleep(5)

                log('Obtained reward from Demon Lord ' + stage)
                self.results['obtained'].append(stage)
            else:
                log('No reward found from Demon Lord ' + stage)
            sleep(2)

    def attack(self):
        global DEMON_LORD_REWARD_COORDINATES
        # attack
        while len(self.stages) and not self.terminate:
            # zero-indexed Demon Lord level is always next
            stage = self.stages[0]
            x = DEMON_LORD_REWARD_COORDINATES[stage][0]
            y = DEMON_LORD_REWARD_COORDINATES[stage][1]

            # click on the certain demon lord
            click(x, y)
            sleep(.5)

            # click on battle
            click(860, 480)
            sleep(.5)

            # terminates the loop
            self._check_refill()
            if self.terminate:
                break

            # click on start
            click(860, 480)
            if pixel_wait('End of the battle with Demon Lord: ' + str(stage) + ' level', 20, 112, [255, 255, 255], 3):
                # return to the demon lord menu
                click(420, 490)
                close_popup()
                sleep(2)
                # removing already attacked Demon Lord from the array
                self.stages.remove(stage)
                self.results['attacked'].append(str(stage))

    def finish(self):
        go_index_page()
        log('DONE - Demon Lord')

    def report(self):
        s = None
        has_obtained = len(self.results['obtained'])
        has_attacked = len(self.results['attacked'])

        if has_obtained or has_attacked:
            s = 'Demon Lord'
            if has_obtained:
                s += ' | Obtained: ' + ','.join(self.results['obtained'])
            if has_attacked:
                s += ' | Attacked: ' + ','.join(self.results['attacked'])

        return s

    def run(self, props=None):
        self.terminate = False

        self.enter()
        self.obtain()
        self.attack()
        self.finish()
