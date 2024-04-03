import threading
import traceback

import pyautogui
from bot import TelegramBOT
from classes.app import *
from constants.index import IS_DEV

# from telegram.ext import CommandHandler
# import pyautogui
# import os.path
# import pyautogui
# import sys
# import random
# import pytesseract
# from PIL import Image
# from io import BytesIO
# from features.faction_wars.index import *
# from features.hero_preset.index import HeroPreset
# from features.doom_tower.index import *
# from classes.task_iterator import TaskIterator
# from features.quests.index import *
# from in_progress import *

pyautogui.FAILSAFE = False

if not IS_DEV and getattr(sys, 'frozen', False):
    _path = os.path.join(sys._MEIPASS, './vendor/tesseract/tesseract.exe')
    pytesseract.pytesseract.tesseract_cmd = _path
else:
    # @TODO Should be in the env file
    pytesseract.pytesseract.tesseract_cmd = os.path.normpath(r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe')

# quests = Quests()

def main():
    app = App()

    # def test(*args):
    #     msg = 'Test'
    #     counter = 0
    #     while counter < 3:
    #         print(f'{msg}: {counter}')
    #         counter += 1
    #         sleep(1)
    # def screen_test():
    #     screenshot = pyautogui.screenshot(region=[0, 0, 500, 500])
    #
    #     # Convert the screenshot to bytes
    #     image_bytes = BytesIO()
    #     screenshot.save(image_bytes, format='PNG')
    #     image_bytes.seek(0)
    #
    #     return image_bytes
    # telegram_bot = TelegramBOT({
    #     'token': app.config['telegram_token']
    # })
    # telegram_bot.start()
    # telegram_bot.add({
    #     'command': 'screen',
    #     'description': 'Capture and send a screenshot',
    #     'handler': {
    #         'type': 'async',
    #         'callback': lambda upd, ctx: ctx.bot.send_photo(
    #             chat_id=upd.message.chat_id,
    #             photo=screen_test()
    #         ),
    #     },
    # })
    # telegram_bot.add({
    #     'command': 'test',
    #     'handler': {
    #         'callback': lambda upd, ctx: app.queue.put(test)
    #     }
    # })
    # telegram_bot.listen()
    # telegram_bot.join()
    # return

    if IS_DEV or app.validation():
        game_path = app.get_game_path()
        has_telegram_token = 'telegram_token' in app.config
        telegram_bot = None

        try:
            # app.entries['arena_live']['instance'].enter()
            # app.entries['arena_live']['instance'].obtain()

            if app.config['start_immediate']:
                app.start_game()

            if has_telegram_token:
                telegram_bot = TelegramBOT({
                    'token': app.config['telegram_token']
                })
                telegram_bot.start()

                # all callbacks should return truthy values in case of success
                if game_path:
                    telegram_bot.add({
                        'command': 'restart',
                        'description': 'Re-Start the Game',
                        'handler': {
                            'callback': lambda upd, ctx: app.queue.put(app.restart),
                        },
                    })
                    telegram_bot.add({
                        'command': 'launch',
                        'description': 'Re-Launch the Game',
                        'handler': {
                            'callback': lambda upd, ctx: app.queue.put(app.launch),
                        },
                    })
                telegram_bot.add({
                    'command': 'relogin',
                    'description': 'Re-log in',
                    'handler': {
                        'callback': lambda upd, ctx: app.queue.put(app.relogin),
                    },
                })

                # Async
                telegram_bot.add({
                    'command': 'report',
                    'description': 'Report',
                    'handler': {
                        'type': 'async',
                        'callback': lambda upd, ctx: app.report(),
                    },
                })
                # Async
                telegram_bot.add({
                    'command': 'screen',
                    'description': 'Capture and send a screenshot',
                    'handler': {
                        'type': 'async',
                        'callback': lambda upd, ctx: ctx.bot.send_photo(
                            chat_id=upd.message.chat_id,
                            photo=app.screen()
                        ) if bool(app.window) else upd.message.reply_text("No Game window found"),
                    },
                })

                # register main commands according to 'tasks'
                regular_command = []
                if len(app.config['tasks']):
                    regular_command = list(map(lambda task: {
                        'command': task['command'],
                        'description': f"command '{task['title']}'",
                        'handler': {
                            'callback': lambda upd, ctx: app.queue.put(app.get_entry(
                                command_name=task['command']
                            )['instance'].run),
                        },
                    }, app.config['tasks']))

                # register addition commands according to 'presets'
                presets_commands = []
                if len(app.config['presets']):
                    presets_commands = list(map(lambda preset: {
                        'command': make_command_key(f"preset {preset['name']}"),
                        'description': f"commands in a row: {', '.join(preset['commands'])}",
                        'handler': {
                            'callback': lambda upd, ctx: app.queue.put(lambda: list(map(lambda x: app.get_entry(
                                command_name=x
                            )['instance'].run(), preset['commands']))),
                        },
                    }, app.config['presets']))

                commands = regular_command + presets_commands

                for i in range(len(commands)):
                    print(commands[i])
                    telegram_bot.add(commands[i])

                telegram_bot.listen()

        except KeyboardInterrupt:
            error = traceback.format_exc()
            log_save(error)
        except Exception:
            error = traceback.format_exc()
            log_save(error)
        finally:
            log('All tasks are done')

            if has_telegram_token and telegram_bot:
                # Wait for the bot thread to finish
                telegram_bot.join()
    else:
        log_save('An App is outdated')


if __name__ == '__main__':
    main()
