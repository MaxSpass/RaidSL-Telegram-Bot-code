from helpers.common import *
from features.hero_preset.index import *
from classes.Feature import Feature
import pyautogui

AVATAR_FRAME_WIDTH = 38
AVATAR_FRAME_HEIGHT = 56

STACK_FRAME_WIDTH = 180
STACK_FRAME_HEIGHT = 180

HEALTH_FRAME_WIDTH = 135
HEALTH_FRAME_HEIGHT = 10

COLOR_ALIVE = [221, 42, 42]
COLOR_DEAD = [175, 23, 200]

# auto button (bottom/left corner)
BUTTON_AUTO_PIXEL_DISABLED = [47, 460, [206, 174, 66]]
BUTTON_AUTO_REGION = axis_to_region(22, 479, 76, 496)
BUTTON_AUTO_HUE_ACTIVE = 65
BUTTON_AUTO_HUE_DISABLED = 17

# pause button (top/right corner)
BUTTON_PAUSE = [866, 66, [216, 206, 156]]
BUTTON_AUTO = [50, 470, [20, 30, 37]]

HYDRA_HEADS = [
    {'name': 'head_of_blight', 'needle': 'hydra/head_of_blight.png'},
    {'name': 'head_of_decay', 'needle': 'hydra/head_of_decay.png'},
    {'name': 'head_of_mischief', 'needle': 'hydra/head_of_mischief.png'},
    {'name': 'head_of_suffering', 'needle': 'hydra/head_of_suffering.png'},
    {'name': 'head_of_torment', 'needle': 'hydra/head_of_torment.png'},
    {'name': 'head_of_wrath', 'needle': 'hydra/head_of_wrath.png'},
]

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

HYDRA_LOCATIONS = {
    '1': {'swipes': 0, 'x': 616, 'y': 140, 'min_damage': 6.66},
    '2': {'swipes': 0, 'x': 616, 'y': 270, 'min_damage': 20.4},
    '3': {'swipes': 0, 'x': 616, 'y': 390, 'min_damage': 29.4},
    '4': {'swipes': 1, 'x': 616, 'y': 350, 'min_damage': 36.6},
}

DEFAULT_TEAM_PRESET = 1
DEFAULT_ACCEPT_DAMAGE = 0
DEFAULT_PRIORITY = {'head_of_decay': 2, 'head_of_blight': 1}
DEFAULT_RUNS_LIMIT = 2
DEFAULT_RUNS_LIMIT_MAX = 10

button_battle = [855, 455, [165, 113, 8]]
button_start = [855, 455, [212, 155, 5]]
button_free_regroup = [680, 480, [22, 124, 156]]
button_keep_result = [860, 480, [187, 130, 5]]

clash_not_started = [560, 350, [187, 130, 5]]
start_on_auto = [710, 410, [108, 237, 255]]
battle_end = [26, 90, [255, 255, 255]]

screen_all_hydra = [526, 81, [254, 223, 90]]
screen_certain_hydra = [447, 304, [14, 42, 64]]

hero_preset = HeroPreset()


class Hydra(Feature):
    def __init__(self, app, props=None):
        Feature.__init__(self, name='Hydra', app=app, report_predicate=self._report)

        self.runs = []
        self.runs_limit = DEFAULT_RUNS_LIMIT
        self.heads = []
        self.results = {}
        self.current = None
        self.focused_head = None

        self.apply_props(props=props)

        self.event_dispatcher.subscribe('enter', self._enter)
        self.event_dispatcher.subscribe('run', self._run)

    def _report(self):
        res_list = []
        for key, value in self.results.items():
            part_1 = f'{key} hydra | {value["keys"]} keys used'
            part_2 = f'{value["damage"]}M dd in {value["counter"]} attempts'
            part_3 = ''

            if len(value["results"]):
                avg = round(sum(value["results"]) / len(value["results"]), 2)
                part_3 = f'Results: {value["results"]}, Avg: {avg}M'

            line = f"{part_1} | {part_2} | {part_3} \n"
            res_list.append(line)

        return res_list

    def _enter(self):
        click_on_progress_info()
        # Hydra Keys
        click(600, 340)
        sleep(1)

    def _run(self, props=None):
        if props is not None:
            self.apply_props(props=props)

        self.attack()

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

        if 'results' not in self.results[stage]:
            self.results[stage]['results'] = []
        self.results[stage]['results'].append(int_damage)

        self.log('Damage Dealt: ' + str(int_damage) + 'M')
        if int_damage >= min_damage:
            self.log('Dealt Damage is enough')
            await_click([button_keep_result], msg="await 'button_keep_result'", timeout=1, mistake=20)
            self._save_result(int_damage)
        else:
            self.log('Dealt Damage is NOT enough')
            await_click([button_free_regroup], msg="await 'button_free_regroup'", timeout=1, mistake=20)

    def _is_battle_finished(self):
        return pixel_check_new(battle_end)

    def _is_battle_in_progress(self):
        return pixel_check_new(BUTTON_PAUSE, mistake=10)

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
        if hydra is not None:
            name = hydra['name']
            h = HEADS_POSITIONS[i]
            click(h['focus']['x'], 175)
            self.log('Focus: ' + self._format_name(name))
        else:
            self.log(f'No Hydra head with name: {name}')

    def _reset_focus(self):
        if not self._is_battle_in_progress():
            self.log("Resetting focus is interrupted: no 'BUTTON_PAUSE' found")
            return

        # works with critically low FPS
        def _click():
            x = BUTTON_AUTO_PIXEL_DISABLED[0]
            y = BUTTON_AUTO_PIXEL_DISABLED[1]
            click(x, y)
            sleep(.1)

        if pixel_check_new(BUTTON_AUTO_PIXEL_DISABLED, mistake=10):
            _click()

        while not pixel_check_new(BUTTON_AUTO_PIXEL_DISABLED, mistake=10):
            _click()

        await_click([BUTTON_AUTO_PIXEL_DISABLED], mistake=10)
        self.log('Reset focus')

    def _format_name(self, name):
        return name.replace('_', ' ').title()

    def _while_stage_available(self):
        # @TODO Does not work correct
        stage = self.current['stage']
        can_continue = self.current['runs_counter'] < self.runs_limit \
                       and self.results[stage]['damage'] < self.current['min_damage']

        if can_continue:
            self.log('Can continue')
        else:
            self.log("Can't continue")

        return can_continue

    def _certain_hydra_or_all_hydra_screens(self):
        # wait_limit = 3600 * 5
        wait_limit = 60
        return pixels_wait(
            [screen_certain_hydra, screen_all_hydra],
            msg="Certain Hydra/All Hydra",
            timeout=2,
            mistake=10,
            wait_limit=wait_limit
        )

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
            for j in range(len(HYDRA_HEADS)):
                name = HYDRA_HEADS[j]['name']
                needle = HYDRA_HEADS[j]['needle']
                avatar_position = find_needle(needle, region=region_avatar, confidence=.55)
                if avatar_position is not None:
                    hydra_name = name
                    break

            # determining is_digesting
            x_stack = stack['x']
            y_stack = stack['y']
            region_stack = [x_stack, y_stack, STACK_FRAME_WIDTH, STACK_FRAME_HEIGHT]
            digesting_position = find_needle('hydra/hydra_digesting_new.png', region=region_stack, confidence=.6)

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

    def _get_team_preset(self):
        return self.current['team_preset'] if 'team_preset' in self.current else None

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

    def scan(self):
        self.log('Scanning all heads...')
        queue = []
        reset = False

        # Test
        # self.focused_head = 'head_of_decay'
        # queue = [{'name': 'head_of_blight', 'reason': 1, 'priority': 1}]

        while not self._is_battle_finished():
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
                                self.log('Digestion head: ' + self._format_name(name))
                                queue.append({
                                    'name': name,
                                    'reason': 1,
                                    'priority': priority
                                })
                            elif has_priority:
                                self.log('Priority head: ' + self._format_name(name))
                                queue.append({
                                    'name': name,
                                    'reason': 2,
                                    'priority': priority
                                })
                    elif become_dead or not_digesting:
                        queue.pop(d)
                        if become_dead:
                            self.log('Died: ' + self._format_name(name))
                        elif not_digesting:
                            self.log('Saved from digestion by: ' + self._format_name(name))

            queue = self._sort_by_priority(queue)
            self.log(queue)

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
            self.log('Internal method called - hydra_enter')
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
            # True is by default, because team_preset is optional
            is_picked = True

            while self._while_stage_available():
                self.log('Internal method called - hydra_start')
                # skips then logic, when all_hydra_screen appears
                is_certain = self._certain_hydra_or_all_hydra_screens()[0]
                if is_certain:
                    if 'team_preset' in self.current:
                        is_picked = hero_preset.choose(self.current['team_preset'])

                    if is_picked:
                        if not pixel_check_new(start_on_auto, mistake=10):
                            click(start_on_auto[0], start_on_auto[1])

                        await_click([button_start], timeout=1, mistake=10)

                        if pixels_wait([BUTTON_PAUSE], timeout=2, mistake=10, msg='Pause icon', wait_limit=100)[0]:
                            self.log('Battle just started')
                            self.scan()

            # depending on the case: saved damage/regroup the team
            if self._certain_hydra_or_all_hydra_screens()[0] and is_picked:
                self.log("Checking hydra screen after each iteration")
                close_popup()

        for i in range(len(self.runs)):
            if 'skip' in self.runs[i] and bool(self.runs[i]['skip']):
                continue

            self.current = self._prepare_run_props(self.runs[i])
            stage = self.current['stage']
            # team_preset = self.current['team_preset']

            # damage = self.results[stage]['damage']
            # keys = self.results[stage]['keys']

            if stage in HYDRA_LOCATIONS:
                screens = self._certain_hydra_or_all_hydra_screens()

                if screens[0]:
                    self.log('All Hydra')
                elif screens[1]:
                    self.log('Certain Hydra')
                    hydra_enter(HYDRA_LOCATIONS[stage])

                hydra_start()
