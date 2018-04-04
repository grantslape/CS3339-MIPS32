import unittest
import sys
from random import randint

from unittest import TestCase
from myhdl import intbv, delay, Simulation, Signal, StopSimulation

sys.path.append("src/python")
from pc_adder import pc_adder, pc_adder_v
from settings import settings as sf

HALF_PERIOD = delay(sf['PERIOD'] / 2)


def setup(j):
    return [Signal(intbv(0)[32:]) for i in range(j)]


class TestPcAdderZero(TestCase):
    def bench(self, cur_pc, nxt_pc, nxt_pc_v=intbv(0)[32:]):
        cur_pc.next = intbv(0)[32:]
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            yield HALF_PERIOD
            self.assertEqual(bin(nxt_pc), bin(intbv(0)[32:]))
            self.assertEqual(bin(nxt_pc_v), bin(intbv(0)[32:]))
        raise StopSimulation

    def testPcAdderZeroPython(self):
        """test pc adder hold zero Python"""
        cur_pc, nxt_pc = setup(2)
        dut = pc_adder(cur_pc, nxt_pc)
        Simulation(dut, self.bench(cur_pc, nxt_pc)).run(quiet=1)

    def testPcAdderZeroVerilog(self):
        """test pc adder hold zero Verilog"""
        cur_pc, nxt_pc = setup(2)
        dut = pc_adder_v(cur_pc, nxt_pc)
        Simulation(dut, self.bench(cur_pc, nxt_pc)).run(quiet=1)

    def testPcAdderZeroTogether(self):
        """test pc adder hold zero together"""
        cur_pc, nxt_pc, nxt_pc_v = setup(3)
        dut = pc_adder(cur_pc, nxt_pc)
        dut_v = pc_adder_v(cur_pc, nxt_pc_v)
        Simulation(dut, dut_v, self.bench(cur_pc, nxt_pc, nxt_pc_v=nxt_pc_v)).run(quiet=1)


class TestPcAdderDynamic(TestCase):
    def bench(self, cur_pc, nxt_pc):
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            cur_pc.next = intbv(randint(0, sf['UNSIGNED_MAX_VALUE'] - 4))[32:]
            yield HALF_PERIOD
            self.assertEqual(bin(nxt_pc), bin(cur_pc + 4))
        raise StopSimulation

    def testPcAdderDynamicPython(self):
        """test pc adder adds 4 Python"""
        cur_pc, nxt_pc = setup(2)
        dut = pc_adder(cur_pc, nxt_pc)
        Simulation(dut, self.bench(cur_pc, nxt_pc)).run(quiet=1)

    def testPcAdderDynamicVerilog(self):
        """test pc adder adds 4 Verilog"""
        cur_pc, nxt_pc = setup(2)
        dut = pc_adder_v(cur_pc, nxt_pc)
        Simulation(dut, self.bench(cur_pc, nxt_pc)).run(quiet=1)

    def testPcAdderDynamicTogether(self):
        """test pc adder adds 4 together"""
        cur_pc, nxt_pc, nxt_pc_v = setup(3)
        dut = pc_adder(cur_pc, nxt_pc)
        dut_v = pc_adder_v(cur_pc, nxt_pc_v)
        Simulation(dut, dut_v, self.bench(cur_pc, nxt_pc), self.bench(cur_pc, nxt_pc_v)).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
