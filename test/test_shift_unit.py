import unittest
from random import randint
from unittest import TestCase
from myhdl import delay, Signal, intbv, Simulation

import sys
sys.path.append("src/python")

from settings import settings as sf
from shift_unit import shift_unit, shift_unit_v

HALF_PERIOD = delay(sf['PERIOD'] / 2)


def setup():
    imm_in, imm_out = [Signal(intbv(0, min=sf['SIGNED_MIN_VALUE'], max=sf['SIGNED_MAX_VALUE'])) for i in range(2)]
    return imm_in, imm_out


# TODO: Stop repeating yourself...lost of duplicated code here.
class TestShiftUnitZero(TestCase):

    def bench(self, imm_in, imm_out):
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.assertEqual(imm_in, 0)
            self.assertEqual(imm_out, 0)
        yield HALF_PERIOD

    def testHoldZeroPython(self):
        """Checking that modules holds zero w/o input change from Python"""

        imm_in, imm_out = setup()
        dut = shift_unit(imm_in, imm_out)
        stim = self.bench(imm_in, imm_out)

        sim = Simulation(dut, stim)
        sim.run(quiet=1)

    def testHoldZeroVerilog(self):
        """Checking that modules holds zero w/o input change from Verilog"""
        imm_in, imm_out = setup()
        dut = shift_unit_v(imm_in, imm_out)
        stim = self.bench(imm_in, imm_out)

        sim = Simulation(dut, stim)
        sim.run(quiet=1)

    def testHoldZeroTogether(self):
        """Checking that modules holds zero w/o input change from Cosimulation"""
        def v_test():
            for i in range(sf['DEFAULT_TEST_LENGTH']):
                self.assertEqual(imm_out_v, 0)
            yield HALF_PERIOD

        imm_in, imm_out = setup()
        imm_out_v = Signal(intbv(0, min=sf['SIGNED_MIN_VALUE'], max=sf['SIGNED_MAX_VALUE']))
        dut = shift_unit(imm_in, imm_out)
        dut_v = shift_unit_v(imm_in, imm_out_v)
        stim = self.bench(imm_in, imm_out)

        sim = Simulation(dut, dut_v, stim, v_test())
        sim.run(quiet=1)


class TestShiftUnitOutput(TestCase):

    def bench(self, imm_in, imm_out):
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            # Note that our range of input values is 16bits, it was an immediate extended to 32 bits
            imm_in.next = intbv(randint(-1 * 2**15, 2**15 - 1), min=sf['SIGNED_MIN_VALUE'], max=sf['SIGNED_MAX_VALUE'])
            # Might need to switch next two lines
            self.assertEqual(imm_out, imm_in << 2)
            yield HALF_PERIOD

    def testCorrectOutputPython(self):
        """ Checking shift_unit shifts input by 4 in Python"""
        imm_in, imm_out = setup()
        dut = shift_unit(imm_in, imm_out)
        stim = self.bench(imm_in, imm_out)

        sim = Simulation(dut, stim)
        sim.run(quiet=1)

    def testCorrectOutputVerilog(self):
        """ Checking shift_unit shifts input by 4 in Verilog"""
        imm_in, imm_out = setup()
        dut = shift_unit(imm_in, imm_out)
        stim = self.bench(imm_in, imm_out)

        sim = Simulation(dut, stim)
        sim.run(quiet=1)

    def testHoldZeroTogether(self):
        """Checking shift_unit shifts input by 4 in Cosimulation"""
        def v_test():
            for i in range(sf['DEFAULT_TEST_LENGTH']):
                self.assertEqual(imm_out_v, imm_in << 2)
            yield HALF_PERIOD

        imm_in, imm_out = setup()
        imm_out_v = Signal(intbv(0, min=sf['SIGNED_MIN_VALUE'], max=sf['SIGNED_MAX_VALUE']))
        dut = shift_unit(imm_in, imm_out)
        dut_v = shift_unit_v(imm_in, imm_out_v)
        stim = self.bench(imm_in, imm_out)

        sim = Simulation(dut, dut_v, stim, v_test())
        sim.run(quiet=1)


if __name__ == '__main__':
    unittest.main()
