"""EX/MEM Pioeline Register Unit tests"""
import unittest
from unittest import TestCase
from random import randint
from myhdl import Simulation, StopSimulation, intbv, Signal, posedge

from src.python.id_ex import id_ex, id_ex_v
from src.commons.clock import clock_gen
from src.commons.signal_generator import unsigned_signal_set, signed_signal_set, random_signed_intbv
from src.commons.settings import settings as sf


@unittest.skip("EX/MEM Register not implemented")
class TestExMemRegister(TestCase):
    """Testing functionality of EX/MEM Pipeline Register"""

    def setUp(self):
        self.clock, self.branch_in, self.mem_read_in, self.reg_write_in, self.z_in, self.z_out, \
            self.z_out_v, self.branch_out, self.branch_out_v, self.mem_read_out, \
            self.mem_read_out_v, self.mem_write_out, self.mem_write_out_v, self.reg_write_out, \
            self.reg_write_out_v, self.mem_write_in = unsigned_signal_set(16, width=1)
        self.rt_in, self.result_in,  self.rt_out, self.rt_out_v, self.result_out, \
            self.result_out_v = signed_signal_set(6)
        self.jmp_addr_in, self.jmp_addr_out, self.jmp_addr_out_v = unsigned_signal_set(3)
        self.reg_dst, self.reg_dst_out, self.reg_dst_out_v = unsigned_signal_set(3, width=5)

    def get_module(self, which="python"):
        """Return module under test"""
        if which == "python":
            module = id_ex(**self.get_args())
        else:
            module = id_ex_v(**self.get_args(verilog=True))
        return module

    def get_args(self, verilog=False):
        """Set parameter dictionary appropriately"""
        return {
            'clock': self.clock,
            'branch_in': self.branch_in,
            'mem_read_in': self.mem_read_in,
            'mem_write_in': self.mem_write_in,
            'reg_write_in': self.reg_write_in,
            'jmp_addr': self.jmp_addr_in,
            'z_in': self.z_in,
            'result_in': self.result_in,
            'rt_in': self.rt_in,
            'reg_dst': self.reg_dst,
            'jmp_addr_out': self.jmp_addr_out_v if verilog else self.jmp_addr_out,
            'z_out': self.z_out_v if verilog else self.z_out,
            'result_out': self.result_out_v if verilog else self.result_out,
            'rt_out': self.rt_out_v if verilog else self.rt_out,
            'branch_out': self.branch_out_v if verilog else self.branch_out,
            'mem_read_out': self.mem_read_out_v if verilog else self.mem_read_out,
            'mem_write_out': self.mem_write_out_v if verilog else self.mem_write_out,
            'reg_write_out': self.reg_write_out_v if verilog else self.reg_write_out,
            'reg_dst_out': self.reg_dst_out_v if verilog else self.reg_dst_out
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
                self.assertEqual(bin(0), bin(self.branch_out))
                self.assertEqual(bin(0), bin(self.mem_read_out))
                self.assertEqual(bin(0), bin(self.mem_write_out))
                self.assertEqual(bin(0), bin(self.reg_write_out))
