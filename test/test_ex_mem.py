"""EX/MEM Pioeline Register Unit tests"""
import unittest
from random import randint
from unittest import TestCase
from myhdl import Simulation, StopSimulation, bin

from src.python.ex_mem import ex_mem, ex_mem_v
from src.commons.clock import clock_gen
from src.commons.signal_generator import unsigned_signal_set, signed_signal_set, \
    random_unsigned_intbv, rand_unsigned_signal_set, rand_signed_signal_set
from src.commons.settings import settings as sf


class TestExMemRegister(TestCase):
    """Testing functionality of EX/MEM Pipeline Register"""

    def setUp(self):
        self.clock, self.branch_in, self.mem_read_in, self.reg_write_in, self.z_in, self.z_out, \
            self.z_out_v, self.branch_out, self.branch_out_v, self.mem_read_out, \
            self.mem_read_out_v, self.mem_write_out, self.mem_write_out_v, self.reg_write_out, \
            self.reg_write_out_v, self.mem_write_in = unsigned_signal_set(16, width=1)
        self.mem_to_reg_in, self.mem_to_reg_out, self.mem_to_reg_out_v = unsigned_signal_set(3, width=2)
        self.rt_in, self.result_in,  self.rt_out, self.rt_out_v, self.pc_value_in, self.pc_value_out, self.pc_value_out_v, self.result_out, \
            self.result_out_v = signed_signal_set(9)
        self.jmp_addr_in, self.jmp_addr_out, self.jmp_addr_out_v = unsigned_signal_set(3)
        self.reg_dst_in, self.reg_dst_out, self.reg_dst_out_v = unsigned_signal_set(3, width=5)

    def get_module(self, which="python"):
        """Return module under test"""
        if which == "python":
            module = ex_mem(**self.get_args())
        else:
            module = ex_mem_v(**self.get_args(verilog=True))
        return module

    def get_args(self, verilog=False):
        """Set parameter dictionary appropriately"""
        return {
            'clock': self.clock,
            'branch_in': self.branch_in,
            'mem_read_in': self.mem_read_in,
            'mem_write_in': self.mem_write_in,
            'reg_write_in': self.reg_write_in,
            'mem_to_reg_in': self.mem_to_reg_in,
            'jmp_addr': self.jmp_addr_in,
            'pc_value_in':self.pc_value_in,
            'z_in': self.z_in,
            'result_in': self.result_in,
            'rt_in': self.rt_in,
            'reg_dst_in': self.reg_dst_in,
            'jmp_addr_out': self.jmp_addr_out_v if verilog else self.jmp_addr_out,
            'z_out': self.z_out_v if verilog else self.z_out,
            'result_out': self.result_out_v if verilog else self.result_out,
            'rt_out': self.rt_out_v if verilog else self.rt_out,
            'pc_value_out':self.pc_value_out_v if verilog else self.pc_value_out,
            'branch_out': self.branch_out_v if verilog else self.branch_out,
            'mem_read_out': self.mem_read_out_v if verilog else self.mem_read_out,
            'mem_write_out': self.mem_write_out_v if verilog else self.mem_write_out,
            'reg_write_out': self.reg_write_out_v if verilog else self.reg_write_out,
            'reg_dst_out': self.reg_dst_out_v if verilog else self.reg_dst_out,
            'mem_to_reg_in': self.mem_to_reg_in,
            'mem_to_reg_out': self.mem_to_reg_out_v if verilog else self.mem_to_reg_out
        }

    def deassert(self, python=False, verilog=False):
        """Test deasserted functionality (no input)"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            yield self.clock.posedge
            yield self.clock.negedge
            if python:
                self.assertEqual(bin(0), bin(self.jmp_addr_out))
                self.assertEqual(bin(0), bin(self.z_out))
                self.assertEqual(bin(0), bin(self.result_out))
                self.assertEqual(bin(0), bin(self.rt_out))
                self.assertEqual(bin(0), bin(self.pc_value_out))
                self.assertEqual(bin(0), bin(self.branch_out))
                self.assertEqual(bin(0), bin(self.mem_read_out))
                self.assertEqual(bin(0), bin(self.mem_to_reg_out))
                self.assertEqual(bin(0), bin(self.mem_write_out))
                self.assertEqual(bin(0), bin(self.reg_write_out))
                self.assertEqual(bin(0), bin(self.reg_dst_out))
                self.assertEqual(bin(0), bin(self.mem_to_reg_out))
            if verilog:
                self.assertEqual(bin(0), bin(self.jmp_addr_out_v))
                self.assertEqual(bin(0), bin(self.z_out_v))
                self.assertEqual(bin(0), bin(self.result_out_v))
                self.assertEqual(bin(0), bin(self.rt_out_v))
                self.assertEqual(bin(0), bin(self.pc_value_out_v))
                self.assertEqual(bin(0), bin(self.branch_out_v))
                self.assertEqual(bin(0), bin(self.mem_read_out_v))
                self.assertEqual(bin(0), bin(self.mem_to_reg_out_v))
                self.assertEqual(bin(0), bin(self.mem_write_out_v))
                self.assertEqual(bin(0), bin(self.reg_write_out_v))
                self.assertEqual(bin(0), bin(self.reg_dst_out_v))
                self.assertEqual(bin(0), bin(self.mem_to_reg_out_v))
        raise StopSimulation

    def dynamic(self, python=False, verilog=False):
        """Testing dynamic functionality"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.branch_in.next, self.mem_read_in.next, self.reg_write_in.next, \
                self.z_in.next = rand_unsigned_signal_set(4, width=1)
            self.mem_to_reg_in.next = randint(0, 2)
            self.rt_in.next, self.result_in.next, self.pc_value_in.next = rand_signed_signal_set(3)
            self.jmp_addr_in.next = random_unsigned_intbv()
            self.reg_dst_in.next = random_unsigned_intbv(width=5)
            yield self.clock.posedge
            yield self.clock.negedge
            if python:
                self.assertEqual(bin(self.jmp_addr_in), bin(self.jmp_addr_out))
                self.assertEqual(bin(self.z_in), bin(self.z_out))
                self.assertEqual(bin(self.result_in), bin(self.result_out))
                self.assertEqual(bin(self.rt_in), bin(self.rt_out))
                self.assertEqual(bin(self.pc_value_in), bin(self.pc_value_out))
                self.assertEqual(bin(self.branch_in), bin(self.branch_out))
                self.assertEqual(bin(self.mem_read_in), bin(self.mem_read_out))
                self.assertEqual(bin(self.mem_to_reg_in), bin(self.mem_to_reg_out))
                self.assertEqual(bin(self.mem_write_in), bin(self.mem_write_out))
                self.assertEqual(bin(self.reg_write_in), bin(self.reg_write_out))
                self.assertEqual(bin(self.reg_dst_in), bin(self.reg_dst_out))
            if verilog:
                self.assertEqual(bin(self.jmp_addr_in), bin(self.jmp_addr_out_v))
                self.assertEqual(bin(self.z_in), bin(self.z_out_v))
                self.assertEqual(bin(self.result_in), bin(self.result_out_v))
                self.assertEqual(bin(self.rt_in), bin(self.rt_out_v))
                self.assertEqual(bin(self.pc_value_in), bin(self.pc_value_out_v))
                self.assertEqual(bin(self.branch_in), bin(self.branch_out_v))
                self.assertEqual(bin(self.mem_read_in), bin(self.mem_read_out_v))
                self.assertEqual(bin(self.mem_to_reg_in), bin(self.mem_to_reg_out_v))
                self.assertEqual(bin(self.mem_write_in), bin(self.mem_write_out_v))
                self.assertEqual(bin(self.reg_write_in), bin(self.reg_write_out_v))
                self.assertEqual(bin(self.reg_dst_in), bin(self.reg_dst_out_v))
        raise StopSimulation

    def testDeassertPython(self):
        """Check when there is no input Python"""
        clk = clock_gen(self.clock)
        dut = self.get_module()
        stim = self.deassert(python=True)
        Simulation(clk, dut, stim).run(quiet=1)

    def testDeassertVerilog(self):
        """Check when there is no input Verilog"""
        clk = clock_gen(self.clock)
        dut = self.get_module(which="verilog")
        stim = self.deassert(verilog=True)
        Simulation(clk, dut, stim).run(quiet=1)

    def testDeassertTogether(self):
        """Check when there is no input Together"""
        clk = clock_gen(self.clock)
        dut = self.get_module()
        dut_v = self.get_module(which="verilog")
        stim = self.deassert(python=True, verilog=True)
        Simulation(clk, dut, dut_v, stim).run(quiet=1)

    def testDynamicPython(self):
        """Check normal operation Python"""
        clk = clock_gen(self.clock)
        dut = self.get_module()
        stim = self.dynamic(python=True)
        Simulation(clk, dut, stim).run(quiet=1)

    def testDynamicVerilog(self):
        """Check normal operation Verilog"""
        clk = clock_gen(self.clock)
        dut = self.get_module(which="verilog")
        stim = self.dynamic(verilog=True)
        Simulation(clk, dut, stim).run(quiet=1)

    def testDynamicTogether(self):
        """Check normal operation Together"""
        clk = clock_gen(self.clock)
        dut = self.get_module()
        dut_v = self.get_module(which="verilog")
        stim = self.dynamic(python=True, verilog=True)
        Simulation(clk, dut, dut_v, stim).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
