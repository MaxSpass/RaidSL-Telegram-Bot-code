from helpers.common import *

POSITIONS = {
    1: (855, 200),
    2: (855, 295),
    3: (855, 380),
    4: (855, 465),
}
ITEM_HEIGHT = 92
# all swipes calculated based on item height: 92
DICTIONARY_MAP = [
    {
        'swipes': 0,
        'position': 1,
    },
    {
        'swipes': 1,
        'position': 1,
    },
    {
        'swipes': 2,
        'position': 1,
    },
    {
        'swipes': 3,
        'position': 1,
    },
    {
        'swipes': 4,
        'position': 1,
    },
    {
        'swipes': 5,
        'position': 1,
    },
    {
        'swipes': 6,
        'position': 1,
    },
    {
        'swipes': 6,
        'position': 2,
    },
    {
        'swipes': 6,
        'position': 3,
    },
    {
        'swipes': 6,
        'position': 4,
    },
]
STRIKES_LIMIT = 2

# @TODO Refactor, make possible avoid refreshing before each launch
def classic_arena(strikes=STRIKES_LIMIT):
    tracker = []

    def enter():
        click_on_progress_info()
        # classic arena
        click(600, 95)
        sleep(1)

    def attack():
        tracker_local = []
        should_use_multi_swipe = False

        for i in range(len(DICTIONARY_MAP)):
            el = DICTIONARY_MAP[i]
            swipes = el['swipes']
            position = el['position']

            # @TOD Not tested
            def inner_swipe():
                if should_use_multi_swipe:
                    for j in range(swipes):
                        swipe('bottom', 580, 254, ITEM_HEIGHT)
                elif 0 < i < 7:
                    swipe('bottom', 580, 254, ITEM_HEIGHT)

            inner_swipe()

            # pyautogui.moveTo(x, y, 1)

            pos = POSITIONS[position]
            x = pos[0]
            y = pos[1]

            # checking - is an enemy already attacked
            is_not_attacked = len(tracker_local) - 1 < i
            if pixel_check_old(x, y, [187, 130, 5]) and is_not_attacked:
                print('Attacking Classic Arena battle')
                # pyautogui.moveTo(x, y, 1)
                # continue
                click(x, y)
                sleep(0.5)

                # @TODO Should add should_refill_by_coins
                should_refill_for_free = pixel_check_old(455, 380, [187, 130, 5])
                should_refill = should_refill_for_free
                if should_refill:
                    click(439, 395)
                    sleep(0.5)
                    click(x, y)
                    sleep(0.5)
                    # if should_refill_by_coins:
                    #     TAG_ARENA_MAX_REFILL = TAG_ARENA_MAX_REFILL - 1
                    inner_swipe()

                click(860, 480)
                sleep(0.5)
                waiting_battle_end_regular('Classic Arena battle end')

                # battle has been failed
                if pixel_check_old(443, 51, [229, 40, 104], 5):
                    tracker_local.append(False)
                # battle has been won
                else:
                    tracker_local.append(True)

                tap_to_continue()
                sleep(1)
                # tells to skip several teams by swiping
                should_use_multi_swipe = True

                for j in range(len(tracker_local)):
                    tracker.append(tracker_local[j])

    def finish():
        go_index_page()
        log('DONE - Classic Arena')
        log('Won: ' + str(tracker.count(True)) + ' | Lost: ' + str(tracker.count(False)))

    enter()

    for i in range(strikes):
        # @TODO Reconsider
        # refresh_arena()
        attack()

    finish()
