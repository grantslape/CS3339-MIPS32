import unittest
from random import randint
from unittest import TestCase
from myhdl import intbv, Simulation, Signal, StopSimulation
from src.commons.signal_generator import signed_intbv_set, random_signed_intbv
from src.commons.settings import settings as sf
from src.commons.clock import half_period
from src.python.mux32bit2to1 import mux32bit2to1, mux32bit2to1_v


class TestMux32Bit2To1(TestCase):
    """Testing 32bit2to1Mux functionality"""
    def setUp(self):
        self.ctrl_signal = Signal(intbv(0)[1:])
        self.input1, self.input2, self.output, self.output_v = signed_intbv_set(4, value=0)
        self.dut = mux32bit2to1(self.ctrl_signal, self.input1, self.input2, self.output)

    def deassert(self, output):
        """Testing deasserted functionality"""
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.ctrl_signal.next = 0
            self.input2.next = random_signed_intbv()
            self.input1.next = random_signed_intbv()
            yield half_period()
            self.assertEqual(self.ctrl_signal, 0)
            self.assertEqual(output, self.input1)
        raise StopSimulation

    def asserted(self, output):
        """Testing asserted functionality"""
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.ctrl_signal.next = 1
            self.input2.next = random_signed_intbv()
            self.input1.next = random_signed_intbv()
            yield half_period()
            self.assertEqual(self.ctrl_signal, 1)
            self.assertEqual(output, self.input2)
        raise StopSimulation

    def dynamic(self, output):
        """Testing dynamic functionality"""
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.ctrl_signal.next = randint(0, 1)
            self.input2.next = random_signed_intbv()
            self.input1.next = random_signed_intbv()
            yield half_period()
            if self.ctrl_signal == 0:
                self.assertEqual(output, self.input1)
            else:
                self.assertEqual(self.ctrl_signal, 1)
                self.assertEqual(output, self.input2)
        raise StopSimulation

    def testHoldDeassertPython(self):
        """ Checking that result_data is outputted when deasserted Python"""
        stim = self.deassert(self.output)
        Simulation(self.dut, stim).run(quiet=1)

    def testHoldDeassertVerilog(self):
        """ Checking that result_data is outputted when deasserted Verilog"""
        stim = self.deassert(self.output_v)
        dut_v = mux32bit2to1_v(self.ctrl_signal, self.input1, self.input2, self.output_v)
        Simulation(dut_v, stim).run(quiet=1)

    def testHoldDeassertTogether(self):
        """ Checking that result_data is outputted when deasserted Cosimulation"""
        stim = self.deassert(self.output)
        stim_v = self.deassert(self.output_v)
        dut_v = mux32bit2to1_v(self.ctrl_signal, self.input1, self.input2, self.output_v)
        Simulation(self.dut, stim, dut_v, stim_v).run(quiet=1)

    def testHoldAssertPython(self):
        """ Checking that input2 is outputted when Asserted Python"""
        stim = self.asserted(self.output)
        Simulation(self.dut, stim).run(quiet=1)

    def testHoldAssertVerilog(self):
        """ Checking that input2 is outputted when Asserted Verilog"""
        stim = self.asserted(self.output_v)
        dut_v = mux32bit2to1_v(self.ctrl_signal, self.input1, self.input2, self.output_v)
        Simulation(dut_v, stim).run(quiet=1)

    def testHoldAssertTogether(self):
        """ Checking that input2 is outputted when Asserted Cosimulation"""
        stim = self.asserted(self.output)
        stim_v = self.asserted(self.output_v)
        dut_v = mux32bit2to1_v(self.ctrl_signal, self.input1, self.input2, self.output_v)
        Simulation(self.dut, stim, dut_v, stim_v).run(quiet=1)

    def testHoldDynamicPython(self):
        """ Checking that correct output is assigned Python"""
        stim = self.dynamic(self.output)
        Simulation(self.dut, stim).run(quiet=1)

    def testDynamicVerilog(self):
        """ Checking that correct output is assigned Verilog"""
        stim = self.dynamic(self.output_v)
        dut_v = mux32bit2to1_v(self.ctrl_signal, self.input1, self.input2, self.output_v)
        Simulation(dut_v, stim).run(quiet=1)

    def testDynamicTogether(self):
        """ Checking that correct output is assigned Cosimulation"""
        stim = self.dynamic(self.output)
        stim_v = self.dynamic(self.output_v)
        dut_v = mux32bit2to1_v(self.ctrl_signal, self.input1, self.input2, self.output_v)
        Simulation(self.dut, stim, dut_v, stim_v).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
