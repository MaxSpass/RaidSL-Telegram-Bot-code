import traceback
import threading
from classes.app import *
from constants.index import IS_DEV
from bot import TelegramBOT
# import pyautogui
# import os.path
# import pyautogui
# import sys
# import random
# import pytesseract
# from PIL import Image
# from io import BytesIO
# from features.faction_wars.index import *

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

    if IS_DEV or app.validation():
        app.start()
        app.prepare()

        if app.config['start_immediate']:
            app.run()

        has_telegram_token = 'telegram_token' in app.config
        telegram_bot_thread = None

        try:
            if has_telegram_token:
                telegram_bot = TelegramBOT({
                    'token': app.config['telegram_token']
                })

                # all callbacks should return truthy values in case of success
                telegram_bot.add({
                    'command': 'report',
                    'description': 'Report',
                    'handler': {
                        'callback': lambda upd, ctx: app.report(),
                    },
                })
                telegram_bot.add({
                    'command': 'prepare',
                    'description': 'Prepare the window',
                    'handler': {
                        'callback': lambda upd, ctx: app.prepare(),
                    },
                })
                telegram_bot.add({
                    'command': 'run',
                    'description': 'Runs all tasks again',
                    'handler': {
                        'callback': lambda upd, ctx: app.run(),
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
                    'command': 'screen',
                    'description': 'Capture and send a screenshot',
                    'handler': {
                        'callback': lambda upd, ctx: ctx.bot.send_photo(
                            chat_id=upd.message.chat_id,
                            photo=app.screen()
                        ),
                    },
                })

                commands = list(map(lambda task: {
                    'command': task['command'],
                    'description': f"Command '{task['title']}'",
                    'handler': {
                        'callback': lambda upd, ctx: app.get_entry(
                            command_name=task['command']
                        )['instance'].run(),
                    },
                }, app.config['tasks']))

                for i in range(len(commands)):
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
