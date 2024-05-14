from classes.Location import Location
from helpers.common import *
from locations.live_arena.index import E_VICTORY, E_DEFEAT

rgb_grey = [127, 127, 127]
rgb_light_blue = [0, 162, 232]
x = 0
y = 300
width = 250
height = 250
region = [x, y, width, height]

# These events work with an image: 'images/for_test/test_await_image.jpg'
event_grey = {
    "name": 'Grey | Pixel Check',
    "expect": lambda: pixel_check_new([x + 50, y + 50, rgb_grey], mistake=10),
}
event_blue = {
    "name": 'Blue | RGB Check',
    "expect": lambda: rgb_check(rgb_light_blue, dominant_color_rgb(region=region, reverse=False), mistake=10),
}
event_needle = {
    "name": 'Needle Check',
    "expect": lambda: find_needle('market_mystery_shard.jpg', region=region),
    "interval": 5
}


class TestAwait(Location):
    def __init__(self, app, props=None):
        Location.__init__(self, name='Test await', app=app)

        self.event_dispatcher.subscribe('run', self._run)

    def _run(self, *args):
        print('RUN: TestAwait')

        res = self.awaits(
            events=[
                E_VICTORY,
                E_DEFEAT,
                event_grey,
                event_blue,
                event_needle],
            interval=.5
        )

        print(f"Data: {res['data']}")
