"""Control Unit Module Unit Tests"""
import unittest
from unittest import TestCase
from myhdl import Simulation, StopSimulation, ResetSignal

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

    def deassert(self):


if __name__ == '__main__':
    unittest.main()
