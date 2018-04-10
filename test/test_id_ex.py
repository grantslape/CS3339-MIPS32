"""ID/EX Pipeline Register Unit tests"""
import unittest
from unittest import TestCase
from random import randint
from myhdl import Simulation, StopSimulation, intbv, Signal, posedge, ResetSignal

from src.python.id_ex import id_ex, id_ex_v
from src.commons.clock import clock_gen
from src.commons.signal_generator import unsigned_signal_set, signed_signal_set, random_signed_intbv
from src.commons.settings import settings as sf


@unittest.skip("ID/EX Register not implemented")
class TestIdExRegister(TestCase):
    """Testing ID/EX Pipeline Register Functionality"""

    def setUp(self):
        self.clock, self.branch_in, self.mem_read_in, self.mem_to_reg_in, self.mem_write_in, \
            self.alu_src_in, self.reg_write_in, self.reg_dst_in, self.branch_out, \
            self.branch_out_v, self.mem_read_out, self.mem_read_out_v, self.mem_to_reg_out, \
            self.mem_to_reg_out_v, self.mem_write_out, self.mem_write_out_v, self.alu_src_out, \
            self.alu_src_out_v, self.reg_write_out, self.reg_write_out_v, self.reg_dst_out, \
            self.reg_dst_out_v = unsigned_signal_set(22, width=1)
        # TODO: UPDATE WHEN ALU OP CODES ARE DETERMINED
        self.alu_op_in, self.alu_op_out, self.alu_op_out_v = unsigned_signal_set(3)
        self.pc_value_in, self.pc_value_out, self.pc_value_out_v = unsigned_signal_set(3)
        self.r_data1, self.r_data1_out, self.r_data1_out_v, self.r_data2, self.r_data2_out, \
            self.r_data2_out_v, self.imm, self.imm_out, self.imm_out_v, = signed_signal_set(9)
        self.rs, self.rt, self.rd, self.rs_out, self.rs_out_v, self.rt_out, self.rt_out_v, \
            self.rd_out, self.rd_out_v = unsigned_signal_set(9, width=5)
        self.reset_in = ResetSignal(0, active=1, async=True)
        # TODO: break these out into a signal generator function with a switch b/c shared input
        self.params = {
            'clock': self.clock,
            'branch_in': self.branch_in,
            'alu_op': self.alu_op_in,
            'mem_read_in': self.mem_read_in,
            'mem_to_reg_in': self.mem_to_reg_in,
            'mem_write_in': self.mem_write_in,
            'reg_dst_in': self.reg_dst_in,
            'reset_in': self.reset_in,
            'pc_value_in': self.pc_value_in,
            'r_data1': self.r_data1,
            'r_data2': self.r_data2,
            'rs': self.rs,
            'rt': self.rt,
            'rd': self.rd,
            'imm': self.imm,
            'r_data1_out': self.r_data1_out,
            'r_data2_out': self.r_data2_out,
            'imm_out': self.imm_out,
            'rs_out': self.rs_out,
            'rt_out': self.rt_out,
            'rd_out': self.rd_out,
            'pc_value_out': self.pc_value_out,
            'branch_out': self.branch_out,
            'alu_op_out': self.alu_op_out,
            'mem_read_out': self.mem_read_out,
            'mem_write_out': self.mem_write_out,
            'alu_src_out': self.alu_src_out,
            'reg_write_out': self.reg_write_out,
            'reg_dst_out': self.reg_dst_out
        }
        self.v_params = {
            'clock': self.clock,
            'branch_in': self.branch_in,
            'alu_op': self.alu_op_in,
            'mem_read_in': self.mem_read_in,
            'mem_to_reg_in': self.mem_to_reg_in,
            'mem_write_in': self.mem_write_in,
            'reg_dst_in': self.reg_dst_in,
            'reset_in': self.reset_in,
            'pc_value_in': self.pc_value_in,
            'r_data1': self.r_data1,
            'r_data2': self.r_data2,
            'rs': self.rs,
            'rt': self.rt,
            'rd': self.rd,
            'imm': self.imm,
            'r_data1_out': self.r_data1_out_v,
            'r_data2_out': self.r_data2_out_v,
            'imm_out': self.imm_out_v,
            'rs_out': self.rs_out_v,
            'rt_out': self.rt_out_v,
            'rd_out': self.rd_out_v,
            'pc_value_out': self.pc_value_out_v,
            'branch_out': self.branch_out_v,
            'alu_op_out': self.alu_op_out_v,
            'mem_read_out': self.mem_read_out_v,
            'mem_write_out': self.mem_write_out_v,
            'alu_src_out': self.alu_src_out_v,
            'reg_write_out': self.reg_write_out_v,
            'reg_dst_out': self.reg_dst_out_v
        }

        self.dut = id_ex(**self.params)

    # TODO: test signals pass through correctly
    def deassert(self, branch_out, mem_read_out, mem_to_reg_out, mem_write_out, alu_src_out,
                 reg_write_out, reg_dst_out):
        """test deassert functionality"""
        for i in range(sf['DEFAULT_TEST_LENGTH'] / 2):
            self.r_data1.next, self.r_data2.next, self.imm.next = [
                Signal(random_signed_intbv()) for i in range(3)
            ]
            self.rs.next, self.rt.next, self.rd.next = [
                Signal(intbv(randint(0, sf['WIDTH'] - 1))[5:]) for i in range(3)
            ]
            self.pc_value_in.next = Signal(intbv(randint(0, 15))[4:])
            # TODO: UPDATE WHEN ALU OP CODES ARE DETERMINED
            self.alu_op_in = Signal(intbv())

            yield posedge(self.clock)
            self.reset_in = 1
            yield posedge(self.clock)
            self.assertEqual(bin(branch_out), 0b0)
            self.assertEqual(0b0, bin(mem_read_out))
            self.assertEqual(0b0, bin(mem_to_reg_out))
            self.assertEqual(0b0, bin(mem_write_out))
            self.assertEqual(0b0, bin(alu_src_out))
            self.assertEqual(0b0, bin(reg_write_out))
            self.assertEqual(0b0, bin(reg_dst_out))
        raise StopSimulation

# TODO: test signals pass through correctly
    def dynamict(self, branch_out, mem_read_out, mem_to_reg_out, mem_write_out, alu_src_out,
                 reg_write_out, reg_dst_out):
        """Dynamic testing of ID/EX Pipeline Register"""
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.branch_in.next, self.mem_read_in.next, self.mem_to_reg_in.next,\
                self.mem_write_in.next, self.alu_src_in.next, self.reg_write_in.next,\
                self.reg_dst_in.next = unsigned_signal_set(7, randint(0, 1), 1)
            # TODO: UPDATE WHEN ALU OP CODES ARE DETERMINED
            self.alu_op_in = Signal(intbv())
            self.pc_value_in.next = Signal(intbv(randint(0, 15))[4:])
            self.r_data1.next, self.r_data2.next, self.imm.next = [
                Signal(random_signed_intbv()) for i in range(3)
            ]
            self.rs.next, self.rt.next, self.rd.next = [
                Signal(intbv(randint(0, sf['WIDTH'] - 1))[5:]) for i in range(3)
            ]
            yield posedge(self.clock)
            # possibly yield another pos or neg edge
            self.assertEqual(bin(branch_out), bin(self.branch_in))
            self.assertEqual(bin(self.mem_read_in), bin(mem_read_out))
            self.assertEqual(bin(self.mem_to_reg_in), bin(mem_to_reg_out))
            self.assertEqual(bin(self.mem_write_in), bin(mem_write_out))
            self.assertEqual(bin(self.alu_src_in), bin(alu_src_out))
            self.assertEqual(bin(self.reg_write_in), bin(reg_write_out))
            self.assertEqual(bin(self.reg_dst_in), bin(reg_dst_out))
        raise StopSimulation

    def testDeassertPython(self):
        """Checking stalling Python"""
        CLK = clock_gen(self.clock)
        stim = self.deassert(branch_out=self.branch_out,
                             mem_read_out=self.mem_read_out,
                             mem_to_reg_out=self.mem_to_reg_out,
                             mem_write_out=self.mem_write_out,
                             alu_src_out=self.alu_src_out,
                             reg_write_out=self.reg_write_out,
                             reg_dst_out=self.reg_dst_out)
        Simulation(CLK, stim, self.dut).run(quiet=1)

    def testDeassertVerilog(self):
        """Checking stalling Verilog"""
        CLK = clock_gen(self.clock)
        stim_v = self.deassert(branch_out=self.branch_out_v,
                               mem_read_out=self.mem_read_out_v,
                               mem_to_reg_out=self.mem_to_reg_out_v,
                               mem_write_out=self.mem_write_out_v,
                               alu_src_out=self.alu_src_out_v,
                               reg_write_out=self.reg_write_out_v,
                               reg_dst_out=self.reg_dst_out_v)

        dut_v = id_ex_v(**self.v_params)
        Simulation(CLK, stim_v, dut_v).run(quiet=1)

    def testDeassertTogether(self):
        """Checking stalling Together"""
        CLK = clock_gen(self.clock)
        stim = self.deassert(branch_out=self.branch_out,
                             mem_read_out=self.mem_read_out,
                             mem_to_reg_out=self.mem_to_reg_out,
                             mem_write_out=self.mem_write_out,
                             alu_src_out=self.alu_src_out,
                             reg_write_out=self.reg_write_out,
                             reg_dst_out=self.reg_dst_out)
        stim_v = self.deassert(branch_out=self.branch_out_v,
                               mem_read_out=self.mem_read_out_v,
                               mem_to_reg_out=self.mem_to_reg_out_v,
                               mem_write_out=self.mem_write_out_v,
                               alu_src_out=self.alu_src_out_v,
                               reg_write_out=self.reg_write_out_v,
                               reg_dst_out=self.reg_dst_out_v)

        dut_v = id_ex_v(**self.params)
        Simulation(CLK, stim, self.dut, dut_v, stim_v).run(quiet=1)

    def testDynamicPython(self):
        """Checking stalling Python"""
        CLK = clock_gen(self.clock)
        stim = self.dynamict(branch_out=self.branch_out,
                             mem_read_out=self.mem_read_out,
                             mem_to_reg_out=self.mem_to_reg_out,
                             mem_write_out=self.mem_write_out,
                             alu_src_out=self.alu_src_out,
                             reg_write_out=self.reg_write_out,
                             reg_dst_out=self.reg_dst_out)
        Simulation(CLK, stim, self.dut).run(quiet=1)

    def testDynamicVerilog(self):
        """Checking stalling Verilog"""
        CLK = clock_gen(self.clock)
        stim = self.dynamict(branch_out=self.branch_out_v,
                             mem_read_out=self.mem_read_out_v,
                             mem_to_reg_out=self.mem_to_reg_out_v,
                             mem_write_out=self.mem_write_out_v,
                             alu_src_out=self.alu_src_out_v,
                             reg_write_out=self.reg_write_out_v,
                             reg_dst_out=self.reg_dst_out_v)

        dut_v = id_ex_v(**self.v_params)
        Simulation(CLK, stim, dut_v).run(quiet=1)

    def testDynamicTogether(self):
        """Checking stalling Together"""
        CLK = clock_gen(self.clock)
        stim = self.dynamict(branch_out=self.branch_out,
                             mem_read_out=self.mem_read_out,
                             mem_to_reg_out=self.mem_to_reg_out,
                             mem_write_out=self.mem_write_out,
                             alu_src_out=self.alu_src_out,
                             reg_write_out=self.reg_write_out,
                             reg_dst_out=self.reg_dst_out)
        stim_v = self.dynamict(branch_out=self.branch_out_v,
                               mem_read_out=self.mem_read_out_v,
                               mem_to_reg_out=self.mem_to_reg_out_v,
                               mem_write_out=self.mem_write_out_v,
                               alu_src_out=self.alu_src_out_v,
                               reg_write_out=self.reg_write_out_v,
                               reg_dst_out=self.reg_dst_out_v)

        dut_v = id_ex_v(**self.params)
        Simulation(CLK, stim, self.dut, dut_v, stim_v).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
