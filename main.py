from classes.app import *

# DEBUG = True
DEBUG = False

app = App()

if DEBUG:
    ARENA_LIVE_PROPS = {
        'pool': [
            'Arbiter',
            'Sun Wukong',
            'Cupidus',
            'Venus',
            'Duchess Lilitu',
        ],
        'leaders': [
            'Arbiter',
            'Sun Wukong',
        ],
        'refill': 0
    }
    app.load_config({
        'tasks': [
            {'name': 'arena_live', 'enable': 0, 'props': ARENA_LIVE_PROPS},
            {'name': 'arena_classic', 'enable': 1, 'props': {'refill': 0}},
            {'name': 'arena_tag', 'enable': 1, 'props': {'refill': 0}},
            {'name': 'iron_twins', 'enable': 0},
            {'name': 'faction_wars', 'enable': 0},
            {'name': 'demon_lord', 'enable': 0},
        ],
        'after_each': [
            {'check_rewards': 1}
        ],
    })


def main():
    try:
        app.start()
        if is_index_page() is True:
            app.run()
        else:
            go_index_page()
            app.run()
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    main()
