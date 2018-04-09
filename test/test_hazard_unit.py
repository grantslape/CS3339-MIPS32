"""Unit tests for Hazard unit module"""
import unittest
from random import randint
from unittest import TestCase
from myhdl import intbv, Simulation, Signal, StopSimulation
from src.python.hazard_unit import hazard_unit, hazard_unit_v
from src.commons.clock import half_period
from src.commons.signal_generator import unsigned_signal_set, random_unsigned_intbv, rand_unsigned_signal_set
from src.commons.settings import settings as sf


@unittest.skip("Hazard unit not implemented yet")
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

    def deassert(self, pc_write, if_id_write, ex_stall):
        """test hazard unit deassert functionality"""
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.id_ex_rt.next = random_unsigned_intbv(width=5)
            self.mem_read.next = 0
            while self.id_ex_rt == self.if_id_rt or self.id_ex_rt == self.if_id_rs:
                self.if_id_rt.next, self.if_id_rs.next = rand_unsigned_signal_set(2, width=5)
            yield half_period()
            self.assertNotEquals(bin(self.id_ex_rt), bin(self.if_id_rt))
            self.assertNotEquals(bin(self.id_ex_rt), bin(self.if_id_rs))
            self.assertEqual(bin(ex_stall), bin(0))
            self.assertEqual(bin(pc_write), bin(0))
            self.assertEqual(bin(if_id_write), bin(0))
        raise StopSimulation

    def dynamic(self, pc_write, if_id_write, ex_stall):
        """test hazard unit dynamic functionality"""
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.id_ex_rt.next, self.if_id_rt.next, self.if_id_rs.next = \
                rand_unsigned_signal_set(3, width=5)
            self.mem_read.next = randint(0, 1)
            yield half_period()
            if self.mem_read == 1:
                if self.id_ex_rt == self.if_id_rs or self.id_ex_rt == self.if_id_rt:
                    self.assertEqual(bin(1), bin(pc_write))
                    self.assertEqual(bin(1), bin(if_id_write))
                    self.assertEqual(bin(1), bin(ex_stall))
                else:
                    self.assertEqual(bin(0), bin(pc_write))
                    self.assertEqual(bin(0), bin(if_id_write))
                    self.assertEqual(bin(0), bin(ex_stall))
        raise StopSimulation

    def testHazardUnitDeassertedPython(self):
        """Checking Hazard unit functionality when deasserted Python"""
        stim = self.deassert(self.pc_write, self.if_id_write, self.ex_stall)
        Simulation(self.dut, stim).run(quiet=1)

    def testHazardUnitDeassertedVerilog(self):
        """Checking Hazard unit functionality when deasserted Verilog"""
        stim_v = self.deassert(self.pc_write_v, self.if_id_write_v, self.ex_stall_v)
        dut_v = hazard_unit_v(if_id_rs=self.if_id_rs,
                              if_id_rt=self.if_id_rt,
                              id_ex_rt=self.id_ex_rt,
                              mem_read=self.mem_read,
                              pc_write=self.pc_write_v,
                              if_id_write=self.if_id_write_v,
                              ex_stall=self.ex_stall_v)
        Simulation(dut_v, stim_v).run(quiet=1)

    def testHazardUnitDeassertedTogether(self):
        """Checking Hazard unit functionality when deasserted Together"""
        stim = self.deassert(self.pc_write, self.if_id_write, self.ex_stall)
        stim_v = self.deassert(self.pc_write_v, self.if_id_write_v, self.ex_stall_v)
        dut_v = hazard_unit_v(if_id_rs=self.if_id_rs,
                              if_id_rt=self.if_id_rt,
                              id_ex_rt=self.id_ex_rt,
                              mem_read=self.mem_read,
                              pc_write=self.pc_write_v,
                              if_id_write=self.if_id_write_v,
                              ex_stall=self.ex_stall_v)
        Simulation(self.dut, dut_v, stim, stim_v).run(quiet=1)

    def testHazardUnitDynamicPython(self):
        """Checking Hazard unit functionality when Dynamic Python"""
        stim = self.dynamic(self.pc_write, self.if_id_write, self.ex_stall)
        Simulation(self.dut, stim).run(quiet=1)

    def testHazardUnitDynamicVerilog(self):
        """Checking Hazard unit functionality when Dynamic Verilog"""
        stim_v = self.dynamic(self.pc_write_v, self.if_id_write_v, self.ex_stall_v)
        dut_v = hazard_unit_v(if_id_rs=self.if_id_rs,
                              if_id_rt=self.if_id_rt,
                              id_ex_rt=self.id_ex_rt,
                              mem_read=self.mem_read,
                              pc_write=self.pc_write_v,
                              if_id_write=self.if_id_write_v,
                              ex_stall=self.ex_stall_v)
        Simulation(dut_v, stim_v).run(quiet=1)

    def testHazardUnitDynamicTogether(self):
        """Checking Hazard unit functionality when Dynamic Together"""
        stim = self.dynamic(self.pc_write, self.if_id_write, self.ex_stall)
        stim_v = self.dynamic(self.pc_write_v, self.if_id_write_v, self.ex_stall_v)
        dut_v = hazard_unit_v(if_id_rs=self.if_id_rs,
                              if_id_rt=self.if_id_rt,
                              id_ex_rt=self.id_ex_rt,
                              mem_read=self.mem_read,
                              pc_write=self.pc_write_v,
                              if_id_write=self.if_id_write_v,
                              ex_stall=self.ex_stall_v)
        Simulation(self.dut, dut_v, stim, stim_v).run(quiet=1)