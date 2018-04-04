import unittest
import sys

from unittest import TestCase
from myhdl import intbv, delay, Simulation, Signal, StopSimulation

sys.path.append("src/python")
from pc_adder import pc_adder, pc_adder_v
from settings import settings as sf

HALF_PERIOD = delay(sf['PERIOD'] / 2)


def setup():
    return [Signal(intbv(0)[32:]) for i in range(2)]



