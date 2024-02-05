import pyautogui
import sys
import random
import traceback
import pytesseract
import threading
from classes.app import *
from constants.index import IS_DEV
from bot import TelegramBOT

app = App()

if not IS_DEV and getattr(sys, 'frozen', False):
    _path = os.path.join(sys._MEIPASS, './vendor/tesseract/tesseract.exe')
    pytesseract.pytesseract.tesseract_cmd = _path
else:
    # @TODO Should be in the env file
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

if IS_DEV:
    ARENA_LIVE_PROPS = {
        'pool': [
            {'name': 'Arbiter', 'role': 's', 'priority': 1},
            {'name': 'Sun Wukong', 'role': 'a', 'priority': 1},
            {'name': 'Duchess Lilitu', 'role': 's', 'priority': 1},
            {'name': 'Cupidus', 'role': 'a', 'priority': 1},
            {'name': 'Venus', 'role': 's', 'priority': 1},
            {'name': 'Leorius the Proud', 'role': 'a'},
            {'name': 'Rotos', 'role': 'a'},
            {'name': 'Mortu-Macaab', 'role': 'a'},
            {'name': 'Ramantu Drakesblood', 'role': 'a'},
            {'name': 'Candraphon', 'role': 'a'},
            {'name': 'Lady Mikage', 'role': 's'},
            {'name': 'Pythion', 'role': 's'},
            {'name': 'Maulie Tankard', 'role': 's'},
            {'name': 'Lydia the Deathsiren', 'role': 's'},
            {'name': 'Mighty Ukko', 'role': 's'},
        ],
        'leaders': [
            'Arbiter',
            'Sun Wukong',
            'Mortu-Macaab',
            'Duchess Lilitu',
            'Mighty Ukko',
            'Lydia the Deathsiren',
            'Pythion',
        ],
        'refill': 1
    }
    HYDRA_PROPS = {
        'runs_limit': 2,
        'runs': [
            {
                'stage': 4,
                'team_preset': 1,
                'min_damage': 170,
                'skip': 0
            },
            {
                'stage': 3,
                'team_preset': 4,
                'min_damage': 50,
                'skip': 0
            },
            {
                'stage': 1,
                'team_preset': 3,
                'min_damage': 200,
                'skip': 0
            },
        ],
    }
    DUNGEON_PROPS = {
        "bank": False,
        "refill": False,
        "super_raid": False,
        "locations": [
            {"id": 6, "energy": 40},
            {"id": 3, "energy": 40},
        ]
    }

    app.load_config({
        'tasks': [
            {'name': 'dungeon', 'enable': 1, 'props': DUNGEON_PROPS},
            {'name': 'arena_live', 'enable': 1, 'props': ARENA_LIVE_PROPS},
            {'name': 'hydra', 'enable': 1, 'props': HYDRA_PROPS},
            {'name': 'iron_twins', 'enable': 0},
            {'name': 'faction_wars', 'enable': 0},
            {'name': 'arena_classic', 'enable': 0, 'props': {'refill': 0}},
            {'name': 'arena_tag', 'enable': 0, 'props': {'refill': 0}},
            {'name': 'demon_lord', 'enable': 0},
        ],
        'after_each': [
            {'check_rewards': 1}
        ],
    })


def main():
    if IS_DEV or app.validation():
        has_telegram_token = 'telegram_token' in app.config
        telegram_bot_thread = None

        try:
            if has_telegram_token:
                telegram_bot = TelegramBOT({
                    'token': app.config['telegram_token']
                })

                # all callbacks should return truthy values in case of success
                telegram_bot.add({
                    'name': 'report',
                    'description': 'Report',
                    'handler': {
                        'callback': lambda upd, ctx: app.report(),
                    },
                })
                telegram_bot.add({
                    'name': 'run',
                    'description': 'Runs all tasks again',
                    'handler': {
                        'callback': lambda upd, ctx: app.run(),
                    },
                })
                telegram_bot.add({
                    'name': 'relogin',
                    'description': 'Re-log in',
                    'handler': {
                        'callback': lambda upd, ctx: app.relogin(),
                    },
                })
                telegram_bot.add({
                    'name': 'screen',
                    'description': 'Capture and send a screenshot',
                    'handler': {
                        'callback': lambda upd, ctx: ctx.bot.send_photo(
                            chat_id=upd.message.chat_id,
                            photo=app.screen()
                        ),
                    },
                })

                # def test_cb(msg, length=5):
                #     for k in range(length):
                #         print(msg)
                #         sleep(.5)
                #
                #     return 'Done'
                #
                # test_commands = [
                #     {'name': 'test_1', 'description': 'description_1', 'handler': {
                #         'callback': lambda *args: test_cb('1'),
                #     }},
                #     {'name': 'test_2', 'description': 'description_2', 'handler': {
                #         'callback': lambda *args: test_cb('2'),
                #     }},
                #     {'name': 'test_3', 'description': 'description_3', 'handler': {
                #         'callback': lambda *args: test_cb('3'),
                #     }},
                # ]
                # for i in range(len(test_commands)):
                #     telegram_bot.add(test_commands[i])

                commands = list(map(lambda command: {
                    'name': command['name'],
                    'description': f"Runs '{command['name']}' task",
                    'handler': {
                        'callback': lambda upd, ctx: app.get_entry(
                            entry_name=command['name'], prepare=True
                        )['instance'].run(),
                    },
                }, app.config['tasks']))

                for i in range(len(commands)):
                    telegram_bot.add(commands[i])

                telegram_bot_thread = threading.Thread(target=telegram_bot.run)
                telegram_bot_thread.start()
                telegram_bot.updater.idle()


            app.start()
            # go_index_page()
            if app.config['start_immediate']:
                app.run()
        except KeyboardInterrupt:
            error = traceback.format_exc()
            log_save(error)
        except Exception:
            error = traceback.format_exc()
            log_save(error)
        finally:
            log('All tasks are done')

            if has_telegram_token and telegram_bot_thread:
                # Wait for the bot thread to finish
                telegram_bot_thread.join()
    else:
        log_save('An App is outdated')


if __name__ == '__main__':
    main()
