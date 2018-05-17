"""Branch Adder Unit Tests"""
import unittest
from unittest import TestCase
from random import randint
from myhdl import StopSimulation, Simulation, bin
from src.commons.clock import half_period
from src.commons.settings import settings as sf
from src.commons.signal_generator import unsigned_signal_set, unsigned_intbv
from src.python.branch_adder import branch_adder, branch_adder_v


class TestBranchAdder(TestCase):
    """Test Branch Adder module"""
    def setUp(self):
        self.pc_in, self.imm_in, self.addr_out, self.addr_out_v = unsigned_signal_set(4)
        self.dut = branch_adder(pc_in=self.pc_in, addr_out=self.addr_out, imm_in=self.imm_in)

    def getVerilog(self):
        """Return verilog design under test"""
        return branch_adder_v(pc_in=self.pc_in, addr_out=self.addr_out_v, imm_in=self.imm_in)

    def deasserted(self, python=False, verilog=False):
        """test branch adder holds zero value"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            yield half_period()
            if python:
                self.assertEqual(bin(self.addr_out), bin(0))
            if verilog:
                self.assertEqual(bin(self.addr_out_v), bin(0))
        raise StopSimulation

    def dynamic(self, python=False, verilog=False):
        """test branch adder normal operation"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.pc_in.next = unsigned_intbv(randint(0, 0xF423A), width=32)
            self.imm_in.next = unsigned_intbv(randint(0, 2**16))
            yield half_period()
            if python:
                self.assertEqual(bin(self.pc_in + self.imm_in), bin(self.addr_out))
            if verilog:
                self.assertEqual(bin(self.pc_in + self.imm_in), bin(self.addr_out_v))
        raise StopSimulation

    def testBranchAdderZeroPython(self):
        """Test no input python"""
        stim = self.deasserted(python=True)
        Simulation(self.dut, stim).run(quiet=1)

    def testBranchAdderZeroVerilog(self):
        """Test no input verilog"""
        stim = self.deasserted(verilog=True)
        Simulation(self.getVerilog(), stim).run(quiet=1)

    def testBranchAdderZeroTogether(self):
        """Test no input together"""
        stim = self.deasserted(python=True, verilog=True)
        Simulation(self.dut, self.getVerilog(), stim).run(quiet=1)

    def testBranchAdderDynamicPython(self):
        """Test Dynamic Input Python"""
        stim = self.dynamic(python=True)
        Simulation(self.dut, stim).run(quiet=1)

    def testBranchAdderDynamicVerilog(self):
        """Test Dynamic Input Verilog"""
        stim = self.dynamic(verilog=True)
        Simulation(self.getVerilog(), stim).run(quiet=1)

    def testBranchAdderTogether(self):
        """Test dynamic Input together"""
        stim = self.dynamic(python=True, verilog=True)
        Simulation(self.dut, self.getVerilog(), stim).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
