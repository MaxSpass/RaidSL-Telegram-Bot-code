from features.live_arena.index import *
from features.arena.index import *
from features.demon_lord.index import *
from features.iron_twins_fortress.index import *
from features.faction_wars.index import *
from features.rewards.index import *
from features.hero_filter.index import *
from features.dungeons.core import *


def prepare():
    prepare_window()
    sleep(.5)


rewards = Rewards()
hero_filter = HeroFilter()
# @TODO Should be moved to the .env config file
arena_live = ArenaLive(
    pool=[
        'Rotos',
        'Sun Wukong',
        'Cupidus',
        'Venus',
        'Duchess Lilitu',
    ],
    leaders=[
        'Sun Wukong',
        'Cupidus',
    ],
)


def start():
    log('Executing automatic scenarios...')
    start_time = datetime.now()

    # arena_live.run()
    # arena_classic.run()
    # arena_tag.run()
    # demon_lord()
    # iron_twins_fortress()
    # rewards.quests_run()
    # faction_wars()
    # rewards.play_time_start()
    #
    # DungeonCore(DUNGEON_MINOTAUR, [2]).run()

    log('All scenarios are done!')
    print('Duration: {}'.format(datetime.now() - start_time))


def main():
    pyautogui.FAILSAFE = True
    prepare()

    if is_index_page() is True:
        start()
    else:
        go_index_page()
        start()




if __name__ == "__main__":
    main()
