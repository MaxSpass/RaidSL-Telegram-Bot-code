from datetime import datetime


class Duration:
    def __init__(self):
        self.durations = []

    def _get(self, start, end):
        return str(end - start).split('.')[0]

    def _update(self, variant, duration=None):
        # variant = start | end
        if duration is None:
            duration = datetime.now()
        self.durations[len(self.durations) - 1][variant] = duration

    def _create(self):
        self.durations.append({})

    def get_last(self):
        last = self.durations[len(self.durations) - 1]
        start = last['start']
        end = last['end']
        return self._get(start, end)

    def get_total(self):
        first = self.durations[0]
        last = self.durations[len(self.durations) - 1]
        start = first['start']
        end = last['end']
        return self._get(start, end)

    def start(self):
        self._create()
        self._update(variant='start')

    def end(self):
        self._update(variant='end')
