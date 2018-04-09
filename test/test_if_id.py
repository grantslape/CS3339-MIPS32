"""IF/ID Pipeline register unit tests"""
import unittest
from unittest import TestCase
from myhdl import intbv, Simulation, Signal, StopSimulation, posedge, negedge
from src.python.fwd_unit import if_id, if_id_v
from src.commons.signal_generator import unsigned_signal_set, \
    signed_signal_set, rand_unsigned_signal_set
from src.commons.settings import settings as sf
from src.commons.clock import clock_gen


@unittest.skip("IF/ID Register not implemented")
class TestIfIdRegister(TestCase):
    """Test IF/ID Register"""
    def setUp(self):
        self.if_id_write, self.clock = unsigned_signal_set(2, width=1)
        self.nxt_pc, self.inst_in, self.pc_out, self.pc_out_v = unsigned_signal_set(4)
        self.op_code, self.op_code_v, self.funct_out, self.funct_out_v = \
            unsigned_signal_set(4, width=5)
        self.rs, self.rs_v, self.rt, self.rt_v, self.rd, self.rd_v = unsigned_signal_set(6, width=5)
        self.imm, self.imm_v = signed_signal_set(2)
        self.dut = if_id(if_id_write=self.if_id_write,
                         nxt_pc=self.nxt_pc,
                         inst_in=self.inst_in,
                         pc_out=self.pc_out,
                         op_code=self.op_code,
                         funct_out=self.funct_out,
                         rs=self.rs,
                         rt=self.rt,
                         rd=self.rd,
                         imm=self.imm)

    def deassert(self, pc_out, op_code, funct_out, rs, rt, rd, imm):
        self.if_id_write.next = 0
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.nxt_pc.next, self.inst_in.next = rand_unsigned_signal_set(2)
            yield posedge(self.clock)
            yield negedge(self.clock)
            self.assertEqual(bin(self.nxt_pc), bin(pc_out))
            self.assertEqual(bin(self.inst_in[32:26]), bin(op_code))
            self.assertEqual(bin(self.inst_in[26:21]), bin(rs))
            self.assertEqual(bin(self.inst_in[21:16]), bin(rt))
            self.assertEqual(bin(self.inst_in[16:11]), bin(rd))
            self.assertEqual(bin(self.inst_in[16:0]), bin(imm))
            self.assertEqual(bin(self.inst_in[6:0]), bin(funct_out))
        raise StopSimulation

    def asserted(self, pc_out, op_code, funct_out, rs, rt, rd, imm):
        self.if_id_write.next = 0
        self.nxt_pc.next, self.inst_in.next = rand_unsigned_signal_set(2)
        old_inst = self.inst_in
        yield posedge(self.clock)
        yield negedge(self.clock)
        self.if_id_write.next = 1
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            # I'm unsure about this - the way I understand it is if the stall line is active
            # if_id_write then we should keep the OLD instructions as output no matter what
            self.nxt_pc.next, self.inst_in.next = rand_unsigned_signal_set(2)
            yield posedge(self.clock)
            yield negedge(self.clock)
            # This could collide
            self.assertNotEquals(bin(self.nxt_pc), bin(pc_out))
            self.assertEqual(bin(old_inst[32:26]), bin(op_code))
            self.assertEqual(bin(old_inst[26:21]), bin(rs))
            self.assertEqual(bin(old_inst[21:16]), bin(rt))
            self.assertEqual(bin(old_inst[16:11]), bin(rd))
            self.assertEqual(bin(old_inst[16:0]), bin(imm))
            self.assertEqual(bin(old_inst[6:0]), bin(funct_out))

    def testIfIdDeassertedPython(self):
        """Test normal functionality Python"""
        stim = self.deassert(self.pc_out, self.op_code, self.funct_out, self.rs, self.rt, self.rd,
                             self.imm)
        Simulation(stim, self.dut).run(quiet=1)

    def testIfIdDeassertedVerilog(self):
        """Test normal functionality Verilog"""
        stim_v = self.deassert(self.pc_out_v, self.op_code_v, self.funct_out_v, self.rs_v,
                               self.rt_v, self.rd_v, self.imm_v)
        dut_v = if_id_v(if_id_write=self.if_id_write,
                        nxt_pc=self.nxt_pc,
                        inst_in=self.inst_in,
                        pc_out=self.pc_out_v,
                        op_code=self.op_code_v,
                        funct_out=self.funct_out_v,
                        rs=self.rs_v,
                        rt=self.rt_v,
                        rd=self.rd_v,
                        imm=self.imm_v)
        Simulation(stim_v, dut_v).run(quiet=1)

    def testIfIdDeassertedTogther(self):
        """Test normal functionality Together"""
        stim = self.deassert(self.pc_out, self.op_code, self.funct_out, self.rs, self.rt, self.rd,
                             self.imm)
        stim_v = self.deassert(self.pc_out_v, self.op_code_v, self.funct_out_v, self.rs_v,
                               self.rt_v, self.rd_v, self.imm_v)
        dut_v = if_id_v(if_id_write=self.if_id_write,
                        nxt_pc=self.nxt_pc,
                        inst_in=self.inst_in,
                        pc_out=self.pc_out_v,
                        op_code=self.op_code_v,
                        funct_out=self.funct_out_v,
                        rs=self.rs_v,
                        rt=self.rt_v,
                        rd=self.rd_v,
                        imm=self.imm_v)
        Simulation(stim_v, dut_v, stim, self.dut).run(quiet=1)

    def testIfIdAssertedPython(self):
        """Test Asserted functionality Python"""
        stim = self.asserted(self.pc_out, self.op_code, self.funct_out, self.rs, self.rt, self.rd,
                             self.imm)
        Simulation(stim, self.dut).run(quiet=1)

    def testIfIdAssertedVerilog(self):
        """Test Asserted functionality Verilog"""
        stim_v = self.asserted(self.pc_out_v, self.op_code_v, self.funct_out_v, self.rs_v,
                               self.rt_v, self.rd_v, self.imm_v)
        dut_v = if_id_v(if_id_write=self.if_id_write,
                        nxt_pc=self.nxt_pc,
                        inst_in=self.inst_in,
                        pc_out=self.pc_out_v,
                        op_code=self.op_code_v,
                        funct_out=self.funct_out_v,
                        rs=self.rs_v,
                        rt=self.rt_v,
                        rd=self.rd_v,
                        imm=self.imm_v)
        Simulation(stim_v, dut_v).run(quiet=1)

    def testIfIdAssertedTogther(self):
        """Test Asserted functionality Together"""
        stim = self.asserted(self.pc_out, self.op_code, self.funct_out, self.rs, self.rt, self.rd,
                             self.imm)
        stim_v = self.asserted(self.pc_out_v, self.op_code_v, self.funct_out_v, self.rs_v,
                               self.rt_v, self.rd_v, self.imm_v)
        dut_v = if_id_v(if_id_write=self.if_id_write,
                        nxt_pc=self.nxt_pc,
                        inst_in=self.inst_in,
                        pc_out=self.pc_out_v,
                        op_code=self.op_code_v,
                        funct_out=self.funct_out_v,
                        rs=self.rs_v,
                        rt=self.rt_v,
                        rd=self.rd_v,
                        imm=self.imm_v)
        Simulation(stim_v, dut_v, stim, self.dut).run(quiet=1)


if __name__ == '__main__':
    unittest.main()