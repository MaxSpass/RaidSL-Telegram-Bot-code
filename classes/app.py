from helpers.common import *
from features.rewards.index import *
from features.live_arena.index import *
from features.arena.index import *
from features.demon_lord.index import *
from features.faction_wars.index import *
from features.iron_twins_fortress.index import *
from features.dungeons.index import *
from features.hydra.index import *
from io import BytesIO
import atexit
import signal
import sys
import pytesseract

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
}

def prepare_window():
    BURGER_POSITION = [15, 282]
    GAME_WINDOW = 'Raid: Shadow Legends'
    is_prepared = False
    wins = pyautogui.getWindowsWithTitle(GAME_WINDOW)
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
            log('No Burger needle found')
    else:
        log('No RAID window found')

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

    def _prepare_config(self, config_json):
        _config = {
            'start_immediate': True,
            'tasks': [],
            'after_each': []
        }

        if 'start_immediate' in config_json:
            _config['start_immediate'] = bool(config_json['start_immediate'])

        if 'telegram_token' in config_json:
            _config['telegram_token'] = str(config_json['telegram_token'])

        # Tasks
        commands_length = len(config_json['tasks'])
        if commands_length:
            for i in range(commands_length):
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
                                'instance': INSTANCES_MAP[_task](_props),
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

        # After each commands
        if 'after_each' in config_json:
            _config['after_each'] = config_json['after_each']

        return _config

    def validation(self):
        # primitive validation
        currentYear = datetime.now().year
        currentMonth = datetime.now().month
        return currentYear == 2024 and (currentMonth <= 3)

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

    def report(self):
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

    def relogin(self):
        # limit in seconds
        limit = 120
        timeout = 3
        counter = 0

        click(425, 300)
        time.sleep(2)

        burger = find_needle_burger()
        while burger is None and counter < limit:
            time.sleep(timeout)
            counter += timeout
            burger = find_needle_burger()

        if burger:
            return True
        else:
            error = "Can't relogin"
            log(error)

    def screen(self):
        WINDOW_TOP_BAR_HEIGHT = 25
        BORDER_WIDTH = 7

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

    def start(self):
        # atexit.register(self.report)
        signal.signal(signal.SIGINT, self.kill)
        signal.signal(signal.SIGTERM, self.kill)
        # prepare_window()

    def prepare(self):
        self.window = prepare_window()

    def get_entry(self, command_name):
        return self.entries[command_name]

    def run(self):
        self.prepare()
        _dungeons = []

        log('Executing automatic scenarios...')
        start_time = datetime.now()

        # Looping: Tasks List
        for i in range(len(self.config['tasks'])):
            task = self.config['tasks'][i]
            task_name = task['task'].lower()
            log('BOT is starting the TASK: ' + task_name.upper())

            # Run instance
            instance_task = self.get_entry(task_name)['instance']
            instance_task.run()

            # Looping: After Each List
            if 'after_each' in self.config:
                for j in range(len(self.config['after_each'])):
                    # After Each Item
                    aei = self.config['after_each'][j]
                    aei_name = aei.lower()

                    log('BOT is starting the "after_each" action: ' + aei_name.upper())

                    instance_after_each = self.get_entry(aei_name)['instance']
                    instance_after_each.run()

        self.report()

        duration = 'Duration: {}'.format(datetime.now() - start_time)
        log('All scenarios are done!')

        # self.kill()

        return duration
