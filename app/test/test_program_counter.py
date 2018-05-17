"""Unit tests for Program counter module"""
import unittest
from unittest import TestCase
from myhdl import intbv, Simulation, Signal, StopSimulation, posedge
from src.python.program_counter import program_counter, program_counter_v
from src.commons.settings import settings as sf
from src.commons.clock import clock_gen
from src.commons.signal_generator import random_unsigned_intbv, unsigned_signal_set


class TestNormalOperation(TestCase):
    """Test program counter"""
    def setUp(self):
        self.clock, self.pc_write = [Signal(intbv()[1:]) for _ in range(2)]
        self.cur_pc_v, self.cur_pc, self.nxt_inst = unsigned_signal_set(3)
        self.dut = program_counter(self.clock, self.pc_write, self.nxt_inst, self.cur_pc)

    def normal_op(self, python=False, verilog=False):
        """Test normal operations"""
        self.pc_write.next = 0
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.nxt_inst.next = random_unsigned_intbv()
            # First posedge triggers program_counter to do work
            yield self.clock.posedge
            # negedge takes us to actual next cycle
            yield self.clock.negedge
            if python:
                self.assertEqual(bin(self.cur_pc), bin(self.nxt_inst))
            if verilog:
                self.assertEqual(bin(self.cur_pc_v), bin(self.nxt_inst))
        raise StopSimulation

    def stall(self, python=False, verilog=False):
        """test stalling operations"""
        self.pc_write.next = 0
        for _ in range(sf['DEFAULT_TEST_LENGTH'] // 2):
            self.nxt_inst.next = random_unsigned_intbv()
            yield posedge(self.clock)
        self.pc_write.next = 1
        for _ in range(sf['DEFAULT_TEST_LENGTH'] // 2):
            yield posedge(self.clock)
            if python:
                self.assertEqual(self.nxt_inst, self.cur_pc)
            if verilog:
                self.assertEqual(bin(self.nxt_inst), bin(self.cur_pc_v))
        raise StopSimulation

    def testNormalOperationPython(self):
        """Checking normal PC operation Python"""
        CLK = clock_gen(self.clock)
        stim = self.normal_op(python=True)
        Simulation(CLK, self.dut, stim).run(quiet=1)

    def testNormalOperationVerilog(self):
        """Checking normal PC operation Verilog"""
        CLK = clock_gen(self.clock)
        dut_v = program_counter_v(self.clock, self.pc_write, self.nxt_inst, self.cur_pc_v)
        stim = self.normal_op(verilog=True)
        Simulation(CLK, dut_v, stim).run(quiet=1)

    def testNormalOperationTogether(self):
        """Checking normal PC operation together"""
        CLK = clock_gen(self.clock)
        dut_v = program_counter_v(self.clock, self.pc_write, self.nxt_inst, self.cur_pc_v)
        stim = self.normal_op(python=True, verilog=True)
        Simulation(CLK, self.dut, dut_v, stim).run(quiet=1)

    def testStallOperationPython(self):
        """Test when stall line is asserted Python"""
        CLK = clock_gen(self.clock)
        stim = self.stall(python=True)

        Simulation(CLK, self.dut, stim).run(quiet=1)

    def testStallOperationVerilog(self):
        """Checking stall line is asserted Verilog"""
        CLK = clock_gen(self.clock)
        dut_v = program_counter_v(self.clock, self.pc_write, self.nxt_inst, self.cur_pc_v)
        stim = self.stall(verilog=True)

        Simulation(CLK, dut_v, stim).run(quiet=1)

    def testStallOperationTogether(self):
        """Checking stall line is asserted together"""
        CLK = clock_gen(self.clock)
        dut_v = program_counter_v(self.clock, self.pc_write, self.nxt_inst, self.cur_pc_v)
        stim = self.stall(python=True, verilog=True)

        Simulation(CLK, self.dut, dut_v, stim).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
