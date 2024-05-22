from helpers.common import sleep, pixel_check_new, click, log, prepare_event
from datetime import datetime, timedelta
import numpy as np

NOT_FOUND_EVENT = 'EVENT_NOT_FOUND'
DUMMY_RESPONSE = {"name": NOT_FOUND_EVENT, "data": None}


class Foundation:
    E_BATTLE_END = {"name": "Battle end", "interval": 2}
    E_CONNECTION_ERROR = {"name": "No connection", "interval": 300, "blocking": False}

    def __init__(self, name, events=None):
        self.name = name
        self.stop = False
        #
        # if events is not None and type(events) is list:
        #     self.events = events

    def log(self, msg):
        log(f'{self.name} | {msg}')

    def awaits(self, events, interval=1):
        if self.stop:
            return DUMMY_RESPONSE

        response = None
        counter = 0
        time_tracker = {}
        limit_tracker = {}

        events_names_list = list(map(lambda el: el['name'], events))
        events_names_str = str(np.array(events_names_list, dtype=object))
        log(f"Events checking: {events_names_str}")

        # events = self._extend_by_core_events(events)
        while response is None and not self.stop:
            name = events[counter]['name']
            expect = events[counter]['expect']
            limit = int(events[counter]['limit']) if 'limit' in events[counter] else None
            if name not in limit_tracker:
                limit_tracker[name] = limit

            # Skips limited callbacks
            if limit_tracker[name] is None or limit_tracker[name] > 0:
                main_interval = events[counter]['interval'] if 'interval' in events[counter] else interval
                callback = events[counter]['callback'] if 'callback' in events[counter] else None
                blocking = bool(events[counter]['blocking']) \
                    if 'blocking' in events[counter] else True

                current_time = datetime.now()
                last_call_time = time_tracker.get(name, None)

                if last_call_time is None or current_time - last_call_time >= timedelta(seconds=main_interval):
                    # Call the function and update last call time
                    time_tracker[name] = current_time

                    res = expect()
                    if bool(res):
                        log(f'Event occurred: {name}')

                        if blocking:
                            response = {"name": name, "data": res}

                        if callback is not None:
                            callback(res)

                        # Tracks limited events
                        if limit_tracker[name] is not None:
                            limit_tracker[name] = limit_tracker[name] - 1


                        # @TODO No essential solution found | Temp commented
                        # sub_items = events[counter]['children'] \
                        #     if 'children' in events[counter] \
                        #     else None
                        # if sub_items:
                        #     log('Sub-items')
                        #     events_sub_items = self.awaits(
                        #         events=sub_items['events'],
                        #         interval=sub_items['interval'] if 'interval' in sub_items else interval
                        #     )
                        #     events_sub_items()

            # Manages list index
            counter = counter + 1 if counter < len(events) - 1 else 0

        return response if response is not None else DUMMY_RESPONSE

    # def _extend_by_core_events(self, events):
    #     return self.events + events if len(self.events) else events

    def waiting_battle_end_regular(self, msg, timeout=5, x=20, y=46):
        # @TODO rename 'timeout' into 'interval'
        log(f"Waiting battle End: {msg}")

        # for reading the text
        width = 174

        # SHOULD TEST
        x_1 = 268
        y_1 = 278
        rgb_1 = [17, 122, 156]

        x_2 = 472
        y_2 = 278
        rgb_2 = [181, 130, 5]

        def retry_callback(*args):
            log('Establishing connection...')
            click(x_2, y_2)

        e_battle_end = prepare_event(self.E_BATTLE_END, {
            "expect": lambda: pixel_check_new([x, y, [255, 255, 255]], mistake=3),
        })

        e_connection_error = prepare_event(self.E_CONNECTION_ERROR, {
            "callback": retry_callback,
            "expect": lambda: bool(
                pixel_check_new([x_1, y_1, rgb_1], mistake=10) and pixel_check_new([x_2, y_2, rgb_2], mistake=10)
            ),
        })

        battle_end_events = self.awaits(
            events=[e_battle_end, e_connection_error],
            interval=timeout
        )

        return battle_end_events
