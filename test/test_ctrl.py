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
        self.funct_in, self.op_in = unsigned_signal_set(2, width=6)
        self.jump, self.jump_v = unsigned_signal_set(2, width=2)
        self.branch, self.branch_v, self.mem_read, self.mem_read_v, self.mem_to_reg, \
        self.mem_to_reg_v, self.mem_write, self.mem_write_v, self.alu_src, self.alu_src_v, \
            self.reg_write, self.reg_write_v, self.reg_dst, self.reg_dst_v, self.clock = \
            unsigned_signal_set(15, width=1)
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
            'clock': self.clock,
            'funct_in': self.funct_in,
            'op_in': self.op_in,
            'jump': self.jump if which == "python" else self.jump_v,
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

    def test_mem_inst(self, python=False, verilog=False):
        """Test LW and SW instructions"""
        # 35 is op code for lw
        self.op_in.next = intbv(35)[6:]
        yield half_period()
        if python:
            self.assertEqual(0, self.jump)
            self.assertEqual(0, self.branch)
            self.assertEqual(1, self.mem_read)
            self.assertEqual(1, self.mem_to_reg)
            self.assertEqual(0, self.mem_write)
            self.assertEqual(1, self.alu_src)
            self.assertEqual(1, self.reg_write)
            self.assertEqual(0, self.reg_dst)
            self.assertEqual(sf['INACTIVE_HIGH'], self.reset_out)
            self.assertEqual(1, self.alu_op)
        if verilog:
            self.assertEqual(0, self.jump_v)
            self.assertEqual(0, self.branch_v)
            self.assertEqual(1, self.mem_read_v)
            self.assertEqual(1, self.mem_to_reg_v)
            self.assertEqual(0, self.mem_write_v)
            self.assertEqual(1, self.alu_src_v)
            self.assertEqual(1, self.reg_write_v)
            self.assertEqual(0, self.reg_dst_v)
            self.assertEqual(sf['INACTIVE_HIGH'], self.reset_out_v)
            self.assertEqual(1, self.alu_op_v)
        # 43 is op code for sw
        self.op_in.next = intbv(45)[6:]
        yield half_period()
        if python:
            self.assertEqual(0, self.jump)
            self.assertEqual(0, self.branch)
            self.assertEqual(0, self.mem_read)
            self.assertEqual(1, self.mem_write)
            self.assertEqual(1, self.alu_src)
            self.assertEqual(0, self.reg_write)
            self.assertEqual(sf['INACTIVE_HIGH'], self.reset_out)
            self.assertEqual(1, self.alu_op)
        if verilog:
            self.assertEqual(0, self.jump_v)
            self.assertEqual(0, self.branch_v)
            self.assertEqual(0, self.mem_read_v)
            self.assertEqual(1, self.mem_write_v)
            self.assertEqual(1, self.alu_src_v)
            self.assertEqual(0, self.reg_write_v)
            self.assertEqual(sf['INACTIVE_HIGH'], self.reset_out_v)
            self.assertEqual(1, self.alu_op_v)
        raise StopSimulation


    def branch_test(self, python=False, verilog=False):
        """Test branch instructions"""
        # 4 is op code for beq
        self.op_in.next = intbv(4)[6:]
        yield half_period()
        if python:
            self.assertEqual(bin(0b0010), bin(self.alu_op))
            self.assertEqual(0, self.jump)
            self.assertEqual(1, self.branch)
            self.assertEqual(0, self.mem_read)
            self.assertEqual(0, self.mem_write)
            self.assertEqual(0, self.alu_src)
            self.assertEqual(0, self.reg_write)
            self.assertEqual(sf['INACTIVE_HIGH'], self.reset_out)
        if verilog:
            self.assertEqual(bin(0b0010), bin(self.alu_op_v))
            self.assertEqual(0, self.jump_v)
            self.assertEqual(1, self.branch_v)
            self.assertEqual(0, self.mem_read_v)
            self.assertEqual(0, self.mem_write_v)
            self.assertEqual(0, self.alu_src_v)
            self.assertEqual(0, self.reg_write_v)
            self.assertEqual(sf['INACTIVE_HIGH'], self.reset_out_v)
        raise StopSimulation

    def j_lbl_test(self, python=False, verilog=False):
        """Test j lbl style instruction"""
        # 2 is op code for j
        self.op_in.next = intbv(2)[6:]
        yield half_period()
        # These control signals I am unsure about
        if python:
            self.assertEqual(1, self.jump)
            self.assertEqual(0, self.branch)
            self.assertEqual(sf['ACTIVE_LOW'], self.reset_out)
            self.assertEqual(0, self.mem_write)
            self.assertEqual(0, self.reg_write)
            self.assertEqual(0, self.mem_read)
            self.assertEqual(0, self.alu_src)
            self.assertEqual(0, self.alu_op)
        if verilog:
            self.assertEqual(1, self.jump_v)
            self.assertEqual(0, self.branch_v)
            self.assertEqual(sf['ACTIVE_LOW'], self.reset_out_v)
            self.assertEqual(0, self.mem_write_v)
            self.assertEqual(0, self.reg_write_v)
            self.assertEqual(0, self.mem_read_v)
            self.assertEqual(0, self.alu_src_v)
            self.assertEqual(0, self.alu_op_v)
        raise StopSimulation

    def jal_test(self, python=False, verilog=False):
        """Test jump and link instruction"""
        # 3 is op code for jal
        self.op_in.next = intbv(3)[6:]
        yield half_period()
        if python:
            self.assertEqual(1, self.jump)
            self.assertEqual(0, self.branch)
            self.assertEqual(sf['ACTIVE_LOW'], self.reset_out)
            # we may want to "write" here and drop PC+4 value into the flow.
            self.assertEqual(0, self.reg_write)
            self.assertEqual(0, self.mem_read)
            self.assertEqual(0, self.alu_src)
            # Unsure about this, we may way to add here
            self.assertEqual(0, self.alu_op)
            self.assertEqual(0, self.mem_write)
        if verilog:
            self.assertEqual(1, self.jump)
            self.assertEqual(0, self.branch)
            self.assertEqual(sf['ACTIVE_LOW'], self.reset_out)
            # we may want to "write" here and drop PC+4 value into the flow.
            self.assertEqual(0, self.reg_write)
            self.assertEqual(0, self.mem_read)
            self.assertEqual(0, self.alu_src)
            # Unsure about this, we may way to add here
            self.assertEqual(0, self.alu_op)
            self.assertEqual(0, self.mem_write)
        raise StopSimulation

    def jr_ra_test(self, python=False, verilog=False):
        """Test jr $ra instructions"""
        # We are using 25 for op code for jr
        self.op_in = intbv(25)[6:]
        yield half_period()
        if python:
            # might need to do some massaging here with special flow
            self.assertEqual(bin(0b10), bin(self.jump))
            self.assertEqual(0, self.branch)
            self.assertEqual(sf['ACTIVE_LOW'], self.reset_out)
            self.assertEqual(0, self.mem_read)
            self.assertEqual(0, self.alu_src)
            self.assertEqual(0, self.reg_write)
            self.assertEqual(0, self.mem_write)
        if verilog:
            self.assertEqual(bin(0b10), bin(self.jump_v))
            self.assertEqual(0, self.branch_v)
            self.assertEqual(sf['ACTIVE_LOW'], self.reset_out_v)
            self.assertEqual(0, self.mem_read_v)
            self.assertEqual(0, self.alu_src_v)
            self.assertEqual(0, self.reg_write_v)
            self.assertEqual(0, self.mem_write_v)
        raise StopSimulation

    def r_type_python(self):
        """Common R-type assertions"""
        self.assertEqual(0, self.jump)
        self.assertEqual(0, self.branch)
        self.assertEqual(0, self.mem_read)
        self.assertEqual(0, self.mem_to_reg)
        self.assertEqual(0, self.mem_write)
        self.assertEqual(0, self.alu_src)
        self.assertEqual(1, self.reg_write)
        self.assertEqual(1, self.reg_dst)
        self.assertEqual(sf['INACTIVE_HIGH'], self.reset_out)

    def r_type_verilog(self):
        """Common R-type assertions verilog"""
        self.assertEqual(0, self.jump_v)
        self.assertEqual(0, self.branch_v)
        self.assertEqual(0, self.mem_read_v)
        self.assertEqual(0, self.mem_to_reg_v)
        self.assertEqual(0, self.mem_write_v)
        self.assertEqual(0, self.alu_src_v)
        self.assertEqual(1, self.reg_write_v)
        self.assertEqual(1, self.reg_dst_v)
        self.assertEqual(sf['INACTIVE_HIGH'], self.reset_out_v)

    def add_test(self, python=False, verilog=False):
        """Test R style addition"""
        # 0/20 for add
        self.op_in = intbv()[6:]
        self.funct_in = intbv(8)[6:]
        yield half_period()
        if python:
            self.r_type_python()
            self.assertEqual(bin(0b0001), bin(self.alu_op))
        if verilog:
            self.r_type_verilog()
            self.assertEqual(bin(0b0001), bin(self.alu_op_v))
        raise StopSimulation

    def sub_test(self, python=False, verilog=False):
        """Test R style subtraction"""
        # 0/22 for sub
        self.op_in = intbv()[6:]
        self.funct_in = intbv(22)[6:]
        yield half_period()
        if python:
            self.r_type_python()
            self.assertEqual(bin(0b0010), bin(self.alu_op))
        if verilog:
            self.r_type_verilog()
            self.assertEqual(bin(0b0010), bin(self.alu_op_v))
        raise StopSimulation

    def xor_test(self, python=False, verilog=False):
        """Test R style xor"""
        # 0/38 for xor
        self.op_in = intbv()[6:]
        self.funct_in = intbv(38)[6:]
        yield half_period()
        if python:
            self.r_type_python()
            self.assertEqual(bin(0b0011), bin(self.alu_op))
        if verilog:
            self.r_type_verilog()
            self.assertEqual(bin(0b0011), bin(self.alu_op_v))
        raise StopSimulation

    def or_test(self, python=False, verilog=False):
        """Test R style or"""
        # 0/37 for or
        self.op_in = intbv()[6:]
        self.funct_in = intbv(37)[6:]
        yield half_period()
        if python:
            self.r_type_python()
            self.assertEqual(bin(0b0100), bin(self.alu_op))
        if verilog:
            self.r_type_verilog()
            self.assertEqual(bin(0b0100), bin(self.alu_op_v))
        raise StopSimulation

    def and_test(self, python=False, verilog=False):
        """Test R style and"""
        # 0/36 for and
        self.op_in = intbv()[6:]
        self.funct_in = intbv(36)[6:]
        yield half_period()
        if python:
            self.r_type_python()
            self.assertEqual(bin(0b0101), bin(self.alu_op))
        if verilog:
            self.r_type_verilog()
            self.assertEqual(bin(0b0101), bin(self.alu_op_v))
        raise StopSimulation

    def sll_test(self, python=False, verilog=False):
        """Test R style shift left logical"""
        # 0/0 for sll
        self.op_in = intbv()[6:]
        self.funct_in = intbv()[6:]
        yield half_period()
        if python:
            self.r_type_python()
            self.assertEqual(bin(0b0110), bin(self.alu_op))
        if verilog:
            self.r_type_verilog()
            self.assertEqual(bin(0b0110), bin(self.alu_op_v))
        raise StopSimulation

    def srl_test(self, python=False, verilog=False):
        """Test R style shift right logical"""
        # 0/2 for srl
        self.op_in = intbv()[6:]
        self.funct_in = intbv(2)[6:]
        yield half_period()
        if python:
            self.r_type_python()
            self.assertEqual(bin(0b0111), bin(self.alu_op))
        if verilog:
            self.r_type_verilog()
            self.assertEqual(bin(0b0111), bin(self.alu_op_v))
        raise StopSimulation

    def nor_test(self, python=False, verilog=False):
        """Test R style not or"""
        # 0/39 for nor
        self.op_in = intbv()[6:]
        self.funct_in = intbv(39)[6:]
        yield half_period()
        if python:
            self.r_type_python()
            self.assertEqual(bin(0b1000), bin(self.alu_op))
        if verilog:
            self.r_type_verilog()
            self.assertEqual(bin(0b1000), bin(self.alu_op_v))
        raise StopSimulation

    def slt_test(self, python=False, verilog=False):
        """Test R style slt"""
        # 0/42 for slt
        self.op_in = intbv()[6:]
        self.funct_in = intbv(42)[6:]
        yield half_period()
        if python:
            self.r_type_python()
            self.assertEqual(bin(0b1001), bin(self.alu_op))
        if verilog:
            self.r_type_verilog()
            self.assertEqual(bin(0b1001), bin(self.alu_op_v))
        raise StopSimulation


if __name__ == '__main__':
    unittest.main()
