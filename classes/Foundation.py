from helpers.common import *
from datetime import datetime, timedelta
import numpy as np

RGB_PRIMARY = [187, 130, 5]
RGB_SECONDARY = [22, 124, 156]
P_BUTTON_BATTLE_START = [850, 475, RGB_PRIMARY]
P_POPUP_BUTTON_SECONDARY_LEFT = [270, 310, RGB_SECONDARY]
P_POPUP_BUTTON_SECONDARY_RIGHT = [480, 310, RGB_SECONDARY]

NOT_FOUND_EVENT = 'EVENT_NOT_FOUND'
DUMMY_RESPONSE = {"name": NOT_FOUND_EVENT, "data": None}


def callback_retry(*args):
    log('Trying to reconnect...')
    button = find_button(variant='primary')
    if button is not None:
        click(button.x, button.y, random_click=True)
        move_out_cursor()


class Foundation:
    E_BATTLE_END = {
        "name": "Battle end",
        "interval": 2,
        "expect": lambda: pixel_check_new([28, 88, [255, 255, 255]], mistake=3),
    }
    E_CONNECTION_ERROR = {
        "name": "No connection",
        "interval": 300,
        "blocking": False,
        "expect": lambda: bool(find_popup_detector()),
        "callback": callback_retry,
    }
    E_BUTTON_BATTLE_START = {
        "name": "Button battle start",
        "interval": 1,
        "limit": 1,
        "blocking": False,
        "expect": lambda: pixel_check_new(P_BUTTON_BATTLE_START, mistake=10),
        "callback": lambda *args: click(
            x=P_BUTTON_BATTLE_START[0],
            y=P_BUTTON_BATTLE_START[1],
        ),
    }
    E_NO_AURA_SKILL = {
        "name": "No aura skill",
        "interval": 1,
        "limit": 1,
        "wait_limit": 3,
        "expect": lambda: same_pixels_line_list([
            P_POPUP_BUTTON_SECONDARY_LEFT,
            P_POPUP_BUTTON_SECONDARY_RIGHT,
        ]),
        "callback": lambda *args: click(
            x=P_POPUP_BUTTON_SECONDARY_RIGHT[0],
            y=P_POPUP_BUTTON_SECONDARY_RIGHT[1],
            smart=True
        ),
    }

    def __init__(self, name, events=None):
        self.name = name
        self.stop = False

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

        start_call_time = datetime.now()
        current_time = None

        def _check_limit(e):
            name = e['name']
            limit = int(e['limit']) if 'limit' in e else None

            if name not in limit_tracker:
                limit_tracker[name] = limit

            return limit_tracker[name] is None or limit_tracker[name] > 0

        def _check_wait_limit(e):
            wait_limit = int(e['wait_limit']) if 'wait_limit' in e else None
            return datetime.now() <= start_call_time + timedelta(seconds=wait_limit) if wait_limit else True

        def _check_interval(e):
            name = e['name']
            last_call_time = time_tracker.get(name, None)
            main_interval = e['interval'] if 'interval' in e else interval
            return last_call_time is None or datetime.now() - last_call_time >= timedelta(seconds=main_interval)

        while response is None and not self.stop:
            _e = events[counter]

            # Skips limited callbacks and Skips wait_limit exceeded
            if _check_limit(_e) and _check_wait_limit(_e):

                # Interval iterator
                if _check_interval(_e):
                    _name = _e['name']
                    _expect = _e['expect']
                    _blocking = bool(_e['blocking']) if 'blocking' in _e else True
                    _callback = _e['callback'] if 'callback' in _e else None

                    # current_time = datetime.now()
                    # print(f"{current_time.second} - {_name}")

                    # Call the function and update last call time
                    time_tracker[_name] = datetime.now()
                    # print(_name)

                    res = _expect()
                    if bool(res):
                        log(f'Event occurred: {_name}')

                        if _blocking:
                            response = {"name": _name, "data": res}

                        if _callback is not None:
                            _callback(res)

                        # Tracks limited events
                        if limit_tracker[_name] is not None:
                            limit_tracker[_name] = limit_tracker[_name] - 1

            # breaks the main loop, when no active events found (checks 'limit' and 'wait_limit')
            should_break = list(filter(lambda e: _check_limit(e) and _check_wait_limit(e), events))
            if not len(should_break):
                break

            # Manages list index
            counter = counter + 1 if counter < len(events) - 1 else 0

        return response if response is not None else DUMMY_RESPONSE

    def dungeons_start_battle(self):
        # @TODO Duplication
        STAGE_ENTER = [890, 200, [93, 25, 27]]

        if pixel_check_new(STAGE_ENTER, mistake=10):
            self.awaits([self.E_BUTTON_BATTLE_START, self.E_NO_AURA_SKILL])
        else:
            dungeons_replay()

    def waiting_battle_end_regular(self, msg, timeout=5):
        # @TODO rename 'timeout' into 'interval'
        log(f"Waiting battle End: {msg}")

        return self.awaits(
            events=[self.E_BATTLE_END, self.E_CONNECTION_ERROR],
            interval=timeout
        )
