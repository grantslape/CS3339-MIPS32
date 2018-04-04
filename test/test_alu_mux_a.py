import unittest
from random import randint
from unittest import TestCase
from myhdl import intbv, delay, Simulation, Signal, StopSimulation

import sys
sys.path.append("src/python")

from alu_mux_a import alu_mux_a, alu_mux_a_v
from settings import settings as sf

HALF_PERIOD = delay(sf['PERIOD'] / 2)


if __name__ == '__main__':
    unittest.main()


def setup():
    forward_a = Signal(intbv(0)[2:])
    r_data1, mem_rd, wb_rd, op1_out = [Signal(intbv(0, min=sf['MIN_SIGNED_VALUE'], max=sf['MAX_SIGNED_VALUE']))
                                       for i in range(4)]
    return forward_a, r_data1, mem_rd, wb_rd, op1_out


@unittest.skip("ALU Mux A not implemented")
class TestAluMuxADeassert(TestCase):
    """Testing deasserted functionality"""

    def bench(self, forward_a, r_data1, mem_rd, wb_rd, op1_out):
        forward_a.next = 0
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            r_data1.next = Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                        min=sf['MIN_SIGNED_VALUE'],
                                        max=sf['MAX_SIGNED_VALUE']))
            while mem_rd == r_data1 or wb_rd == r_data1:
                mem_rd.next = Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                           min=sf['MIN_SIGNED_VALUE'],
                                           max=sf['MAX_SIGNED_VALUE']))
                wb_rd.next = Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                          min=sf['MIN_SIGNED_VALUE'],
                                          max=sf['MAX_SIGNED_VALUE']))
            yield HALF_PERIOD
            self.assertEqual(op1_out, r_data1)
            self.assertNotEquals(op1_out, mem_rd)
            self.assertNotEquals(op1_out, wb_rd)
        raise StopSimulation

    def testAluMuxADeassertPython(self):
        """Testing deasserted functionality Python"""
        forward_a, r_data1, mem_rd, wb_rd, op1_out = setup()
        dut = alu_mux_a(forward_a, r_data1, mem_rd, wb_rd, op1_out)
        stim = self.bench(forward_a, r_data1, mem_rd, wb_rd, op1_out)

        Simulation(dut, stim).run(quiet=1)

    def testAluMuxADeassertVerilog(self):
        """Testing deasserted functionality Verilog"""
        forward_a, r_data1, mem_rd, wb_rd, op1_out = setup()
        dut = alu_mux_a_v(forward_a, r_data1, mem_rd, wb_rd, op1_out)
        stim = self.bench(forward_a, r_data1, mem_rd, wb_rd, op1_out)

        Simulation(dut, stim).run(quiet=1)

    def testAluMuxADeassertTogether(self):
        """Testing deasserted functionality together"""
        forward_a, r_data1, mem_rd, wb_rd, op1_out = setup()
        op1_out_v = Signal(intbv(0, min=sf['MIN_SIGNED_VALUE'], max=sf['MAX_SIGNED_VALUE']))
        dut = alu_mux_a(forward_a, r_data1, mem_rd, wb_rd, op1_out)
        dut_v = alu_mux_a_v(forward_a, r_data1, mem_rd, wb_rd, op1_out_v)
        stim = self.bench(forward_a, r_data1, mem_rd, wb_rd, op1_out)
        stim_v = self.bench(forward_a, r_data1, mem_rd, wb_rd, op1_out_v)

        Simulation(dut, stim, dut_v, stim_v).run(quiet=1)


@unittest.skip("ALU Mux A not implemented")
class TestAluMuxAMemForward(TestCase):
    """Testing MemForward functionality"""

    def bench(self, forward_a, r_data1, mem_rd, wb_rd, op1_out):
        forward_a.next = 1
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            mem_rd.next = Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                       min=sf['MIN_SIGNED_VALUE'],
                                       max=sf['MAX_SIGNED_VALUE']))
            while mem_rd == r_data1 or wb_rd == mem_rd:
                r_data1.next = Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                           min=sf['MIN_SIGNED_VALUE'],
                                           max=sf['MAX_SIGNED_VALUE']))
                wb_rd.next = Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                          min=sf['MIN_SIGNED_VALUE'],
                                          max=sf['MAX_SIGNED_VALUE']))
            yield HALF_PERIOD
            self.assertEqual(op1_out, mem_rd)
            self.assertNotEquals(op1_out, r_data1)
            self.assertNotEquals(op1_out, wb_rd)
        raise StopSimulation

    def testAluMuxAMemForwardPython(self):
        """Testing MemForward functionality Python"""
        forward_a, r_data1, mem_rd, wb_rd, op1_out = setup()
        dut = alu_mux_a(forward_a, r_data1, mem_rd, wb_rd, op1_out)
        stim = self.bench(forward_a, r_data1, mem_rd, wb_rd, op1_out)

        Simulation(dut, stim).run(quiet=1)

    def testAluMuxAMemForwardVerilog(self):
        """Testing MemForward functionality Verilog"""
        forward_a, r_data1, mem_rd, wb_rd, op1_out = setup()
        dut = alu_mux_a_v(forward_a, r_data1, mem_rd, wb_rd, op1_out)
        stim = self.bench(forward_a, r_data1, mem_rd, wb_rd, op1_out)

        Simulation(dut, stim).run(quiet=1)

    def testAluMuxAMemForwardTogether(self):
        """Testing MemForward functionality together"""
        forward_a, r_data1, mem_rd, wb_rd, op1_out = setup()
        op1_out_v = Signal(intbv(0, min=sf['MIN_SIGNED_VALUE'], max=sf['MAX_SIGNED_VALUE']))
        dut = alu_mux_a(forward_a, r_data1, mem_rd, wb_rd, op1_out)
        dut_v = alu_mux_a_v(forward_a, r_data1, mem_rd, wb_rd, op1_out_v)
        stim = self.bench(forward_a, r_data1, mem_rd, wb_rd, op1_out)
        stim_v = self.bench(forward_a, r_data1, mem_rd, wb_rd, op1_out_v)

        Simulation(dut, stim, dut_v, stim_v).run(quiet=1)


@unittest.skip("ALU Mux A not implemented")
class TestAluMuxAWbForward(TestCase):
    """Testing WbForward functionality"""

    def bench(self, forward_a, r_data1, mem_rd, wb_rd, op1_out):
        forward_a.next = 2
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            wb_rd.next = Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                      min=sf['MIN_SIGNED_VALUE'],
                                      max=sf['MAX_SIGNED_VALUE']))
            while wb_rd == r_data1 or wb_rd == mem_rd:
                mem_rd.next = Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                           min=sf['MIN_SIGNED_VALUE'],
                                           max=sf['MAX_SIGNED_VALUE']))
                r_data1.next = Signal(intbv(randint(sf['MIN_SIGNED_VALUE'], sf['MAX_SIGNED_VALUE']),
                                            min=sf['MIN_SIGNED_VALUE'],
                                            max=sf['MAX_SIGNED_VALUE']))
            yield HALF_PERIOD
            self.assertEqual(op1_out, wb_rd)
            self.assertNotEquals(op1_out, r_data1)
            self.assertNotEquals(op1_out, mem_rd)
        raise StopSimulation

    def testAluMuxAWbForwardPython(self):
        """Testing WbForward functionality Python"""
        forward_a, r_data1, mem_rd, wb_rd, op1_out = setup()
        dut = alu_mux_a(forward_a, r_data1, mem_rd, wb_rd, op1_out)
        stim = self.bench(forward_a, r_data1, mem_rd, wb_rd, op1_out)

        Simulation(dut, stim).run(quiet=1)

    def testAluMuxAWbForwardVerilog(self):
        """Testing WbForward functionality Verilog"""
        forward_a, r_data1, mem_rd, wb_rd, op1_out = setup()
        dut = alu_mux_a_v(forward_a, r_data1, mem_rd, wb_rd, op1_out)
        stim = self.bench(forward_a, r_data1, mem_rd, wb_rd, op1_out)

        Simulation(dut, stim).run(quiet=1)

    def testAluMuxAWbForwardTogether(self):
        """Testing WbForward functionality together"""
        forward_a, r_data1, mem_rd, wb_rd, op1_out = setup()
        op1_out_v = Signal(intbv(0, min=sf['MIN_SIGNED_VALUE'], max=sf['MAX_SIGNED_VALUE']))
        dut = alu_mux_a(forward_a, r_data1, mem_rd, wb_rd, op1_out)
        dut_v = alu_mux_a_v(forward_a, r_data1, mem_rd, wb_rd, op1_out_v)
        stim = self.bench(forward_a, r_data1, mem_rd, wb_rd, op1_out)
        stim_v = self.bench(forward_a, r_data1, mem_rd, wb_rd, op1_out_v)

        Simulation(dut, stim, dut_v, stim_v).run(quiet=1)


if __name__ == '__main)__':
    unittest.main()
