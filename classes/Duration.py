from datetime import datetime, timedelta


class Duration:
    def __init__(self):
        self.durations = []

    def _format(self, duration):
        return str(duration).split('.')[0]

    def get_last(self):
        last = self.durations[len(self.durations) - 1]
        return self._format(timedelta() + last['end'] - last['start'])

    def get_total(self, durations=None):
        if durations is None:
            durations = self.durations

        total_duration = timedelta()
        for item in durations:
            if item['start'] is not None and item['end'] is not None:
                total_duration += item['end'] - item['start']

        return self._format(total_duration)

    def _update(self, variant, duration=None):
        # variant = start | end
        if duration is None:
            duration = datetime.now()
        self.durations[len(self.durations) - 1][variant] = duration

    def _create(self):
        self.durations.append({'start': None, 'end': None})

    def start(self):
        self._create()
        self._update(variant='start')

    def end(self):
        self._update(variant='end')
