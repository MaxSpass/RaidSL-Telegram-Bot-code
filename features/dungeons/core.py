from helpers.common import *
from more_itertools import first_true

DUNGEON_IRON_TWINS = "Iron Twins Fortress"
DUNGEON_MINOTAUR = "Minotaur's Labyrinth"
DUNGEON_GOLEM = "Ice Golem's Peak"
DUNGEON_SPIDER = "Spider's Den"
DUNGEON_DRAGON = "Dragon's Lair"
DUNGEON_FIRE = "Fire Knight's Castle"
DUNGEON_SAND_DEVIL = "Sand Devil's Necropolis"
DUNGEON_PHANTOM = "Phantom Shogun's Grove"

DUNGEON_LOCATIONS = [
    # @TODO Not implemented yet
    # special case for Iron Twin | currently it's a different file
    # {
    #     'name': DUNGEON_IRON_TWINS,
    #     'swipe': 0,
    #     'click': {'x': 280, 'y': 230}
    # },
    {
        'name': DUNGEON_MINOTAUR,
        'swipe': 1,
        'click': {'x': 420, 'y': 300}
    },
    {
        'name': DUNGEON_GOLEM,
        'swipe': 1,
        'click': {'x': 540, 'y': 160}
    },
    {
        'name': DUNGEON_SPIDER,
        'swipe': 1,
        'click': {'x': 680, 'y': 300}

    },
    {
        'name': DUNGEON_DRAGON,
        'swipe': 1,
        'click': {'x': 775, 'y': 175}
    },
    {
        'name': DUNGEON_FIRE,
        'swipe': 2,
        'click': {'x': 490, 'y': 300}
    },
    {
        'name': DUNGEON_SAND_DEVIL,
        'swipe': 2,
        'click': {'x': 650, 'y': 170}
    },
    {
        'name': DUNGEON_PHANTOM,
        'swipe': 2,
        'click': {'x': 810, 'y': 340}
    },
]

check_box_super_raid = [655, 336, [108, 237, 255]]
refill_paid = [440, 376, [255, 33, 51]]
defeat = [443, 51, [229, 40, 104]]


# props
# { 'String', [ Int, 'battle' | 'energy' ], {
# refill_force: Boolean,
# refill_max: Int,
# difficulty: 'normal' | 'hard'
# enable_super_raid: Boolean
# }}

# @TODO
# - passing 'difficulty' and 'enable_super_raid'
# - choosing certain lvl/stage for each dungeon
class DungeonCore:
    counter = 0
    tracker = []
    terminate = False

    counter_runs = 0
    counter_energy = 0

    # define in constructor
    dungeon = None
    strategy = [0, 0]
    refill_force = False
    refill_max = 0

    # define while initialization
    location = None
    runs = 0
    # 'battle' | 'energy'
    count_by = 'battle'

    def __init__(self, dungeon, strategy=None, props=None):
        self.dungeon = dungeon

        if strategy is not None:
            self.strategy = strategy

        if props is not None:
            if props.refill_force is not None:
                self.refill_force = props.refill_force
            if props.refill_max is not None:
                self.refill_max = props.refill_max

        if self.strategy is None:
            if self.strategy == '*':
                # @TODO
                log('Not implemented yet. Please specify amount runs or energy')
            else:
                self.strategy = strategy

        self._initialization()

    def _initialization(self):
        self.location = self._get_location(self.dungeon)

        if 0 in self.strategy:
            self.runs = self.strategy[0]

        if 1 in self.strategy:
            self.count_by = self.strategy[1]

    def _get_location(self, name):
        return first_true(DUNGEON_LOCATIONS, pred=lambda el: el['name'] == name)

    def enter(self):
        battles_click()
        sleep(1)

        # enter all dungeons
        click(300, 300)

        length = self.location['swipe']
        for i in range(length):
            # moving to the certain dungeon
            swipe('right', 850, 400, 800, speed=.5)
            x = self.location['click']['x']
            y = self.location['click']['y']
            # click on dragon icon
            click(x, y)
            sleep(1)

        # swiping bottom
        swipe('bottom', 500, 450, 400, speed=.5)

        # click last floor
        click(850, 475)
        sleep(.5)

        # @TODO validate
        if not pixel_check_new(check_box_super_raid, mistake=10):
            x = check_box_super_raid[0]
            y = check_box_super_raid[1]
            click(x, y)
            sleep(.3)

    def attack(self):
        def _start_battle():
            if self.counter == 0:
                # click on 'Start'
                click(850, 475)
            else:
                # click on 'Replay'
                dungeons_replay()
            sleep(2)

        _start_battle()

        # @TODO Ideally - to check the current energy amount as well
        # checking existing of paid refill
        if pixel_check_new(refill_paid, mistake=10):
            if self.count_by == 'battle':
                if self.refill_max > 0:
                    click(refill_paid[0], refill_paid[1])
                    sleep(1)
                    _start_battle()
                    self.refill_max -= 1
                else:
                    log('No more refill sacs - Terminate')
                    self.terminate = True
            elif self.count_by == 'energy':
                # @TODO In progress
                log('Not implemented yet!')
                if self.refill_force:
                    log('force refill')
                else:
                    log('No force refill - Terminate')
                    self.terminate = True

        # @TODO Test, considering with the code above
        waiting_battle_end_regular('Dragon battle End', x=28, y=88)
        sleep(1)

        result = not pixel_check_new(defeat)
        self.tracker.append(result)

    def finish(self):
        dungeons_results_finish()
        go_index_page()
        log('DONE - Dragon')
        log('Victory: ' + str(self.tracker.count(True)) + ' | ' + 'Defeat: ' + str(self.tracker.count(False)))

    def done(self):
        return not (self.counter < self.runs)

    def run(self):
        self.enter()

        while not self.done() and self.terminate is False:
            log('Dungeon battle ' + str(self.counter + 1) + ' is starting')
            self.attack()
            self.counter += 1

        self.finish()
