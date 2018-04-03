import unittest
import sys

from unittest import TestCase
from myhdl import intbv, delay, Simulation, Signal, StopSimulation

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


class TestFwdUnitBaseCases(TestCase):
    """Test Forwarding Known Cases"""
    def noForwardTest(self, rt_in, rs_in, forward_b, forward_a, forward_a_v=intbv(0), forward_b_v=intbv(0)):
        """Stim for no forwarding"""
        rt_in.next = 10
        rs_in.next = 11
        yield HALF_PERIOD
        self.assertEqual(forward_b, 0)
        self.assertEqual(forward_a, 0)
        self.assertEqual(forward_a_v, 0)
        self.assertEqual(forward_b_v, 0)
        raise StopSimulation

    def forwardATest(self, rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, forward_a, forward_b):
        """Stim for forward A cases.  See p310 of book"""
        rs_in.next = 11
        ex_rd.next = 11
        rt_in.next = 10
        mem_reg_write.next = 1
        yield HALF_PERIOD
        self.assertEqual(forward_b, 0)
        self.assertEqual(forward_a, 0b10)
        ex_rd.next = 12
        mem_rd.next = 11
        yield HALF_PERIOD
        self.assertEqual(forward_b, 0)
        self.assertEqual(forward_a, 0b01)
        mem_reg_write.next = 0
        yield HALF_PERIOD
        self.assertEqual(forward_b, 0)
        self.assertEqual(forward_a, 0)
        rs_in.next = 11
        ex_rd.next = 11
        mem_reg_write.next = 1
        mem_rd.next = 1
        yield HALF_PERIOD
        self.assertEqual(forward_b, 0)
        self.assertEqual(forward_a, 0b10)

    def forwardBTest(self, rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, forward_a, forward_b):
        """Stim for forward A cases.  See p310 of book"""
        rt_in.next = 11
        ex_rd.next = 11
        rs_in.next = 10
        mem_reg_write.next = 1
        yield HALF_PERIOD
        self.assertEqual(forward_a, 0)
        self.assertEqual(forward_b, 0b10)
        ex_rd.next = 12
        mem_rd.next = 11
        yield HALF_PERIOD
        self.assertEqual(forward_a, 0)
        self.assertEqual(forward_b, 0b01)
        mem_reg_write.next = 0
        yield HALF_PERIOD
        self.assertEqual(forward_b, 0)
        self.assertEqual(forward_a, 0)
        rt_in.next = 11
        ex_rd.next = 11
        mem_reg_write.next = 1
        mem_rd.next = 1
        yield HALF_PERIOD
        self.assertEqual(forward_a, 0)
        self.assertEqual(forward_b, 0b10)


    def testNoForwardPython(self):
        """Test no forwarding Python"""
        rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b = setup()
        dut = fwd_unit(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b)

        sim = Simulation(dut, self.noForwardTest(rt_in, rs_in, forward_b, forward_a))
        sim.run(quiet=1)

    def testNoForwardVerilog(self):
        """Test no forwarding Verilog"""
        rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b = setup()
        dut = fwd_unit_v(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b)

        sim = Simulation(dut, self.noForwardTest(rt_in, rs_in, forward_b, forward_a))
        sim.run(quiet=1)

    def testNoForwardTogether(self):
        """Test no forwarding Verilog"""
        rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b = setup()
        forward_a_v, forward_b_v = [Signal(intbv(0)[2:]) for i in range(2)]
        dut = fwd_unit(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b)
        dut_v = fwd_unit_v(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a_v, forward_b_v)

        sim = Simulation(dut, dut_v, self.noForwardTest(rt_in, rs_in, forward_b, forward_a))
        sim.run(quiet=1)

    def testForwardACasesPython(self):
        """Test Forward A cases Python"""
        rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b = setup()
        dut = fwd_unit(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b)

        sim = Simulation(dut, self.forwardATest(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, forward_a, forward_b))
        sim.run(quiet=1)

    def testForwardACasesVerilog(self):
        """Test Forward A cases Verilog"""
        rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b = setup()
        dut = fwd_unit_v(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b)

        sim = Simulation(dut, self.forwardATest(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, forward_a, forward_b))
        sim.run(quiet=1)

    def testForwardACasesTogether(self):
        """Test Forward A cases together"""
        def test():
            yield HALF_PERIOD
            self.assertEqual(forward_b_v, 0)
            self.assertEqual(forward_a_v, 0b10)
            yield HALF_PERIOD
            self.assertEqual(forward_b_v, 0)
            self.assertEqual(forward_a_v, 0b01)
            yield HALF_PERIOD
            self.assertEqual(forward_b_v, 0)
            self.assertEqual(forward_a_v, 0)
            yield HALF_PERIOD
            self.assertEqual(forward_b_v, 0)
            self.assertEqual(forward_a_v, 0b10)

        forward_a_v, forward_b_v = [Signal(intbv(0)[2:]) for i in range(2)]
        rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b = setup()
        dut = fwd_unit(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b)
        dut_v = fwd_unit_v(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a_v, forward_b_v)

        stim = self.forwardATest(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, forward_a, forward_b)
        sim = Simulation(dut, dut_v, stim, test())
        sim.run(quiet=1)

    def testForwardBCasesPython(self):
        """Test Forward B cases Python"""
        rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b = setup()
        dut = fwd_unit(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b)

        sim = Simulation(dut, self.forwardBTest(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, forward_a, forward_b))
        sim.run(quiet=1)

    def testForwardBCasesVerilog(self):
        """Test Forward B cases Verilog"""
        rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b = setup()
        dut = fwd_unit_v(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b)

        sim = Simulation(dut, self.forwardBTest(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, forward_a, forward_b))
        sim.run(quiet=1)

    def testForwardBCasesTogether(self):
        """Test Forward A cases together"""
        def test():
            yield HALF_PERIOD
            self.assertEqual(forward_a_v, 0)
            self.assertEqual(forward_b_v, 0b10)
            yield HALF_PERIOD
            self.assertEqual(forward_a_v, 0)
            self.assertEqual(forward_b_v, 0b01)
            yield HALF_PERIOD
            self.assertEqual(forward_b_v, 0)
            self.assertEqual(forward_a_v, 0)
            yield HALF_PERIOD
            self.assertEqual(forward_a_v, 0)
            self.assertEqual(forward_b_v, 0b10)

        forward_a_v, forward_b_v = [Signal(intbv(0)[2:]) for i in range(2)]
        rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b = setup()
        dut = fwd_unit(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b)
        dut_v = fwd_unit_v(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a_v, forward_b_v)

        stim = self.forwardATest(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, forward_a, forward_b)
        sim = Simulation(dut, dut_v, stim, test())
        sim.run(quiet=1)


class TestForwardUnitDynamic(TestCase):
    # TODO: Dynamically test this module over many iterations
    pass


if __name__ == '__main__':
    unittest.main()
