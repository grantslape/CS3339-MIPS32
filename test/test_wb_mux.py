import unittest
import sys
from random import randint

from unittest import TestCase
from myhdl import intbv, delay, Simulation, Signal, StopSimulation

sys.path.append("src/python")
from wb_mux import wb_mux, wb_mux_v
from settings import settings as sf

HALF_PERIOD = delay(sf['PERIOD'] / 2)


def setup():
    mem_to_reg = Signal(intbv(0)[1:])
    rdata_in, result_in, wb_out = [Signal(intbv(0, min=sf['SIGNED_MIN_VALUE'], max=sf['SIGNED_MAX_VALUE']))
                                   for i in range(3)]

    return mem_to_reg, rdata_in, result_in, wb_out


@unittest.skip("WB Mux not implemented")
class TestWbMux(TestCase):
    """Testing deasserted functionality"""
    def setUp(self):
        self.mem_to_reg = Signal(intbv(0)[1:])
        self.rdata_in, self.result_in, self.wb_out, self.wb_out_v = [
            Signal(intbv(0, min=sf['SIGNED_MIN_VALUE'], max=sf['SIGNED_MAX_VALUE'])) for i in range(4)
        ]
        self.dut = wb_mux(self.mem_to_reg, self.rdata_in, self.result_in, self.wb_out)

    def deassert(self, wb_out):
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.mem_to_reg.next = 0
            self.rdata_in.next = intbv(randint(sf['SIGNED_MIN_VALUE'], sf['SIGNED_MAX_VALUE']))
            self.result_in.next = intbv(randint(sf['SIGNED_MIN_VALUE'], sf['SIGNED_MAX_VALUE']))
            yield HALF_PERIOD
            self.assertEqual(self.mem_to_reg, 0)
            self.assertEqual(wb_out, self.result_in)
        raise StopSimulation

    def asserted(self, wb_out):
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.mem_to_reg.next = 1
            self.rdata_in.next = intbv(randint(sf['SIGNED_MIN_VALUE'], sf['SIGNED_MAX_VALUE']))
            self.result_in.next = intbv(randint(sf['SIGNED_MIN_VALUE'], sf['SIGNED_MAX_VALUE']))
            yield HALF_PERIOD
            self.assertEqual(self.mem_to_reg, 1)
            self.assertEqual(wb_out, self.rdata_in)
        raise StopSimulation

    def dynamic(self, wb_out):
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.mem_to_reg.next = randint(0, 1)
            self.rdata_in.next = intbv(randint(sf['SIGNED_MIN_VALUE'], sf['SIGNED_MAX_VALUE']))
            self.result_in.next = intbv(randint(sf['SIGNED_MIN_VALUE'], sf['SIGNED_MAX_VALUE']))
            yield HALF_PERIOD
            if self.mem_to_reg == 0:
                self.assertEqual(wb_out, self.result_in)
            else:
                self.assertEqual(self.mem_to_reg, 1)
                self.assertEqual(wb_out, self.rdata_in)
        raise StopSimulation

    def testHoldDeassertPython(self):
        """ Checking that result_data is outputted when deasserted Python"""
        stim = self.deassert(self.wb_out)
        Simulation(self.dut, stim).run(quiet=1)

    def testHoldDeassertVerilog(self):
        """ Checking that result_data is outputted when deasserted Verilog"""
        stim = self.deassert(self.wb_out_v)
        dut_v = wb_mux_v(self.mem_to_reg, self.rdata_in, self.result_in, self.wb_out_v)
        Simulation(dut_v, stim).run(quiet=1)

    def testHoldDeassertTogether(self):
        """ Checking that result_data is outputted when deasserted Cosimulation"""
        stim = self.deassert(self.wb_out)
        stim_v = self.deassert(self.wb_out_v)
        dut_v = wb_mux_v(self.mem_to_reg, self.rdata_in, self.result_in, self.wb_out_v)
        Simulation(self.dut, stim, dut_v, stim_v).run(quiet=1)

    def testHoldAssertPython(self):
        """ Checking that rdata_in is outputted when Asserted Python"""
        stim = self.asserted(self.wb_out)
        Simulation(self.dut, stim).run(quiet=1)

    def testHoldAssertVerilog(self):
        """ Checking that rdata_in is outputted when Asserted Verilog"""
        stim = self.asserted(self.wb_out_v)
        dut_v = wb_mux_v(self.mem_to_reg, self.rdata_in, self.result_in, self.wb_out_v)
        Simulation(dut_v, stim).run(quiet=1)

    def testHoldAssertTogether(self):
        """ Checking that rdata_in is outputted when Asserted Cosimulation"""
        stim = self.asserted(self.wb_out)
        stim_v = self.asserted(self.wb_out_v)
        dut_v = wb_mux_v(self.mem_to_reg, self.rdata_in, self.result_in, self.wb_out_v)
        Simulation(self.dut, stim, dut_v, stim_v).run(quiet=1)

    def testHoldDynamicPython(self):
        """ Checking that correct output is assigned Python"""
        stim = self.dynamic(self.wb_out)
        Simulation(self.dut, stim).run(quiet=1)

    def testDynamicVerilog(self):
        """ Checking that correct output is assigned Verilog"""
        stim = self.dynamic(self.wb_out_v)
        dut_v = wb_mux_v(self.mem_to_reg, self.rdata_in, self.result_in, self.wb_out_v)
        Simulation(dut_v, stim).run(quiet=1)

    def testDynamicTogether(self):
        """ Checking that correct output is assigned Cosimulation"""
        stim = self.dynamic(self.wb_out)
        stim_v = self.dynamic(self.wb_out_v)
        dut_v = wb_mux_v(self.mem_to_reg, self.rdata_in, self.result_in, self.wb_out_v)
        Simulation(self.dut, stim, dut_v, stim_v).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
