import unittest
import sys
from random import randint

from unittest import TestCase
from myhdl import intbv, delay, Simulation, Signal, StopSimulation, posedge

sys.path.append("src/python")
from program_counter import program_counter, program_counter_v
from settings import settings as sf
from clock import clock_gen


@unittest.skip("Program Counter not implemented")
class TestNormalOperation(TestCase):
    """Test program counter"""
    def setUp(self):
        self.clock, self.pc_write = [Signal(intbv(0)[1:]) for i in range(2)]
        self.cur_pc_v, self.cur_pc, self.nxt_inst = [Signal(intbv(0)[32:]) for i in range(3)]
        self.dut = program_counter(self.clock, self.pc_write, self.nxt_inst, self.cur_pc)
        self.dut_v = program_counter_v(self.clock, self.pc_write, self.nxt_inst, self.cur_pc_v)

    def normalOp(self, cur_pc):
        self.pc_write.next = intbv(0)[1:]
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.nxt_inst.next = intbv(randint(0, sf['MAX_UNSIGNED_VALUE']))[32:]
            yield posedge(self.clock)
            self.assertEqual(cur_pc, self.nxt_inst)
        raise StopSimulation

    def stall(self, cur_pc):
        self.pc_write.next = intbv(0)[1:]
        for i in range(sf['DEFAULT_TEST_LENGTH'] / 2):
            self.nxt_inst.next = intbv(randint(0, sf['MAX_UNSIGNED_VALUE']))[32:]
            yield posedge(self.clock)
        self.pc_write.next = intbv(1)[1:]
        for i in range(sf['DEFAULT_TEST_LENGTH'] / 2):
            self.assertEqual(self.nxt_inst, cur_pc)
        raise StopSimulation

    def testNormalOperationPython(self):
        """Checking normal PC operation Python"""
        CLK = clock_gen(self.clock)
        stim = self.normalOp(self.cur_pc)
        Simulation(CLK, self.dut, stim).run(quiet=1)

    def testNormalOperationVerilog(self):
        """Checking normal PC operation Verilog"""
        CLK = clock_gen(self.clock)
        stim = self.normalOp(self.cur_pc_v)
        Simulation(CLK, self.dut_v, stim).run(quiet=1)

    def testNormalOperationTogether(self):
        """Checking normal PC operation together"""
        CLK = clock_gen(self.clock)
        stim = self.normalOp(self.cur_pc)
        stim_v = self.normalOp(self.cur_pc_v)
        Simulation(CLK, self.dut, self.dut_v, stim, stim_v).run(quiet=1)

    def testStallOperationPython(self):
        """Test when stall line is asserted Python"""
        CLK = clock_gen(self.clock)
        stim = self.stall(self.cur_pc)

        Simulation(CLK, self.dut, stim).run(quiet=1)

    def testStallOperationVerilog(self):
        """Checking stall line is asserted Verilog"""
        CLK = clock_gen(self.clock)
        stim = self.stall(self.cur_pc_v)

        Simulation(CLK, self.dut_v, stim).run(quiet=1)

    def testStallOperationTogether(self):
        """Checking stall line is asserted together"""
        CLK = clock_gen(self.clock)
        stim = self.stall(self.cur_pc)
        stim_v = self.stall(self.cur_pc_v)

        Simulation(CLK, self.dut, self.dut_v, stim, stim_v).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
