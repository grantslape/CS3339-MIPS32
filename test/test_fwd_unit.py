import unittest
import sys

from unittest import TestCase
from myhdl import intbv, delay, Simulation, Signal

sys.path.append("src/python")
from fwd_unit import fwd_unit, fwd_unit_v
from settings import settings as sf

HALF_PERIOD = delay(sf['PERIOD'] / 2)


def setup():
    rt_in = Signal(intbv(0)[5:])
    rs_in = Signal(intbv(0)[5:])
    ex_rd, mem_rd = [Signal(intbv(0)[5:]) for i in range(2)]
    mem_reg_write, wb_reg_write = [Signal(intbv(0)[1:]) for i in range(2)]
    forward_a, forward_b = [Signal(intbv(0)[2:]) for i in range(2)]
    return rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b


class TestFwdUnitHoldValue(TestCase):

    def bench(self, rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b):
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.assertEqual(forward_a, 0)
            self.assertEqual(forward_b, 0)
            self.assertEqual(mem_reg_write, 0)
            self.assertEqual(wb_reg_write, 0)
            self.assertEqual(rt_in, 0)
            self.assertEqual(rs_in, 0)
            self.assertEqual(ex_rd, 0)
            self.assertEqual(mem_rd, 0)
            yield HALF_PERIOD

    def testHoldValuePython(self):
        """ Checking that module holds value when no input changes from Python """
        rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b = setup()
        dut = fwd_unit(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b)
        stim = self.bench(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b)

        sim = Simulation(dut, stim)
        sim.run(quiet=1)

    def testHoldValueVerilog(self):
        """ Checking that module holds value when no input changes from Verilog """
        rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b = setup()
        dut = fwd_unit_v(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b)
        stim = self.bench(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b)

        sim = Simulation(dut, stim)
        sim.run(quiet=1)

    def testHoldValueTogether(self):
        """ Checking that module holds value when no input changes from Cosimulation """
        def test():
            for i in range(sf['DEFAULT_TEST_LENGTH']):
                self.assertEqual(forward_a_v, 0)
                self.assertEqual(forward_b_v, 0)
            yield HALF_PERIOD

        rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b = setup()
        forward_a_v, forward_b_v = [Signal(intbv(0)[2:]) for i in range(2)]
        dut = fwd_unit(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b)
        dut_v = fwd_unit_v(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a_v, forward_b_v)
        stim = self.bench(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b)

        sim = Simulation(dut, dut_v, stim, test())
        sim.run(quiet=1)


if __name__ == '__main__':
    unittest.main()
