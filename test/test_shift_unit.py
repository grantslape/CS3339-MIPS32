import unittest
from random import randint
from unittest import TestCase
from myhdl import Simulation
from src.python.shift_unit import shift_unit, shift_unit_v
from src.commons.settings import settings as sf
from src.commons.clock import half_period
from src.commons.signal_generator import signed_signal_set, signed_intbv


class TestShiftUnit(TestCase):
    """Test no change on input """
    def setUp(self):
        self.imm_in, self.imm_out, self.imm_out_v = signed_signal_set(3, 0)
        self.dut = shift_unit(self.imm_in, self.imm_out)

    def hold(self, imm_out):
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.assertEqual(self.imm_in, 0)
            self.assertEqual(imm_out, 0)
        yield half_period()

    def outputTest(self, imm_out):
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            # Note that our range of input values is 16bits, it was an immediate extended to 32 bits
            self.imm_in.next = signed_intbv(randint(-1 * 2**15, 2**15 - 1))
            yield half_period()
            self.assertEqual(imm_out, self.imm_in << 2)

    def testHoldZeroPython(self):
        """Checking that modules holds zero w/o input change from Python"""
        stim = self.hold(self.imm_out)
        Simulation(self.dut, stim).run(quiet=1)

    def testHoldZeroVerilog(self):
        """Checking that modules holds zero w/o input change from Verilog"""
        stim = self.hold(self.imm_out_v)
        dut_v = shift_unit_v(self.imm_in, self.imm_out_v)
        Simulation(dut_v, stim).run(quiet=1)

    def testHoldZeroTogether(self):
        """Checking that modules holds zero w/o input change from Cosimulation"""
        stim = self.hold(self.imm_out)
        stim_v = self.hold(self.imm_out_v)
        dut_v = shift_unit_v(self.imm_in, self.imm_out_v)
        Simulation(self.dut, stim, stim_v, dut_v).run(quiet=1)

    def testCorrectOutputPython(self):
        """ Checking shift_unit shifts input by 4 in Python"""
        stim = self.hold(self.imm_out)
        Simulation(self.dut, stim).run(quiet=1)

    def testCorrectOutputVerilog(self):
        """ Checking shift_unit shifts input by 4 in Verilog"""
        stim = self.outputTest(self.imm_out_v)
        dut_v = shift_unit_v(self.imm_in, self.imm_out_v)
        Simulation(dut_v, stim).run(quiet=1)

    def testCorrectOutputTogether(self):
        """Checking shift_unit shifts input by 4 in Cosimulation"""
        stim = self.outputTest(self.imm_out)
        stim_v = self.outputTest(self.imm_out_v)
        dut_v = shift_unit_v(self.imm_in, self.imm_out_v)
        Simulation(self.dut, dut_v, stim, stim_v).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
