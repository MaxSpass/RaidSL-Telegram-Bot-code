import traceback
import pyautogui
from bot import TelegramBOT
from classes.App import *
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
# from features.quests.index import *
# from in_progress import *

pyautogui.FAILSAFE = False

if not IS_DEV and getattr(sys, 'frozen', False):
    _path = os.path.join(sys._MEIPASS, './vendor/tesseract/tesseract.exe')
    pytesseract.pytesseract.tesseract_cmd = _path
else:
    # @TODO Should be in the env file
    pytesseract.pytesseract.tesseract_cmd = os.path.normpath(r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe')

def main():
    # print(str(np.array([1,2,3], dtype=object)))
    # return

    # for i in range(2):
    #     swipe('bottom', 450, 490, 340, speed=3)
    # return

    # print(pyautogui.pixel(220, 90))
    # return

    # quests = Quests()
    # quests.handle_quest('1')
    # return

    app = App()

    if IS_DEV or app.validation():
        game_path = app.get_game_path()
        has_telegram_token = 'telegram_token' in app.config
        telegram_bot = None

        try:
            quests = app.entries['daily_quests']['instance']
            arena_classic = app.entries['arena_classic']['instance']

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
                        'handler': app.task(name='restart', cb=app.restart),
                    })
                    telegram_bot.add({
                        'command': 'launch',
                        'description': 'Re-Launch the Game',
                        'handler': app.task(name='launch', cb=app.launch),
                    })
                telegram_bot.add({
                    'command': 'relogin',
                    'description': 'Re-log in',
                    'handler': app.task(name='relogin', cb=app.relogin),
                })

                # Sync
                telegram_bot.add({
                    'command': 'report',
                    'description': 'Report',
                    'handler': app.task(
                        name='report',
                        cb=app.report,
                        task_type='sync'
                    ),
                })
                # Sync
                telegram_bot.add({
                    'command': 'screen',
                    'description': 'Capture and send a screenshot',
                    'handler': app.task(
                        name='screen',
                        cb=lambda upd, ctx: ctx.bot.send_photo(
                            chat_id=upd.message.chat_id,
                            photo=app.screen()
                        ) if bool(app.window) else upd.message.reply_text("No Game window found"),
                        task_type='sync'
                    ),
                })

                # register main commands according to 'tasks'
                regular_command = []
                if len(app.config['tasks']):
                    regular_command = list(map(lambda task: {
                        'command': task['command'],
                        'description': f"command '{task['title']}'",
                        'handler': app.task(
                            name=task['command'],
                            cb=app.get_entry(command_name=task['command'])['instance'].run
                        ),
                    }, app.config['tasks']))

                # TEST | Quests related commands
                quests_daily = [
                    {
                        'command': 'daily_quest_1',
                        'description': "Increase Champion's Level in Tavern 3 times",
                        'handler': app.task(name='daily_quest_1', cb=lambda *args: quests.daily_quest_1()),
                    },
                    {
                        'command': 'daily_quest_2',
                        'description': "Make 4 Artifact/Accessory upgrade attempts",
                        'handler': app.task(name='daily_quest_2', cb=lambda *args: quests.daily_quest_2()),
                    },
                    {
                        'command': 'daily_quest_3',
                        'description': "Summon 3 Champions",
                        'handler': app.task(name='daily_quest_3', cb=lambda *args: quests.daily_quest_3()),
                    },

                    # Taken from another class
                    {
                        'command': 'daily_quest_5',
                        'description': "Fight in Classic Arena 5 times",
                        'handler': app.task(name='daily_quest_5', cb=lambda *args: arena_classic.run()),
                    },

                    {
                        'command': 'daily_quest_6',
                        'description': "Purchase an item at the Market",
                        'handler': app.task(name='daily_quest_6', cb=lambda *args: quests.daily_quest_6()),
                    },
                    {
                        'command': 'daily_quest_7',
                        'description': "Beat a Campaign Boss 3 times",
                        'handler': app.task(name='daily_quest_7', cb=lambda *args: quests.daily_quest_7()),
                    },
                    {
                        'command': 'daily_quest_8',
                        'description': "Win Campaign Battles 7 times",
                        'handler': app.task(name='daily_quest_8', cb=lambda *args: quests.daily_quest_8()),
                    }
                ]

                # register addition commands according to 'presets'
                presets_commands = []
                if len(app.config['presets']):
                    presets_commands = list(map(lambda preset: {
                            'command': make_command_key(f"preset {preset['name']}"),
                            'description': f"commands in a row: {', '.join(preset['commands'])}",
                            'handler': app.task(
                                name=make_command_key(f"preset {preset['name']}"),
                                cb=lambda *args: list(map(lambda x: app.get_entry(
                                    command_name=x
                                )['instance'].run(), preset['commands']))
                            ),
                        }, app.config['presets']))

                commands = regular_command + quests_daily + presets_commands

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

            if has_telegram_token and telegram_bot:
                # Wait for the bot thread to finish
                telegram_bot.join()
    else:
        log_save('An App is outdated')


if __name__ == '__main__':
    main()
