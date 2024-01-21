from helpers.common import *
from features.hero_preset.index import *
import pyautogui

AVATAR_FRAME_WIDTH = 38
AVATAR_FRAME_HEIGHT = 56

STACK_FRAME_WIDTH = 180
STACK_FRAME_HEIGHT = 180

HEALTH_FRAME_WIDTH = 135
HEALTH_FRAME_HEIGHT = 10

COLOR_ALIVE = [221, 42, 42]
COLOR_DEAD = [175, 23, 200]

# x1, 44, x2, 94
HEADS_POSITIONS = [
    {
        'avatar': {'x': 15, 'y': 42},
        'health': {'x': 56, 'y': 82},
        'focus': {'x': 207},
        'stack': {'x': 15, 'y': 96}
    },
    {
        'avatar': {'x': 232, 'y': 42},
        'health': {'x': 273, 'y': 82},
        'focus': {'x': 358},
        'stack': {'x': 232, 'y': 96}
    },
    {
        'avatar': {'x': 449, 'y': 42},
        'health': {'x': 491, 'y': 82},
        'focus': {'x': 516},
        'stack': {'x': 449, 'y': 96}
    },
    {
        'avatar': {'x': 666, 'y': 42},
        'health': {'x': 708, 'y': 82},
        'focus': {'x': 675},
        'stack': {'x': 666, 'y': 96}
    }
]
HYDRA_DATA = {
    '1': {'swipes': 0, 'x': 616, 'y': 140, 'min_damage': 6.66},
    '2': {'swipes': 0, 'x': 616, 'y': 270, 'min_damage': 20.4},
    '3': {'swipes': 0, 'x': 616, 'y': 390, 'min_damage': 29.4},
    '4': {'swipes': 1, 'x': 616, 'y': 350, 'min_damage': 36.6},
}
HEADS = [
    {'name': 'head_of_blight', 'needle': 'hydra/head_of_blight.png'},
    {'name': 'head_of_decay', 'needle': 'hydra/head_of_decay.png'},
    {'name': 'head_of_mischief', 'needle': 'hydra/head_of_mischief.png'},
    {'name': 'head_of_suffering', 'needle': 'hydra/head_of_suffering.png'},
    {'name': 'head_of_torment', 'needle': 'hydra/head_of_torment.png'},
    {'name': 'head_of_wrath', 'needle': 'hydra/head_of_wrath.png'},
]

DEFAULT_TEAM_PRESET = 1
DEFAULT_ACCEPT_DAMAGE = 0
DEFAULT_PRIORITY = {'head_of_decay': 2, 'head_of_blight': 1}
DEFAULT_RUNS_LIMIT = 2
DEFAULT_RUNS_LIMIT_MAX = 10

# pause icon is on the top/right corner
icon_pause = [866, 66, [216, 206, 156]]
icon_auto = [50, 470, [20, 30, 37]]

button_battle = [855, 455, [165, 113, 8]]
button_start = [855, 455, [212, 155, 5]]
button_free_regroup = [680, 480, [22, 124, 156]]
button_keep_result = [860, 480, [187, 130, 5]]

clash_not_started = [560, 350, [187, 130, 5]]
start_on_auto = [710, 410, [108, 237, 255]]
battle_end = [26, 90, [255, 255, 255]]

screen_all_hydra = [526, 81, [254, 223, 90]]
screen_certain_hydra = [447, 304, [14, 42, 64]]

preset = HeroPreset()


class Hydra:
    LOCATION_NAME = 'Hydra'

    def __init__(self, props=None):
        self.runs = []
        self.runs_limit = DEFAULT_RUNS_LIMIT
        self.heads = []
        self.results = {}
        self.current = None
        self.focused_head = None

        self.apply_props(props)

    def _get_priority(self, head_name):
        priority = self.current['priority']
        has_priority = head_name in priority
        if priority is None or head_name == 'dead_hydra' or not has_priority:
            return 0

        if has_priority:
            return priority[head_name]

    def _save_result(self, int_damage):
        stage = self.current['stage']

        self.results[stage]['keys'] += 1
        self.results[stage]['damage'] += int_damage

    def _proceed_end(self):
        stage = self.current['stage']
        min_damage = self.current['min_damage']
        int_damage = read_dealt_damage()
        self.current['runs_counter'] += 1

        self.results[stage]['counter'] = self.current['runs_counter']

        log('Damage Dealt: ' + str(int_damage) + 'M')
        if int_damage >= min_damage:
            log(self.LOCATION_NAME + ' | Dealt Damage is enough')
            # @TODO Temp
            await_click([button_keep_result], timeout=1)
            self._save_result(int_damage)
        else:
            log(self.LOCATION_NAME + ' | Dealt Damage is NOT enough')
            # @TODO Temp
            await_click([button_free_regroup], timeout=1)


    def _check_end(self):
        return pixel_check_new(battle_end)

    def _sort_by_priority(self, queue):
        p1 = []
        p2 = []
        for i in range(len(queue)):
            el = queue[i]
            if el['reason'] == 1:
                p1.append(el)
            elif el['reason'] == 2:
                p2.append(el)

        # sorting by exist priority
        queue_sorted = sorted(p2, key=lambda x: (-x.get('priority', 0), x.get('priority', 0)))
        # filter by priority > 0
        queue_filtered = list(filter(lambda x: 'priority' in x and x.get('priority') > 0, queue_sorted))

        new_queue = p1 + queue_filtered

        return new_queue

    def _focus_head(self, name):
        self.focused_head = name
        i, hydra = find(self.heads, lambda x: x['name'] == name)
        name = hydra['name']
        h = HEADS_POSITIONS[i]
        click(h['focus']['x'], 175)
        log(self.LOCATION_NAME + ' | Focus: ' + self._format_name(name))

    def _reset_focus(self):
        pyautogui.click(x=50, y=470, clicks=2, interval=.1)
        log(self.LOCATION_NAME + ' | Reset focus')

    def _format_name(self, name):
        return name.replace('_', ' ').title()

    def _while_stage_available(self):
        stage = self.current['stage']
        return self.current['runs_counter'] < self.runs_limit \
               or self.current['min_damage'] < self.results[stage]['damage']

    def _certain_hydra_or_all_hydra_screens(self):
        # @TODO
        return pixels_wait([screen_certain_hydra, screen_all_hydra], msg="Certain Hydra/All Hydra",
                           timeout=2, mistake=10)

    def _update_heads(self):
        prev_heads = self.heads
        current_heads = []
        for i in range(len(HEADS_POSITIONS)):
            el = HEADS_POSITIONS[i]
            avatar = el['avatar']
            health = el['health']
            stack = el['stack']
            hydra_name = 'dead_hydra'

            # determining is alive hydra
            x_health = health['x']
            y_health = health['y']

            # determining hydra heads
            x_avatar = avatar['x']
            y_avatar = avatar['y']
            region_avatar = [x_avatar, y_avatar, AVATAR_FRAME_WIDTH, AVATAR_FRAME_HEIGHT]
            for j in range(len(HEADS)):
                name = HEADS[j]['name']
                needle = HEADS[j]['needle']
                avatar_position = find_needle(needle, region=region_avatar, confidence=.55)
                if avatar_position is not None:
                    hydra_name = name
                    break

            # determining is_digesting
            x_stack = stack['x']
            y_stack = stack['y']
            region_stack = [x_stack, y_stack, STACK_FRAME_WIDTH, STACK_FRAME_HEIGHT]
            digesting_position = find_needle('hydra/hydra_digesting.png', region=region_stack, confidence=.55)

            current_heads.append({
                'name': hydra_name,
                'priority': self._get_priority(hydra_name),
                'is_digesting': digesting_position is not None,
                'is_alive': pixel_check_new([x_health, y_health, COLOR_ALIVE]),
            })

        # @TODO Should fix when BOT does not change focus from non-is_digesting hydra
        # prev state equals current state
        self.heads = current_heads

        # for first population
        if not len(prev_heads):
            prev_heads = current_heads

        return {
            'prev': prev_heads,
            'current': current_heads,
        }

    def _prepare_run_props(self, run):
        stage = str(run['stage'])

        self.results[stage] = {
            'keys': 0,
            'damage': 0,
            'counter': 0
        }

        self.current = {
            'stage': stage,
            'team_preset': DEFAULT_TEAM_PRESET,
            'min_damage': DEFAULT_ACCEPT_DAMAGE,
            'priority': DEFAULT_PRIORITY,
            'runs_counter': 0
        }

        if 'team_preset' in run:
            self.current['team_preset'] = int(run['team_preset'])
        if 'min_damage' in run:
            self.current['min_damage'] = int(run['min_damage'])
        if 'priority' in run:
            self.current['priority'] = run['priority']

        return self.current

    def apply_props(self, props=None):
        if props is not None:
            if 'runs' in props:
                self.runs = props['runs']
            if 'runs_limit' in props:
                limit = int(props['runs_limit'])
                if limit > DEFAULT_RUNS_LIMIT_MAX:
                    limit = DEFAULT_RUNS_LIMIT_MAX
                self.runs_limit = limit

    def enter(self):
        go_index_page()
        click_on_progress_info()
        # Hydra Keys
        click(600, 340)
        sleep(1)

    def report(self):
        res = None
        for key, value in self.results.items():
            if res is None:
                res = 'Hydra Report\n'

            line_1 = f'{key} hydra | {value["keys"]} keys used'
            line_2 = f'{value["damage"]}M dd in {value["counter"]} attempts'

            res += line_1 + ' | ' + line_2 + '\n'

        return res

    def finish(self):
        go_index_page()
        log('DONE - ' + self.LOCATION_NAME)
        log(self.results)

    def scan(self):
        queue = []
        reset = False

        # Test
        # self.focused_head = 'head_of_decay'
        # queue = [{'name': 'head_of_blight', 'reason': 1, 'priority': 1}]

        while not self._check_end():
            heads = self._update_heads()
            state_prev = heads['prev']
            state_current = heads['current']

            if len(state_current):
                for i in range(len(state_current)):
                    prev_state = state_prev[i]
                    current_state = state_current[i]
                    name = current_state['name']
                    priority = current_state['priority']
                    digesting = not prev_state['is_digesting'] and current_state['is_digesting']
                    has_priority = 'priority' in current_state and current_state['priority'] > 0
                    not_digesting = prev_state['is_digesting'] and not current_state['is_digesting']
                    is_not_focused = self.focused_head != name
                    is_alive = current_state['is_alive']
                    become_dead = prev_state['is_alive'] and not current_state['is_alive']

                    # Test
                    # if name == 'head_of_blight':
                    #     digesting = True

                    d, dl = find(queue, lambda x: x['name'] == name)
                    if d is None:
                        if is_alive and is_not_focused:
                            if digesting:
                                print('DIGESTING', name)
                                queue.append({
                                    'name': name,
                                    'reason': 1,
                                    'priority': priority
                                })
                                log(self.LOCATION_NAME + ' | Digestion head: ' + self._format_name(name))
                            elif has_priority:
                                log(self.LOCATION_NAME + ' | Priority head: ' + self._format_name(name))
                                queue.append({
                                    'name': name,
                                    'reason': 2,
                                    'priority': priority
                                })
                    elif become_dead or not_digesting:
                        queue.pop(d)
                        if become_dead:
                            log(self.LOCATION_NAME + ' | Died: ' + self._format_name(name))
                        elif not_digesting:
                            log(self.LOCATION_NAME + ' | Saved from digestion by: ' + self._format_name(name))

            queue = self._sort_by_priority(queue)
            print('queue', queue)

            if len(queue):
                name = queue[0]['name']

                if self.focused_head != name:
                    # self.focused_head = queue[0]
                    self._reset_focus()
                    self._focus_head(name)
                    reset = True
                    # queue_prev = queue
                    # if not len(queue_prev):
                    #     self._reset_focus()
            elif reset:
                reset = False
                self.focused_head = None
                self._reset_focus()
                # queue_prev = []

        self._proceed_end()
        # avoid sudden popup
        sleep(5)

    def attack(self):
        def hydra_enter(data):
            swipes = data['swipes']
            x = data['x']
            y = data['y']

            for i in range(swipes):
                swipe('bottom', 616, 400, 350, speed=.3, sleep_after_end=.3)

            click(x, y)

            await_click([button_battle], timeout=1, mistake=10)

            # @TODO Skip not started clash
            if True:
                await_click([clash_not_started], timeout=1, mistake=10, wait_limit=2)

        def hydra_start():
            while self._while_stage_available():

                # skips then logic, when all_hydra_screen appears
                is_certain = self._certain_hydra_or_all_hydra_screens()[0]
                if is_certain:

                    preset.choose(team_preset)

                    if not pixel_check_new(start_on_auto, mistake=10):
                        click(start_on_auto[0], start_on_auto[1])

                    log('Scanning all heads...')
                    await_click([button_start], timeout=1, mistake=10)

                    if pixels_wait([icon_pause], timeout=2, mistake=10)[0]:
                        log(self.LOCATION_NAME + ' | ' + 'Battle just started')
                        self.scan()


        for i in range(len(self.runs)):
            if 'skip' in self.runs[i] and bool(self.runs[i]['skip']):
                continue

            self.current = self._prepare_run_props(self.runs[i])
            stage = self.current['stage']
            team_preset = self.current['team_preset']

            # damage = self.results[stage]['damage']
            # keys = self.results[stage]['keys']

            if stage in HYDRA_DATA:

                screens = self._certain_hydra_or_all_hydra_screens()

                if screens[0]:
                    log(self.LOCATION_NAME + ' | ' + 'All Hydra')
                    hydra_start()
                elif screens[1]:
                    log(self.LOCATION_NAME + ' | ' + 'Certain Hydra')
                    hydra_enter(HYDRA_DATA[stage])
                    hydra_start()

                if self._certain_hydra_or_all_hydra_screens()[0]:
                    close_popup()

    def run(self, props):
        self.apply_props(props)

        self.enter()
        self.attack()

        self.finish()

        go_index_page()
