"""ID Shift Left Module Unit Test"""
import unittest
from unittest import TestCase
from myhdl import Signal, StopSimulation, intbv, Simulation

from src.commons.clock import half_period
from src.commons.settings import settings as sf
from src.commons.signal_generator import unsigned_signal_set, unsigned_intbv, random_unsigned_intbv
from src.python.id_shift_left import id_shift_left, id_shift_left_v


@unittest.skip('ID Shift not implemented')
class TestIdShiftLeft(TestCase):
    """Test ID Shift Left Module"""
    def setUp(self):
        self.top4 = Signal(unsigned_intbv(width=4))
        self.target = Signal(unsigned_intbv(width=26))
        self.output, self.output_v = unsigned_signal_set(2)
        self.dut = id_shift_left(self.top4, self.target, self.output)

    def zero_test(self, output):
        """Zero test"""
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            yield half_period()
            self.assertEqual(bin(output), bin(0))
        raise StopSimulation

    def dynamic(self, output):
        """Zero test"""
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.top4 = random_unsigned_intbv(width=4)
            self.target = random_unsigned_intbv(width=26)
            expected = intbv()[sf['WIDTH':]]
            expected[32:29] = self.top4
            expected[29:0] = self.target
            yield half_period()
            self.assertEqual(bin(expected), bin(output))
        raise StopSimulation

    def testIdShiftUnitZeroPython(self):
        """Test ID Shift Unit Hold zero Python"""
        Simulation(self.dut, self.zero_test(self.output)).run(quiet=1)

    def testIdShiftUnitZeroVerilog(self):
        """Test ID Shift Unit Hold zero Verilog"""
        dut_v = id_shift_left_v(self.top4, self.target, self.output_v)
        stim_v = self.zero_test(output=self.output_v)
        Simulation(dut_v, stim_v).run(quiet=1)

    def testIdShiftUnitZeroTogether(self):
        """Test ID Shift Unit Hold zero Together"""
        stim = self.zero_test(output=self.output)
        stim_v = self.dynamic(output=self.output_v)
        dut_v = id_shift_left_v(self.top4, self.target, self.output_v)
        Simulation(dut_v, stim_v, stim, self.dut).run(quiet=1)

    def testIdShiftUnitDynamicPython(self):
        """Test ID Shift Unit Hold dynamic Python"""
        Simulation(self.dut, self.dynamic(self.output)).run(quiet=1)

    def testIdShiftUnitDynamicVerilog(self):
        """Test ID Shift Unit Hold dynamic Verilog"""
        dut_v = id_shift_left_v(self.top4, self.target, self.output_v)
        stim_v = self.dynamic(output=self.output_v)
        Simulation(dut_v, stim_v).run(quiet=1)

    def testIdShiftUnitDynamicTogether(self):
        """Test ID Shift Unit Hold dynamic Together"""
        stim = self.dynamic(output=self.output)
        stim_v = self.dynamic(output=self.output_v)
        dut_v = id_shift_left_v(self.top4, self.target, self.output_v)
        Simulation(dut_v, stim_v, stim, self.dut).run(quiet=1)