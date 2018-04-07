import sys
from myhdl import delay

sys.path.append("src/python")
from settings import settings as sf

HALF_PERIOD = delay(sf['PERIOD'] / 2)


def clock_gen(clock):
    while 1:
        yield HALF_PERIOD
        clock.next = not clock


def half_period(period=sf['PERIOD']):
    return delay(period / 2)
