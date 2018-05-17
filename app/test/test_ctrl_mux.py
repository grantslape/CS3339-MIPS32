"""Ctrl Mux unit tests"""
import unittest
from unittest import TestCase
from myhdl import Simulation, StopSimulation, intbv, Signal

from src.python.ctrl_mux import ctrl_mux, ctrl_mux_v
from src.commons.clock import half_period
from src.commons.settings import settings as sf
from src.commons.signal_generator import unsigned_signal_set, random_unsigned_intbv


class TestControlMux(TestCase):
    """Testing Ctrl multiplexer functionality"""

    def setUp(self):
        # INPUTS
        self.jump = Signal(intbv()[2:])
        self.branch, self.mem_read, self.mem_write, self.alu_src, self.reg_write, \
            self.ex_stall = unsigned_signal_set(6, width=1)
        self.mem_to_reg, self.reg_dst = unsigned_signal_set(2, width=2)
        self.alu_op = Signal(intbv()[sf['ALU_CODE_SIZE']:])

        # OUTPUTS
        self.jump_out, self.jump_out_v = unsigned_signal_set(2, width=2)
        self.branch_out, self.branch_out_v, self.mem_read_out, self.mem_read_out_v, \
            self.mem_write_out, self.mem_write_out_v, \
            self.alu_src_out, self.alu_src_out_v, self.reg_write_out, self.reg_write_out_v = unsigned_signal_set(10, width=1)
        self.mem_to_reg_out, self.mem_to_reg_out_v, self.reg_dst_out, self.reg_dst_out_v = unsigned_signal_set(4, width=2)
        self.alu_op_out, self.alu_op_out_v = unsigned_signal_set(2, width=sf['ALU_CODE_SIZE'])

    def get_args(self, which="python"):
        """return appropriate args"""
        return {
            'ex_stall': self.ex_stall,
            'jump': self.jump,
            'branch': self.branch,
            'mem_read': self.mem_read,
            'mem_to_reg': self.mem_to_reg,
            'mem_write': self.mem_write,
            'alu_src': self.alu_src,
            'reg_write': self.reg_write,
            'reg_dst': self.reg_dst,
            'alu_op': self.alu_op,
            'jump_out': self.jump_out if which == "python" else self.jump_out_v,
            'branch_out': self.branch_out if which == "python" else self.branch_out_v,
            'mem_read_out': self.mem_read_out if which == "python" else self.mem_read_out_v,
            'mem_to_reg_out': self.mem_to_reg_out if which == "python" else self.mem_to_reg_out_v,
            'mem_write_out': self.mem_write_out if which == "python" else self.mem_write_out_v,
            'alu_src_out': self.alu_src_out if which == "python" else self.alu_src_out_v,
            'reg_write_out': self.reg_write_out if which == "python" else self.reg_write_out_v,
            'reg_dst_out': self.reg_dst_out if which == "python" else self.reg_dst_out_v,
            'alu_op_out': self.alu_op_out if which == "python" else self.alu_op_out_v
        }

    def get_module(self, which="python"):
        """return module under test"""
        if which == "python":
            return ctrl_mux(**self.get_args())
        return ctrl_mux_v(**self.get_args(which="verilog"))

    def random_input(self):
        """Randomize input signals for test cases"""
        self.jump.next = random_unsigned_intbv(width=2)
        self.branch.next, self.mem_read.next, self.mem_write.next, \
            self.alu_src.next, self.reg_write.next = \
            unsigned_signal_set(5, width=1)
        self.mem_to_reg.next, self.reg_dst.next = unsigned_signal_set(2, width=2)
        self.alu_op.next = random_unsigned_intbv(width=sf['ALU_CODE_SIZE'])

    def deassert(self, python=False, verilog=False):
        """test normal functionality"""
        self.ex_stall.next = 0
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.random_input()
            yield half_period()
            if python:
                self.assertEqual(self.jump, self.jump_out)
                self.assertEqual(self.branch, self.branch_out)
                self.assertEqual(self.mem_read, self.mem_read_out)
                self.assertEqual(self.mem_to_reg, self.mem_to_reg_out)
                self.assertEqual(self.mem_write, self.mem_write_out)
                self.assertEqual(self.alu_src, self.alu_src_out)
                self.assertEqual(self.reg_write, self.reg_write_out)
                self.assertEqual(self.reg_dst, self.reg_dst_out)
                self.assertEqual(self.alu_op, self.alu_op_out)
            if verilog:
                self.assertEqual(self.jump, self.jump_out_v)
                self.assertEqual(self.branch, self.branch_out_v)
                self.assertEqual(self.mem_read, self.mem_read_out_v)
                self.assertEqual(self.mem_to_reg, self.mem_to_reg_out_v)
                self.assertEqual(self.mem_write, self.mem_write_out_v)
                self.assertEqual(self.alu_src, self.alu_src_out_v)
                self.assertEqual(self.reg_write, self.reg_write_out_v)
                self.assertEqual(self.reg_dst, self.reg_dst_out_v)
                self.assertEqual(self.alu_op, self.alu_op_out_v)
        raise StopSimulation

    def asserted(self, python=False, verilog=False):
        """test stalled functionality"""
        self.ex_stall.next = 1
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.random_input()
            yield half_period()
            if python:
                self.assertEqual(0, self.jump_out)
                self.assertEqual(0, self.branch_out)
                self.assertEqual(0, self.mem_read_out)
                self.assertEqual(0, self.mem_to_reg_out)
                self.assertEqual(0, self.mem_write_out)
                self.assertEqual(0, self.alu_src_out)
                self.assertEqual(0, self.reg_write_out)
                self.assertEqual(0, self.reg_dst_out)
                self.assertEqual(0, self.alu_op_out)
            if verilog:
                self.assertEqual(0, self.jump_out_v)
                self.assertEqual(0, self.branch_out_v)
                self.assertEqual(0, self.mem_read_out_v)
                self.assertEqual(0, self.mem_to_reg_out_v)
                self.assertEqual(0, self.mem_write_out_v)
                self.assertEqual(0, self.alu_src_out_v)
                self.assertEqual(0, self.reg_write_out_v)
                self.assertEqual(0, self.reg_dst_out_v)
                self.assertEqual(0, self.alu_op_out_v)
        raise StopSimulation

    def testNormalOperationPython(self):
        """testing normal operations python"""
        stim = self.deassert(python=True)
        dut = self.get_module()
        Simulation(dut, stim).run(quiet=1)

    def testNormalOperationVerilog(self):
        """testing normal operations verilog"""
        stim = self.deassert(verilog=True)
        dut_v = self.get_module(which="verilog")
        Simulation(stim, dut_v).run(quiet=1)

    def testNormalOperationTogether(self):
        """testing normal operations together"""
        stim = self.deassert(verilog=True, python=True)
        dut = self.get_module()
        dut_v = self.get_module(which="verilog")
        Simulation(stim, dut_v, dut).run(quiet=1)

    def testStallOperationPython(self):
        """testing Stall operations python"""
        stim = self.asserted(python=True)
        dut = self.get_module()
        Simulation(dut, stim).run(quiet=1)

    def testStallOperationVerilog(self):
        """testing Stall operations verilog"""
        stim = self.asserted(verilog=True)
        dut_v = self.get_module(which="verilog")
        Simulation(stim, dut_v).run(quiet=1)

    def testStallOperationTogether(self):
        """testing Stall operations together"""
        stim = self.asserted(verilog=True, python=True)
        dut = self.get_module()
        dut_v = self.get_module(which="verilog")
        Simulation(stim, dut_v, dut).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
