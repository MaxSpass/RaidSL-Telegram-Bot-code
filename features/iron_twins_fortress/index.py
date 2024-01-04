from helpers.common import *

# twin fortress
TWIN_ATTACKS_LIMIT = 6

defeat = [443, 51, [229, 40, 104]]


# @TODO Must be reworked by following new standard
def iron_twins_fortress():
    tracker = []

    def enter():
        go_index_page()

        battles_click()
        sleep(0.5)
        # click on dungeons
        click(306, 290)
        sleep(0.5)
        # click on iron twins fortress
        click(280, 235)
        sleep(0.5)
        dungeons_scroll()

    # @TODO Refactor
    def attack():
        attack_limit = TWIN_ATTACKS_LIMIT
        click(830, 460)
        sleep(.5)

        while attack_limit > 0:
            if attack_limit == TWIN_ATTACKS_LIMIT:
                # starts first battle
                click(830, 460)
                sleep(.5)
            else:
                # repeat all subsequent battles
                dungeons_replay()

            waiting_battle_end_regular('Iron Twins Fortress', x=28, y=88)

            res = not pixel_check_new(defeat)
            tracker.append(res)
            if res:
                attack_limit -= 1

    def finish():
        dungeons_results_finish()
        go_index_page()
        log('DONE - Iron Twins')
        log('Used ' + str(tracker.count(True)) + ' keys in ' + str(len(tracker)) + ' attempts')

    enter()
    attack()
    finish()
