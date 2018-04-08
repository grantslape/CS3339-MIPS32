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

    def deassert(self, output):
        """Testing deasserted functionality"""
        self.ctrl_signal.next = 0
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.data3.next, self.data2.next, self.data1.next = rand_signed_signal_set(3)
            yield half_period()
            self.assertEqual(output, self.data1)
            self.assertNotEquals(output, self.data2)
            self.assertNotEquals(output, self.data3)
        raise StopSimulation

    def forwardA(self, output):
        """testing forward A functionality"""
        self.ctrl_signal.next = 1
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.data3.next, self.data2.next, self.data1.next = rand_signed_signal_set(3)
            yield half_period()
            self.assertEqual(output, self.data2)
            self.assertNotEquals(output, self.data1)
            self.assertNotEquals(output, self.data3)
        raise StopSimulation

    def forwardB(self, output):
        """testing forward B functionality"""
        self.ctrl_signal.next = 2
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.data3.next, self.data2.next, self.data1.next = rand_signed_signal_set(3)
            yield half_period()
            self.assertEqual(output, self.data3)
            self.assertNotEquals(output, self.data1)
            self.assertNotEquals(output, self.data2)
        raise StopSimulation

    def test3To1MuxDeassertPython(self):
        """Testing deasserted functionality Python"""
        stim = self.deassert(self.output)

        Simulation(self.dut, stim).run(quiet=1)

    def test3To1MuxDeassertVerilog(self):
        """Testing deasserted functionality Verilog"""
        stim = self.deassert(self.output_v)
        dut_v = mux32bit3to1_v(self.ctrl_signal, self.data1, self.data2, self.data3, self.output_v)

        Simulation(dut_v, stim).run(quiet=1)

    def test3To1MuxDeassertTogether(self):
        """Testing deasserted functionality together"""
        dut_v = mux32bit3to1_v(self.ctrl_signal, self.data1, self.data2, self.data3, self.output_v)
        stim = self.deassert(self.output)
        stim_v = self.deassert(self.output_v)

        Simulation(self.dut, stim, dut_v, stim_v).run(quiet=1)

    def test3To1MuxForwardPython(self):
        """Testing ForwardA functionality Python"""
        stim = self.forwardA(self.output)

        Simulation(self.dut, stim).run(quiet=1)

    def test3To1MuxForwardAVerilog(self):
        """Testing ForwardA functionality Verilog"""
        dut_v = mux32bit3to1_v(self.ctrl_signal, self.data1, self.data2, self.data3, self.output_v)
        stim = self.forwardA(self.output_v)

        Simulation(dut_v, stim).run(quiet=1)

    def test3To1MuxForwardATogether(self):
        """Testing ForwardA functionality together"""
        dut_v = mux32bit3to1_v(self.ctrl_signal, self.data1, self.data2, self.data3, self.output_v)
        stim = self.forwardA(self.output)
        stim_v = self.forwardA(self.output_v)

        Simulation(self.dut, stim, dut_v, stim_v).run(quiet=1)

    def test3To1MuxForwardBPython(self):
        """Testing ForwardB functionality Python"""
        stim = self.forwardB(self.output)

        Simulation(self.dut, stim).run(quiet=1)

    def test3To1MuxForwardBVerilog(self):
        """Testing ForwardB functionality Verilog"""
        dut_v = mux32bit3to1_v(self.ctrl_signal, self.data1, self.data2, self.data3, self.output_v)
        stim = self.forwardB(self.output_v)

        Simulation(dut_v, stim).run(quiet=1)

    def test3To1MuxForwardBTogether(self):
        """Testing ForwardB functionality together"""
        dut_v = mux32bit3to1_v(self.ctrl_signal, self.data1, self.data2, self.data3, self.output_v)
        stim = self.forwardB(self.output)
        stim_v = self.forwardB(self.output_v)

        Simulation(self.dut, stim, dut_v, stim_v).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
