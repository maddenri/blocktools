import time
from datetime import datetime


def to_utc(timestamp):
    utc_time = datetime.utcfromtimestamp(timestamp)
    return utc_time.strftime("%Y-%m-%d %H:%M:%S.%f+00:00 (UTC)")


def get_current_time():
    return int(time.time())
