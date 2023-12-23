from datetime import datetime
from time import gmtime, localtime
from helpers.common import *

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

    def temp(self):
        now = datetime.now()
        print(now)
        year = '{:02d}'.format(now.year)
        month = '{:02d}'.format(now.month)
        day = '{:02d}'.format(now.day)
        hour = '{:02d}'.format(now.hour)
        minute = '{:02d}'.format(now.minute)
        day_month_year = '{}-{}-{}'.format(year, month, day)

        print('hour: ' + hour)
        print('minute: ' + minute)
        # print(now.timetuple())


# print(gmtime(time.time()))

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
