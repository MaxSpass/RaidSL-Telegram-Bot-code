from classes.app import *

# DEV = True
DEV = False

app = App()

if DEV:
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
        'refill': 1
    }
    app.load_config({
        'tasks': [
            {'name': 'arena_live', 'enable': 0, 'props': ARENA_LIVE_PROPS},
            {'name': 'iron_twins', 'enable': 1},
            {'name': 'arena_classic', 'enable': 0, 'props': {'refill': 0}},
            {'name': 'faction_wars', 'enable': 1},
            {'name': 'arena_tag', 'enable': 0, 'props': {'refill': 0}},
            {'name': 'demon_lord', 'enable': 0},
        ],
        'after_each': [
            {'check_rewards': 1}
        ],
    })


def main():
    if DEV or app.validation():
        try:
            app.start()
            if is_index_page() is True:
                app.run()
            else:
                go_index_page()
                app.run()
        except KeyboardInterrupt:
            return 0
    else:
        log('An App is outdated')


if __name__ == "__main__":
    main()
