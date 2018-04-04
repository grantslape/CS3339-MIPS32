import unittest
from random import randint
from unittest import TestCase
from myhdl import intbv, delay, Simulation, Signal, StopSimulation

import sys
sys.path.append("src/python")

from alu_mux_a import alu_mux_a, alu_mux_a_v
from settings import settings as sf

HALF_PERIOD = delay(sf['PERIOD'] / 2)


@unittest.skip("ALU Mux A not implemented")
class TestAluMuxA(TestCase):
    """Testing ALU Mux A functionality"""

    def setUp(self):
        self.forward_a = Signal(intbv(0)[2:])
        self.r_data1, self.mem_rd, self.wb_rd, self.op1_out, self.op1_out_v = [
            Signal(intbv(0, min=sf['MIN_SIGNED_VALUE'], max=sf['MAX_SIGNED_VALUE'])) for i in range(5)
        ]
        self.dut = alu_mux_a(self.forward_a, self.r_data1, self.mem_rd, self.wb_rd, self.op1_out)

    def deassert(self, op1_out):
        self.forward_a.next = 0
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.r_data1.next = Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                        min=sf['MIN_SIGNED_VALUE'],
                                        max=sf['MAX_SIGNED_VALUE']))
            while self.mem_rd == self.r_data1 or self.wb_rd == self.r_data1:
                self.mem_rd.next, self.wb_rd.next = [
                    Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                 min=sf['MIN_SIGNED_VALUE'],
                                 max=sf['MAX_SIGNED_VALUE']))
                    for i in range (2)]
            yield HALF_PERIOD
            self.assertEqual(op1_out, self.r_data1)
            self.assertNotEquals(op1_out, self.mem_rd)
            self.assertNotEquals(op1_out, self.wb_rd)
        raise StopSimulation

    def memForward(self, op1_out):
        self.forward_a.next = 1
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.mem_rd.next = Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                            min=sf['MIN_SIGNED_VALUE'],
                                            max=sf['MAX_SIGNED_VALUE']))
            while self.mem_rd == self.r_data1 or self.wb_rd == self.mem_rd:
                self.r_data1.next, self.wb_rd.next = [
                    Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                 min=sf['MIN_SIGNED_VALUE'],
                                 max=sf['MAX_SIGNED_VALUE']))
                    for i in range(2)]
            yield HALF_PERIOD
            self.assertEqual(op1_out, self.mem_rd)
            self.assertNotEquals(op1_out, self.r_data1)
            self.assertNotEquals(op1_out, self.wb_rd)
        raise StopSimulation

    def wbForward(self, op1_out):
        self.forward_a.next = 2
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.wb_rd.next = Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                           min=sf['MIN_SIGNED_VALUE'],
                                           max=sf['MAX_SIGNED_VALUE']))
            while self.wb_rd == self.r_data1 or self.wb_rd == self.mem_rd:
                self.r_data1.next, self.mem_rd.next = [
                    Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                 min=sf['MIN_SIGNED_VALUE'],
                                 max=sf['MAX_SIGNED_VALUE']))
                    for i in range(2)]
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
        stim = self.memForward(self.op1_out)

        Simulation(self.dut, stim).run(quiet=1)

    def testAluMuxAMemForwardVerilog(self):
        """Testing MemForward functionality Verilog"""
        dut_v = alu_mux_a_v(self.forward_a, self.r_data1, self.mem_rd, self.wb_rd, self.op1_out_v)
        stim = self.memForward(self.op1_out_v)

        Simulation(dut_v, stim).run(quiet=1)

    def testAluMuxAMemForwardTogether(self):
        """Testing MemForward functionality together"""
        dut_v = alu_mux_a_v(self.forward_a, self.r_data1, self.mem_rd, self.wb_rd, self.op1_out_v)
        stim = self.memForward(self.op1_out)
        stim_v = self.memForward(self.op1_out_v)

        Simulation(self.dut, stim, dut_v, stim_v).run(quiet=1)

    def testAluMuxAWbForwardPython(self):
        """Testing WbForward functionality Python"""
        stim = self.wbForward(self.op1_out)

        Simulation(self.dut, stim).run(quiet=1)

    def testAluMuxAWbForwardVerilog(self):
        """Testing WbForward functionality Verilog"""
        dut_v = alu_mux_a_v(self.forward_a, self.r_data1, self.mem_rd, self.wb_rd, self.op1_out_v)
        stim = self.wbForward(self.op1_out_v)

        Simulation(dut_v, stim).run(quiet=1)

    def testAluMuxAWbForwardTogether(self):
        """Testing WbForward functionality together"""
        dut_v = alu_mux_a_v(self.forward_a, self.r_data1, self.mem_rd, self.wb_rd, self.op1_out_v)
        stim = self.wbForward(self.op1_out)
        stim_v = self.wbForward(self.op1_out_v)

        Simulation(self.dut, stim, dut_v, stim_v).run(quiet=1)


if __name__ == '__main)__':
    unittest.main()
