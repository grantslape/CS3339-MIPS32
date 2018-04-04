import unittest
from random import randint
from unittest import TestCase
from myhdl import intbv, delay, Simulation, Signal, StopSimulation

import sys
sys.path.append("src/python")

from alu_mux_b import alu_mux_b, alu_mux_b_v
from settings import settings as sf

HALF_PERIOD = delay(sf['PERIOD'] / 2)


if __name__ == '__main__':
    unittest.main()


def setup():
    forward_a = Signal(intbv(0)[2:])
    r_data2, mem_rd, wb_rd, op2_out = [Signal(intbv(0, min=sf['MIN_SIGNED_VALUE'], max=sf['MAX_SIGNED_VALUE']))
                                       for i in range(4)]
    return forward_a, r_data2, mem_rd, wb_rd, op2_out


class TestAluMuxBDeassert(TestCase):
    """Testing deasserted functionality"""

    def bench(self, forward_a, r_data2, mem_rd, wb_rd, op2_out):
        forward_a.next = 0
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            r_data2.next = Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                        min=sf['MIN_SIGNED_VALUE'],
                                        max=sf['MAX_SIGNED_VALUE']))
            while mem_rd == r_data2 or wb_rd == r_data2:
                mem_rd.next = Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                           min=sf['MIN_SIGNED_VALUE'],
                                           max=sf['MAX_SIGNED_VALUE']))
                wb_rd.next = Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                          min=sf['MIN_SIGNED_VALUE'],
                                          max=sf['MAX_SIGNED_VALUE']))
            yield HALF_PERIOD
            self.assertEqual(op2_out, r_data2)
            self.assertNotEquals(op2_out, mem_rd)
            self.assertNotEquals(op2_out, wb_rd)
        raise StopSimulation

    def testAluMuxBDeassertPython(self):
        """Testing deasserted functionality Python"""
        forward_a, r_data2, mem_rd, wb_rd, op2_out = setup()
        dut = alu_mux_b(forward_a, r_data2, mem_rd, wb_rd, op2_out)
        stim = self.bench(forward_a, r_data2, mem_rd, wb_rd, op2_out)

        Simulation(dut, stim).run(quiet=1)

    def testAluMuxBDeassertVerilog(self):
        """Testing deasserted functionality Verilog"""
        forward_a, r_data2, mem_rd, wb_rd, op2_out = setup()
        dut = alu_mux_b_v(forward_a, r_data2, mem_rd, wb_rd, op2_out)
        stim = self.bench(forward_a, r_data2, mem_rd, wb_rd, op2_out)

        Simulation(dut, stim).run(quiet=1)

    def testAluMuxBDeassertTogether(self):
        """Testing deasserted functionality together"""
        forward_a, r_data2, mem_rd, wb_rd, op2_out = setup()
        op2_out_v = Signal(intbv(0, min=sf['MIN_SIGNED_VALUE'], max=sf['MAX_SIGNED_VALUE']))
        dut = alu_mux_b(forward_a, r_data2, mem_rd, wb_rd, op2_out)
        dut_v = alu_mux_b_v(forward_a, r_data2, mem_rd, wb_rd, op2_out_v)
        stim = self.bench(forward_a, r_data2, mem_rd, wb_rd, op2_out)
        stim_v = self.bench(forward_a, r_data2, mem_rd, wb_rd, op2_out_v)

        Simulation(dut, stim, dut_v, stim_v).run(quiet=1)


class TestAluMuxBMemForward(TestCase):
    """Testing MemForward functionality"""

    def bench(self, forward_a, r_data2, mem_rd, wb_rd, op2_out):
        forward_a.next = 1
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            mem_rd.next = Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                       min=sf['MIN_SIGNED_VALUE'],
                                       max=sf['MAX_SIGNED_VALUE']))
            while mem_rd == r_data2 or wb_rd == mem_rd:
                mem_rd.next = Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                           min=sf['MIN_SIGNED_VALUE'],
                                           max=sf['MAX_SIGNED_VALUE']))
                wb_rd.next = Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                          min=sf['MIN_SIGNED_VALUE'],
                                          max=sf['MAX_SIGNED_VALUE']))
            yield HALF_PERIOD
            self.assertEqual(op2_out, mem_rd)
            self.assertNotEquals(op2_out, r_data2)
            self.assertNotEquals(op2_out, wb_rd)
        raise StopSimulation

    def testAluMuxBMemForwardPython(self):
        """Testing MemForward functionality Python"""
        forward_a, r_data2, mem_rd, wb_rd, op2_out = setup()
        dut = alu_mux_b(forward_a, r_data2, mem_rd, wb_rd, op2_out)
        stim = self.bench(forward_a, r_data2, mem_rd, wb_rd, op2_out)

        Simulation(dut, stim).run(quiet=1)

    def testAluMuxbMemForwardVerilog(self):
        """Testing MemForward functionality Verilog"""
        forward_a, r_data2, mem_rd, wb_rd, op2_out = setup()
        dut = alu_mux_b_v(forward_a, r_data2, mem_rd, wb_rd, op2_out)
        stim = self.bench(forward_a, r_data2, mem_rd, wb_rd, op2_out)

        Simulation(dut, stim).run(quiet=1)

    def testAluMuxBMemForwardTogether(self):
        """Testing MemForward functionality together"""
        forward_a, r_data2, mem_rd, wb_rd, op2_out = setup()
        op2_out_v = Signal(intbv(0, min=sf['MIN_SIGNED_VALUE'], max=sf['MAX_SIGNED_VALUE']))
        dut = alu_mux_b(forward_a, r_data2, mem_rd, wb_rd, op2_out)
        dut_v = alu_mux_b_v(forward_a, r_data2, mem_rd, wb_rd, op2_out_v)
        stim = self.bench(forward_a, r_data2, mem_rd, wb_rd, op2_out)
        stim_v = self.bench(forward_a, r_data2, mem_rd, wb_rd, op2_out_v)

        Simulation(dut, stim, dut_v, stim_v).run(quiet=1)


class TestAluMuxBWbForward(TestCase):
    """Testing WbForward functionality"""

    def bench(self, forward_a, r_data2, mem_rd, wb_rd, op2_out):
        forward_a.next = 2
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            wb_rd.next = Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                      min=sf['MIN_SIGNED_VALUE'],
                                      max=sf['MAX_SIGNED_VALUE']))
            while wb_rd == r_data2 or wb_rd == mem_rd:
                mem_rd.next = Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                           min=sf['MIN_SIGNED_VALUE'],
                                           max=sf['MAX_SIGNED_VALUE']))
                r_data2.next = Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                            min=sf['MIN_SIGNED_VALUE'],
                                            max=sf['MAX_SIGNED_VALUE']))
            yield HALF_PERIOD
            self.assertEqual(op2_out, wb_rd)
            self.assertNotEquals(op2_out, r_data2)
            self.assertNotEquals(op2_out, mem_rd)
        raise StopSimulation

    def testAluMuxBWbForwardPython(self):
        """Testing WbForward functionality Python"""
        forward_a, r_data2, mem_rd, wb_rd, op2_out = setup()
        dut = alu_mux_b(forward_a, r_data2, mem_rd, wb_rd, op2_out)
        stim = self.bench(forward_a, r_data2, mem_rd, wb_rd, op2_out)

        Simulation(dut, stim).run(quiet=1)

    def testAluMuxBWbForwardVerilog(self):
        """Testing WbForward functionality Verilog"""
        forward_a, r_data2, mem_rd, wb_rd, op2_out = setup()
        dut = alu_mux_b_v(forward_a, r_data2, mem_rd, wb_rd, op2_out)
        stim = self.bench(forward_a, r_data2, mem_rd, wb_rd, op2_out)

        Simulation(dut, stim).run(quiet=1)

    def testAluMuxBWbForwardTogether(self):
        """Testing WbForward functionality together"""
        forward_a, r_data2, mem_rd, wb_rd, op2_out = setup()
        op2_out_v = Signal(intbv(0, min=sf['MIN_SIGNED_VALUE'], max=sf['MAX_SIGNED_VALUE']))
        dut = alu_mux_b(forward_a, r_data2, mem_rd, wb_rd, op2_out)
        dut_v = alu_mux_b_v(forward_a, r_data2, mem_rd, wb_rd, op2_out_v)
        stim = self.bench(forward_a, r_data2, mem_rd, wb_rd, op2_out)
        stim_v = self.bench(forward_a, r_data2, mem_rd, wb_rd, op2_out_v)

        Simulation(dut, stim, dut_v, stim_v).run(quiet=1)
