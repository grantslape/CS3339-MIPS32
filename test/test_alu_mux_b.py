import unittest
from random import randint
from unittest import TestCase
from myhdl import intbv, delay, Simulation, Signal, StopSimulation

import sys
sys.path.append("src/python")

from alu_mux_b import alu_mux_b, alu_mux_b_v
from settings import settings as sf

HALF_PERIOD = delay(sf['PERIOD'] / 2)


@unittest.skip("ALU Mux B not implemented")
class TestAluMuxB(TestCase):
    """Testing ALU Mux B functionality"""

    def setUp(self):
        self.forward_b = Signal(intbv(0)[2:])
        self.r_data2, self.mem_rd, self.wb_rd, self.op2_out, self.op2_out_v = [
            Signal(intbv(0, min=sf['MIN_SIGNED_VALUE'], max=sf['MAX_SIGNED_VALUE'])) for i in range(5)
        ]
        self.dut = alu_mux_b(self.forward_b, self.r_data2, self.mem_rd, self.wb_rd, self.op2_out)
        self.dut_v = alu_mux_b_v(self.forward_b, self.r_data2, self.mem_rd, self.wb_rd, self.op2_out_v)

    def deassert(self, op2_out):
        self.forward_b.next = 0
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.r_data2.next = Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                        min=sf['MIN_SIGNED_VALUE'],
                                        max=sf['MAX_SIGNED_VALUE']))
            while self.mem_rd == self.r_data2 or self.wb_rd == self.r_data2:
                self.mem_rd.next, self.wb_rd.next = [
                    Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                 min=sf['MIN_SIGNED_VALUE'],
                                 max=sf['MAX_SIGNED_VALUE']))
                    for i in range (2)]
            yield HALF_PERIOD
            self.assertEqual(op2_out, self.r_data2)
            self.assertNotEquals(op2_out, self.mem_rd)
            self.assertNotEquals(op2_out, self.wb_rd)
        raise StopSimulation

    def memForward(self, op2_out):
        self.forward_b.next = 1
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.mem_rd.next = Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                            min=sf['MIN_SIGNED_VALUE'],
                                            max=sf['MAX_SIGNED_VALUE']))
            while self.mem_rd == self.r_data2 or self.wb_rd == self.mem_rd:
                self.r_data2.next, self.wb_rd.next = [
                    Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                 min=sf['MIN_SIGNED_VALUE'],
                                 max=sf['MAX_SIGNED_VALUE']))
                    for i in range(2)]
            yield HALF_PERIOD
            self.assertEqual(op2_out, self.mem_rd)
            self.assertNotEquals(op2_out, self.r_data2)
            self.assertNotEquals(op2_out, self.wb_rd)
        raise StopSimulation

    def wbForward(self, op2_out):
        self.forward_b.next = 2
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.wb_rd.next = Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                           min=sf['MIN_SIGNED_VALUE'],
                                           max=sf['MAX_SIGNED_VALUE']))
            while self.wb_rd == self.r_data2 or self.wb_rd == self.mem_rd:
                self.r_data2.next, self.mem_rd.next = [
                    Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                 min=sf['MIN_SIGNED_VALUE'],
                                 max=sf['MAX_SIGNED_VALUE']))
                    for i in range(2)]
            yield HALF_PERIOD
            self.assertEqual(op2_out, self.wb_rd)
            self.assertNotEquals(op2_out, self.r_data2)
            self.assertNotEquals(op2_out, self.mem_rd)
        raise StopSimulation

    def testAluMuxBDeassertPython(self):
        """Testing deasserted functionality Python"""
        stim = self.deassert(self.op2_out)

        Simulation(self.dut, stim).run(quiet=1)

    def testAluMuxBDeassertVerilog(self):
        """Testing deasserted functionality Verilog"""
        stim = self.deassert(self.op2_out_v)

        Simulation(self.dut_v, stim).run(quiet=1)

    def testAluMuxBDeassertTogether(self):
        """Testing deasserted functionality together"""
        stim = self.deassert(self.op2_out)
        stim_v = self.deassert(self.op2_out_v)

        Simulation(self.dut, stim, self.dut_v, stim_v).run(quiet=1)

    def testAluMuxBMemForwardPython(self):
        """Testing MemForward functionality Python"""
        stim = self.memForward(self.op2_out)

        Simulation(self.dut, stim).run(quiet=1)

    def testAluMuxBMemForwardVerilog(self):
        """Testing MemForward functionality Verilog"""
        stim = self.memForward(self.op2_out_v)

        Simulation(self.dut_v, stim).run(quiet=1)

    def testAluMuxBMemForwardTogether(self):
        """Testing MemForward functionality together"""
        stim = self.memForward(self.op2_out)
        stim_v = self.memForward(self.op2_out_v)

        Simulation(self.dut, stim, self.dut_v, stim_v).run(quiet=1)

    def testAluMuxBWbForwardPython(self):
        """Testing WbForward functionality Python"""
        stim = self.wbForward(self.op2_out)

        Simulation(self.dut, stim).run(quiet=1)

    def testAluMuxBWbForwardVerilog(self):
        """Testing WbForward functionality Verilog"""
        stim = self.wbForward(self.op2_out_v)

        Simulation(self.dut_v, stim).run(quiet=1)

    def testAluMuxBWbForwardTogether(self):
        """Testing WbForward functionality together"""
        stim = self.wbForward(self.op2_out)
        stim_v = self.wbForward(self.op2_out_v)

        Simulation(self.dut, stim, self.dut_v, stim_v).run(quiet=1)


if __name__ == '__main)__':
    unittest.main()
