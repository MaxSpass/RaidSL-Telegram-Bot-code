from datetime import datetime, timedelta


class Duration:
    def __init__(self):
        self.durations = []

    def _format(self, duration):
        return str(duration).split('.')[0]

    def get_last(self):
        last = self.durations[len(self.durations) - 1]
        return self._format(timedelta() + last[1] - last[0])

    def get_total(self, durations=None):
        if durations is None:
            durations = self.durations

        total_duration = timedelta()
        for item in durations:
            if item[0] is not None and item[1] is not None:
                total_duration += item[1] - item[0]

        return self._format(total_duration)

    def _update(self, stage, duration=None):
        # variant = start | end
        if duration is None:
            duration = datetime.now()
        self.durations[len(self.durations) - 1][stage] = duration

    def _create(self):
        self.durations.append([None, None])

    def start(self):
        self._create()
        self._update(stage=0)

    def end(self):
        self._update(stage=1)
