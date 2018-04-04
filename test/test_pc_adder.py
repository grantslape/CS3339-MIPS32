import unittest
import sys
from random import randint

from unittest import TestCase
from myhdl import intbv, delay, Simulation, Signal, StopSimulation

sys.path.append("src/python")
from pc_adder import pc_adder, pc_adder_v
from settings import settings as sf

HALF_PERIOD = delay(sf['PERIOD'] / 2)


@unittest.skip("PC Adder not implemented")
class TestPcAdderZero(TestCase):
    """Test PC Adder"""
    def setUp(self):
        self.cur_pc, self.nxt_pc, self.nxt_pc_v = [Signal(intbv(0)[32:]) for i in range(3)]
        self.dut = pc_adder(self.cur_pc, self.nxt_pc)
        self.dut_v = pc_adder_v(self.cur_pc, self.nxt_pc_v)

    def zeroTest(self):
        self.cur_pc.next = intbv(0)[32:]
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            yield HALF_PERIOD
            self.assertEqual(bin(self.nxt_pc), bin(intbv(0)[32:]))
            self.assertEqual(bin(self.nxt_pc_v), bin(intbv(0)[32:]))
        raise StopSimulation

    def dynamic(self, nxt_pc):
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.cur_pc.next = intbv(randint(0, sf['UNSIGNED_MAX_VALUE'] - 4))[32:]
            yield HALF_PERIOD
            self.assertEqual(bin(nxt_pc), bin(self.cur_pc + 4))
        raise StopSimulation

    def testPcAdderZeroPython(self):
        """test pc adder hold zero Python"""
        Simulation(self.dut, self.zeroTest()).run(quiet=1)

    def testPcAdderZeroVerilog(self):
        """test pc adder hold zero Verilog"""
        Simulation(self.dut_v, self.zeroTest()).run(quiet=1)

    def testPcAdderZeroTogether(self):
        """test pc adder hold zero together"""
        Simulation(self.dut, self.dut_v, self.zeroTest()).run(quiet=1)

    def testPcAdderDynamicPython(self):
        """test pc adder adds 4 Python"""
        Simulation(self.dut, self.dynamic(self.nxt_pc)).run(quiet=1)

    def testPcAdderDynamicVerilog(self):
        """test pc adder adds 4 Verilog"""
        Simulation(self.dut, self.dynamic(self.nxt_pc)).run(quiet=1)

    def testPcAdderDynamicTogether(self):
        """test pc adder adds 4 together"""
        stim = self.dynamic(self.nxt_pc)
        stim_v = self.dynamic(self.nxt_pc_v)
        Simulation(self.dut, self.dut_v, stim, stim_v).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
