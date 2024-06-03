import traceback
import pyautogui
import copy
from bot import TelegramBOT
from classes.App import *
from classes.Debug import *
from classes.Foundation import *
# from classes.Storage import *
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
    scheduler = BackgroundScheduler()

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



    # s = '2024-05-23T21:44:45.770613'
    # print(datetime.fromisoformat(s))
    # return

    # def timelens(*args, **kwargs):
    #     return format_date(datetime.now() - timedelta(**kwargs))
    #
    # s = Storage(name='storage')
    #
    # s.add(
    #     title='Arena Live',
    #     data={'results_record': [True], 'duration_record': [timelens(minutes=10), timelens(minutes=5)]},
    # )
    # s.add(
    #     title='Arena Tag',
    #     data={'results_record': [True, False], 'duration_record': [timelens(minutes=4), timelens(minutes=2)]},
    #     date=timelens(minutes=60)
    # )
    # s.add(
    #     title='Arena Tag',
    #     data={'results_record': [True, True, False], 'duration_record': [timelens(minutes=20), timelens(minutes=5)]},
    #     date=timelens(minutes=55)
    # )
    # s.add(
    #     title='Arena Classic',
    #     data={'results_record': [True, True, True], 'duration_record': [timelens(minutes=20), timelens(minutes=5)]},
    #     date=timelens(minutes=45)
    # )
    # s.add(
    #     title='Arena Live',
    #     data={'results_record': [True], 'duration_record': [timelens(minutes=10), timelens(minutes=5)]},
    #     date=timelens(minutes=35)
    # )
    # s.add(
    #     title='Arena Live',
    #     data={'results_record': [True], 'duration_record': [timelens(minutes=10), timelens(minutes=5)]},
    #     date=timelens(minutes=15)
    # )
    #
    # # entries = s.get_entries(days=0, title='Arena Live')
    # entries = s.get_entries(days=0)
    # print('entries len', len(entries))
    #
    # for i in range(len(entries)):
    #     print(entries[i])
    #
    # return

    # returns [21, 32, 39]
    # print(pyautogui.pixel(737, 138))
    # return

    # foundation = Foundation('test')
    # res = foundation.awaits(events=[
    #     {
    #         "name": 'test 1',
    #         "expect": lambda: pixel_check_new([260, 15, [243, 243, 243]]),
    #         "callback": lambda *args: print('Occurred: test 1'),
    #         "blocking": False,
    #         "limit": 1,
    #     },
    #     {
    #         "name": 'test 2',
    #         "expect": lambda: pixel_check_new([737, 138, [87, 157, 255]]),
    #         "callback": lambda *args: print('Occurred: test 2'),
    #     },
    #     {
    #         "name": 'test 3',
    #         "expect": lambda: pixel_check_new([737, 138, [87, 157, 255]]),
    #         "callback": lambda *args: print('Occurred: test 3'),
    #     }
    # ])
    # print(res)
    # return

    #
    # E_VICTORY_COPY = prepare_event(E_VICTORY, {
    #     "callback": lambda *args: tap_to_continue(wait_after=2)
    # })
    # E_DEFEAT_COPY = prepare_event(E_DEFEAT, {
    #     "callback": lambda *args: tap_to_continue(wait_after=2)
    # })
    #
    # res = foundation.awaits(events=[E_BATTLE_START_REGULAR, E_VICTORY_COPY, E_DEFEAT_COPY])
    # print('res', res)
    # return

    # hero_filter = HeroFilter()
    #
    # pool = ['arbiter', 'leo', 'madam', 'armanz']
    #
    # for i in range(len(pool)):
    #     title = pool[i]
    #     hero_filter.choose(title)
    #
    # return

    # print(pyautogui.pixel(653, 104))
    # print(pyautogui.pixel(570, 493))
    # print(pyautogui.pixel(450, 490))
    # print(pyautogui.pixel(660, 490))
    # return

    # offsets were taken from 'images/for_test/live_arena_issue.png'

    # x_offset = 371
    # y_offset = 278
    # copy_victory = copy.copy(victory)
    # copy_victory[0] = copy_victory[0] + x_offset
    # copy_victory[1] = copy_victory[1] + y_offset
    # foundation = Foundation('test')
    #
    # foundation.dungeons_start_battle()
    # return
    #
    # E_VICTORY_TEST = {
    #     "name": "1",
    #     "expect": lambda: pixel_check_new(copy_victory, mistake=30),
    # }
    #
    # E_VICTORY_TEST_2 = {
    #     "name": "2",
    #     "expect": lambda: pixel_check_new(copy_victory),
    # }
    #
    # e_victory = prepare_event(E_VICTORY_TEST, {
    #     'interval': 5,
    #     'callback': lambda *args: print('FOUND 1')
    # })
    #
    # e_victory_2 = prepare_event(E_VICTORY_TEST_2, {
    #     'interval': 0.5,
    #     'callback': lambda *args: print('FOUND 2'),
    #     'wait_limit': 2,
    # })
    #
    # res = foundation.awaits([e_victory_2, foundation.E_NO_AURA_SKILL])
    # return

    # _copy = copy.copy(cant_find_opponent_button_cancel)
    # x_offset = 828
    # y_offset = 432
    # _copy[0] = _copy[0] + x_offset
    # _copy[1] = _copy[1] + y_offset
    # res = pixels_every(same_pixels_line(_copy), lambda p: pixel_check_new(p, mistake=5))
    # print('res', res)
    # return

    # print(pixels_every(pixels_row(_p), lambda _p: pixel_check_new(_p, mistake=1)))
    # return

    # _w = 48
    # _h = 64
    #
    # for i in range(len(my_slots)):
    #     el = my_slots[i]
    #     x = el[0] + x_offset
    #     y = el[1] + y_offset
    #
    #     show_pyautogui_image(pyautogui.screenshot(region=[x, y, _w, _h]))
    # return

    # print(read_available_energy())
    # print(read_keys_bank())
    # position = find_needle_close_popup()
    # print(position)
    # return

    # hero_filter = HeroFilter()
    # hero_filter.choose('Armanz')
    # return

    # print(pyautogui.pixel(725, 50))
    # return

    # same = False
    # counter = 0
    # while not same:
    #     x_test = pixel_debug[0]
    #     y_test = pixel_debug[1] + counter
    #     print(f"X: {x_test}, Y: {y_test}")
    #     _pixel = pyautogui.pixel(x_test, y_test)
    #     same = rgb_check(rgb_test, _pixel)
    #     print('O Pixel:', rgb_test)
    #     print('D Pixel:', _pixel)
    #     print('===================')
    #     counter += 1
    #     sleep(.3)

    # while True:
    #     print('original', pyautogui.pixel(pixel_origin[0], pixel_origin[1]))
    #     show_pyautogui_image(
    #         pyautogui.screenshot(region=[pixel_origin[0], pixel_origin[1], 20, 20])
    #     )
    #     print('debug', pyautogui.pixel(pixel_debug[0], pixel_debug[1]))
    #     show_pyautogui_image(
    #         pyautogui.screenshot(region=[pixel_debug[0], pixel_debug[1], 20, 20])
    #     )
    # return

    # folder_ensure()
    # debug_save_screenshot(output=f"test/{get_date_for_log()}")
    # return
    # print(pyautogui.pixel(350, 294))
    # print(pyautogui.pixel(550, 294))
    # return

    # for affinity, region in TAVERN_AFFINITY_REGIONS.items():
    #     beer_total_float = read_text(
    #         region=region,
    #         scale=6,
    #         parser=parse_energy_cost
    #     )
    #     print(f"{str(beer_total_float)}")
    #     if affinity == 'spirit':
    #         show_pyautogui_image(pyautogui.screenshot(region=region))
    # return

    # print(read_keys_bank())
    # return
    # for i in range(10):
    #     # print(E_VICTORY['expect']())
    #     print(E_DEFEAT['expect']())
    #     sleep(1)
    # return

    # print(pyautogui.pixel(x_img_2, y_img_2))
    # return

    # print(pyautogui.pixel(x, y))
    # print(dominant_color_rgb([1400, 560, 50, 50]))
    # return

    # quests = Quests()
    # quests.get_not_completed_ids()
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

                # print('BackgroundScheduler')
                # scheduler = BackgroundScheduler()
                # schedule_predicate = app.commands['report']['cb']
                # date_now = datetime.now()
                # scheduler.add_job(schedule_predicate, 'cron', hour=date_now.hour, minute=date_now.minute, second=date_now.second+30)
                # scheduler.start()

                # debug = Debug(app=app, name='arena_live')
                # time_for_log = get_time_for_log(s='_')
                # date_for_log = get_date_for_log()
                # print('time_for_log', time_for_log)
                # print('date_for_log', date_for_log)
                # debug.screenshot(folder=time_for_log, suffix_name='opponent_left')

                # debug_save_screenshot(region=app.get_window_region(), quality=100, ext='png')
                # debug.screenshot(suffix_name="Custom prefix name")
                # app.get_instance('daily_quests').daily_quest_1()


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
