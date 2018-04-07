import unittest
from unittest import TestCase
from myhdl import Simulation, StopSimulation
# TODO: Update this to generic 32 bit mux
from src.python.alu_mux_a import alu_mux_a, alu_mux_a_v
from src.commons.signal_generator import *
from src.commons.clock import half_period


@unittest.skip("ALU Mux 3:1 not implemented")
class Test32Bit3To1Mux(TestCase):
    """Testing ALU Mux A functionality"""

    def setUp(self):
        self.ctrl_signal = Signal(intbv(0)[2:])
        self.data1, self.data2, self.data3, self.output, self.output_v = signed_signal_set(5)
        self.dut = alu_mux_a(self.ctrl_signal, self.data1, self.data2, self.data3, self.output)

    def deassert(self, output):
        """Testing deasserted functionality"""
        self.ctrl_signal.next = 0
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.data1.next = Signal()
            while self.data2 == self.data1 or self.data3 == self.data1:
                self.data2.next, self.data3.next = [
                    Signal(random_signed_intbv())
                    for i in range(2)]
            yield half_period()
            self.assertEqual(output, self.data1)
            self.assertNotEquals(output, self.data2)
            self.assertNotEquals(output, self.data3)
        raise StopSimulation

    def forwardA(self, output):
        """"""
        self.ctrl_signal.next = 1
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.data2.next = Signal(random_signed_intbv())
            while self.data2 == self.data1 or self.data3 == self.data2:
                self.data1.next, self.data3.next = [
                    Signal(random_signed_intbv())
                    for i in range(2)]
            yield half_period()
            self.assertEqual(output, self.data2)
            self.assertNotEquals(output, self.data1)
            self.assertNotEquals(output, self.data3)
        raise StopSimulation

    def forwardB(self, output):
        self.ctrl_signal.next = 2
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.data3.next = Signal(random_signed_intbv())
            while self.data3 == self.data1 or self.data3 == self.data2:
                self.data1.next, self.data2.next = [
                    Signal(random_signed_intbv()) for i in range(2)
                ]
            yield half_period()
            self.assertEqual(output, self.data3)
            self.assertNotEquals(output, self.data1)
            self.assertNotEquals(output, self.data2)
        raise StopSimulation

    def testAluMuxADeassertPython(self):
        """Testing deasserted functionality Python"""
        stim = self.deassert(self.output)

        Simulation(self.dut, stim).run(quiet=1)

    def testAluMuxADeassertVerilog(self):
        """Testing deasserted functionality Verilog"""
        stim = self.deassert(self.output_v)
        dut_v = alu_mux_a_v(self.ctrl_signal, self.data1, self.data2, self.data3, self.output_v)

        Simulation(dut_v, stim).run(quiet=1)

    def testAluMuxADeassertTogether(self):
        """Testing deasserted functionality together"""
        dut_v = alu_mux_a_v(self.ctrl_signal, self.data1, self.data2, self.data3, self.output_v)
        stim = self.deassert(self.output)
        stim_v = self.deassert(self.output_v)

        Simulation(self.dut, stim, dut_v, stim_v).run(quiet=1)

    def testAluMuxAMemForwardPython(self):
        """Testing MemForward functionality Python"""
        stim = self.forwardA(self.output)

        Simulation(self.dut, stim).run(quiet=1)

    def testAluMuxAMemForwardVerilog(self):
        """Testing MemForward functionality Verilog"""
        dut_v = alu_mux_a_v(self.ctrl_signal, self.data1, self.data2, self.data3, self.output_v)
        stim = self.forwardA(self.output_v)

        Simulation(dut_v, stim).run(quiet=1)

    def testAluMuxAMemForwardTogether(self):
        """Testing MemForward functionality together"""
        dut_v = alu_mux_a_v(self.ctrl_signal, self.data1, self.data2, self.data3, self.output_v)
        stim = self.forwardA(self.output)
        stim_v = self.forwardA(self.output_v)

        Simulation(self.dut, stim, dut_v, stim_v).run(quiet=1)

    def testAluMuxAWbForwardPython(self):
        """Testing WbForward functionality Python"""
        stim = self.forwardB(self.output)

        Simulation(self.dut, stim).run(quiet=1)

    def testAluMuxAWbForwardVerilog(self):
        """Testing WbForward functionality Verilog"""
        dut_v = alu_mux_a_v(self.ctrl_signal, self.data1, self.data2, self.data3, self.output_v)
        stim = self.forwardB(self.output_v)

        Simulation(dut_v, stim).run(quiet=1)

    def testAluMuxAWbForwardTogether(self):
        """Testing WbForward functionality together"""
        dut_v = alu_mux_a_v(self.ctrl_signal, self.data1, self.data2, self.data3, self.output_v)
        stim = self.forwardB(self.output)
        stim_v = self.forwardB(self.output_v)

        Simulation(self.dut, stim, dut_v, stim_v).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
