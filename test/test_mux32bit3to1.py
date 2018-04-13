"""32 bit Multiplexer 3:1 unit tests"""
import unittest
from unittest import TestCase
from myhdl import Simulation, StopSimulation, Signal, intbv
from src.python.mux32bit3to1 import mux32bit3to1, mux32bit3to1_v
from src.commons.signal_generator import random_signed_intbv, signed_signal_set, \
    rand_signed_signal_set
# TODO: Update this to generic 32 bit mux
from src.commons.clock import half_period
from src.commons.settings import settings as sf


class Test32Bit3To1Mux(TestCase):
    """Testing 3:1 Mux functionality"""

    def setUp(self):
        self.ctrl_signal = Signal(intbv()[2:])
        self.data1, self.data2, self.data3, self.output, self.output_v = signed_signal_set(5)
        self.dut = mux32bit3to1(self.ctrl_signal, self.data1, self.data2, self.data3, self.output)

    def deassert(self, python=False, verilog=False):
        """Testing deasserted functionality"""
        self.ctrl_signal.next = 0
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.data3.next, self.data2.next, self.data1.next = rand_signed_signal_set(3)
            yield half_period()
            if python:
                self.assertEqual(self.output, self.data1)
                self.assertNotEquals(self.output, self.data2)
                self.assertNotEquals(self.output, self.data3)
            if verilog:
                self.assertEqual(self.output_v, self.data1)
                self.assertNotEquals(self.output_v, self.data2)
                self.assertNotEquals(self.output_v, self.data3)
        raise StopSimulation

    def forwardA(self, python=False, verilog=False):
        """testing forward A functionality"""
        self.ctrl_signal.next = 1
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.data3.next, self.data2.next, self.data1.next = rand_signed_signal_set(3)
            yield half_period()
            if python:
                self.assertEqual(self.output, self.data2)
                self.assertNotEquals(self.output, self.data1)
                self.assertNotEquals(self.output, self.data3)
            if verilog:
                self.assertEqual(self.output_v, self.data2)
                self.assertNotEquals(self.output_v, self.data1)
                self.assertNotEquals(self.output_v, self.data3)
        raise StopSimulation

    def forwardB(self, python=False, verilog=False):
        """testing forward B functionality"""
        self.ctrl_signal.next = 2
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.data3.next, self.data2.next, self.data1.next = rand_signed_signal_set(3)
            yield half_period()
            if python:
                self.assertEqual(self.output, self.data3)
                self.assertNotEquals(self.output, self.data1)
                self.assertNotEquals(self.output, self.data2)
            if verilog:
                self.assertEqual(self.output_v, self.data3)
                self.assertNotEquals(self.output_v, self.data1)
                self.assertNotEquals(self.output_v, self.data2)
        raise StopSimulation

    def test3To1MuxDeassertPython(self):
        """Testing deasserted functionality Python"""
        stim = self.deassert(python=True)

        Simulation(self.dut, stim).run(quiet=1)

    def test3To1MuxDeassertVerilog(self):
        """Testing deasserted functionality Verilog"""
        stim = self.deassert(verilog=True)
        dut_v = mux32bit3to1_v(self.ctrl_signal, self.data1, self.data2, self.data3, self.output_v)

        Simulation(dut_v, stim).run(quiet=1)

    def test3To1MuxDeassertTogether(self):
        """Testing deasserted functionality together"""
        dut_v = mux32bit3to1_v(self.ctrl_signal, self.data1, self.data2, self.data3, self.output_v)
        stim = self.deassert(python=True, verilog=True)

        Simulation(self.dut, stim, dut_v).run(quiet=1)

    def test3To1MuxForwardPython(self):
        """Testing ForwardA functionality Python"""
        stim = self.forwardA(python=True)

        Simulation(self.dut, stim).run(quiet=1)

    def test3To1MuxForwardAVerilog(self):
        """Testing ForwardA functionality Verilog"""
        dut_v = mux32bit3to1_v(self.ctrl_signal, self.data1, self.data2, self.data3, self.output_v)
        stim = self.forwardA(verilog=True)

        Simulation(dut_v, stim).run(quiet=1)

    def test3To1MuxForwardATogether(self):
        """Testing ForwardA functionality together"""
        dut_v = mux32bit3to1_v(self.ctrl_signal, self.data1, self.data2, self.data3, self.output_v)
        stim = self.forwardA(python=True, verilog=True)

        Simulation(self.dut, stim, dut_v).run(quiet=1)

    def test3To1MuxForwardBPython(self):
        """Testing ForwardB functionality Python"""
        stim = self.forwardB(python=True)

        Simulation(self.dut, stim).run(quiet=1)

    def test3To1MuxForwardBVerilog(self):
        """Testing ForwardB functionality Verilog"""
        dut_v = mux32bit3to1_v(self.ctrl_signal, self.data1, self.data2, self.data3, self.output_v)
        stim = self.forwardB(verilog=True)

        Simulation(dut_v, stim).run(quiet=1)

    def test3To1MuxForwardBTogether(self):
        """Testing ForwardB functionality together"""
        dut_v = mux32bit3to1_v(self.ctrl_signal, self.data1, self.data2, self.data3, self.output_v)
        stim = self.forwardB(python=True, verilog=True)

        Simulation(self.dut, stim, dut_v).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
