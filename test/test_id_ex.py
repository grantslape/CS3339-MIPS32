"""ID/EX Pipeline Register Unit tests"""
import unittest
from unittest import TestCase
from random import randint
from myhdl import Simulation, StopSimulation, intbv, Signal

from src.python.id_ex import id_ex, id_ex_v
from src.commons.clock import clock_gen
from src.commons.signal_generator import unsigned_signal_set, signed_signal_set, random_signed_intbv
from src.commons.settings import settings as sf


class TestIdExRegister(TestCase):
    """Testing ID/EX Pipeline Register Functionality"""

    def setUp(self):
        self.clock, self.branch_in, self.mem_read_in, self.mem_write_in, \
            self.alu_src_in, self.reg_write_in, self.reg_dst_in, self.branch_out, \
            self.branch_out_v, self.mem_read_out, self.mem_read_out_v, \
            self.mem_write_out, self.mem_write_out_v, self.alu_src_out, \
            self.alu_src_out_v, self.reg_write_out, self.reg_write_out_v = unsigned_signal_set(17, width=1)
        self.mem_to_reg_in,self.mem_to_reg_out, self.mem_to_reg_out_v, self.reg_dst_out, self.reg_dst_out_v = unsigned_signal_set(5, width=2)
        self.alu_op_in, self.alu_op_out, self.alu_op_out_v = unsigned_signal_set(3, width=sf['ALU_CODE_SIZE'])
        self.pc_value_in, self.pc_value_out, self.pc_value_out_v = unsigned_signal_set(3)
        self.r_data1, self.r_data1_out, self.r_data1_out_v, self.r_data2, self.r_data2_out, \
            self.r_data2_out_v, self.imm, self.imm_out, self.imm_out_v, = signed_signal_set(9)
        self.rs, self.rt, self.rd, self.rs_out, self.rs_out_v, self.rt_out, self.rt_out_v, \
            self.rd_out, self.rd_out_v = unsigned_signal_set(9, width=5)

    def get_module(self, which="python"):
        """Return module instantiation"""
        if which == "python":
            module = id_ex(**self.get_args())
        else:
            module = id_ex_v(**self.get_args(which="verilog"))
        return module

    def get_args(self, which="python"):
        """Set parameter dictionary appropriately"""
        return {
            'clock': self.clock,
            'branch_in': self.branch_in,
            'reg_write_in': self.reg_write_in,
            'alu_src_in': self.alu_src_in,
            'alu_op_in': self.alu_op_in,
            'mem_read_in': self.mem_read_in,
            'mem_to_reg_in': self.mem_to_reg_in,
            'mem_write_in': self.mem_write_in,
            'reg_dst_in': self.reg_dst_in,
            'pc_value_in': self.pc_value_in,
            'r_data1': self.r_data1,
            'r_data2': self.r_data2,
            'rs': self.rs,
            'rt': self.rt,
            'rd': self.rd,
            'imm': self.imm,
            'r_data1_out': self.r_data1_out if which == "python" else self.r_data1_out_v,
            'r_data2_out': self.r_data2_out if which == "python" else self.r_data2_out_v,
            'imm_out': self.imm_out if which == "python" else self.imm_out_v,
            'rs_out': self.rs_out if which == "python" else  self.rs_out_v,
            'rt_out': self.rt_out if which == "python" else self.rt_out_v,
            'rd_out': self.rd_out if which == "python" else self.rd_out_v,
            'pc_value_out': self.pc_value_out if which == "python" else self.pc_value_out_v,
            'branch_out': self.branch_out if which == "python" else self.branch_out_v,
            'alu_op_out': self.alu_op_out if which == "python" else self.alu_op_out_v,
            'mem_read_out': self.mem_read_out if which == "python" else self.mem_read_out_v,
            'mem_write_out': self.mem_write_out if which == "python" else self.mem_write_out_v,
            'alu_src_out': self.alu_src_out if which == "python" else self.alu_src_out_v,
            'reg_write_out': self.reg_write_out if which == "python" else self.reg_write_out_v,
            'reg_dst_out': self.reg_dst_out if which == "python" else self.reg_dst_out_v,
            'mem_to_reg_out': self.mem_to_reg_out if which == "python" else self.mem_to_reg_out_v
        }

    def deassert(self, python=False, verilog=False):
        """test deassert functionality"""
        for _ in range(sf['DEFAULT_TEST_LENGTH'] / 2):
            yield self.clock.posedge
            yield self.clock.negedge
            if python:
                self.assertEqual(bin(self.branch_out), bin(0b0))
                self.assertEqual(bin(0b0), bin(self.mem_read_out))
                self.assertEqual(bin(0b0), bin(self.mem_to_reg_out))
                self.assertEqual(bin(0b0), bin(self.mem_write_out))
                self.assertEqual(bin(0b0), bin(self.alu_src_out))
                self.assertEqual(bin(0b0), bin(self.reg_write_out))
                self.assertEqual(bin(0b0), bin(self.reg_dst_out))
                self.assertEqual(bin(0b0), bin(self.alu_op_out))
                self.assertEqual(bin(0b0), bin(self.pc_value_out))
                self.assertEqual(bin(0b0), bin(self.r_data1_out))
                self.assertEqual(bin(0b0), bin(self.r_data2_out))
                self.assertEqual(bin(0b0), bin(self.imm_out))
                self.assertEqual(bin(0b0), bin(self.rs_out))
                self.assertEqual(bin(0b0), bin(self.rt_out))
                self.assertEqual(bin(0b0), bin(self.rd_out))
            if verilog:
                self.assertEqual(bin(self.branch_out_v), bin(0b0))
                self.assertEqual(bin(0b0), bin(self.mem_read_out_v))
                self.assertEqual(bin(0b0), bin(self.mem_to_reg_out_v))
                self.assertEqual(bin(0b0), bin(self.mem_write_out_v))
                self.assertEqual(bin(0b0), bin(self.alu_src_out_v))
                self.assertEqual(bin(0b0), bin(self.reg_write_out_v))
                self.assertEqual(bin(0b0), bin(self.reg_dst_out_v))
                self.assertEqual(bin(0b0), bin(self.alu_op_out_v))
                self.assertEqual(bin(0b0), bin(self.pc_value_out_v))
                self.assertEqual(bin(0b0), bin(self.r_data1_out_v))
                self.assertEqual(bin(0b0), bin(self.r_data2_out_v))
                self.assertEqual(bin(0b0), bin(self.imm_out_v))
                self.assertEqual(bin(0b0), bin(self.rs_out_v))
                self.assertEqual(bin(0b0), bin(self.rt_out_v))
                self.assertEqual(bin(0b0), bin(self.rd_out_v))
        raise StopSimulation

    def dynamic(self, python=False, verilog=False):
        """Dynamic testing of ID/EX Pipeline Register"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.branch_in.next, self.mem_read_in.next,\
                self.mem_write_in.next, self.alu_src_in.next, self.reg_write_in.next = unsigned_signal_set(5, randint(0, 1), 1)
            self.mem_to_reg_in.next, self.reg_dst_in.next = unsigned_signal_set(2, randint(0,2), 1)
            self.alu_op_in = Signal(intbv()[sf['ALU_CODE_SIZE']:])
            self.pc_value_in.next = Signal(intbv(randint(0, 15))[4:])
            self.r_data1.next, self.r_data2.next, self.imm.next = [
                Signal(random_signed_intbv()) for _ in range(3)
            ]
            self.rs.next, self.rt.next, self.rd.next = [
                Signal(intbv(randint(0, sf['WIDTH'] - 1))[5:]) for _ in range(3)
            ]
            yield self.clock.posedge
            yield self.clock.negedge
            if python:
                self.assertEqual(bin(self.branch_out), bin(self.branch_in))
                self.assertEqual(bin(self.mem_read_in), bin(self.mem_read_out))
                self.assertEqual(bin(self.mem_to_reg_in), bin(self.mem_to_reg_out))
                self.assertEqual(bin(self.mem_write_in), bin(self.mem_write_out))
                self.assertEqual(bin(self.alu_src_in), bin(self.alu_src_out))
                self.assertEqual(bin(self.reg_write_in), bin(self.reg_write_out))
                self.assertEqual(bin(self.reg_dst_in), bin(self.reg_dst_out))
                self.assertEqual(bin(self.alu_op_in), bin(self.alu_op_out))
                self.assertEqual(bin(self.pc_value_in), bin(self.pc_value_out))
                self.assertEqual(bin(self.r_data1), bin(self.r_data1_out))
                self.assertEqual(bin(self.r_data2), bin(self.r_data2_out))
                self.assertEqual(bin(self.imm), bin(self.imm_out))
                self.assertEqual(bin(self.rs), bin(self.rs_out))
                self.assertEqual(bin(self.rt), bin(self.rt_out))
                self.assertEqual(bin(self.rd), bin(self.rd_out))
            if verilog:
                self.assertEqual(bin(self.branch_out_v), bin(self.branch_in))
                self.assertEqual(bin(self.mem_read_in), bin(self.mem_read_out_v))
                self.assertEqual(bin(self.mem_to_reg_in), bin(self.mem_to_reg_out_v))
                self.assertEqual(bin(self.mem_write_in), bin(self.mem_write_out_v))
                self.assertEqual(bin(self.alu_src_in), bin(self.alu_src_out_v))
                self.assertEqual(bin(self.reg_write_in), bin(self.reg_write_out_v))
                self.assertEqual(bin(self.reg_dst_in), bin(self.reg_dst_out_v))
                self.assertEqual(bin(self.alu_op_in), bin(self.alu_op_out_v))
                self.assertEqual(bin(self.pc_value_in), bin(self.pc_value_out_v))
                self.assertEqual(bin(self.r_data1), bin(self.r_data1_out_v))
                self.assertEqual(bin(self.r_data2), bin(self.r_data2_out_v))
                self.assertEqual(bin(self.imm), bin(self.imm_out_v))
                self.assertEqual(bin(self.rs), bin(self.rs_out_v))
                self.assertEqual(bin(self.rt), bin(self.rt_out_v))
                self.assertEqual(bin(self.rd), bin(self.rd_out_v))
        raise StopSimulation

    def testDeassertPython(self):
        """Checking stalling Python"""
        dut = self.get_module()
        CLK = clock_gen(self.clock)
        stim = self.deassert(python=True)
        Simulation(CLK, stim, dut).run(quiet=1)

    def testDeassertVerilog(self):
        """Checking stalling Verilog"""
        dut_v = self.get_module("verilog")
        CLK = clock_gen(self.clock)
        stim_v = self.deassert(verilog=True)
        Simulation(CLK, stim_v, dut_v).run(quiet=1)

    def testDeassertTogether(self):
        """Checking stalling Together"""
        dut = self.get_module()
        dut_v = self.get_module("verilog")
        CLK = clock_gen(self.clock)
        stim = self.deassert(python=True, verilog=True)
        Simulation(CLK, stim, dut, dut_v).run(quiet=1)

    def testDynamicPython(self):
        """Checking stalling Python"""
        dut = self.get_module()
        CLK = clock_gen(self.clock)
        stim = self.dynamic(python=True)
        Simulation(CLK, stim, dut).run(quiet=1)

    def testDynamicVerilog(self):
        """Checking stalling Verilog"""
        dut_v = self.get_module("verilog")
        CLK = clock_gen(self.clock)
        stim = self.dynamic(verilog=True)
        Simulation(CLK, stim, dut_v).run(quiet=1)

    def testDynamicTogether(self):
        """Checking stalling Together"""
        dut = self.get_module()
        dut_v = self.get_module("verilog")
        CLK = clock_gen(self.clock)
        stim = self.dynamic(python=True, verilog=True)
        Simulation(CLK, stim, dut, dut_v).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
