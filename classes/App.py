from helpers.common import *
from classes.TaskManager import TaskManager
from features.rewards.index import *
from features.live_arena.index import *
from features.arena.index import *
from features.demon_lord.index import *
from features.faction_wars.index import *
from features.iron_twins_fortress.index import *
from features.dungeons.index import *
from features.hydra.index import *
from features.doom_tower.index import *
from features.quests.index import *
import atexit
import signal
import sys
import pytesseract
import subprocess
import psutil
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw
from io import BytesIO

GAME_WINDOW = 'Raid: Shadow Legends'
GAME_PROCESS_NAME = 'Raid.exe'
WINDOW_TOP_BAR_HEIGHT = 25
BORDER_WIDTH = 7
# GAME_PATH = r"C:\Users\user\AppData\Local\PlariumPlay\PlariumPlay.exe"

CONFIG_PATH = "config.json"
WINDOW_SIZE = [920, 540]
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
}

def find_process_by_name(name):
    for proc in psutil.process_iter(['pid', 'name']):
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

def get_game_windows():
    return pyautogui.getWindowsWithTitle(GAME_WINDOW)

def resize_window():
    win = None
    wins = get_game_windows()
    if len(wins):
        win = wins[0]
        win.activate()
        time.sleep(.5)
        win.resizeTo(WINDOW_SIZE[0], WINDOW_SIZE[1])
        win.moveTo(0, 0)
        time.sleep(.5)
    else:
        log("No RAID window found")
    return win

def calibrate_window():
    BURGER_POSITION = [15, 282]
    is_prepared = False
    x = 0
    y = 0
    wins = get_game_windows()
    if len(wins):
        win = wins[0]
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
    if not is_prepared:
        raise Exception("Game windows is NOT prepared")


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

class App:
    def __init__(self):
        self.config = None
        self.window = None
        self.entries = {}
        self.read_config()
        self.taskManager = TaskManager()

    def _prepare_config(self, config_json):
        _config = {
            'start_immediate': True,
            'tasks': [],
            'presets': [],
            'after_each': [],
            'game_path': ''
        }

        # Temp properties
        if 'game_path' in config_json and bool(config_json['game_path']):
            _config['game_path'] = os.path.normpath(str(config_json['game_path']))

        if 'start_immediate' in config_json:
            _config['start_immediate'] = bool(config_json['start_immediate'])

        if 'telegram_token' in config_json:
            _config['telegram_token'] = str(config_json['telegram_token'])

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
                        else make_command_key(f"{_task} {task['title']}") \
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
                                'instance': INSTANCES_MAP[_task](props=_props),
                            }
                        else:
                            raise f"No {_task} among all instances"
                    else:
                        raise f"{_command} is already exist, please provide the different"

                    _config['tasks'].append(task_d)

            # rewards init
            self.entries['rewards'] = {
                'instance': INSTANCES_MAP['rewards']()
            }

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

    def get_game_path(self):
        return self.config['game_path']

    def validation(self):
        # primitive validation
        currentYear = datetime.now().year
        currentMonth = datetime.now().month
        return currentYear == 2024 and (currentMonth <= 4)

    def load_config(self, config):
        self.config = self._prepare_config(config)
        log('Load App Config')

    def read_config(self):
        try:
            with open(CONFIG_PATH) as config_file:
                config = json.load(config_file)
                self.config = self._prepare_config(config)
                log('Reading App Config...')

        except SystemError:
            log('An error occurred while reading ' + CONFIG_PATH + ' file')

    def exit(self):
        self.report()

    def report(self, *args):
        res = None
        instances = list(map(lambda x: x['instance'], self.entries.values()))
        reports = list(map(lambda x: x.report(), instances))

        if reports.count(None) < len(reports):
            res = ''
            for i in range(len(reports)):
                report = reports[i]
                if report:
                    res += f'{report}\n'

        if res:
            log(res)

        return res

    def kill(self, *args):
        log('App is terminated')
        input('Confirm by pressing any key')
        sys.exit(0)

    def relogin(self, *args):
        # limit in seconds
        limit = 60
        timeout = 3
        counter = 0

        click(425, 300)
        time.sleep(2)

        burger = find_needle_burger()
        while burger is None and counter < limit:
            time.sleep(timeout)
            counter += timeout
            burger = find_needle_burger()

        if not burger:
            self.restart()

        return True

    def screen(self, *args):
        global WINDOW_TOP_BAR_HEIGHT
        global BORDER_WIDTH
        # hidden window
        # <Win32Window left="-32000", top="-32000", width="160", height="28", title="Raid: Shadow Legends">

        x = self.window.left
        y = self.window.top
        width = self.window.width
        height = self.window.height

        # calculates region
        region = [
            x + BORDER_WIDTH,
            y + BORDER_WIDTH + WINDOW_TOP_BAR_HEIGHT,
            width - BORDER_WIDTH * 2,
            height - BORDER_WIDTH * 2 - WINDOW_TOP_BAR_HEIGHT,
        ]

        screenshot = pyautogui.screenshot(region=region)

        # Convert the screenshot to bytes
        image_bytes = BytesIO()
        screenshot.save(image_bytes, format='PNG')
        image_bytes.seek(0)

        return image_bytes

    def click(self, upd, ctx):
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

    def start_game(self):
        # atexit.register(self.report)
        signal.signal(signal.SIGINT, self.kill)
        signal.signal(signal.SIGTERM, self.kill)
        # prepare_window()

        game_path = self.get_game_path()

        if find_process_by_name(GAME_PROCESS_NAME):
            self.prepare()
        elif game_path:
            self.launch()
        else:
            raise "No 'game_path' provided field in the config"

    def launch(self, *args):
        game_path = self.get_game_path()
        if game_path:
            subprocess.run(f"{game_path} -gameid=101 -tray-start")
            sleep(3)
            self.window = resize_window()

            while not is_index_page(logger=False):
                log('Waiting the game window')
                sleep(5)

            calibrate_window()
            log('Game window is ready')
        else:
            return "No 'game_path' provided field in the config"

    def restart(self, *args):
        game_path = self.get_game_path()
        if game_path:
            terminate_process_by_name(GAME_PROCESS_NAME)
            sleep(2)

            self.launch()
        else:
            return "No 'game_path' provided field in the config"

    def prepare(self):
        self.window = resize_window()
        calibrate_window()

    def get_entry(self, command_name):
        return self.entries[command_name]

    def task(self, name, cb, task_type="aside"):
        return lambda upd, ctx: self.taskManager.add(name, lambda: cb(upd, ctx), props={
            'onDone': upd.message.reply_text,
            'onError': upd.message.reply_text,
            'type': task_type,
        })

    # def run(self):
    #     self.prepare()
    #     _dungeons = []
    #
    #     log('Executing automatic scenarios...')
    #     start_time = datetime.now()
    #
    #     # Looping: Tasks List
    #     for i in range(len(self.config['tasks'])):
    #         task = self.config['tasks'][i]
    #         task_name = task['task'].lower()
    #         log('BOT is starting the TASK: ' + task_name.upper())
    #
    #         # Run instance
    #         instance_task = self.get_entry(task_name)['instance']
    #         instance_task.run()
    #
    #         # Looping: After Each List
    #         if 'after_each' in self.config:
    #             for j in range(len(self.config['after_each'])):
    #                 # After Each Item
    #                 aei = self.config['after_each'][j]
    #                 aei_name = aei.lower()
    #
    #                 log('BOT is starting the "after_each" action: ' + aei_name.upper())
    #
    #                 instance_after_each = self.get_entry(aei_name)['instance']
    #                 instance_after_each.run()
    #
    #     self.report()
    #
    #     duration = 'Duration: {}'.format(datetime.now() - start_time)
    #     log('All scenarios are done!')
    #
    #     # self.kill()
    #
    #     return duration
