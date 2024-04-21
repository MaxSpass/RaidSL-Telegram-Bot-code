from helpers.common import *
from classes.Feature import Feature


class TestFeature(Feature):
    def __init__(self, app, props=None):
        Feature.__init__(self, feature_name='Test feature', app=app)
        self.event_dispatcher.subscribe('run', self._run)
        self.seconds = 3600

        if props is not None:
            if 'seconds' in props:
                self.seconds = props['seconds']


    def _run(self, props=None):
        counter = 0
        while counter < self.seconds:
            self.log(counter)
            counter += 1
            sleep(1)

    def report(self):
        return None
