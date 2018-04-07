import unittest
from unittest import TestCase
from random import randint
from myhdl import intbv, Simulation, Signal, StopSimulation
from src.python.ex_mux import ex_mux, ex_mux_v
from src.commons.settings import settings as sf
from src.commons.clock import half_period


@unittest.skip("Ex Mux not implemented")
class TestExMuxDeasserted(TestCase):
    """Test Ex mux"""
    def setUp(self):
        self.reg_dst = Signal(intbv(0)[1:])
        self.rt_in, self.rd_in, self.dest, self.dest_v = [Signal(intbv(0)[5:]) for i in range(4)]
        self.dut = ex_mux(self.reg_dst, self.rt_in, self.rd_in, self.dest)

    def deassert(self, dest):
        """Test Deasserted functionality"""
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.reg_dst.next = 0
            self.rt_in.next = intbv(randint(0, sf['WIDTH']))[5:]
            self.rd_in.next = intbv(randint(0, sf['WIDTH']))[5:]
            while self.rd_in == self.rt_in:
                self.rd_in.next = intbv(randint(0, sf['WIDTH']))[5:]
            yield half_period()
            self.assertEqual(dest, self.rt_in)
            self.assertNotEquals(dest, self.rd_in)
        raise StopSimulation

    def asserted(self, dest):
        """Test Asserted functionality"""
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.reg_dst.next = 1
            self.rt_in.next = intbv(randint(0, sf['WIDTH']))[5:]
            self.rd_in.next = intbv(randint(0, sf['WIDTH']))[5:]
            while self.rd_in == self.rt_in:
                self.rd_in.next = intbv(randint(0, sf['WIDTH']))[5:]
            yield half_period()
            self.assertEqual(dest, self.rd_in)
            self.assertNotEquals(dest, self.rt_in)
        raise StopSimulation

    def dynamic(self, dest):
        """Test Dynamic functionality"""
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.reg_dst.next = randint(0, 1)
            self.rt_in.next = intbv(randint(0, sf['WIDTH']))[5:]
            self.rd_in.next = intbv(randint(0, sf['WIDTH']))[5:]
            while self.rd_in == self.rt_in:
                self.rd_in.next = intbv(randint(0, sf['WIDTH']))[5:]
            yield half_period()
            if self.reg_dst == 0:
                self.assertEqual(dest, self.rt_in)
                self.assertNotEquals(dest, self.rd_in)
            else:
                self.assertEqual(self.reg_dst, 1)
                self.assertEqual(dest, self.rd_in)
                self.assertNotEquals(dest, self.rt_in)
        raise StopSimulation

    def testExMuxDeassertedPython(self):
        """Check that RT is returned when reg_dst deasserted Python"""
        stim = self.deassert(self.dest)
        Simulation(self.dut, stim).run(quiet=1)

    def testExMuxDeassertedVerilog(self):
        """Check that RT is returned when reg_dst deasserted Verilog"""
        dut_v = ex_mux_v(self.reg_dst, self.rt_in, self.rd_in, self.dest_v)
        stim = self.deassert(self.dest_v)
        Simulation(dut_v, stim).run(quiet=1)

    def testExMuxDeassertedTogether(self):
        """Check that RT is returned when reg_dst deasserted Together"""
        dut_v = ex_mux_v(self.reg_dst, self.rt_in, self.rd_in, self.dest_v)
        stim = self.deassert(self.dest)
        stim_v = self.deassert(self.dest_v)
        Simulation(self.dut, dut_v, stim, stim_v).run(quiet=1)

    def testExMuxAssertedPython(self):
        """Check that RT is returned when reg_dst Asserted Python"""
        stim = self.asserted(self.dest)
        Simulation(self.dut, stim).run(quiet=1)

    def testExMuxAssertedVerilog(self):
        """Check that RT is returned when reg_dst Asserted Verilog"""
        dut_v = ex_mux_v(self.reg_dst, self.rt_in, self.rd_in, self.dest_v)
        stim = self.asserted(self.dest_v)
        Simulation(dut_v, stim).run(quiet=1)

    def testExMuxAssertedTogether(self):
        """Check that RT is returned when reg_dst Asserted Together"""
        dut_v = ex_mux_v(self.reg_dst, self.rt_in, self.rd_in, self.dest_v)
        stim = self.asserted(self.dest)
        stim_v = self.asserted(self.dest_v)
        Simulation(self.dut, dut_v, stim, stim_v).run(quiet=1)

    def testExMuxDynamicPython(self):
        """Check dynamic behavior Python"""
        stim = self.dynamic(self.dest)
        Simulation(self.dut, stim).run(quiet=1)

    def testExMuxDynamicVerilog(self):
        """Check dynamic behavior Verilog"""
        dut_v = ex_mux_v(self.reg_dst, self.rt_in, self.rd_in, self.dest_v)
        stim = self.dynamic(self.dest_v)
        Simulation(dut_v, stim).run(quiet=1)

    def testExMuxDynamicTogether(self):
        """Check dynamic behavior Together"""
        dut_v = ex_mux_v(self.reg_dst, self.rt_in, self.rd_in, self.dest_v)
        stim = self.dynamic(self.dest)
        stim_v = self.dynamic(self.dest_v)
        Simulation(self.dut, dut_v, stim, stim_v).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
