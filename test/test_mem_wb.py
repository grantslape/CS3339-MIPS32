"""MEM/WB Pipeline Register Unit Tests"""
import unittest
from unittest import TestCase
from random import randint
from myhdl import StopSimulation, Simulation, ResetSignal
from src.commons.clock import clock_gen
from src.commons.settings import settings as sf
from src.commons.signal_generator import unsigned_signal_set, signed_signal_set, \
    rand_signed_signal_set, random_unsigned_intbv
from src.python.mem_wb import mem_wb, mem_wb_v


class TestMemWb(TestCase):
    """Test MEM/WB Pipeline register"""
    def setUp(self):
        self.clock, self.reset, self.reg_write_in, self.reg_write_out, self.reg_write_out_v, \
            self.mux_ctl_in, self.mux_ctl_out = unsigned_signal_set(7, width=1)
        self.rdata_in, self.result_in, self.rdata_out, self.rdata_out_v, self.result_out, \
            self.result_out_v = signed_signal_set(6)
        self.rt_in, self.rt_out, self.rt_out_v = unsigned_signal_set(3, width=5)
        self.dut = mem_wb(self.clock, self.reset,
                          w_reg_ctl_in=self.reg_write_in,
                          mem_data_in=self.rdata_in,
                          alu_result_in=self.result_in,
                          w_reg_addr_in=self.rt_in,
                          mem_data_out=self.rdata_out,
                          alu_result_out=self.result_out,
                          w_reg_addr_out=self.rt_out,
                          w_reg_ctl_out=self.reg_write_out,
                          mux_ctl_in=self.mux_ctl_in,
                          mux_ctl_out=self.mux_ctl_out)

    def getVerilog(self):
        """Return verilog design under test"""
        return mem_wb_v(self.clock, self.reset,
                        w_reg_ctl_in=self.reg_write_in,
                        mem_data_in=self.rdata_in,
                        alu_result_in=self.result_in,
                        w_reg_addr_in=self.rt_in,
                        mem_data_out=self.rdata_out_v,
                        alu_result_out=self.result_out_v,
                        w_reg_addr_out=self.rt_out_v,
                        w_reg_ctl_out=self.reg_write_out_v,
                        mux_ctl_in=self.mux_ctl_in,
                        mux_ctl_out=self.mux_ctl_out)


    def hold_zero(self, python=False, verilog=False):
        """Test when inputs are held zero"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            yield self.clock.posedge
            yield self.clock.negedge
            if python:
                self.assertEqual(bin(self.rdata_out), bin(0))
                self.assertEqual(bin(self.result_out), bin(0))
                self.assertEqual(bin(self.rt_out), bin(0))
                self.assertEqual(bin(self.reg_write_out), bin(0))
            if verilog:
                self.assertEqual(bin(self.rdata_out_v), bin(0))
                self.assertEqual(bin(self.result_out_v), bin(0))
                self.assertEqual(bin(self.rt_out_v), bin(0))
                self.assertEqual(bin(self.reg_write_out_v), bin(0))
        raise StopSimulation

    def dynamic(self, python=False, verilog=False):
        """Test dynamic (normal) operation"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.reg_write_in.next = randint(0, 1)
            self.rdata_in.next, self.result_in.next = rand_signed_signal_set(2)
            self.rt_in.next = random_unsigned_intbv(width=5)
            yield self.clock.posedge
            yield self.clock.negedge
            if python:
                self.assertEqual(bin(self.reg_write_in), bin(self.reg_write_out))
                self.assertEqual(bin(self.rdata_in), bin(self.rdata_out))
                self.assertEqual(bin(self.result_in), bin(self.result_out))
                self.assertEqual(bin(self.rt_in), bin(self.rt_out))
            if verilog:
                self.assertEqual(bin(self.reg_write_in), bin(self.reg_write_out_v))
                self.assertEqual(bin(self.rdata_in), bin(self.rdata_out_v))
                self.assertEqual(bin(self.result_in), bin(self.result_out_v))
                self.assertEqual(bin(self.rt_in), bin(self.rt_out_v))
        raise StopSimulation

    def testMemWbHoldZeroPython(self):
        """Checking output stays zero Python"""
        clk = clock_gen(self.clock)
        stim = self.hold_zero(python=True)
        Simulation(clk, stim, self.dut).run(quiet=1)

    def testMemWbHoldZeroVerilog(self):
        """Checking output stays zero Verilog"""
        clk = clock_gen(self.clock)
        stim = self.hold_zero(verilog=True)
        dut_v = self.getVerilog()
        Simulation(clk, stim, dut_v).run(quiet=1)

    def testMemWbHoldZeroTogether(self):
        """Checking output stays zero Together"""
        clk = clock_gen(self.clock)
        stim = self.hold_zero(python=True, verilog=True)
        dut_v = self.getVerilog()
        Simulation(clk, stim, self.dut, dut_v).run(quiet=1)

    def testMemWbDynamicPython(self):
        """Checking dynamic normal operations Python"""
        stim = self.dynamic(python=True)
        clk = clock_gen(self.clock)
        Simulation(clk, stim, self.dut).run(quiet=1)

    def testMemWbDynamicVerilog(self):
        """Checking dynamic normal operations Verilog"""
        clk = clock_gen(self.clock)
        dut_v = self.getVerilog()
        stim = self.dynamic(verilog=True)
        Simulation(clk, stim, dut_v).run(quiet=1)

    def testMemWbDynamicTogether(self):
        """Checking dynamic normal operations Together"""
        clk = clock_gen(self.clock)
        stim = self.dynamic(python=True, verilog=True)
        dut_v = self.getVerilog()
        Simulation(clk, stim, self.dut, dut_v).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
