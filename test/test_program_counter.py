import unittest
import sys
from random import randint

from unittest import TestCase
from myhdl import intbv, delay, Simulation, Signal, StopSimulation, posedge

sys.path.append("src/python")
from program_counter import program_counter, program_counter_v
from settings import settings as sf

HALF_PERIOD = delay(sf['PERIOD'] / 2)


def clock_gen(clock):
    while 1:
        yield HALF_PERIOD
        clock.next = not clock


def setup():
    clock, pc_write = [Signal(intbv(0)[1:]) for i in range(2)]
    cur_pc, nxt_inst = [Signal(intbv(0)[32:]) for i in range(2)]
    return clock, pc_write, nxt_inst, cur_pc


@unittest.skip("Program Counter not implemented")
class TestNormalOperation(TestCase):
    """Test normal in and out of program counter"""
    def bench(self, clock, pc_write, nxt_inst, cur_pc):
        pc_write.next = intbv(0)[1:]
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            nxt_inst.next = intbv(randint(0, sf['MAX_UNSIGNED_VALUE']))[32:]
            yield posedge(clock)
            self.assertEqual(cur_pc, nxt_inst)
        raise StopSimulation

    def testNormalOperationPython(self):
        """Checking normal PC operation Python"""
        clock, pc_write, nxt_inst, cur_pc = setup()
        CLK = clock_gen(clock)
        dut = program_counter(clock, pc_write, nxt_inst, cur_pc)
        stim = self.bench(clock, pc_write, nxt_inst, cur_pc)

        Simulation(CLK, dut, stim).run(quiet=1)

    def testNormalOperationVerilog(self):
        """Checking normal PC operation Verilog"""
        clock, pc_write, nxt_inst, cur_pc = setup()
        CLK = clock_gen(clock)
        dut = program_counter_v(clock, pc_write, nxt_inst, cur_pc)
        stim = self.bench(clock, pc_write, nxt_inst, cur_pc)

        Simulation(CLK, dut, stim).run(quiet=1)

    def testNormalOperationTogether(self):
        """Checking normal PC operation together"""
        clock, pc_write, nxt_inst, cur_pc = setup()
        cur_pc_v = Signal(intbv(0)[32:])
        CLK = clock_gen(clock)
        dut = program_counter(clock, pc_write, nxt_inst, cur_pc)
        dut_v = program_counter_v(clock, pc_write, nxt_inst, cur_pc_v)
        stim = self.bench(clock, pc_write, nxt_inst, cur_pc)
        stim_v = self.bench(clock, pc_write, nxt_inst, cur_pc_v)

        Simulation(CLK, dut, dut_v, stim, stim_v).run(quiet=1)


@unittest.skip("Program Counter not implemented")
class TestStallOperation(TestCase):
    """Test when stall line is asserted"""
    def bench(self, clock, pc_write, nxt_inst, cur_pc):
        pc_write.next = intbv(0)[1:]
        for i in range(sf['DEFAULT_TEST_LENGTH'] / 2):
            nxt_inst.next = intbv(randint(0, sf['MAX_UNSIGNED_VALUE']))[32:]
            yield posedge(clock)
        pc_write.next = intbv(0)[1:]
        for i in range(sf['DEFAULT_TEST_LENGTH'] / 2):
            self.assertEqual(nxt_inst, cur_pc)
        raise StopSimulation

    def testStallOperationPython(self):
        """Test when stall line is asserted Python"""
        clock, pc_write, nxt_inst, cur_pc = setup()
        CLK = clock_gen(clock)
        dut = program_counter(clock, pc_write, nxt_inst, cur_pc)
        stim = self.bench(clock, pc_write, nxt_inst, cur_pc)

        Simulation(CLK, dut, stim).run(quiet=1)

    def testStallOperationVerilog(self):
        """Checking stall line is asserted Verilog"""
        clock, pc_write, nxt_inst, cur_pc = setup()
        CLK = clock_gen(clock)
        dut = program_counter_v(clock, pc_write, nxt_inst, cur_pc)
        stim = self.bench(clock, pc_write, nxt_inst, cur_pc)

        Simulation(CLK, dut, stim).run(quiet=1)

    def testStallOperationTogether(self):
        """Checking stall line is asserted together"""
        clock, pc_write, nxt_inst, cur_pc = setup()
        cur_pc_v = Signal(intbv(0)[32:])
        CLK = clock_gen(clock)
        dut = program_counter(clock, pc_write, nxt_inst, cur_pc)
        dut_v = program_counter_v(clock, pc_write, nxt_inst, cur_pc_v)
        stim = self.bench(clock, pc_write, nxt_inst, cur_pc)
        stim_v = self.bench(clock, pc_write, nxt_inst, cur_pc_v)

        Simulation(CLK, dut, dut_v, stim, stim_v).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
