from myhdl import delay
from src.commons.settings import settings as sf


def clock_gen(clock):
    while 1:
        yield half_period()
        clock.next = not clock


def half_period(period=sf['PERIOD']):
    return delay(period / 2)
