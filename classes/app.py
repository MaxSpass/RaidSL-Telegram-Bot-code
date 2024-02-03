from helpers.common import *
from features.rewards.index import *
from features.live_arena.index import *
from features.arena.index import *
from features.demon_lord.index import *
from features.faction_wars.index import *
from features.iron_twins_fortress.index import *
from features.dungeons.index import *
from features.hydra.index import *
import atexit
import signal
import sys
import pytesseract

CONFIG_PATH = "config.json"

arena_live = ArenaLive()
arena_classic = ArenaClassic()
arena_tag = ArenaTag()
demon_lord = DemonLord()
hydra = Hydra()
dungeons = Dungeons()
faction_wars = FactionWars()
iron_twins = IronTwins()
rewards = Rewards()

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
    WINDOW_SIZE = [920, 540]
    BURGER_POSITION = [15, 282]
    GAME_WINDOW = 'Raid: Shadow Legends'
    is_prepared = False
    wins = pyautogui.getWindowsWithTitle(GAME_WINDOW)
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
        go_index_page()

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
            go_index_page()
        else:
            log('No Burger needle found')

    else:
        log('No RAID window found')

    if not is_prepared:
        raise Exception("Game windows is NOT prepared")


class App:
    def __init__(self):
        self.config = None
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

        # Tasks
        tasks_length = len(config_json['tasks'])
        if tasks_length:
            for i in range(tasks_length):
                task = config_json['tasks'][i]
                if 'enable' not in task or bool(task['enable']):
                    _name = task['name'].lower()
                    _props = task['props'] if 'props' in task else None

                    task_d = {'name': _name, 'props': _props}

                    # task_d['props'] = task['props']

                    # accumulated instances
                    if _name in INSTANCES_MAP and _name not in self.entries:
                        # @TODO should take from memory later on
                        self.entries[_name] = {
                            'instance': INSTANCES_MAP[_name](_props),
                        }

                    _config['tasks'].append(task_d)

        # After each tasks
        after_each_length = len(config_json['after_each'])
        if after_each_length:
            for i in range(after_each_length):
                task = config_json['after_each'][i]
                for key, val in task.items():
                    if bool(val):
                        _config['after_each'].append({
                            'name': key
                        })

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
            res = '\n================   Report   ================\n'
            for i in range(len(reports)):
                report = reports[i]
                if report:
                    res += f'{report}\n'
            res += '================   Report   ================\n'

        if res:
            log(res)

        return res

    def kill(self, *args):
        log('App is terminated')
        input('Confirm by pressing any key')
        sys.exit(0)

    def start(self):
        # atexit.register(self.report)
        signal.signal(signal.SIGINT, self.kill)
        signal.signal(signal.SIGTERM, self.kill)
        # prepare_window()
        return 0

    def prepare(self):
        prepare_window()
        return 1

    def get_entry(self, entry_name, prepare=False):
        # if prepare:
        #     self.prepare()

        return self.entries[entry_name]

    def run(self, *args):
        self.prepare()
        _dungeons = []

        log('Executing automatic scenarios...')
        start_time = datetime.now()

        # Looping: Tasks List
        for i in range(len(self.config['tasks'])):
            task = self.config['tasks'][i]
            task_name = task['name'].lower()
            log('BOT is starting the TASK: ' + task_name.upper())

            # Run instance
            instance = self.get_entry(task_name)['instance']
            instance.run()

            # Looping: After Each List
            for j in range(len(self.config['after_each'])):
                # After Each Item
                aei = self.config['after_each'][j]
                aei_name = aei['name'].lower()

                log('BOT is starting the "after_each" action: ' + aei_name.upper())

                # @TODO Refactor
                if aei_name == 'check_rewards':
                    rewards.run()

        # @TODO Test
        self.report()

        duration = 'Duration: {}'.format(datetime.now() - start_time)
        log('All scenarios are done!')

        # self.kill()

        return duration
