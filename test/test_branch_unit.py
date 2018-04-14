"""Branch Unit unit tests"""
import unittest
from unittest import TestCase
from random import randint
from myhdl import StopSimulation, Simulation
from src.commons.clock import half_period
from src.commons.settings import settings as sf
from src.commons.signal_generator import unsigned_signal_set
from src.python.branch_unit import branch_unit, branch_unit_v


@unittest.skip("Branch Unit not implemented")
class TestBranchUnit(TestCase):
    """Test Branch Unit module"""
    def setUp(self):
        self.branch_ctrl, self.zero_in, self.pc_src, self.pc_src_v = unsigned_signal_set(4, width=1)
        self.dut = branch_unit(branch_ctrl=self.branch_ctrl,
                               zero_in=self.zero_in,
                               pc_src=self.pc_src)

    def getVerilog(self):
        """Return Verilog design under test"""
        return branch_unit_v(branch_ctrl=self.branch_ctrl,
                             zero_in=self.zero_in,
                             pc_src=self.pc_src_v)

    def deassert(self, python=False, verilog=False):
        """Test when branch_Ctrl off"""
        self.branch_ctrl.next = 0
        for _ in range(sf['DEFAULT_TEST_LENGTH'] / 10):
            self.zero_in.next = randint(0, 1)
            yield half_period()
            if python:
                self.assertEqual(bin(0), self.pc_src)
            if verilog:
                self.assertEqual(bin(0), self.pc_src_v)
        raise StopSimulation

    def asserted(self, python=False, verilog=False):
        """Test when branch_Ctrl off"""
        self.branch_ctrl.next = 1
        self.zero_in.next = 1
        for _ in range(sf['DEFAULT_TEST_LENGTH'] / 10):
            yield half_period()
            if python:
                self.assertEqual(bin(1), self.pc_src)
            if verilog:
                self.assertEqual(bin(1), self.pc_src_v)
        raise StopSimulation

    def dynamic(self, python=False, verilog=False):
        """Test dynamic operations"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.branch_ctrl.next = randint(0, 1)
            self.zero_in.next = randint(0, 1)
            yield half_period()
            if self.branch_ctrl == 1 and self.zero_in == 1:
                if python:
                    self.assertEqual(bin(1), self.pc_src)
                if verilog:
                    self.assertEqual(bin(1), self.pc_src_v)
            else:
                if python:
                    self.assertEqual(bin(0), self.pc_src)
                if verilog:
                    self.assertEqual(bin(0), self.pc_src_v)
        raise StopSimulation

    def testDeassertedPython(self):
        """Test deasserted functionality Python"""
        stim = self.deassert(python=True)
        Simulation(stim, self.dut).run(quiet=1)

    def testDeassertedVerilog(self):
        """Test deasserted functionality Verilog"""
        stim = self.deassert(verilog=True)
        Simulation(stim, self.getVerilog()).run(quiet=1)

    def testDeassertedTogether(self):
        """Test deasserted functionality Together"""
        stim = self.deassert(python=True, verilog=True)
        dut_v = self.getVerilog()
        Simulation(stim, self.dut, dut_v).run(quiet=1)

    def testAssertedPython(self):
        """Test Asserted functionality Python"""
        stim = self.asserted(python=True)
        Simulation(stim, self.dut).run(quiet=1)

    def testAssertedVerilog(self):
        """Test Asserted functionality Verilog"""
        stim = self.asserted(verilog=True)
        Simulation(stim, self.getVerilog()).run(quiet=1)

    def testAssertedTogether(self):
        """Test Asserted functionality Together"""
        stim = self.asserted(python=True, verilog=True)
        dut_v = self.getVerilog()
        Simulation(stim, self.dut, dut_v).run(quiet=1)

    def testDynamicPython(self):
        """Test Dynamic functionality Python"""
        stim = self.dynamic(python=True)
        Simulation(stim, self.dut).run(quiet=1)

    def testDynamicVerilog(self):
        """Test deasserted functionality Verilog"""
        stim = self.dynamic(verilog=True)
        Simulation(stim, self.getVerilog()).run(quiet=1)

    def testDynamicTogether(self):
        """Test deasserted functionality Together"""
        stim = self.dynamic(python=True, verilog=True)
        dut_v = self.getVerilog()
        Simulation(stim, self.dut, dut_v).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
