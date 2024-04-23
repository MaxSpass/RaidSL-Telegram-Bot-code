from datetime import datetime


class Duration:
    def __init__(self):
        self.durations = []

    def update(self, variant, duration=datetime.now()):
        # variant = start | end
        self.durations[len(self.durations) - 1][variant] = duration

    def get_last(self):
        last = self.durations[len(self.durations) - 1]
        start = last['start']
        end = last['end']
        return str(end - start).split('.')[0]

    def get_total(self):
        first = self.durations[0]
        last = self.durations[len(self.durations) - 1]
        start = first['start']
        end = last['end']
        return str(end - start).split('.')[0]

    def create(self):
        self.durations.append({})
