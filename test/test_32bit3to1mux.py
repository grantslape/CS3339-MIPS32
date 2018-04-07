import sys
import unittest
from random import randint
from unittest import TestCase
from myhdl import intbv, delay, Simulation, Signal, StopSimulation

sys.path.append("src/python")
# TODO: Update this to generic 32 bit mux
from alu_mux_a import alu_mux_a, alu_mux_a_v
sys.path.append("src/commons")
from settings import settings as sf
from intbv_generator import *

HALF_PERIOD = delay(sf['PERIOD'] / 2)


@unittest.skip("ALU Mux A not implemented")
class Test32Bit3To1Mux(TestCase):
    """Testing ALU Mux A functionality"""

    def setUp(self):
        self.forward_a = Signal(intbv(0)[2:])
        self.r_data1, self.mem_rd, self.wb_rd, self.op1_out, self.op1_out_v = [
            Signal(signed_intbv(0))
            for i in range(5)
        ]
        self.dut = alu_mux_a(self.forward_a, self.r_data1, self.mem_rd, self.wb_rd, self.op1_out)

    def deassert(self, op1_out):
        """Testing deasserted functionality"""
        self.forward_a.next = 0
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.r_data1.next = Signal()
            while self.mem_rd == self.r_data1 or self.wb_rd == self.r_data1:
                self.mem_rd.next, self.wb_rd.next = [
                    Signal(random_signed_intbv())
                    for i in range(2)]
            yield HALF_PERIOD
            self.assertEqual(op1_out, self.r_data1)
            self.assertNotEquals(op1_out, self.mem_rd)
            self.assertNotEquals(op1_out, self.wb_rd)
        raise StopSimulation

    def forwardA(self, op1_out):
        """"""
        self.forward_a.next = 1
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.mem_rd.next = Signal(random_signed_intbv())
            while self.mem_rd == self.r_data1 or self.wb_rd == self.mem_rd:
                self.r_data1.next, self.wb_rd.next = [
                    Signal(random_signed_intbv())
                    for i in range(2)]
            yield HALF_PERIOD
            self.assertEqual(op1_out, self.mem_rd)
            self.assertNotEquals(op1_out, self.r_data1)
            self.assertNotEquals(op1_out, self.wb_rd)
        raise StopSimulation

    def forwardB(self, op1_out):
        self.forward_a.next = 2
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.wb_rd.next = Signal(random_signed_intbv())
            while self.wb_rd == self.r_data1 or self.wb_rd == self.mem_rd:
                self.r_data1.next, self.mem_rd.next = [
                    Signal(random_signed_intbv()) for i in range(2)
                ]
            yield HALF_PERIOD
            self.assertEqual(op1_out, self.wb_rd)
            self.assertNotEquals(op1_out, self.r_data1)
            self.assertNotEquals(op1_out, self.mem_rd)
        raise StopSimulation

    def testAluMuxADeassertPython(self):
        """Testing deasserted functionality Python"""
        stim = self.deassert(self.op1_out)

        Simulation(self.dut, stim).run(quiet=1)

    def testAluMuxADeassertVerilog(self):
        """Testing deasserted functionality Verilog"""
        stim = self.deassert(self.op1_out_v)
        dut_v = alu_mux_a_v(self.forward_a, self.r_data1, self.mem_rd, self.wb_rd, self.op1_out_v)

        Simulation(dut_v, stim).run(quiet=1)

    def testAluMuxADeassertTogether(self):
        """Testing deasserted functionality together"""
        dut_v = alu_mux_a_v(self.forward_a, self.r_data1, self.mem_rd, self.wb_rd, self.op1_out_v)
        stim = self.deassert(self.op1_out)
        stim_v = self.deassert(self.op1_out_v)

        Simulation(self.dut, stim, dut_v, stim_v).run(quiet=1)

    def testAluMuxAMemForwardPython(self):
        """Testing MemForward functionality Python"""
        stim = self.forwardA(self.op1_out)

        Simulation(self.dut, stim).run(quiet=1)

    def testAluMuxAMemForwardVerilog(self):
        """Testing MemForward functionality Verilog"""
        dut_v = alu_mux_a_v(self.forward_a, self.r_data1, self.mem_rd, self.wb_rd, self.op1_out_v)
        stim = self.forwardA(self.op1_out_v)

        Simulation(dut_v, stim).run(quiet=1)

    def testAluMuxAMemForwardTogether(self):
        """Testing MemForward functionality together"""
        dut_v = alu_mux_a_v(self.forward_a, self.r_data1, self.mem_rd, self.wb_rd, self.op1_out_v)
        stim = self.forwardA(self.op1_out)
        stim_v = self.forwardA(self.op1_out_v)

        Simulation(self.dut, stim, dut_v, stim_v).run(quiet=1)

    def testAluMuxAWbForwardPython(self):
        """Testing WbForward functionality Python"""
        stim = self.forwardB(self.op1_out)

        Simulation(self.dut, stim).run(quiet=1)

    def testAluMuxAWbForwardVerilog(self):
        """Testing WbForward functionality Verilog"""
        dut_v = alu_mux_a_v(self.forward_a, self.r_data1, self.mem_rd, self.wb_rd, self.op1_out_v)
        stim = self.forwardB(self.op1_out_v)

        Simulation(dut_v, stim).run(quiet=1)

    def testAluMuxAWbForwardTogether(self):
        """Testing WbForward functionality together"""
        dut_v = alu_mux_a_v(self.forward_a, self.r_data1, self.mem_rd, self.wb_rd, self.op1_out_v)
        stim = self.forwardB(self.op1_out)
        stim_v = self.forwardB(self.op1_out_v)

        Simulation(self.dut, stim, dut_v, stim_v).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
