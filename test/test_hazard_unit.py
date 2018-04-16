"""Unit tests for Hazard unit module"""
import unittest
from unittest import TestCase
from random import randint
from myhdl import Simulation, StopSimulation
from src.python.hazard_unit import hazard_unit, hazard_unit_v
from src.commons.clock import half_period
from src.commons.signal_generator import unsigned_signal_set, random_unsigned_intbv, rand_unsigned_signal_set
from src.commons.settings import settings as sf


# @unittest.skip("Hazard unit not implemented yet")
class TestHazardUnit(TestCase):
    """Test Hazard Unit functionality"""
    def setUp(self):
        self.if_id_rs, self.if_id_rt, self.id_ex_rt = rand_unsigned_signal_set(3, width=5)
        self.mem_read, self.pc_write, self.if_id_write, self.ex_stall, self.pc_write_v, \
            self.if_id_write_v, self.ex_stall_v = unsigned_signal_set(7, width=1)
        self.dut = hazard_unit(if_id_rs=self.if_id_rs,
                               if_id_rt=self.if_id_rt,
                               id_ex_rt=self.id_ex_rt,
                               mem_read=self.mem_read,
                               pc_write=self.pc_write,
                               if_id_write=self.if_id_write,
                               ex_stall=self.ex_stall)

    def getVerilog(self):
        """Return Verilog design under test"""
        return hazard_unit_v(if_id_rs=self.if_id_rs,
                             if_id_rt=self.if_id_rt,
                             id_ex_rt=self.id_ex_rt,
                             mem_read=self.mem_read,
                             pc_write=self.pc_write_v,
                             if_id_write=self.if_id_write_v,
                             ex_stall=self.ex_stall_v)

    def deassert(self, python=False, verilog=False):
        """test hazard unit deassert functionality"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.id_ex_rt.next = random_unsigned_intbv(width=5)
            self.mem_read.next = 0
            while self.id_ex_rt.next == self.if_id_rt.next:
                self.if_id_rt.next = random_unsigned_intbv(width=5)
            while self.id_ex_rt.next == self.if_id_rs.next:
                self.if_id_rs.next = random_unsigned_intbv(width=5)
            yield half_period()
            if python:
                self.assertNotEquals(bin(self.id_ex_rt), bin(self.if_id_rt))
                self.assertNotEquals(bin(self.id_ex_rt), bin(self.if_id_rs))
                self.assertEqual(bin(self.ex_stall), bin(0))
                self.assertEqual(bin(self.pc_write), bin(0))
                self.assertEqual(bin(self.if_id_write), bin(0))
            if verilog:
                self.assertNotEquals(bin(self.id_ex_rt), bin(self.if_id_rt))
                self.assertNotEquals(bin(self.id_ex_rt), bin(self.if_id_rs))
                self.assertEqual(bin(self.ex_stall_v), bin(0))
                self.assertEqual(bin(self.pc_write_v), bin(0))
                self.assertEqual(bin(self.if_id_write_v), bin(0))
        raise StopSimulation

    def dynamic(self, python=False, verilog=False):
        """test hazard unit dynamic functionality"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.id_ex_rt.next, self.if_id_rt.next, self.if_id_rs.next = \
                rand_unsigned_signal_set(3, width=5)
            self.mem_read.next = randint(0, 1)
            yield half_period()
            if self.mem_read == 1:
                if self.id_ex_rt.next == self.if_id_rs.next or \
+                        self.id_ex_rt.next == self.if_id_rt.next:
                    if python:
                        self.assertEqual(bin(1), bin(self.pc_write))
                        self.assertEqual(bin(1), bin(self.if_id_write))
                        self.assertEqual(bin(1), bin(self.ex_stall))
                    if verilog:
                        self.assertEqual(bin(1), bin(self.pc_write_v))
                        self.assertEqual(bin(1), bin(self.if_id_write_v))
                        self.assertEqual(bin(1), bin(self.ex_stall_v))
                else:
                    if python:
                        self.assertEqual(bin(0), bin(self.pc_write))
                        self.assertEqual(bin(0), bin(self.if_id_write))
                        self.assertEqual(bin(0), bin(self.ex_stall))
                    if verilog:
                        self.assertEqual(bin(0), bin(self.pc_write_v))
                        self.assertEqual(bin(0), bin(self.if_id_write_v))
                        self.assertEqual(bin(0), bin(self.ex_stall_v))
        raise StopSimulation

    def testHazardUnitDeassertedPython(self):
        """Checking Hazard unit functionality when deasserted Python"""
        stim = self.deassert(python=True)
        Simulation(self.dut, stim).run(quiet=1)

    def testHazardUnitDeassertedVerilog(self):
        """Checking Hazard unit functionality when deasserted Verilog"""
        stim_v = self.deassert(verilog=True)
        dut_v = self.getVerilog()
        Simulation(dut_v, stim_v).run(quiet=1)

    def testHazardUnitDeassertedTogether(self):
        """Checking Hazard unit functionality when deasserted Together"""
        stim = self.deassert(python=True, verilog=True)
        dut_v = self.getVerilog()
        Simulation(self.dut, dut_v, stim).run(quiet=1)

    def testHazardUnitDynamicPython(self):
        """Checking Hazard unit functionality when Dynamic Python"""
        stim = self.dynamic(python=True)
        Simulation(self.dut, stim).run(quiet=1)

    def testHazardUnitDynamicVerilog(self):
        """Checking Hazard unit functionality when Dynamic Verilog"""
        stim_v = self.dynamic(verilog=True)
        dut_v = self.getVerilog()
        Simulation(dut_v, stim_v).run(quiet=1)

    def testHazardUnitDynamicTogether(self):
        """Checking Hazard unit functionality when Dynamic Together"""
        stim = self.dynamic(python=True, verilog=True)
        dut_v = self.getVerilog()
        Simulation(self.dut, dut_v, stim).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
