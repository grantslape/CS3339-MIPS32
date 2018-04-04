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


class TestWbMuxDeassert(TestCase):
    """Testing deasserted functionality"""

    def bench(self, mem_to_reg, rdata_in, result_in, wb_out):
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            mem_to_reg.next = 0
            rdata_in.next = intbv(randint(sf['SIGNED_MIN_VALUE'], sf['SIGNED_MAX_VALUE']))
            result_in.next = intbv(randint(sf['SIGNED_MIN_VALUE'], sf['SIGNED_MAX_VALUE']))
            yield HALF_PERIOD
            self.assertEqual(mem_to_reg, 0)
            self.assertEqual(wb_out, result_in)
        raise StopSimulation

    def testHoldDeassertPython(self):
        """ Checking that result_data is outputted when deasserted Python"""
        mem_to_reg, rdata_in, result_in, wb_out = setup()
        dut = wb_mux(mem_to_reg, rdata_in, result_in, wb_out)
        stim = self.bench(mem_to_reg, rdata_in, result_in, wb_out)

        Simulation(dut, stim).run(quiet=1)

    def testHoldDeassertVerilog(self):
        """ Checking that result_data is outputted when deasserted Verilog"""
        mem_to_reg, rdata_in, result_in, wb_out = setup()
        dut = wb_mux_v(mem_to_reg, rdata_in, result_in, wb_out)
        stim = self.bench(mem_to_reg, rdata_in, result_in, wb_out)

        Simulation(dut, stim).run(quiet=1)

    def testHoldDeassertTogether(self):
        """ Checking that result_data is outputted when deasserted Cosimulation"""
        mem_to_reg, rdata_in, result_in, wb_out = setup()
        wb_out_v = Signal(intbv(0, min=sf['SIGNED_MIN_VALUE'], max=sf['SIGNED_MAX_VALUE']))
        dut = wb_mux(mem_to_reg, rdata_in, result_in, wb_out)
        dut_v = wb_mux_v(mem_to_reg, rdata_in, result_in, wb_out_v)
        stim = self.bench(mem_to_reg, rdata_in, result_in, wb_out)
        stim_v = self.bench(mem_to_reg, rdata_in, result_in, wb_out_v)

        Simulation(dut, dut_v, stim, stim_v).run(quiet=1)


class TestWbMuxAssert(TestCase):
    """Testing asserted functionality"""

    def bench(self, mem_to_reg, rdata_in, result_in, wb_out):
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            mem_to_reg.next = 1
            rdata_in.next = intbv(randint(sf['SIGNED_MIN_VALUE'], sf['SIGNED_MAX_VALUE']))
            result_in.next = intbv(randint(sf['SIGNED_MIN_VALUE'], sf['SIGNED_MAX_VALUE']))
            yield HALF_PERIOD
            self.assertEqual(mem_to_reg, 1)
            self.assertEqual(wb_out, rdata_in)
        raise StopSimulation

    def testHoldAssertPython(self):
        """ Checking that rdata_in is outputted when Asserted Python"""
        mem_to_reg, rdata_in, result_in, wb_out = setup()
        dut = wb_mux(mem_to_reg, rdata_in, result_in, wb_out)
        stim = self.bench(mem_to_reg, rdata_in, result_in, wb_out)

        Simulation(dut, stim).run(quiet=1)

    def testHoldAssertVerilog(self):
        """ Checking that rdata_in is outputted when Asserted Verilog"""
        mem_to_reg, rdata_in, result_in, wb_out = setup()
        dut = wb_mux_v(mem_to_reg, rdata_in, result_in, wb_out)
        stim = self.bench(mem_to_reg, rdata_in, result_in, wb_out)

        Simulation(dut, stim).run(quiet=1)

    def testHoldAssertTogether(self):
        """ Checking that rdata_in is outputted when Asserted Cosimulation"""
        mem_to_reg, rdata_in, result_in, wb_out = setup()
        wb_out_v = Signal(intbv(0, min=sf['SIGNED_MIN_VALUE'], max=sf['SIGNED_MAX_VALUE']))
        dut = wb_mux(mem_to_reg, rdata_in, result_in, wb_out)
        dut_v = wb_mux_v(mem_to_reg, rdata_in, result_in, wb_out_v)
        stim = self.bench(mem_to_reg, rdata_in, result_in, wb_out)
        stim_v = self.bench(mem_to_reg, rdata_in, result_in, wb_out_v)

        Simulation(dut, dut_v, stim, stim_v).run(quiet=1)


class TestWbMuxDynamic(TestCase):
    """Testing dynamic functionality"""

    def bench(self, mem_to_reg, rdata_in, result_in, wb_out):
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            mem_to_reg.next = randint(0, 1)
            rdata_in.next = intbv(randint(sf['SIGNED_MIN_VALUE'], sf['SIGNED_MAX_VALUE']))
            result_in.next = intbv(randint(sf['SIGNED_MIN_VALUE'], sf['SIGNED_MAX_VALUE']))
            yield HALF_PERIOD
            if mem_to_reg == 0:
                self.assertEqual(wb_out, result_in)
            else:
                self.assertEqual(mem_to_reg, 1)
                self.assertEqual(wb_out, rdata_in)
        raise StopSimulation

    def testHoldDynamicPython(self):
        """ Checking that correct output is assigned Python"""
        mem_to_reg, rdata_in, result_in, wb_out = setup()
        dut = wb_mux(mem_to_reg, rdata_in, result_in, wb_out)
        stim = self.bench(mem_to_reg, rdata_in, result_in, wb_out)

        Simulation(dut, stim).run(quiet=1)

    def testDynamicVerilog(self):
        """ Checking that correct output is assigned Verilog"""
        mem_to_reg, rdata_in, result_in, wb_out = setup()
        dut = wb_mux_v(mem_to_reg, rdata_in, result_in, wb_out)
        stim = self.bench(mem_to_reg, rdata_in, result_in, wb_out)

        Simulation(dut, stim).run(quiet=1)

    def testDynamicTogether(self):
        """ Checking that correct output is assigned Cosimulation"""
        mem_to_reg, rdata_in, result_in, wb_out = setup()
        wb_out_v = Signal(intbv(0, min=sf['SIGNED_MIN_VALUE'], max=sf['SIGNED_MAX_VALUE']))
        dut = wb_mux(mem_to_reg, rdata_in, result_in, wb_out)
        dut_v = wb_mux_v(mem_to_reg, rdata_in, result_in, wb_out_v)
        stim = self.bench(mem_to_reg, rdata_in, result_in, wb_out)
        stim_v = self.bench(mem_to_reg, rdata_in, result_in, wb_out_v)

        Simulation(dut, dut_v, stim, stim_v).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
