"""ID Shift Left Module Unit Test"""
import unittest
from unittest import TestCase
from myhdl import Signal, StopSimulation, intbv, Simulation, concat, bin

from src.commons.clock import half_period
from src.commons.settings import settings as sf
from src.commons.signal_generator import unsigned_signal_set, unsigned_intbv, random_unsigned_intbv
from src.python.id_shift_left import id_shift_left, id_shift_left_v


class TestIdShiftLeft(TestCase):
    """Test ID Shift Left Module"""
    def setUp(self):
        self.top4 = Signal(unsigned_intbv(width=4))
        self.target = Signal(unsigned_intbv(width=26))
        self.output, self.output_v = unsigned_signal_set(2)
        self.dut = id_shift_left(self.top4, self.target, self.output)

    def zero_test(self, python=False, verilog=False):
        """Zero test"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            yield half_period()
            if python:
                self.assertEqual(bin(self.output), bin(0))
            if verilog:
                self.assertEqual(bin(self.output_v), bin(0))
        raise StopSimulation

    def dynamic(self, python=False, verilog=False):
        """Zero test"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.top4.next = random_unsigned_intbv(width=4)
            self.target.next = random_unsigned_intbv(width=26)
            yield half_period()
            if python:
                self.assertEqual(bin(concat(self.top4, self.target, intbv()[2:])), bin(self.output))
            if verilog:
                self.assertEqual(bin(concat(self.top4, self.target, intbv()[2:])), bin(self.output_v))
        raise StopSimulation

    def testIdShiftUnitZeroPython(self):
        """Test ID Shift Unit Hold zero Python"""
        Simulation(self.dut, self.zero_test(python=True)).run(quiet=1)

    def testIdShiftUnitZeroVerilog(self):
        """Test ID Shift Unit Hold zero Verilog"""
        dut_v = id_shift_left_v(self.top4, self.target, self.output_v)
        stim_v = self.zero_test(verilog=True)
        Simulation(dut_v, stim_v).run(quiet=1)

    def testIdShiftUnitZeroTogether(self):
        """Test ID Shift Unit Hold zero Together"""
        stim = self.zero_test(python=True, verilog=True)
        dut_v = id_shift_left_v(self.top4, self.target, self.output_v)
        Simulation(dut_v, stim, self.dut).run(quiet=1)

    def testIdShiftUnitDynamicPython(self):
        """Test ID Shift Unit Hold dynamic Python"""
        Simulation(self.dut, self.dynamic(python=True)).run(quiet=1)

    def testIdShiftUnitDynamicVerilog(self):
        """Test ID Shift Unit Hold dynamic Verilog"""
        dut_v = id_shift_left_v(self.top4, self.target, self.output_v)
        stim_v = self.dynamic(verilog=True)
        Simulation(dut_v, stim_v).run(quiet=1)

    def testIdShiftUnitDynamicTogether(self):
        """Test ID Shift Unit Hold dynamic Together"""
        stim = self.dynamic(python=True, verilog=True)
        dut_v = id_shift_left_v(self.top4, self.target, self.output_v)
        Simulation(dut_v, stim, self.dut).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
