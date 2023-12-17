from helpers.common import *

TAG_ARENA_MAX_REFILL = 2
STRIKES_LIMIT = 3
ITEM_HEIGHT = 100


def tag_arena(strikes=STRIKES_LIMIT):
    tracker = []
    
    # @TODO Should check TAG_ARENA_MAX_REFILL and actual amount of available battles
    sleep(2)

    def get_canvas():
        return capture_by_source('images/needles/tag_arena_weak_team.jpg', axis_to_region(425, 175, 882, 521),
                                 confidence=.9)

    def enter():
        click_on_progress_info()
        # tag arena
        click(600, 135)
        sleep(1)

    def attack():
        global TAG_ARENA_MAX_REFILL
        for i in range(7):
            team_for_attack = get_canvas()

            # @TODO
            # sleep(.5)
            # click(team_for_attack[0] + 135, team_for_attack[1])
            # break

            while team_for_attack is not None:
                log('Found a team')
                # The battle button is positioned at 135 pixels with an offset to the right
                x = team_for_attack[0] + 135
                y = team_for_attack[1]
                # pyautogui.moveTo(team_for_attack[0] + 135, team_for_attack[1], 1, random_easying())
                click(x, y)
                sleep(0.5)

                should_refill_by_coins = pixel_check_old(439, 395, [255, 38, 46]) and TAG_ARENA_MAX_REFILL > 0
                should_refill_for_free = pixel_check_old(455, 374, [187, 130, 5])
                should_refill = should_refill_by_coins or should_refill_for_free
                if should_refill:
                    click(439, 395)
                    sleep(0.5)
                    if should_refill_by_coins:
                        TAG_ARENA_MAX_REFILL = TAG_ARENA_MAX_REFILL - 1

                # @TODO Might be in the "if" condition same nesting, above
                click(x, y)
                sleep(1)

                click(860, 480)
                waiting_battle_end_regular('Tag Arena Battle end')

                # battle has been failed
                if pixel_check_old(443, 51, [229, 40, 104]):
                    tracker.append(False)
                # battle has been won
                else:
                    tracker.append(True)

                tap_to_continue()
                sleep(2)
                team_for_attack = get_canvas()

            log('No team found in this frame')
            swipe('bottom', 580, 254, ITEM_HEIGHT)

    def finish():
        go_index_page()
        log('DONE - Tag Arena')
        log('Won: ' + str(tracker.count(True)) + ' | Lost: ' + str(tracker.count(False)))

    enter()

    for i in range(strikes):
        refresh_arena()
        attack()

    finish()

    return 0
