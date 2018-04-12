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

    def deassert(self, python=False, verilog=False):
        """Testing deasserted functionality"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.ctrl_signal.next = 0
            self.input2.next = random_signed_intbv()
            self.input1.next = random_signed_intbv()
            yield half_period()
            if python:
                self.assertEqual(self.ctrl_signal, 0)
                self.assertEqual(bin(self.output), bin(self.input1))
            if verilog:
                self.assertEqual(self.ctrl_signal, 0)
                self.assertEqual(bin(self.output_v), bin(self.input1))
        raise StopSimulation

    def asserted(self, python=False, verilog=False):
        """Testing asserted functionality"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.ctrl_signal.next = 1
            self.input2.next = random_signed_intbv()
            self.input1.next = random_signed_intbv()
            yield half_period()
            if python:
                self.assertEqual(self.ctrl_signal, 1)
                self.assertEqual(bin(self.output), bin(self.input2))
            if verilog:
                self.assertEqual(self.ctrl_signal, 1)
                self.assertEqual(bin(self.output_v), bin(self.input2))
        raise StopSimulation

    def dynamic(self, python=False, verilog=False):
        """Testing dynamic functionality"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.ctrl_signal.next = randint(0, 1)
            self.input2.next = random_signed_intbv()
            self.input1.next = random_signed_intbv()
            yield half_period()
            if self.ctrl_signal == 0:
                if python:
                    self.assertEqual(self.output, self.input1)
                if verilog:
                    self.assertEqual(self.output_v, self.input1)
            else:
                if python:
                    self.assertEqual(self.ctrl_signal, 1)
                    self.assertEqual(bin(self.output), bin(self.input2))
                if verilog:
                    self.assertEqual(self.ctrl_signal, 1)
                    self.assertEqual(bin(self.output_v), bin(self.input2))
        raise StopSimulation

    def inst_mem(self, python=False, verilog=False):
        """testing inst mem mux functionality"""
        self.input2.next = 0b0
        self.ctrl_signal.next = 1
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.input1.next = random_signed_intbv()
            yield half_period()
            if python:
                self.assertEqual(bin(self.output), bin(0))
                self.assertNotEquals(bin(self.output), bin(self.input1))
            if verilog:
                self.assertEqual(bin(self.output_v), bin(0))
                self.assertNotEquals(bin(self.output_v), bin(self.input1))
        raise StopSimulation

    def testHoldDeassertPython(self):
        """ Checking that input1 is outputted when deasserted Python"""
        stim = self.deassert(python=True)
        Simulation(self.dut, stim).run(quiet=1)

    def testHoldDeassertVerilog(self):
        """ Checking that input1 is outputted when deasserted Verilog"""
        stim = self.deassert(verilog=True)
        dut_v = mux32bit2to1_v(self.ctrl_signal, self.input1, self.input2, self.output_v)
        Simulation(dut_v, stim).run(quiet=1)

    def testHoldDeassertTogether(self):
        """ Checking that input1 is outputted when deasserted Cosimulation"""
        stim = self.deassert(python=True, verilog=True)
        dut_v = mux32bit2to1_v(self.ctrl_signal, self.input1, self.input2, self.output_v)
        Simulation(self.dut, stim, dut_v).run(quiet=1)

    def testHoldAssertPython(self):
        """ Checking that input2 is outputted when Asserted Python"""
        stim = self.asserted(python=True)
        Simulation(self.dut, stim).run(quiet=1)

    def testHoldAssertVerilog(self):
        """ Checking that input2 is outputted when Asserted Verilog"""
        stim = self.asserted(verilog=True)
        dut_v = mux32bit2to1_v(self.ctrl_signal, self.input1, self.input2, self.output_v)
        Simulation(dut_v, stim).run(quiet=1)

    def testHoldAssertTogether(self):
        """ Checking that input2 is outputted when Asserted Cosimulation"""
        stim = self.asserted(python=True, verilog=True)
        dut_v = mux32bit2to1_v(self.ctrl_signal, self.input1, self.input2, self.output_v)
        Simulation(self.dut, stim, dut_v).run(quiet=1)

    def testHoldDynamicPython(self):
        """ Checking that correct output is assigned Python"""
        stim = self.dynamic(python=True)
        Simulation(self.dut, stim).run(quiet=1)

    def testDynamicVerilog(self):
        """ Checking that correct output is assigned Verilog"""
        stim = self.dynamic(verilog=True)
        dut_v = mux32bit2to1_v(self.ctrl_signal, self.input1, self.input2, self.output_v)
        Simulation(dut_v, stim).run(quiet=1)

    def testDynamicTogether(self):
        """ Checking that correct output is assigned Cosimulation"""
        stim = self.dynamic(python=True, verilog=True)
        dut_v = mux32bit2to1_v(self.ctrl_signal, self.input1, self.input2, self.output_v)
        Simulation(self.dut, stim, dut_v).run(quiet=1)

    def testInstMemMuxPython(self):
        """Checking special inst_mem_mux Python"""
        stim = self.inst_mem(python=True)
        Simulation(self.dut, stim).run(quiet=1)

    def testInstMemMuxVerilog(self):
        """Checking special inst_mem_mux Verilog"""
        stim = self.inst_mem(verilog=True)
        dut_v = mux32bit2to1_v(self.ctrl_signal, self.input1, self.input2, self.output_v)
        Simulation(dut_v, stim).run(quiet=1)

    def testInstMemTogether(self):
        """Checking special inst_mem_mux Together"""
        stim = self.inst_mem(python=True, verilog=True)
        dut_v = mux32bit2to1_v(self.ctrl_signal, self.input1, self.input2, self.output_v)
        Simulation(self.dut, dut_v, stim).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
