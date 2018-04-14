"""Control Unit Module Unit Tests"""
import unittest
from unittest import TestCase
from myhdl import Simulation, StopSimulation, ResetSignal, intbv

from src.python.ctrl import ctrl, ctrl_v
from src.commons.clock import half_period
from src.commons.settings import settings as sf
from src.commons.signal_generator import unsigned_signal_set

@unittest.skip("Ctrl unit not implemented")
class TestControlUnit(TestCase):
    """Testing Control unit functionality"""

    def setUp(self):
        self.funct_in, self.op_in = unsigned_signal_set(2, width=5)
        self.jump, self.jump_v, self.branch, self.branch_v, self.mem_read, self.mem_read_v, \
            self.mem_to_reg, self.mem_to_reg_v, self.mem_write, self.mem_write_v, self.alu_src, \
            self.alu_src_v, self.reg_write, self.reg_write_v, self.reg_dst, self.reg_dst_v = \
            unsigned_signal_set(16, width=1)
        self.alu_op, self.alu_op_v = unsigned_signal_set(2, width=sf['ALU_CODE_SIZE'])
        self.reset_out, self.reset_out_v = ResetSignal(sf['INACTIVE_HIGH'],
                                                       active=sf['ACTIVE_LOW'],
                                                       async=True)

    def get_module(self, which="python"):
        """Return module under test"""
        if which == "python":
            module = ctrl(**self.get_args())
        else
            module = ctrl_v(**self.get_args(which="verilog"))
        return module

    def get_args(self, which="python"):
        """Set parameter dictionary appropriately"""
        return {
            'funct_in': self.funct_in,
            'op_in': self.op_in,
            'branch': self.branch if which == "python" else self.branch_v,
            'mem_read': self.mem_read if which == "python" else self.mem_read_v,
            'mem_to_reg': self.mem_to_reg if which == "python" else self.mem_to_reg_v,
            'mem_write': self.mem_write if which == "python" else self.mem_write_v,
            'alu_src': self.alu_src if which == "python" else self.alu_src_v,
            'reg_write': self.reg_write if which == "python" else self.reg_write_v,
            'reg_dst': self.reg_dst if which == "python" else self.reg_dst_v,
            'alu_op': self.alu_op if which == "python" else self.alu_op_v,
            'reset_out': self.reset_out if which == "python" else self.reset_out_v
        }

    def deassert(self, python=False, verilog=False):
        """Test deasserted functionality"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            yield half_period()
            if python:
                self.assertEqual(bin(0), bin(self.branch))
                self.assertEqual(bin(0), bin(self.mem_read))
                self.assertEqual(bin(0), bin(self.mem_to_reg))
                self.assertEqual(bin(0), bin(self.mem_write))
                self.assertEqual(bin(0), bin(self.alu_src))
                self.assertEqual(bin(0), bin(self.reg_write))
                self.assertEqual(bin(0), bin(self.reg_dst))
                self.assertEqual(bin(0), bin(self.alu_op))
                self.assertEqual(self.reset_out, sf['INACTIVE_HIGH'])
            if verilog:
                self.assertEqual(bin(0), bin(self.branch_v))
                self.assertEqual(bin(0), bin(self.mem_read_v))
                self.assertEqual(bin(0), bin(self.mem_to_reg_v))
                self.assertEqual(bin(0), bin(self.mem_write_v))
                self.assertEqual(bin(0), bin(self.alu_src_v))
                self.assertEqual(bin(0), bin(self.reg_write_v))
                self.assertEqual(bin(0), bin(self.reg_dst_v))
                self.assertEqual(bin(0), bin(self.alu_op_v))
                self.assertEqual(self.reset_out_v, sf['INACTIVE_HIGH'])
        raise StopSimulation

    def test_mem_inst(self, python=False, verilog=False):
        """Test LW and SW instructions"""
        self.op_in.next = intbv(35)[5:]
        yield half_period()
        if python:
            self.assertEqual(0, self.jump)
            self.assertEqual(0, self.branch)


    def branch_test(self, python=False, verilog=False):
        """Test branch instructions"""

    def jump_test(self, python=False, verilog=False):
        """Test jump style instructions"""

    def add_test(self, python=False, verilog=False):
        """Test R style addition"""

    def sub_test(self, python=False, verilog=False):
        """Test R style subtraction"""

    def xor_test(self, python=False, verilog=False):
        """Test R style xor"""

    def or_test(self, python=False, verilog=False):
        """Test R style or"""

    def and_test(self, python=False, verilog=False):
        """Test R style and"""

    def sll_test(self, python=False, verilog=False):
        """Test R style shift left logical"""

    def srl_test(self, python=False, verilog=False):
        """Test R style shift right logical"""

    def nor_test(self, python=False, verilog=False):
        """Test R style not or"""

    def slt_test(self, python=False, verilog=False):
        """Test R style slt"""


if __name__ == '__main__':
    unittest.main()
