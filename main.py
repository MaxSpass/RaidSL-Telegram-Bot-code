import threading
import traceback

import pyautogui
from bot import TelegramBOT
from classes.app import *
from constants.index import IS_DEV

# import asyncio
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

# from in_progress import *

pyautogui.FAILSAFE = False

if not IS_DEV and getattr(sys, 'frozen', False):
    _path = os.path.join(sys._MEIPASS, './vendor/tesseract/tesseract.exe')
    pytesseract.pytesseract.tesseract_cmd = _path
else:
    # @TODO Should be in the env file
    pytesseract.pytesseract.tesseract_cmd = os.path.normpath(r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe')

app = App()

def main():
    # track_mouse_position()
    # return

    # in_progress_determine_quests_text()
    # in_progress_task_iterator()
    # in_progress_find_squares()
    # print(pyautogui.pixel(269, 196))
    # return

    # dungeon_select_difficulty('normal')
    # screenshot = pyautogui.screenshot(region=axis_to_region(810, 93, 866, 115))
    # show_pyautogui_image(screenshot)
    # return

    if IS_DEV or app.validation():
        game_path = app.get_game_path()
        has_telegram_token = 'telegram_token' in app.config
        telegram_bot_thread = None

        try:
            # app.entries['arena_live']['instance'].enter()
            # app.entries['arena_live']['instance'].obtain()

            if app.config['start_immediate']:
                app.start()

            if has_telegram_token:
                telegram_bot = TelegramBOT({
                    'token': app.config['telegram_token']
                })

                # all callbacks should return truthy values in case of success
                if game_path:
                    telegram_bot.add({
                        'command': 'restart',
                        'description': 'Re-Start the Game',
                        'handler': {
                            'callback': lambda upd, ctx: app.restart(),
                        },
                    })
                    telegram_bot.add({
                        'command': 'launch',
                        'description': 'Re-Launch the Game',
                        'handler': {
                            'callback': lambda upd, ctx: app.launch(),
                        },
                    })
                telegram_bot.add({
                    'command': 'relogin',
                    'description': 'Re-log in',
                    'handler': {
                        'callback': lambda upd, ctx: app.relogin(),
                    },
                })
                telegram_bot.add({
                    'command': 'report',
                    'description': 'Report',
                    'handler': {
                        'callback': lambda upd, ctx: app.report(),
                    },
                })
                telegram_bot.add({
                    'command': 'screen',
                    'description': 'Capture and send a screenshot',
                    'handler': {
                        'callback': lambda upd, ctx: ctx.bot.send_photo(
                            chat_id=upd.message.chat_id,
                            photo=app.screen()
                        ) if bool(app.window) else upd.message.reply_text("No Game window found"),
                    },
                })

                # @TODO In progress
                # async def test1(*args, msg='1'):
                #     counter = 0
                #     while counter < 5:
                #         print(msg)
                #         counter += 1
                #         sleep(1)
                #
                # async def test2(*args, msg='2'):
                #     counter = 0
                #     while counter < 5:
                #         print(msg)
                #         counter += 1
                #         sleep(1)

                # async def async_command_1(upd, ctx):
                #     # Your asynchronous code here
                #     await asyncio.sleep(4)
                #     await upd.message.reply_text("Async command executed! 1")
                #
                # async def async_command_2(upd, ctx):
                #     # Your asynchronous code here
                #     await asyncio.sleep(2)
                #     await upd.message.reply_text("Async command executed! 2")

                # telegram_bot.add({
                #     'command': 'test_1',
                #     'description': 'Test 1',
                #     'handler': {
                #         'callback': handler_function_1,
                #     },
                # })
                #
                # telegram_bot.add({
                #     'command': 'test_2',
                #     'description': 'Test 2',
                #     'handler': {
                #         'callback': handler_function_2,
                #     },
                # })

                # telegram_bot.dp.add_handler(CommandHandler('test_1', async_command_1))
                # telegram_bot.dp.add_handler(CommandHandler('test_2', async_command_2))

                # register main commands according to 'tasks'
                regular_command = []
                if len(app.config['tasks']):
                    regular_command = list(map(lambda task: {
                        'command': task['command'],
                        'description': f"command '{task['title']}'",
                        'handler': {
                            'callback': lambda upd, ctx: app.get_entry(
                                command_name=task['command']
                            )['instance'].run(),
                        },
                    }, app.config['tasks']))

                # register addition commands according to 'presets'
                presets_commands = []
                if len(app.config['presets']):
                    presets_commands = list(map(lambda preset: {
                        'command': make_command_key(f"preset {preset['name']}"),
                        'description': f"commands in a row: {', '.join(preset['commands'])}",
                        'handler': {
                            'callback': lambda upd, ctx: list(map(lambda x: app.get_entry(
                                command_name=x
                            )['instance'].run(), preset['commands'])),
                        },
                    }, app.config['presets']))

                commands = regular_command + presets_commands

                for i in range(len(commands)):
                    print(commands[i])
                    telegram_bot.add(commands[i])

                telegram_bot_thread = threading.Thread(target=telegram_bot.run)
                telegram_bot_thread.start()
                telegram_bot.updater.idle()

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
