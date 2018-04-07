from random import randint

from myhdl import intbv
from settings import settings as sf


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
    return signed_intbv(randint(sf['SIGNED_MIN_VALUE'], sf['SIGNED_MIN_VALUE']))


def unsigned_intbv(value=0):
    """
    Generate an unsigned intbv
    :param value: initial value
    :return: intbv
    """
    return intbv(value)[32:]


def unsigned_intbv_set(j, value=0):
    """
    Generate many unsigned intbvs
    :param j: # of intbvs to generate
    :param value: initial value
    :return: list of j intbvs
    """
    return [unsigned_intbv(value) for i in range(j)]


def random_unsigned_intbv():
    """Return random unsigned 32 bit intbv"""
    return unsigned_intbv(randint(0, sf['UNSIGNED_MAX_VALUE']))[32:]


def unsigned_signal_set(j, value=0):
    """
    Generate many unsigned intbv signals
    :param j:
    :param value:
    :return:
    """
    return Sig