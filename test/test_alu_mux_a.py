import unittest
from random import randint
from unittest import TestCase
from myhdl import intbv, delay, Simulation, Signal

import sys
sys.path.append("src/python")

from alu_mux_a import alu_mux_a, alu_mux_a_v
from settings import settings as sf

HALF_PERIOD = delay(sf['PERIOD'] / 2)



