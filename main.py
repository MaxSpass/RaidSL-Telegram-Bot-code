import traceback
import pyautogui
import copy
from bot import TelegramBOT
from classes.App import *
from classes.Location import *
from constants.index import IS_DEV
from features.quests.index import QUEST_DAILY_DATA

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
# from in_progress import *

pyautogui.FAILSAFE = False
is_prod = is_production()

if not IS_DEV and is_prod:
    _path = os.path.join(sys._MEIPASS, './vendor/tesseract/tesseract.exe')
    pytesseract.pytesseract.tesseract_cmd = _path
else:
    # @TODO Should be in the env file
    pytesseract.pytesseract.tesseract_cmd = os.path.normpath(r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe')

def main():
    # print(pyautogui.pixel(x_img_2, y_img_2))
    # return

    # print(pyautogui.pixel(x, y))
    # print(dominant_color_rgb([1400, 560, 50, 50]))
    # return

    # # @TODO Location in progress START 1150, 600
    # rgb_grey = [127, 127, 127]
    # rgb_light_blue = [0, 162, 232]
    # x = 0
    # y = 300
    # width = 250
    # height = 250
    # region = [x, y, width, height]
    #
    # test_var = 333
    # context = {'test': 333}
    #
    # def test(msg):
    #     context['test'] = 444
    #     print(f"Test: {msg} | {str(test_var)}")
    #
    # event_grey = {
    #     "name": 'Grey | Pixel Check',
    #     "expect": lambda: pixel_check_new([x+50, y+50, rgb_grey], mistake=10),
    #     "callback": lambda *args: test('1'),
    # }
    #
    # event_blue = {
    #     "name": 'Blue | RGB Check',
    #     "expect": lambda: rgb_check(rgb_light_blue, dominant_color_rgb(region=region, reverse=False), mistake=10),
    #     "callback": lambda *args: test('2'),
    # }
    #
    # event_needle = {
    #     "name": 'Needle Check',
    #     "expect": lambda: find_needle('market_mystery_shard.jpg', region=region),
    #     "callback": lambda *args: test('3'),
    #     "children": {"events": [event_blue], "interval": 2},
    # }
    #
    # tree_main = Location(core_events=[event_grey])
    #
    # # event_needle_ext = event_needle.copy()
    # # event_needle_ext.items()
    #
    # events_core = tree_main.create(
    #     events=[event_blue, event_needle],
    #     interval=.5
    # )
    #
    # events_core()
    # # print('test_var', context['test'])
    #
    # return
    # @TODO Location in progress END

    # print(str(np.array([1,2,3], dtype=object)))
    # return

    # for i in range(2):
    #     swipe('bottom', 450, 490, 340, speed=3)
    # return

    # print(pyautogui.pixel(320, 420))
    # return

    # quests = Quests()
    # quests.get_not_completed_ids()
    # return

    if is_prod:
        log("The App is starting, don't touch the mouse and keyboard")
        sleep(10)

    app = App()
    # return

    if IS_DEV or app.validation():
        game_path = app.get_game_path()
        has_telegram_token = 'telegram_token' in app.config
        telegram_bot = None

        try:
            if app.config['start_immediate']:
                app.start()

            if has_telegram_token:
                telegram_bot = TelegramBOT({
                    'token': app.config['telegram_token']
                })
                telegram_bot.start()

                # 'game_path' dependant commands
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
                # Sync
                telegram_bot.add({
                    'command': 'click',
                    'description': 'Click by provided coordinates: x, y',
                    'handler': app.task(
                        name='click',
                        cb=app.click,
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

                # register addition commands according to 'presets'
                presets_commands = []
                if len(app.config['presets']):
                    def process_preset_commands(upd, ctx, preset):
                        for i in range(len(preset['commands'])):
                            command = preset['commands'][i]
                            cb = app.get_entry(command_name=command)['instance'].run
                            app.task(
                                name=command,
                                cb=cb
                            )(upd, ctx)
                        return None

                    presets_commands = list(map(lambda preset: {
                        'command': make_command_key(f"preset {preset['name']}"),
                        'description': f"commands in a row: {', '.join(preset['commands'])}",
                        'handler': lambda upd, ctx: process_preset_commands(upd, ctx, preset),
                    }, app.config['presets']))

                commands = regular_command + presets_commands

                for i in range(len(commands)):
                    print(commands[i])
                    telegram_bot.add(commands[i])

                # daily_quests = app.get_instance('daily_quests')
                # doom_tower = app.get_instance('doom_tower')
                # daily_quests.daily_quest_2()

                telegram_bot.listen()
                telegram_bot.updater.idle()

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
