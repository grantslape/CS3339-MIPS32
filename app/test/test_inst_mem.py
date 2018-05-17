"""Unit tests for instruction memory"""
import unittest
from unittest import TestCase
from random import randint
from myhdl import Simulation, StopSimulation, intbv, Signal
from src.commons.settings import settings as sf
from src.commons.clock import half_period
from src.commons.signal_generator import unsigned_signal_set
from src.python.inst_mem import inst_mem, inst_mem_v


class TestInstructionMemory(TestCase):
    """Unit Tests for Instruction Memory"""
    def setUp(self):
        self.inst_reg, self.inst_out, self.inst_out_v = unsigned_signal_set(3)
        self.dut = inst_mem(inst_reg=self.inst_reg, inst_out=self.inst_out)
        self.mem = []
        mem_file = open('lib/instructions')
        try:
            self.mem = [intbv(line) for line in mem_file]
        except IOError:
            pass
        mem_file.close()

    def getVerilog(self):
        """Return Verilog design under test"""
        return inst_mem_v(inst_reg=self.inst_reg, inst_out=self.inst_out_v)

    def dynamic(self, python=False, verilog=False):
        """Test random instructions from file"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            # account for byte vs. word addressing
            index = Signal(intbv(randint(0, len(self.mem)) * 4))
            self.inst_reg.next = index
            yield half_period()
            if python:
                self.assertEqual(self.mem[index//4], self.inst_out)
            if verilog:
                self.assertEqual(self.mem[index//4], self.inst_out_v)
        raise StopSimulation

    def testInstMemDynamicPython(self):
        """Testing regular operation Python"""
        stim = self.dynamic(python=True)
        Simulation(stim, self.dut).run(quiet=1)

    def testInstMemDynamicVerilog(self):
        """Testing regular operations Verilog"""
        stim = self.dynamic(verilog=True)
        Simulation(stim, self.getVerilog()).run(quiet=1)

    def testInstMemDynamicTogether(self):
        """Testing regular operations Together"""
        stim = self.dynamic(python=True, verilog=True)
        Simulation(stim, self.dut, self.getVerilog()).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
