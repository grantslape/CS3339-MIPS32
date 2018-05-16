"""PC Adder Unit Tests"""
import unittest
from unittest import TestCase
from random import randint
from myhdl import intbv, Simulation, StopSimulation

from src.commons.signal_generator import unsigned_signal_set
from src.python.pc_adder import pc_adder, pc_adder_v
from src.commons.settings import settings as sf
from src.commons.clock import half_period


class TestPcAdder(TestCase):
    """Test PC Adder"""
    def setUp(self):
        self.cur_pc, self.nxt_pc, self.nxt_pc_v = unsigned_signal_set(3)
        self.dut = pc_adder(self.cur_pc, self.nxt_pc)

    def dynamic(self, python=False, verilog=False):
        """Test dynamic values"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.cur_pc.next = intbv(randint(0, sf['UNSIGNED_MAX_VALUE'] - 4))[32:]
            yield half_period()
            if python:
                self.assertEqual(bin(self.nxt_pc), bin(self.cur_pc + 4))
            if verilog:
                self.assertEqual(bin(self.nxt_pc_v), bin(self.cur_pc + 4))
        raise StopSimulation

    def testPcAdderDynamicPython(self):
        """test pc adder adds 4 Python"""
        Simulation(self.dut, self.dynamic(python=True)).run(quiet=1)

    def testPcAdderDynamicVerilog(self):
        """test pc adder adds 4 Verilog"""
        dut_v = pc_adder_v(self.cur_pc, self.nxt_pc_v)
        Simulation(dut_v, self.dynamic(verilog=True)).run(quiet=1)

    def testPcAdderDynamicTogether(self):
        """test pc adder adds 4 together"""
        dut_v = pc_adder_v(self.cur_pc, self.nxt_pc_v)
        stim = self.dynamic(python=True, verilog=True)
        Simulation(self.dut, dut_v, stim).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
