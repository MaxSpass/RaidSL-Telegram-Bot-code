from helpers.common import *
from classes.TaskManager import TaskManager
from classes.Storage import Storage
from classes.Foundation import *
from locations.rewards.index import *
# from locations.live_arena.index_old import *
from locations.live_arena.index import *
from locations.arena.index import *
from locations.demon_lord.index import *
from locations.faction_wars.index import *
from locations.iron_twins_fortress.index import *
from locations.dungeons.index import *
from locations.hydra.index import *
from locations.doom_tower.index import *
from locations.quests.index import *
from locations.test.index import *
from locations.test_await.index import *
from constants.index import *
# import atexit
import signal
import sys
# import pytesseract
import subprocess
import psutil
import os
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
# @TODO Temp commented
# from apscheduler.schedulers.background import BackgroundScheduler
# import pytz
from datetime import datetime

# from telegram.error import NetworkError

# GAME_WINDOW = 'Raid: Shadow Legends'
# PROCESS_GAME_NAME = 'Raid.exe'
# WINDOW_TOP_BAR_HEIGHT = 25
# BORDER_WIDTH = 7
# CONFIG_PATH = "config.json"
# WINDOW_SIZE = [920, 540]

INSTANCES_MAP = {
    'arena_live': ArenaLive,
    'arena_classic': ArenaClassic,
    'arena_tag': ArenaTag,
    'demon_lord': DemonLord,
    'hydra': Hydra,
    'dungeon': Dungeons,
    'faction_wars': FactionWars,
    'iron_twins': IronTwins,
    'rewards': Rewards,
    'doom_tower': DoomTower,
    'daily_quests': Quests,
    'test_feature': TestFeature,
    'test_await': TestAwait,
}
SUPPORTED_LANGUAGES = ['eng', 'deu', 'ukr', 'rus']

# EMULATE_NETWORK_ERROR = False

def find_process_by_name(name):
    for proc in psutil.process_iter(['pid', 'name']):
        # print(proc.info['name'])
        if proc.info['name'] == name:
            return proc

    log(f"No process found with the title: {name}")
    return False


def terminate_process_by_name(name):
    proc = find_process_by_name(name)
    if proc:
        log(f"Terminating process {proc.info['name']} (PID: {proc.info['pid']})")
        proc.terminate()
        return True

    log(f"No process found with the title: {name}")
    return False


def get_windows(title):
    return pyautogui.getWindowsWithTitle(title)


def get_game_windows():
    return get_windows(GAME_WINDOW)


def resize_window(x_move=0, y_move=0):
    win = None
    wins = get_game_windows()
    if len(wins):
        win = wins[0]
        win.activate()
        time.sleep(.5)
        win.resizeTo(WINDOW_SIZE[0], WINDOW_SIZE[1])
        win.moveTo(int(x_move), int(y_move))
        time.sleep(.5)
    else:
        log("No RAID window found")
    return win


def calibrate_window(window_axis=None):
    log('Preparing the window')
    BURGER_POSITION = [15, 282]
    is_prepared = False
    x = 0
    y = 0
    wins = get_game_windows()
    if len(wins):
        win = wins[0]
        # going back to the index page
        close_popup_recursive()

        if window_axis is not None:
            print('window_axis', window_axis)
            x = window_axis['x']
            y = window_axis['y']
        else:
            burger = find_needle_burger()
            if burger is not None:
                if burger[0] != BURGER_POSITION[0] or burger[1] != BURGER_POSITION[1]:
                    x_burger = burger[0] - BURGER_POSITION[0]
                    y_burger = burger[1] - BURGER_POSITION[1]
                    x -= x_burger
                    y -= y_burger

        win.move(int(x), int(y))

        is_prepared = True

        # waiting and closing sudden popups
        sleep(3)
        close_popup_recursive()

    if not is_prepared:
        raise Exception("Game windows is NOT prepared")

    return {'x': x, 'y': y}


def prepare_window():
    BURGER_POSITION = [15, 282]
    is_prepared = False
    wins = get_game_windows()
    win = None
    if len(wins):
        win = wins[0]
        win.activate()
        time.sleep(.5)

        x = 0
        y = 0

        win.resizeTo(WINDOW_SIZE[0], WINDOW_SIZE[1])
        win.moveTo(x, y)
        time.sleep(.5)

        # going back to the index page
        close_popup_recursive()

        burger = find_needle_burger()
        if burger is not None:
            if burger[0] != BURGER_POSITION[0] or burger[1] != BURGER_POSITION[1]:
                x_burger = burger[0] - BURGER_POSITION[0]
                y_burger = burger[1] - BURGER_POSITION[1]
                x -= x_burger
                y -= y_burger
                win.move(int(x), int(y))
            is_prepared = True

            # waiting and closing sudden popups
            sleep(3)
            close_popup_recursive()
        else:
            log("No Burger needle found")
    else:
        log("No RAID window found")

    if not is_prepared:
        raise Exception("Game windows is NOT prepared")

    return win


def make_command_key(input_string):
    # Remove special characters and convert to lowercase
    clean_string = re.sub(r'[^a-zA-Z0-9\s]', '', input_string).lower()
    # Replace spaces with underscores
    formatted_string = clean_string.replace(' ', '_')
    return formatted_string


def make_title(input_string):
    return input_string.replace('_', ' ').title()


def expect_relogin(lang):
    # @TODO Rework text hardcode
    return find_detected_button({'text': 're-log in'}, detect_buttons_new(lang=lang))

class App(Foundation):
    COMMANDS_GAME_PATH_DEPENDANT = ['restart', 'launch', 'relogin', 'prepare']
    COMMANDS_COMMON = ['report', 'screen', 'click', 'stop']

    def __init__(self):
        Foundation.__init__(self, name='App')

        self.config = None
        self.window = None
        self.window_region = None
        self.window_axis = None
        self.entries = {}
        self.taskManager = TaskManager()
        self.scheduler = None
        # @TODO Temp commented
        # self.storage = Storage(name='storage', folder='temp')
        self.read_config()
        self.commands = self.get_commands()

        self.INDEX_PAGE_DETECTED = {
            'name': "Index+",
            'interval': 2,
            'expect': find_needle_burger,
        }

        self.INDEX_PAGE_NOT_DETECTED = {
            'name': "Index-",
            'interval': .5,
            'blocking': False,
            'expect': lambda: not find_needle_burger(),
            'callback': lambda *args: close_popup()
        }

        self.E_TERMINATE_GAME = {
            'name': "TerminateGame",
            'interval': 120,
            'delay': 120,
            'limit': 1,
            'blocking': False,
            "expect": lambda: True,
            'callback': lambda *args: self.restart(terminate_list=[PROCESS_GAME_NAME]),
        }

        self.E_TERMINATE_ALL = {
            'name': "TerminateAll",
            'interval': 300,
            'delay': 300,
            'limit': 1,
            'blocking': False,
            'expect': lambda: True,
            'callback': self.restart,
        }

        self.E_POPUP_RELOGIN_ERROR = prepare_event(self.E_POPUP_ERROR, {
            "limit": 1,
            "wait_limit": 2,
            "expect": lambda: expect_relogin(lang=self.config['lang']) if self.config['lang'] else is_logged_out(),
            "callback": lambda *args: click_detected_button(*args) if self.config['lang'] else click(350, 294)
        })
        
    def get_commands(self):
        return {
            'restart': {
                'description': 'Re-Start the Game',
                'handler': self.task('restart', self.restart, task_type='aside'),
            },
            'launch': {
                'description': 'Re-Launch the Game',
                'handler': self.task('launch', self.launch, task_type='aside'),
            },
            # @TODO Does not work properly when it's running right after bot starts
            'relogin': {
                'description': 'Re-log in',
                'handler': self.task('relogin', self.relogin, task_type='aside'),
            },
            'prepare': {
                'description': 'Prepares the Game window',
                'handler': self.task('prepare', lambda *args: self.prepare(calibrate=False), task_type='sync'),
            },
            'screen': {
                'description': 'Capture and send a screenshot',
                'handler': self.task('screen', self._screenshot, task_type='sync'),
            },
            'click': {
                'description': 'Click by provided coordinates: x, y',
                'handler': self.task('click', self._click, task_type='sync'),
            },
            'stop': {
                'description': 'Terminates instances and clears the queue',
                'handler': self.task('stop', self._stop, task_type='sync'),
            },
            'report': {
                'description': 'Report',
                'handler': self.task('report', self.report, task_type='sync'),
            },
        }

    def _screenshot(self, upd, ctx):
        # @TODO Bug
        # if not bool(self.window):
        #     self.prepare()

        if bool(self.window):
            return ctx.bot.send_photo(chat_id=upd.message.chat_id, photo=self.screen())
        else:
            upd.message.reply_text('No window found')
            return False

    def _prepare_config(self, config_json):
        _config = {
            'start_immediate': True,
            'tasks': [],
            'presets': [],
            'after_each': [],
            'game_path': '',
            'lang': None
        }

        # Temp properties
        if 'game_path' in config_json and bool(config_json['game_path']):
            _config['game_path'] = os.path.normpath(str(config_json['game_path']))

        if 'start_immediate' in config_json:
            _config['start_immediate'] = bool(config_json['start_immediate'])

        if 'telegram_token' in config_json:
            _config['telegram_token'] = str(config_json['telegram_token'])

        if 'lang' in config_json:
            _lang = str(config_json['lang']).lower()
            if _lang in SUPPORTED_LANGUAGES:
                _config['lang'] = _lang

        # Tasks
        tasks_length = len(config_json['tasks'])
        if tasks_length:
            for i in range(tasks_length):
                task = config_json['tasks'][i]
                if 'enable' not in task or bool(task['enable']):

                    _task = task['task'].lower()
                    _props = task['props'] if 'props' in task else None
                    _title = task['title'] if 'title' in task else make_title(_task)
                    _command = task['command'] \
                        if 'command' in task \
                        else f"{_task}_" + make_command_key(f"{task['title']}") \
                        if 'title' in task \
                        else _task

                    # The most important data object for command registration
                    task_d = {
                        'task': _task,
                        'command': _command,
                        'title': _title,
                        'props': _props,
                    }

                    # @TODO Removed: and _task not in self.entries
                    # accumulated instances
                    if _command not in self.entries:
                        if _task in INSTANCES_MAP:
                            # @TODO should take from memory later on

                            self.entries[_command] = {
                                'instance': INSTANCES_MAP[_task](app=self, props=_props),
                            }
                        else:
                            raise f"No {_task} among all instances"
                    else:
                        raise f"{_command} is already exist, please provide the different"

                    _config['tasks'].append(task_d)

            # handling presets
            presets_length = len(config_json['presets'])
            if presets_length:
                # @TODO Refactor
                # _config['presets'] = config_json['presets']

                presets_filtered = []
                for i in range(presets_length):
                    preset_name = config_json['presets'][i]['name']
                    preset_tasks = config_json['presets'][i]['commands']

                    presets_filtered.append({
                        'name': preset_name,
                        'commands': list(filter(
                            lambda x: any(dct['command'] == x for dct in _config['tasks']), preset_tasks
                        ))
                    })
                _config['presets'] = presets_filtered

        # After each commands
        if 'after_each' in config_json:
            _config['after_each'] = config_json['after_each']

        return _config

    def validation(self):
        # primitive validation
        date_now = datetime.now()
        return date_now.year == 2024 and (date_now.month <= 12)

    def load_config(self, config):
        self.config = self._prepare_config(config)
        log('Load App Config')

    def read_config(self):
        try:
            with open(CONFIG_PATH) as config_file:
                config = json.load(config_file)
                self.config = self._prepare_config(config)
                log('Config is processed')

        except SystemError:
            log('An error occurred while reading ' + CONFIG_PATH + ' file')

    def report(self, *args):
        print('App -> Report')
        res = None
        instances = list(map(lambda x: x['instance'], self.entries.values()))
        reports = list(map(lambda x: x.report(), instances))

        if reports.count(None) < len(reports):
            res = ''
            for i in range(len(reports)):
                report = reports[i]
                if report:
                    res += f'{report}\n\n'

        return res or "No reports yet"

    def kill(self, *args):
        if self.scheduler is not None:
            self.scheduler.shutdown()
        self.report()
        log('App is terminated')
        input('Confirm by pressing any key')
        sys.exit(0)

    def relogin(self, *args):

        self.awaits(events=[
            self.E_POPUP_RELOGIN_ERROR,
            self.INDEX_PAGE_DETECTED,
            self.INDEX_PAGE_NOT_DETECTED,
            self.E_TERMINATE_GAME,
            self.E_TERMINATE_ALL,
        ])

        sleep(5)
        close_popup_recursive()

        return True

    def get_window_region(self):
        if self.window_region is not None:
            return self.window_region

        if self.window is None:
            self.window = resize_window()

        x = self.window.left
        y = self.window.top
        width = self.window.width
        height = self.window.height

        # calculates region
        region = [
            int(x + BORDER_WIDTH),
            int(y + BORDER_WIDTH + WINDOW_TOP_BAR_HEIGHT),
            int(width - BORDER_WIDTH * 2),
            int(height - BORDER_WIDTH * 2 - WINDOW_TOP_BAR_HEIGHT),
        ]

        self.window_region = region
        log(f"Window region: {str(region)}")

        return region

    def screen(self, *args):
        _region = self.get_window_region()
        screenshot = pyautogui.screenshot(region=_region)

        # Convert the screenshot to bytes
        image_bytes = BytesIO()
        screenshot.save(image_bytes, format='PNG')
        image_bytes.seek(0)

        return image_bytes

    def _stop(self, *args):
        # Needs when bot is starting
        sleep(1)

        # Terminates all instances
        for key, value in self.entries.items():
            instance = value['instance']
            instance.terminate = True
            instance.stop = True

        # Empty the queue
        queue = self.taskManager.queue
        while not queue.empty():
            queue.get()

    def _click(self, upd, ctx):
        response = []

        def _get_grid_screenshot():
            gap_size = 100
            font_scale = .5
            font_color = (150, 255, 0)
            grid_color = (150, 255, 0)

            image_bytes = self.screen()
            # Convert the image to a numpy array
            img_np = np.array(Image.open(image_bytes))

            # Get the image dimensions
            height, width, _ = img_np.shape

            # Draw vertical lines
            for x in range(0, width, gap_size):
                cv2.line(img_np, (x, 0), (x, height), grid_color, 1)

            # Draw horizontal lines
            for y in range(0, height, gap_size):
                cv2.line(img_np, (0, y), (width, y), grid_color, 1)

            # Draw pixel coordinates
            font = cv2.FONT_HERSHEY_SIMPLEX
            for y in range(0, height, gap_size):
                for x in range(0, width, gap_size):
                    x_final = int(x + gap_size / 2)
                    y_final = int(y + gap_size / 2)
                    text = f"({x_final},{y_final})"
                    text_size = cv2.getTextSize(text, font, font_scale, 1)[0]
                    text_x = x + (gap_size - text_size[0]) // 2
                    text_y = y + (gap_size + text_size[1]) // 2
                    cv2.putText(img_np, text, (text_x, text_y), font, font_scale, font_color, 1, cv2.LINE_AA)

            # Convert the numpy array back to an image
            img_with_grid = Image.fromarray(img_np)

            # Convert the image to bytes using BytesIO
            buffered_image = BytesIO()
            img_with_grid.save(buffered_image, format="JPEG")  # Change format if necessary
            buffered_image.seek(0)

            return buffered_image

        def _send_grid_screenshot():
            if bool(self.window):
                grid_screen = _get_grid_screenshot()
                ctx.bot.send_photo(
                    chat_id=upd.message.chat_id,
                    photo=grid_screen
                )
            else:
                response.append("No Game window found")

        if len(ctx.args) < 2:
            _send_grid_screenshot()
            response.append('Provide coordinates: x y')

        else:
            x = ctx.args[0]
            y = ctx.args[1]

            if is_number(x) and is_number(y):
                click(
                    int(x) + BORDER_WIDTH,
                    int(y) + WINDOW_TOP_BAR_HEIGHT + BORDER_WIDTH
                )
                sleep(.5)
                _send_grid_screenshot()
            else:
                response.append('X and Y must be numbers')

        if len(response):
            return upd.message.reply_text('\n'.join(response))

    def start(self):
        # atexit.register(self.report)
        signal.signal(signal.SIGINT, self.kill)
        signal.signal(signal.SIGTERM, self.kill)

        game_path = self.config['game_path']
        if find_process_by_name(PROCESS_GAME_NAME):
            self.prepare(predicate=self.relogin)
        elif game_path:
            self.launch()
        else:
            raise "No 'game_path' provided field in the config"

    def launch(self, *args):
        game_path = self.config['game_path']
        if game_path:
            subprocess.run(f"{game_path} -gameid=101 -tray-start")
            sleep(3)
            self.prepare()
            log('Game window is ready')
        else:
            return "No 'game_path' provided field in the config"

    def restart(self, *args, terminate_list=None):
        if terminate_list is None:
            terminate_list = [PROCESS_GAME_NAME, PROCESS_PLARIUM_SERVICE_NAME, PROCESS_PLARIUM_PLAY_NAME]

        game_path = self.config['game_path']
        if game_path:
            if type(terminate_list) is list and len(terminate_list):
                for t in range(len(terminate_list)):
                    terminate_process_by_name(terminate_list[t])
            sleep(2)
            self.launch()
            sleep(2)
        else:
            return "No 'game_path' provided field in the config"

    def prepare(self, predicate=None, calibrate=True):
        x_move = self.window_axis['x'] if self.window_axis and 'x' in self.window_axis else 0
        y_move = self.window_axis['y'] if self.window_axis and 'y' in self.window_axis else 0
        self.window = resize_window(x_move=x_move, y_move=y_move)

        if predicate is not None:
            predicate()

        self.awaits([
            self.E_POPUP_RELOGIN_ERROR,
            self.INDEX_PAGE_DETECTED,
            self.INDEX_PAGE_NOT_DETECTED
        ])

        if calibrate:
            self.window_axis = calibrate_window(self.window_axis)

    def get_entry(self, command_name):
        return self.entries[command_name] \
            if command_name in self.entries \
            else None

    def get_instance(self, command_name):
        entry = self.get_entry(command_name)
        return entry['instance'] if entry and 'instance' in entry else None

    # def on_message(self, upd, text, retry=True):
    #     global EMULATE_NETWORK_ERROR
    #     try:
    #         if EMULATE_NETWORK_ERROR:
    #             EMULATE_NETWORK_ERROR = False
    #             raise NetworkError('from App.on_message')
    #
    #         upd.message.reply_text(text)
    #     except NetworkError as e:
    #         if retry:
    #             self.on_message(upd, text, retry=False)
    #     except Exception:
    #         pass

    def task(self, name, cb, task_type="aside"):
        # @TODO
        # self.tasks[name] =
        return lambda upd, ctx: self.taskManager.add(name, lambda: cb(upd, ctx), props={
            # 'onDone': lambda text: self.on_message(upd, text),
            # 'onError': lambda text: self.on_message(upd, text),
            'onDone': upd.message.reply_text,
            'onError': upd.message.reply_text,
            'type': task_type,
        })

    def schedule(self, predicate=None):
        # @TODO Temp commented
        # if self.scheduler is None:
        #     self.scheduler = BackgroundScheduler()

        if predicate is not None:
            tf = get_time_future(seconds=20)
            self.scheduler.add_job(predicate, 'cron', hour=tf.hour, minute=tf.minute, second=tf.second)

        self.scheduler.start()
