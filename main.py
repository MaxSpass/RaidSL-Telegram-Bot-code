from features.live_arena.index import *
from features.arena.index import *
from features.demon_lord.index import *
from features.iron_twins_fortress.index import *
from features.faction_wars.index import *
from features.rewards.index import *
from features.hero_filter.index import *
from features.dungeons.core import *
from helpers.common import *
from constants.index import *
import sys


def prepare():
    WINDOW_SIZE = [920, 540]
    BURGER_POSITION = [15, 282]
    GAME_WINDOW = 'Raid: Shadow Legends'
    is_prepared = False
    wins = pyautogui.getWindowsWithTitle(GAME_WINDOW)
    if len(wins):
        win = wins[0]
        win.activate()
        time.sleep(.5)

        x = 0
        y = 0

        win.resizeTo(WINDOW_SIZE[0], WINDOW_SIZE[1])
        win.moveTo(x, y)
        time.sleep(.5)

        burger = find_needle_burger()
        if burger is not None:
            if burger[0] != BURGER_POSITION[0] or burger[1] != BURGER_POSITION[1]:
                x_burger = burger[0] - BURGER_POSITION[0]
                y_burger = burger[1] - BURGER_POSITION[1]
                x -= x_burger
                y -= y_burger
                win.move(int(x), int(y))
            is_prepared = True
        else:
            log('No Burger needle found')

    else:
        log('No RAID window found')

    if not is_prepared:
        raise Exception("Game windows is NOT prepared")


rewards = Rewards()
hero_filter = HeroFilter()
# @TODO Should be moved to the .env config file
arena_live = ArenaLive(
    pool=[
        'Arbiter',
        'Sun Wukong',
        'Cupidus',
        'Venus',
        'Duchess Lilitu',
    ],
    leaders=[
        'Arbiter',
        'Sun Wukong',
    ],
    # pool=[
    #     'Warlord',
    #     'Sun Wukong',
    #     'Arbiter',
    #     'Trunda',
    #     'Duchess Lilitu',
    # ],
    # leaders=[
    #     'Arbiter',
    #     'Sun Wukong',
    # ],
)


# def flat(arr):
#     return list(itertools.chain.from_iterable(arr))

def start():
    log('Executing automatic scenarios...')
    start_time = datetime.now()

    # demon_lord()
    # arena_live.run()
    # arena_classic.run()
    # arena_tag.run()
    # rewards.quests_run()
    # faction_wars()
    # rewards.play_time_run()
    # iron_twins_fortress()
    # arena_tag.run()

    # DungeonCore(DUNGEON_FIRE, [65], props={
    #     'allow_super_raid': True
    # }).run()

    # arena_live.report()
    # arena_classic.report()
    # arena_tag.report()

    log('All scenarios are done!')
    print('Duration: {}'.format(datetime.now() - start_time))


def main():
    # pyautogui.FAILSAFE = True
    try:
        prepare()
        if is_index_page() is True:
            start()
        else:
            go_index_page()
            start()
    except KeyboardInterrupt:
        sys.exit()


if __name__ == "__main__":
    main()
