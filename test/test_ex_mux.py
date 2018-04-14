"""EX stage Multiplexer unit tests"""
import unittest
from unittest import TestCase
from random import randint
from myhdl import intbv, Simulation, Signal, StopSimulation
from src.python.ex_mux import ex_mux, ex_mux_v
from src.commons.settings import settings as sf
from src.commons.clock import half_period
from src.commons.signal_generator import random_unsigned_intbv, unsigned_signal_set


class TestExMuxDeasserted(TestCase):
    """Test Ex mux"""
    def setUp(self):
        self.reg_dst = Signal(intbv(0)[1:])
        self.rt_in, self.rd_in, self.dest, self.dest_v = unsigned_signal_set(4, width=5)
        self.dut = ex_mux(self.reg_dst, self.rt_in, self.rd_in, self.dest)

    def deassert(self, python=False, verilog=False):
        """Test Deasserted functionality"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.reg_dst.next = 0
            self.rt_in.next = random_unsigned_intbv(5)
            self.rd_in.next = random_unsigned_intbv(5)
            while self.rd_in.next == self.rt_in.next:
                self.rd_in.next = random_unsigned_intbv(5)
            yield half_period()
            if python:
                self.assertEqual(self.dest, self.rt_in)
                self.assertNotEquals(self.dest, self.rd_in)
            if verilog:
                self.assertEqual(self.dest_v, self.rt_in)
                self.assertNotEquals(self.dest_v, self.rd_in)
        raise StopSimulation

    def asserted(self, python=False, verilog=False):
        """Test Asserted functionality"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.reg_dst.next = 1
            self.rt_in.next = random_unsigned_intbv(5)
            self.rd_in.next = random_unsigned_intbv(5)
            while self.rd_in.next == self.rt_in.next:
                self.rd_in.next = random_unsigned_intbv(5)
            yield half_period()
            if python:
                self.assertEqual(self.dest, self.rd_in)
                self.assertNotEquals(self.dest, self.rt_in)
            if verilog:
                self.assertEqual(self.dest_v, self.rd_in)
                self.assertNotEquals(self.dest_v, self.rt_in)
        raise StopSimulation

    def dynamic(self, python=False, verilog=False):
        """Test Dynamic functionality"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.reg_dst.next = randint(0, 1)
            self.rt_in.next = random_unsigned_intbv(5)
            self.rd_in.next = random_unsigned_intbv(5)
            while self.rd_in.next == self.rt_in.next or self.rd_in.next == self.rt_in:
                self.rd_in.next = random_unsigned_intbv(5)
            yield half_period()
            if self.reg_dst == 0:
                if python:
                    self.assertEqual(self.dest, self.rt_in)
                    self.assertNotEquals(self.dest, self.rd_in)
                if verilog:
                    self.assertEqual(self.dest_v, self.rt_in)
                    self.assertNotEquals(self.dest_v, self.rd_in)
            else:
                if python:
                    self.assertEqual(self.reg_dst, 1)
                    self.assertEqual(self.dest, self.rd_in)
                    self.assertNotEquals(self.dest, self.rt_in)
                if verilog:
                    self.assertEqual(self.reg_dst, 1)
                    self.assertEqual(self.dest_v, self.rd_in)
                    self.assertNotEquals(self.dest_v, self.rt_in)
        raise StopSimulation

    def testExMuxDeassertedPython(self):
        """Check that RT is returned when reg_dst deasserted Python"""
        stim = self.deassert(python=True)
        Simulation(self.dut, stim).run(quiet=1)

    def testExMuxDeassertedVerilog(self):
        """Check that RT is returned when reg_dst deasserted Verilog"""
        dut_v = ex_mux_v(self.reg_dst, self.rt_in, self.rd_in, self.dest_v)
        stim = self.deassert(verilog=True)
        Simulation(dut_v, stim).run(quiet=1)

    def testExMuxDeassertedTogether(self):
        """Check that RT is returned when reg_dst deasserted Together"""
        dut_v = ex_mux_v(self.reg_dst, self.rt_in, self.rd_in, self.dest_v)
        stim = self.deassert(python=True, verilog=True)
        Simulation(self.dut, dut_v, stim).run(quiet=1)

    def testExMuxAssertedPython(self):
        """Check that RT is returned when reg_dst Asserted Python"""
        stim = self.asserted(python=True)
        Simulation(self.dut, stim).run(quiet=1)

    def testExMuxAssertedVerilog(self):
        """Check that RT is returned when reg_dst Asserted Verilog"""
        dut_v = ex_mux_v(self.reg_dst, self.rt_in, self.rd_in, self.dest_v)
        stim = self.asserted(verilog=True)
        Simulation(dut_v, stim).run(quiet=1)

    def testExMuxAssertedTogether(self):
        """Check that RT is returned when reg_dst Asserted Together"""
        dut_v = ex_mux_v(self.reg_dst, self.rt_in, self.rd_in, self.dest_v)
        stim = self.asserted(python=True, verilog=True)
        Simulation(self.dut, dut_v, stim).run(quiet=1)

    def testExMuxDynamicPython(self):
        """Check dynamic behavior Python"""
        stim = self.dynamic(python=True)
        Simulation(self.dut, stim).run(quiet=1)

    def testExMuxDynamicVerilog(self):
        """Check dynamic behavior Verilog"""
        dut_v = ex_mux_v(self.reg_dst, self.rt_in, self.rd_in, self.dest_v)
        stim = self.dynamic(verilog=True)
        Simulation(dut_v, stim).run(quiet=1)

    def testExMuxDynamicTogether(self):
        """Check dynamic behavior Together"""
        dut_v = ex_mux_v(self.reg_dst, self.rt_in, self.rd_in, self.dest_v)
        stim = self.dynamic(verilog=True, python=True)
        Simulation(self.dut, dut_v, stim).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
