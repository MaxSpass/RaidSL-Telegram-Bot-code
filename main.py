from classes.app import *

DEBUG = True

app = App()

if DEBUG:
    app.load_config({
        'check_rewards': 1,
        'tasks': [
            {
                'name': 'arena_live',
                'enable': 0,
                'props': {
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
                },
            },
            {'name': 'iron_twins', 'enable': 1},
            {'name': 'arena_classic', 'enable': 1},
            {'name': 'arena_tag', 'enable': 1},
            {'name': 'faction_wars', 'enable': 0},
            {'name': 'demon_lord', 'enable': 0},
        ]
    })

def main():
    return
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
