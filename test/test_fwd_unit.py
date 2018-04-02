import unittest
import sys

from unittest import TestCase
from myhdl import intbv, delay, Simulation, Signal, Cosimulation

sys.path.append("src/python")
from fwd_unit import fwd_unit, fwd_unit_v
from settings import settings as sf

HALF_PERIOD = delay(sf['PERIOD'] / 2)


class TestFwdUnitHoldValue(TestCase):
    def setup(self):
        rt_in = Signal(intbv(10)[5:])
        rs_in = Signal(intbv(11)[5:])
        ex_rd, mem_rd = [Signal(intbv(0)[5:]) for i in range(2)]
        mem_reg_write, wb_reg_write = [Signal(intbv(0)[1:]) for i in range(2)]
        forward_a, forward_b = [Signal(intbv(0)[2:]) for i in range(2)]
        return rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b

    def bench(self, rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b):
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.assertEqual(forward_a, 0)
            self.assertEqual(forward_b, 0)
            self.assertEqual(mem_reg_write, 0)
            self.assertEqual(wb_reg_write, 0)
            yield HALF_PERIOD

    def testHoldValuePython(self):
        """ Checking that module holds value when no input changes from Python """
        rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b = self.setup()
        dut = fwd_unit(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b)
        stim = self.bench(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b)

        sim = Simulation(dut, stim)
        sim.run(quiet=1)

    def testHoldValueVerilog(self):
        rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b = self.setup()
        dut = fwd_unit_v(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b)
        stim = self.bench(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b)

        sim = Simulation(dut, stim)
        sim.run(quiet=1)


if __name__ == '__main__':
    unittest.main()
