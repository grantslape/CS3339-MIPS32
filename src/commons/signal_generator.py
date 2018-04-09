from random import randint

from myhdl import intbv, Signal
from src.commons.settings import settings as sf


def signed_intbv(value=0):
    """
    Generate a signed int
    :param value: initial value
    :return: intbv
    """
    return intbv(value, min=sf['SIGNED_MIN_VALUE'], max=sf['SIGNED_MAX_VALUE'])


def signed_intbv_set(j, value=0):
    """
    Generate many signed intbvs
    :param j: # of ints to generate
    :param value: initial value of all
    :return: list of j intbv's
    """
    return [signed_intbv(value) for i in range(j)]


def random_signed_intbv():
    """Return random signed 32 bit intbv"""
    return signed_intbv(randint(sf['SIGNED_MIN_VALUE'], sf['SIGNED_MAX_VALUE']))


def unsigned_intbv(value=0, width=sf['WIDTH']):
    """
    Generate an unsigned intbv
    :param value: initial value
    :param width: width of intbv
    :return: intbv
    """
    return intbv(value)[width:]


def unsigned_intbv_set(j, value=0):
    """
    Generate many unsigned intbvs
    :param j: # of intbvs to generate
    :param value: initial value
    :return: list of j intbvs
    """
    return [unsigned_intbv(value) for i in range(j)]


def random_unsigned_intbv(width=sf['WIDTH']):
    """Return random unsigned 32 bit intbv"""
    return unsigned_intbv(randint(0, sf['UNSIGNED_MAX_VALUE']))[width:]


def unsigned_signal_set(j, value=0, width=sf['WIDTH']):
    """
    Generate many unsigned intbv signals
    :param j: # of signals to generate
    :param value: initial value
    :param width: width of intbv
    :return:
    """
    return [Signal(unsigned_intbv(value, width)) for i in range(j)]


def signed_signal_set(j, value=0):
    """
    Generate many unsigned intbv signals
    :param j: # of signals to generate
    :param value: initial value
    :return:
    """
    return [Signal(signed_intbv(value)) for i in range(j)]


def rand_signed_signal_set(j):
    """
    Generate many signed intbv signals
    :param j: # of signals to generate
    :return: list of Signals
    """
    response = []
    for i in range(j):
        response.append(random_signed_intbv())
    return response


def rand_unsigned_signal_set(j, width=sf['WIDTH']):
    """
    Generate many unsigned intbv signals
    :param j: # of signals to generate
    :param width: width of signal
    :return: list of Signals
    """
    response = []
    for i in range(j):
        response.append(random_unsigned_intbv(width))
    return response
