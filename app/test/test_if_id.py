"""IF/ID Pipeline register unit tests"""
import unittest
from unittest import TestCase
from myhdl import Simulation, StopSimulation, Signal, intbv, bin
from src.python.if_id import if_id, if_id_v
from src.commons.signal_generator import unsigned_signal_set, random_unsigned_intbv
from src.commons.settings import settings as sf
from src.commons.clock import clock_gen


class TestIfIdRegister(TestCase):
    """Test IF/ID Register"""
    def setUp(self):
        self.if_id_write, self.clock, self.reset = unsigned_signal_set(3, width=1)
        self.nxt_pc, self.inst_in, self.pc_out, self.pc_out_v = unsigned_signal_set(4)
        self.op_code, self.op_code_v, self.funct_out, self.funct_out_v = \
            unsigned_signal_set(4, width=6)
        self.rs, self.rs_v, self.rt, self.rt_v, self.rd, self.rd_v = unsigned_signal_set(6, width=5)
        self.imm, self.imm_v = [
            Signal(intbv(min=sf['16_SIGNED_MIN_VALUE'], max=sf['16_SIGNED_MAX_VALUE']))
            for _ in range(2)
        ]
        self.top4, self.top4_v = unsigned_signal_set(2, width=4)
        self.target_out, self.target_out_v = unsigned_signal_set(2, width=26)
        self.dut = if_id(clock=self.clock,
                         if_id_write=self.if_id_write,
                         nxt_pc=self.nxt_pc,
                         inst_in=self.inst_in,
                         pc_out=self.pc_out,
                         op_code=self.op_code,
                         funct_out=self.funct_out,
                         rs=self.rs,
                         rt=self.rt,
                         rd=self.rd,
                         imm=self.imm,
                         top4=self.top4,
                         target_out=self.target_out)

    def getVerilog(self):
        """Return Verilog design under test"""
        return if_id_v(clock=self.clock,
                       if_id_write=self.if_id_write,
                       nxt_pc=self.nxt_pc,
                       inst_in=self.inst_in,
                       pc_out=self.pc_out_v,
                       op_code=self.op_code_v,
                       funct_out=self.funct_out_v,
                       rs=self.rs_v,
                       rt=self.rt_v,
                       rd=self.rd_v,
                       imm=self.imm_v,
                       top4=self.top4_v,
                       target_out=self.target_out_v)

    def deassert(self, python=False, verilog=False):
        """Test when stall line is off (normal op)"""
        self.if_id_write.next = 0
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            old_inst = Signal(random_unsigned_intbv())
            old_pc = Signal(random_unsigned_intbv())
            self.inst_in.next = old_inst
            self.nxt_pc.next = old_pc
            yield self.clock.negedge
            if python:
                self.assertEqual(bin(self.nxt_pc), bin(self.pc_out))
                self.assertEqual(bin(self.nxt_pc[32:28]), bin(self.top4))
                self.assertEqual(bin(self.inst_in[32:26]), bin(self.op_code))
                self.assertEqual(bin(self.inst_in[26:21]), bin(self.rs))
                self.assertEqual(bin(self.inst_in[21:16]), bin(self.rt))
                self.assertEqual(bin(self.inst_in[16:11]), bin(self.rd))
                self.assertEqual(bin(self.inst_in[16:0].signed()), bin(self.imm))
                self.assertEqual(bin(self.inst_in[6:0]), bin(self.funct_out))
                self.assertEqual(bin(self.inst_in[26:0]), bin(self.target_out))
            if verilog:
                self.assertEqual(bin(self.nxt_pc), bin(self.pc_out_v))
                self.assertEqual(bin(self.nxt_pc[32:28]), bin(self.top4_v))
                self.assertEqual(bin(self.inst_in[32:26]), bin(self.op_code_v))
                self.assertEqual(bin(self.inst_in[26:21]), bin(self.rs_v))
                self.assertEqual(bin(self.inst_in[21:16]), bin(self.rt_v))
                self.assertEqual(bin(self.inst_in[16:11]), bin(self.rd_v))
                self.assertEqual(bin(self.inst_in[16:0].signed()), bin(self.imm_v))
                self.assertEqual(bin(self.inst_in[6:0]), bin(self.funct_out_v))
                self.assertEqual(bin(self.inst_in[26:0]), bin(self.target_out_v))
        raise StopSimulation

    def asserted(self, python=False, verilog=False):
        """Test when stall line is on"""
        self.if_id_write.next = 0
        old_inst = Signal(random_unsigned_intbv())
        old_pc = Signal(random_unsigned_intbv())
        self.inst_in.next = old_inst
        self.nxt_pc.next = old_pc
        yield self.clock.negedge
        self.if_id_write.next = 1
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            # I'm unsure about this - the way I understand it is if the stall line is active
            # if_id_write then we should keep the OLD instructions as output no matter what
            self.inst_in.next = Signal(random_unsigned_intbv())
            self.nxt_pc.next = Signal(random_unsigned_intbv())
            yield self.clock.negedge
            # This could collide
            if python:
                self.assertNotEquals(bin(self.nxt_pc), bin(self.pc_out))
                self.assertEqual(bin(old_inst[32:26]), bin(self.op_code))
                self.assertEqual(bin(old_inst[26:21]), bin(self.rs))
                self.assertEqual(bin(old_inst[21:16]), bin(self.rt))
                self.assertEqual(bin(old_inst[16:11]), bin(self.rd))
                self.assertEqual(bin(old_inst[16:0].signed()), bin(self.imm))
                self.assertEqual(bin(old_inst[6:0]), bin(self.funct_out))
                self.assertEqual(bin(old_pc[32:28]), bin(self.top4))
                self.assertEqual(bin(old_inst[26:0]), bin(self.target_out))
            if verilog:
                self.assertNotEquals(bin(self.nxt_pc), bin(self.pc_out_v))
                self.assertEqual(bin(old_inst[32:26]), bin(self.op_code_v))
                self.assertEqual(bin(old_inst[26:21]), bin(self.rs_v))
                self.assertEqual(bin(old_inst[21:16]), bin(self.rt_v))
                self.assertEqual(bin(old_inst[16:11]), bin(self.rd_v))
                self.assertEqual(bin(old_inst[16:0].signed()), bin(self.imm_v))
                self.assertEqual(bin(old_inst[6:0]), bin(self.funct_out_v))
                self.assertEqual(bin(old_pc[32:28]), bin(self.top4_v))
                self.assertEqual(bin(old_inst[26:0]), bin(self.target_out_v))
        raise StopSimulation

    def testIfIdDeassertedPython(self):
        """Test normal functionality Python"""
        clk = clock_gen(self.clock)
        stim = self.deassert(python=True)
        Simulation(stim, self.dut, clk).run(quiet=1)

    def testIfIdDeassertedVerilog(self):
        """Test normal functionality Verilog"""
        clk = clock_gen(self.clock)
        stim_v = self.deassert(verilog=True)
        dut_v = self.getVerilog()
        Simulation(stim_v, dut_v, clk).run(quiet=1)

    def testIfIdDeassertedTogther(self):
        """Test normal functionality Together"""
        clk = clock_gen(self.clock)
        stim = self.deassert(python=True, verilog=True)
        dut_v = self.getVerilog()
        Simulation(dut_v, stim, self.dut, clk).run(quiet=1)

    def testIfIdAssertedPython(self):
        """Test Asserted functionality Python"""
        clk = clock_gen(self.clock)
        stim = self.asserted(python=True)
        Simulation(stim, self.dut, clk).run(quiet=1)

    def testIfIdAssertedVerilog(self):
        """Test Asserted functionality Verilog"""
        clk = clock_gen(self.clock)
        stim_v = self.asserted(verilog=True)
        dut_v = self.getVerilog()
        Simulation(stim_v, dut_v, clk).run(quiet=1)

    def testIfIdAssertedTogther(self):
        """Test Asserted functionality Together"""
        clk = clock_gen(self.clock)
        stim = self.asserted(python=True, verilog=True)
        dut_v = self.getVerilog()
        Simulation(dut_v, stim, self.dut, clk).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
