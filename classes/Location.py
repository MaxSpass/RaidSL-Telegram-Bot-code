from helpers.common import sleep, pixel_check_new, click, log
from datetime import datetime, timedelta
import numpy as np

# pixels_wait
# await_click
# await_needle

NOT_FOUND_EVENT = 'EVENT_NOT_FOUND'
DUMMY_RESPONSE = {"name": NOT_FOUND_EVENT, "data": None}

class Location:
    def __init__(self, name, events=None):
        self.name = name
        self.stop = False
        #
        # if events is not None and type(events) is list:
        #     self.events = events

    def awaits(self, events, interval=1):
        if self.stop:
            return DUMMY_RESPONSE
        response = None
        counter = 0
        time_tracker = {}

        events_names_list = list(map(lambda el: el['name'], events))
        events_names_str = str(np.array(events_names_list, dtype=object))
        log(f"Events checking: {events_names_str}")

        # events = self._extend_by_core_events(events)
        while response is None and not self.stop:
            name = events[counter]['name']
            expect = events[counter]['expect']
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

            if counter < len(events) - 1:
                counter += 1
            else:
                counter = 0

            sleep(interval)

        return response if response is not None else DUMMY_RESPONSE

    # def _extend_by_core_events(self, events):
    #     return self.events + events if len(self.events) else events

    def waiting_battle_end_regular(self, msg, timeout=5, x=20, y=46):
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

        E_BATTLE_END = {
            "name": "Battle end",
            "interval": 5,
            "expect": lambda: pixel_check_new([x, y, [255, 255, 255]], mistake=10),
        }

        E_CONNECTION_ERROR = {
            "name": "No connection",
            "interval": 300,
            "blocking": False,
            "callback": retry_callback,
            "expect": lambda: bool(
                pixel_check_new([x_1, y_1, rgb_1], mistake=10) and pixel_check_new([x_2, y_2, rgb_2], mistake=10)
            ),
        }

        battle_end_events = self.awaits(
            events=[E_BATTLE_END, E_CONNECTION_ERROR],
            interval=timeout
        )

        # @TODO Return right result
        return battle_end_events
