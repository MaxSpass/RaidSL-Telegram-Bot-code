from helpers.common import *
from classes.Location import Location


class TestFeature(Location):
    def __init__(self, app, props=None):
        Location.__init__(self, name='Test feature', app=app)
        self.event_dispatcher.subscribe('run', self._run)
        self.seconds = 3600

        if props is not None:
            if 'seconds' in props:
                self.seconds = props['seconds']

    def _run(self, props=None):
        counter = 0
        while counter < self.seconds and not self.terminate:
            self.log(counter)
            counter += 1
            sleep(1)

    def report(self):
        return None
