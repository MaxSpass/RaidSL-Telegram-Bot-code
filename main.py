import random
import traceback
import pyautogui
import copy
from bot import TelegramBOT
from classes.App import *
from classes.Debug import *
from classes.Foundation import *
# from classes.Storage import *
# from classes.Refill import *
from constants.index import IS_DEV
from locations.hero_filter.index import *

# from locations.quests.index import QUEST_DAILY_DATA
# from telegram.ext import CommandHandler
# import pyautogui
# import os.path
# import pyautogui
# import sys
# import random
# import pytesseract
# from PIL import Image
# from io import BytesIO
# from locations.faction_wars.index import *
# from locations.hero_preset.index import HeroPreset
# from locations.doom_tower.index import *
# from in_progress import *

# from apscheduler.schedulers.background import BackgroundScheduler
# from datetime import datetime
# import pytz

pyautogui.FAILSAFE = False
is_prod = is_production()

if not IS_DEV and is_prod:
    _path = os.path.join(sys._MEIPASS, './vendor/tesseract/tesseract.exe')
    pytesseract.pytesseract.tesseract_cmd = _path
else:
    # @TODO Should be in the env file
    pytesseract.pytesseract.tesseract_cmd = os.path.normpath(r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe')


# # TEST 1
# x = 633
# y = 41
# rgb_test = [255, 34, 51]
# x_offset = 825
# y_offset = 448
#
# TEST 2
# x = 725
# y = 50
# rgb_test = [16, 40, 49]
# x_offset = 826
# y_offset = 449
#
# pixel_origin = [x, y, rgb_test]
# x_mistake = x_offset + 2
# y_mistake = y_offset - 30
# pixel_debug = [
#     x + x_mistake,
#     y + y_mistake,
#     rgb_test
# ]

def schedule(seconds, predicate=None):
    def my_function(s=0):
        print(f"Function is running: {str(s)}")

    if predicate is None:
        predicate = my_function

    # Create a background scheduler
    # @TODO Temp commented
    # scheduler = BackgroundScheduler()
    scheduler = None

    # Define the time you want the function to run in UTC
    # For example, June 1, 2024, at 14:00:00 UTC
    # utc_time = datetime(2024, 6, 1, 11, 41, 0, tzinfo=pytz.timezone('utc'))

    # utc_time = datetime(2024, 6, 1, 11, 41, 0, tzinfo=pytz.utc)
    # print('utc_time', utc_time)

    # Schedule the function to run at the specified UTC time
    # scheduler.add_job(my_function, 'date', run_date=utc_time)

    tf = get_time_future(seconds=seconds)
    scheduler.add_job(predicate, 'cron', hour=tf.hour, minute=tf.minute, second=tf.second)
    # scheduler.add_job(predicate, 'cron', hour=hour, minute=minute)

    # Start the scheduler
    scheduler.start()

    # try:
    #     print("Runs")
    #     while True:
    #         pass
    # except (KeyboardInterrupt, SystemExit):
    #     # Shut down the scheduler
    #     scheduler.shutdown()


def main():
    # _w = 828
    # _h = 452 - 32
    # _region = [190, 150, 550, 50]
    # _region[0] = _region[0] + _w
    # _region[1] = _region[1] + _h

    # show_pyautogui_image(pyautogui.screenshot(region=_region))

    # energy = read_available_energy()
    # print('energy', energy)

    # keys = read_keys_bank()
    # print('keys', keys)
    # return

    # burger = find_needle_burger()
    # print('burger', burger)

    # close = find_needle_close_popup()
    # print('close', close)
    # return

    # debug_save_screenshot(region=[591, 247, 10, 69], quality=100)

    # f = Foundation(name='Test')
    #
    # E_SKIP_BATTLE = {
    #     'name': 'Skip battle',
    #     'interval': 10,
    #     'delay': 10,
    #     'blocking': False,
    #     'expect': lambda: bool(detect_pause_button()),
    #     'callback': lambda *args: skip_battle_arena()
    # }
    #
    # f.awaits(
    #     [ArenaClassic.E_BATTLE_END, E_SKIP_BATTLE],
    # )
    # return
    # f.dungeons_start_battle()
    # dungeons_start_battle()
    # res = f.waiting_battle_end_regular('Test battle')
    # print('res', res)
    # return

    # debug_save_screenshot(region=[258, 272, 10, 56], quality=100)
    # debug_save_screenshot(region=[0, 0, 900, 530], quality=100, suffix_name='arena_classic')

    # res_arena_classic = find_refill_arena_classic()
    # res_arena_tag = find_refill_arena_tag()
    # res_arena_live = find_refill_arena_live()
    # res_iron_twins_keys = find_refill_iron_twins_keys()
    # res_energy = find_refill_energy()
    #
    # print('classic', res_arena_classic)
    # print('tag', res_arena_tag)
    # print('live', res_arena_live)
    # print('iron_twins_keys', res_iron_twins_keys)
    # print('energy', res_energy)

    # refill = Refill()
    # refill.check()
    # return

    # time_future = get_time_future(minutes=1)
    # print('time_future', time_future)
    # return

    # def check_availability():
    #     # @TODO Finish
    #     # res = {
    #     #     'is_active': False,
    #     #     'open_hour': None
    #     # }
    #     # live_arena_open_hours = [[6, 8], [14, 16], [20, 22]]
    #     utc_timestamp = datetime.utcnow().timestamp()
    #     utc_datetime = datetime.fromtimestamp(utc_timestamp)
    #     parsed_time = time_mgr.timestamp_to_datetime(utc_datetime)
    #
    #     year = parsed_time['year']
    #     month = parsed_time['month']
    #     day = parsed_time['day']
    #     # @TODO
    #     hour = parsed_time['hour']
    #     print(parsed_time)
    #
    #     # hour = 14
    #     pause.until(datetime(year, month, day, hour, 1, 30, tzinfo=timezone.utc))

    # check_availability()
    # print('test')

    # return

    def scheduled(app, seconds=20):
        print('BackgroundScheduler')
        # p = lambda: print('Scheduled callback')
        p = app.commands['report']['cb']
        tf = get_time_future(seconds=seconds)
        print(f"Time future: {str(tf)}")
        app.scheduler.add_job(p, 'cron', hour=tf.hour, minute=tf.minute, second=tf.second)
        app.scheduler.start()

    if is_prod:
        log("The App is starting, don't touch the mouse and keyboard")
        sleep(10)

    app = App()

    # doom_tower = app.get_instance('doom_tower')
    # boss = doom_tower.find_boss_position_by_id(1)
    # print('boss', boss)
    # return

    if IS_DEV or app.validation():
        game_path = app.config['game_path']
        has_telegram_token = 'telegram_token' in app.config
        telegram_bot = None

        try:
            if app.config['start_immediate']:
                app.start()
                # app.get_instance('daily_quests').daily_quest_2()

                # print('BackgroundScheduler')
                # scheduler = BackgroundScheduler()
                # schedule_predicate = app.commands['report']['cb']
                # date_now = datetime.now()
                # scheduler.add_job(schedule_predicate, 'cron', hour=date_now.hour, minute=date_now.minute, second=date_now.second+30)
                # scheduler.start()

            if has_telegram_token:
                telegram_bot = TelegramBOT({
                    'token': app.config['telegram_token']
                })
                telegram_bot.start()

                commands_to_apply = copy.copy(app.COMMANDS_GAME_PATH_DEPENDANT) if game_path else []
                commands_to_apply += app.COMMANDS_COMMON

                for i in range(len(commands_to_apply)):
                    command_name = commands_to_apply[i]
                    command_data = app.commands[command_name]
                    telegram_bot.add({
                        'command': command_name,
                        'description': command_data['description'],
                        'handler': command_data['handler'],
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
                            app.task(
                                name=command,
                                cb=app.get_entry(command_name=command)['instance'].run
                            )(upd, ctx)

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

                # @TODO
                # app.schedule(predicate=lambda: print('Scheduled callback'))

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
