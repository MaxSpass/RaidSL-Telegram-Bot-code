from helpers.common import *
from features.rewards.index import *
from features.live_arena.index import *
from features.arena.index import *
from features.demon_lord.index import *
from features.faction_wars.index import *
from features.iron_twins_fortress.index import *
import atexit
import signal
import sys

CONFIG_PATH = "config.json"

rewards = Rewards()
arena_live = ArenaLive()
arena_classic = ArenaClassic()
arena_tag = ArenaTag()
demon_lord = DemonLord()


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
        self.read_config()

    def _prepare_config(self, config_json):
        _config = {
            'tasks': [],
            'after_each': []
        }

        # Tasks
        tasks_length = len(config_json['tasks'])
        if tasks_length:
            for i in range(tasks_length):
                task = config_json['tasks'][i]
                if 'enable' not in task or bool(task['enable']):
                    task_d = {
                        'name': task['name']
                    }

                    if 'props' in task:
                        task_d['props'] = task['props']

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


        log(_config)
        return _config

    def load_config(self, config):
        self.config = self._prepare_config(config)
        log('Load App Config')

    def read_config(self):
        try:
            with open(CONFIG_PATH) as config_file:
                config = json.load(config_file)
                self.config = self._prepare_config(config)
                log('Read App Config')

        except SystemError:
            log('An error occurred while reading ' + CONFIG_PATH + ' file')

    def exit(self):
        entries = list(map(lambda x: x.report(), [
            arena_live,
            arena_classic,
            arena_tag,
            rewards,
            demon_lord,
        ]))

        if entries.count(None) < len(entries):
            log('================   Report   ================')
            for i in range(len(entries)):
                report = entries[i]
                if report:
                    log(report)
            log('================   Report   ================')

    def kill(self, *args):
        log('App is terminated')
        input('Confirm by pressing any key')
        sys.exit(0)

    def start(self):
        atexit.register(self.exit)
        signal.signal(signal.SIGINT, self.kill)
        signal.signal(signal.SIGTERM, self.kill)
        prepare_window()

    def run(self):
        log('Executing automatic scenarios...')
        start_time = datetime.now()

        # Looping: Tasks List
        for i in range(len(self.config['tasks'])):
            # Task Item
            ti = self.config['tasks'][i]
            ti_name = ti['name'].lower()
            ti_props = None

            if 'props' in ti:
                ti_props = ti['props']

            log('BOT is starting the TASK: ' + ti_name.upper())

            # @TODO Refactor
            if ti_name == 'arena_live':
                arena_live.run(props=ti_props)
            elif ti_name == 'arena_classic':
                arena_classic.run(props=ti_props)
            elif ti_name == 'arena_tag':
                arena_tag.run(props=ti_props)
            elif ti_name == 'demon_lord':
                demon_lord.run()
            elif ti_name == 'faction_wars':
                faction_wars()
            elif ti_name == 'iron_twins':
                iron_twins_fortress()

            # Looping: After Each List
            for j in range(len(self.config['after_each'])):
                # After Each Item
                aei = self.config['after_each'][j]
                aei_name = aei['name'].lower()

                log('BOT is starting the "after_each" action: ' + aei_name.upper())

                # @TODO Refactor
                if aei_name == 'check_rewards':
                    rewards.run()

        # demon_lord()
        # arena_live.run()

        # arena_live.run()
        # arena_classic.run()
        # arena_tag.run()

        # arena_classic.run()
        # arena_tag.run()
        # rewards.quests_run()
        # faction_wars()
        # rewards.play_time_run()
        # iron_twins_fortress()
        # arena_tag.run()

        # DungeonCore(DUNGEON_FIRE, [65], props={
        #     'allow_super_raid': True
        # }).run()

        log('All scenarios are done!')
        log('Duration: {}'.format(datetime.now() - start_time))

        # @TODO Test
        self.exit()
        self.kill()
