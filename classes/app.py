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
        r1 = arena_live.report()
        r2 = arena_classic.report()
        r3 = arena_tag.report()
        if r1 is not None or r2 is not None or r3 is not None:
            log('================   Report   ================')
            if r1:
                log(r1)
            if r2:
                log(r2)
            if r3:
                log(r3)
            log('================   Report   ================')

    def kill(self, *args):
        log('App is terminated')
        sys.exit(0)

    def start(self):
        atexit.register(self.exit)
        signal.signal(signal.SIGINT, self.kill)
        signal.signal(signal.SIGTERM, self.kill)
        prepare_window()

    def run(self):
        log('Executing automatic scenarios...')
        start_time = datetime.now()

        # Tasks
        for i in range(len(self.config['tasks'])):
            item = self.config['tasks'][i]
            item_name = item['name']
            item_props = None

            if 'props' in item:
                item_props = item['props']

            log('BOT is starting the task: ' + item_name)

            if item_name == 'arena_live':
                arena_live.run(props=item_props)
            elif item_name == 'arena_classic':
                arena_classic.run(props=item_props)
            elif item_name == 'arena_tag':
                arena_tag.run(props=item_props)
            elif item_name == 'demon_lord':
                demon_lord()
            elif item_name == 'faction_wars':
                faction_wars()
            elif item_name == 'iron_twins':
                iron_twins_fortress()

        # After Each Task
        for i in range(len(self.config['after_each'])):
            item = self.config['after_each'][i]
            item_name = item['name']

            if item_name == 'check_rewards':
                rewards.quests_run()
                rewards.play_time_run()



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
        print('Duration: {}'.format(datetime.now() - start_time))