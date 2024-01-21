from datetime import datetime, timezone, timedelta
from time import gmtime, localtime
from helpers.common import *
import pause

FIELD_NAMES = [
    "year",
    "month",
    "day",
    "hour",
    "min",
    "sec",
    "weekday",
    "md",
    "yd"
]


def get_stamp():
    return time.time()


def read_stamp(is_local=None, stamp=None):
    if is_local is None:
        is_local = True

    if stamp is None:
        stamp = time.time()

    if is_local:
        parsed_stamp = localtime(stamp)
    else:
        parsed_stamp = gmtime(stamp)

    return dict(zip(FIELD_NAMES, parsed_stamp))


def log_output(is_local=None):
    s = read_stamp(is_local)
    return str(s['hour']) + ':' + str(s['min']) + ':' + str(s['sec'])


class TimeMgr:

    def timestamp_to_datetime(self, dt=None):
        now = datetime.now()

        if dt is not None:
            now = dt

        year = '{:02d}'.format(now.year)
        month = '{:02d}'.format(now.month)
        day = '{:02d}'.format(now.day)
        hour = '{:02d}'.format(now.hour)
        minute = '{:02d}'.format(now.minute)
        second = '{:02d}'.format(now.second)
        day_month_year = '{}-{}-{}'.format(year, month, day)

        return {
            'year': int(year),
            'month': int(month),
            'day': int(day),
            'hour': int(hour),
            'minute': int(minute),
            'second': int(second),
        }

# // 1_000_000

# time_mgr = TimeMgr()
#
# utc_timestamp = datetime.utcnow().timestamp()
# utc_datetime = datetime.fromtimestamp(utc_timestamp)
# utc_next_day_datetime = utc_datetime + timedelta(days=1)
# parsed_time = time_mgr.timestamp_to_datetime(utc_datetime)
# parsed_time_delta = time_mgr.timestamp_to_datetime(utc_next_day_datetime)

# print(parsed_time_delta)

# h = None
# live_arena_open_hours = [[6,8], [14,16], [20,22]]
# def check_is_active():
#     res = {
#         'is_active': False,
#         'open_hour': None
#     }
#
#     utc_timestamp = datetime.utcnow().timestamp()
#     utc_datetime = datetime.fromtimestamp(utc_timestamp)
#     parsed_time = time_mgr.timestamp_to_datetime(utc_datetime)
#     hour = parsed_time['hour']
#     # hour = 9
#
#     length = len(live_arena_open_hours)
#     for i in range(len(live_arena_open_hours)):
#         arr = live_arena_open_hours[i]
#         for j in range(len(arr)):
#             if arr[0] < hour < arr[1]:
#                 res['is_active'] = True
#                 break
#             elif arr[1] <= hour and i < length:
#                 res['open_hour'] = live_arena_open_hours[i+1]

    # for i in range(len(live_arena_open_hours)):
    #     length = len(live_arena_open_hours)
    #     for j in range(len(live_arena_open_hours[length - 1])):
    #         arr = live_arena_open_hours[length - 1]
    #         if arr[0] < hour < arr[1]:
    #             res['is_active'] = True
    #             break
    #         else :
    #

# should_wait = list(map(check_is_active, live_arena_open_hours))
#
# is_active = check_is_active()

# log(parsed_time)

# if parsed_time_delta['hour'] >:

# log(parsed_time)
# log(utc_datetime - timedelta(days=1))

# 6, 14, 20
# pause.until(datetime(2024, 1, 2, 20, 6, 30, tzinfo=timezone.utc))
# log('TEST')

# print(read_stamp_new())
# read_stamp_new()

# print(read_stamp())
# print(read_stamp())
# print(read_stamp(1521174681))
# log(log_output())
# TimeMgr().temp()
# read_stamp()


# print(time.time())
# print(gmtime(1521174681))
