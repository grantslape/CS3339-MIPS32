"""Unit tests for 32 bit 2 to 1 Multiplexer"""
import unittest
from unittest import TestCase
from random import randint
from myhdl import intbv, Simulation, Signal, StopSimulation
from src.commons.signal_generator import random_signed_intbv, signed_signal_set
from src.commons.settings import settings as sf
from src.commons.clock import half_period
from src.python.mux32bit2to1 import mux32bit2to1, mux32bit2to1_v


class TestMux32Bit2To1(TestCase):
    """Testing 32bit2to1Mux functionality"""
    def setUp(self):
        self.ctrl_signal = Signal(intbv(0)[1:])
        self.input1, self.input2, self.output, self.output_v = signed_signal_set(4)
        self.dut = mux32bit2to1(self.ctrl_signal, self.input1, self.input2, self.output)

    def deassert(self, output):
        """Testing deasserted functionality"""
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.ctrl_signal.next = 0
            self.input2.next = random_signed_intbv()
            self.input1.next = random_signed_intbv()
            yield half_period()
            self.assertEqual(self.ctrl_signal, 0)
            self.assertEqual(bin(output), bin(self.input1))
        raise StopSimulation

    def asserted(self, output):
        """Testing asserted functionality"""
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.ctrl_signal.next = 1
            self.input2.next = random_signed_intbv()
            self.input1.next = random_signed_intbv()
            yield half_period()
            self.assertEqual(self.ctrl_signal, 1)
            self.assertEqual(bin(output), bin(self.input2))
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
                self.assertEqual(bin(output), bin(self.input2))
        raise StopSimulation

    def inst_mem(self, output):
        """testing inst mem mux functionality"""
        self.input2.next = 0b0
        self.ctrl_signal.next = 1
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.input1.next = random_signed_intbv()
            yield half_period()
            self.assertEqual(bin(output), bin(0))
            self.assertNotEquals(bin(output), bin(self.input1))
        raise StopSimulation

    def testHoldDeassertPython(self):
        """ Checking that input1 is outputted when deasserted Python"""
        stim = self.deassert(self.output)
        Simulation(self.dut, stim).run(quiet=1)

    def testHoldDeassertVerilog(self):
        """ Checking that input1 is outputted when deasserted Verilog"""
        stim = self.deassert(self.output_v)
        dut_v = mux32bit2to1_v(self.ctrl_signal, self.input1, self.input2, self.output_v)
        Simulation(dut_v, stim).run(quiet=1)

    def testHoldDeassertTogether(self):
        """ Checking that input1 is outputted when deasserted Cosimulation"""
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

    def testInstMemMuxPython(self):
        """Checking special inst_mem_mux Python"""
        stim = self.inst_mem(self.output)
        Simulation(self.dut, stim).run(quiet=1)

    def testInstMemMuxVerilog(self):
        """Checking special inst_mem_mux Verilog"""
        stim = self.inst_mem(self.output_v)
        dut_v = mux32bit2to1_v(self.ctrl_signal, self.input1, self.input2, self.output_v)
        Simulation(dut_v, stim).run(quiet=1)

    def testInstMemTogether(self):
        """Checking special inst_mem_mux Together"""
        stim = self.inst_mem(self.output)
        stim_v = self.inst_mem(self.output_v)
        dut_v = mux32bit2to1_v(self.ctrl_signal, self.input1, self.input2, self.output_v)
        Simulation(self.dut, dut_v, stim, stim_v).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
